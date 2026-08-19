"""Verify the local development environment.

Phase 0.8 — turn assumptions into facts. Every check here is something a later phase
depends on; discovering a missing one in Phase 2 (mid-build) is far more expensive
than discovering it now.

Dependency-free by design: uses only the standard library, so it runs before any
project dependencies are installed.

Usage:
    python scripts/dev/verify_env.py
    make verify

Exit code 0 = ready to build. 1 = at least one hard requirement failed.
"""

from __future__ import annotations

import shutil
import socket
import subprocess
import sys
from pathlib import Path

# --- result vocabulary -------------------------------------------------------
PASS = "PASS"
FAIL = "FAIL"  # hard requirement; blocks
WARN = "WARN"  # needed by a later phase, not yet
SKIP = "SKIP"  # cannot be determined here

REPO_ROOT = Path(__file__).resolve().parents[2]
MIN_PYTHON = (3, 11)
POSTGRES_PORT = 5432
REDIS_PORT = 6379

Result = tuple[str, str, str]  # (status, name, detail)


# --- checks ------------------------------------------------------------------
def check_python_version() -> Result:
    v = sys.version_info
    got = f"{v.major}.{v.minor}.{v.micro}"
    if (v.major, v.minor) >= MIN_PYTHON:
        return PASS, "Python version", f"{got} (>= {MIN_PYTHON[0]}.{MIN_PYTHON[1]})"
    return FAIL, "Python version", f"{got} — need >= {MIN_PYTHON[0]}.{MIN_PYTHON[1]}"


def check_active_env() -> Result:
    prefix = Path(sys.prefix).resolve()
    expected = (REPO_ROOT / "myvenv").resolve()
    if prefix == expected:
        return PASS, "Active interpreter", str(prefix)
    return (
        FAIL,
        "Active interpreter",
        (f"{prefix} — expected {expected}. Run: conda activate ./myvenv"),
    )


def check_hermetic() -> Result:
    """User site-packages must not leak into the environment (see roadmap 0.7)."""
    import site

    if not site.ENABLE_USER_SITE:
        return PASS, "Hermetic env", "user site-packages disabled"
    return (
        FAIL,
        "Hermetic env",
        (
            "user site-packages ENABLED — run: "
            "conda env config vars set PYTHONNOUSERSITE=1 -p ./myvenv"
        ),
    )


def check_tools() -> list[Result]:
    results: list[Result] = []
    for tool in ("ruff", "mypy", "pytest", "pre-commit", "git", "make"):
        path = shutil.which(tool)
        if path:
            results.append((PASS, f"Tool: {tool}", path))
        else:
            results.append((FAIL, f"Tool: {tool}", "not on PATH"))
    return results


def _port_open(host: str, port: int, timeout: float = 1.5) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def _run(cmd: list[str], timeout: int = 15) -> tuple[int, str]:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=False)
        return p.returncode, (p.stdout + p.stderr).strip()
    except FileNotFoundError:
        return 127, "command not found"
    except subprocess.TimeoutExpired:
        return 124, "timed out"


def check_docker() -> Result:
    """Required from Phase 2 (Postgres, Redis, MinIO run in containers)."""
    if shutil.which("docker") is None:
        return WARN, "Docker", "not installed — required from Phase 2"
    code, out = _run(["docker", "info", "--format", "{{.ServerVersion}}"])
    if code == 0 and out:
        return PASS, "Docker", f"daemon running (server {out.splitlines()[0]})"
    return WARN, "Docker", "installed but daemon not running — required from Phase 2"


def check_postgres() -> Result:
    if _port_open("127.0.0.1", POSTGRES_PORT):
        return PASS, "PostgreSQL", f"reachable on 127.0.0.1:{POSTGRES_PORT}"
    return WARN, "PostgreSQL", f"nothing listening on {POSTGRES_PORT} — required from Phase 2"


def check_pgvector() -> Result:
    """pgvector is an extension: having PostgreSQL 17 does NOT mean it is installed."""
    if shutil.which("psql") is None:
        return SKIP, "pgvector", "psql not on PATH — verify manually before Phase 2"
    if not _port_open("127.0.0.1", POSTGRES_PORT):
        return SKIP, "pgvector", "PostgreSQL not reachable"
    code, out = _run(
        [
            "psql",
            "-w",  # never prompt: a check script must not block on stdin
            "-tAc",
            "SELECT default_version FROM pg_available_extensions WHERE name = 'vector';",
        ]
    )
    if code != 0:
        return (
            SKIP,
            "pgvector",
            (
                "auth/connection not configured — verify manually: "
                "psql -U postgres -c \"SELECT * FROM pg_available_extensions WHERE name='vector';\""
            ),
        )
    if out.strip():
        return PASS, "pgvector", f"available (version {out.strip().splitlines()[0]})"
    return WARN, "pgvector", "NOT available — install before Phase 2 (CREATE EXTENSION vector)"


def check_redis() -> Result:
    if _port_open("127.0.0.1", REDIS_PORT):
        return PASS, "Redis", f"reachable on 127.0.0.1:{REDIS_PORT}"
    return WARN, "Redis", f"nothing listening on {REDIS_PORT} — required from Phase 2 (Docker)"


def check_git_repo() -> list[Result]:
    results: list[Result] = []
    code, branch = _run(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    results.append(
        (PASS, "Git branch", branch) if code == 0 else (FAIL, "Git branch", "not a git repository")
    )
    code, remote = _run(["git", "remote", "get-url", "origin"])
    results.append(
        (PASS, "Git remote", remote)
        if code == 0
        else (WARN, "Git remote", "no 'origin' configured")
    )
    return results


def check_private_ignored() -> list[Result]:
    """The repo is public: these must never be trackable."""
    results: list[Result] = []
    for target in ("CLAUDE.md", "private/", ".env"):
        code, out = _run(["git", "check-ignore", "-v", target])
        if code == 0:
            rule = out.split("\t")[0] if "\t" in out else out
            results.append((PASS, f"Ignored: {target}", rule))
        else:
            results.append((FAIL, f"Ignored: {target}", "NOT IGNORED — public repo leak risk"))
    return results


def check_env_file() -> Result:
    if (REPO_ROOT / ".env").exists():
        return PASS, ".env", "present (gitignored)"
    return WARN, ".env", "absent — copy from .env.example before Phase 2"


# --- report ------------------------------------------------------------------
def main() -> int:
    checks: list[Result] = [
        check_python_version(),
        check_active_env(),
        check_hermetic(),
        *check_tools(),
        *check_git_repo(),
        *check_private_ignored(),
        check_docker(),
        check_postgres(),
        check_pgvector(),
        check_redis(),
        check_env_file(),
    ]

    width = max(len(name) for _, name, _ in checks)
    print(f"\nAI_Keystone — environment verification\n{'-' * (width + 40)}")
    for status, name, detail in checks:
        print(f"[{status}] {name.ljust(width)}  {detail}")

    failures = [c for c in checks if c[0] == FAIL]
    warnings = [c for c in checks if c[0] == WARN]
    print("-" * (width + 40))
    print(f"{len(checks)} checks — {len(failures)} failed, {len(warnings)} warnings\n")

    if failures:
        print("BLOCKED: fix the FAIL items above before building.\n")
        return 1
    if warnings:
        print("READY for Phase 0-1. WARN items are required from Phase 2 onward.\n")
    else:
        print("READY.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
