# ADR 0003: Choice of MySQL 8.0 for Database Engine

## Status
Accepted

## Context
The Marketing Intelligence Platform requires a highly reliable relational store with strict foreign key constraints across clients, projects, locations, integrations, and metrics. Furthermore, high-throughput background ingestion workers perform idempotent upserts over daily metrics.

## Decision
We chose **MySQL 8.0** as the primary relational database.
- Uses native `INSERT ... ON DUPLICATE KEY UPDATE` dialect syntax via SQLAlchemy.
- Supports indexed `JSON` columns for flexible storing of complex aggregated metrics and raw connector payloads.
- Validated cleanly across CI service containers matching production deployment targets.

## Consequences
- Guaranteed relational integrity and strict foreign key enforcement.
- Eliminates database engine mismatch bugs during migration rollouts.
