# ADR 0005: Staged Metrics Ingestion Pipeline

## Status
Accepted

## Context
External APIs return varying payload structures. Auditing, debugging, and data recoverability require storing untouched original responses before transforming them into uniform time-series metrics.

## Decision
We implemented a two-stage metrics ingestion architecture:
1. **Raw Metric Stage**: Untouched raw JSON payload stored directly in `RawMetric`.
2. **Normalization Stage**: Domain-specific normalizer maps raw payload into standardized `NormalizedMetric` time-series rows.
3. **Summary Builder Stage**: `DashboardSummaryBuilder` pre-aggregates normalized metrics into `DashboardSummary` tables for immediate UI consumption.

## Consequences
- 100% Auditability: Original API responses are preserved.
- Full Recoverability: `rebuild_normalized_metrics` can replay historical raw logs if normalizer logic changes.
