# ADR 0004: Asynchronous Worker Architecture & Celery Beat Scheduling

## Status
Accepted

## Context
Third-party API data fetching (Google Analytics, Search Console, Meta, Ahrefs, SEMrush) can be slow or encounter rate limits (HTTP 429). User dashboard reads must remain sub-50ms and completely decoupled from external API latency.

## Decision
We chose **Celery with Redis** as the task queue and worker architecture.
- Long-running sync jobs are dispatched asynchronously using `@celery_app.task`.
- Implements exponential backoff and retry policies for network failures.
- Configured **Celery Beat** periodic schedule for daily dashboard summary calculations and recurring syncs.

## Consequences
- User experience is instantaneous. Dashboard loading never waits on external API calls.
- Workers can be scaled horizontally independent of FastAPI web servers.
