# ADR 0001: Standardizing on BigInteger for Database Primary and Foreign Keys

## Status
Accepted

## Context
When designing the relational schema using SQLAlchemy 2.0 and Alembic, we initially started with standard `Integer` primary keys for `Clients` and `Projects`. As the schema evolved and the `Integrations` module was introduced, discrepancies arose where some foreign keys expected `BigInteger` (due to older migrations defaulting to `BigInteger` or varying column types) while the referenced primary keys were `Integer`. 

In MySQL, a foreign key constraint strictly requires both the referencing column and the referenced column to have the exact same data type (including signed/unsigned attributes and size). Mixing `Integer` and `BigInteger` resulted in `sqlalchemy.exc.OperationalError: (pymysql.err.OperationalError) (3780, "Referencing column and referenced column are incompatible.")` during `alembic upgrade head`.

## Decision
We decided to standardize **all primary keys (IDs) and their corresponding foreign keys** across the entire application to use `BigInteger`. 

## Consequences
- **Positive**: Complete compatibility with MySQL foreign key constraints. No more migration errors regarding incompatible types.
- **Positive**: Future-proof against ID exhaustion, particularly useful for large-scale enterprise data (e.g., millions of records processed in sync jobs).
- **Negative**: Slightly larger storage footprint in the database (8 bytes vs 4 bytes per ID), which is negligible for our current scale.
