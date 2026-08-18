# ADR-0004 · PostgreSQL + pgvector as the primary store

- **Status:** Proposed
- **Date:** 2026-08-18
- **Phase:** 0

## Context

The system needs a transactional store (runs, event log, leases, audit, tenancy) **and** a vector
store (embeddings for retrieval and memory). Running one well-understood engine is cheaper to
operate solo than running two, and keeps the event-log append and its indexing transactional.

## Decision

PostgreSQL 17 is the primary datastore; the pgvector extension provides vector search in the same
database. Redis is used for cache, streams, and rate limiting; MinIO/S3 for the L3 object tier.
A dedicated vector database is deferred and compared later (OpenSearch, Phase 16) behind the
retrieval port.

## Alternatives considered

| Option | Why not chosen |
| --- | --- |
| Dedicated vector DB now (Qdrant/Milvus) | A second store to operate; premature at ~150k docs; pgvector suffices |
| NoSQL primary (Mongo/Dynamo) | Weaker transactional guarantees for the event log and leases |
| SQLite | No real concurrency; won't model production behaviour |

## Consequences

**Positive** — one engine for transactional + vector data; transactional event append; the SQL
knowledge is directly reusable; RLS available for tenancy (Ph 14).

**Negative / accepted** — pgvector at very large scale is weaker than a specialised ANN engine;
acceptable at project scale, and the retrieval port keeps a swap cheap.

**Revisit if** — measured recall/latency at scale (Ph 8/16) justifies a dedicated vector store.
