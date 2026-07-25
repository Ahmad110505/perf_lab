# ADR 0002: Provider Registry and Connector Framework Pattern

## Status
Accepted

## Context
The platform needs to sync data with numerous third-party systems (Procore, Autodesk, Generic Webhooks, etc.). Implementing a massive monolithic service that handles all providers with `if/elif` statements would violate the Open-Closed Principle. It would make `services.py` unmaintainable, testable, and highly coupled to provider-specific logic and API clients.

## Decision
We implemented a **Registry and Abstract Factory Pattern** for the Connector Framework:
1. `BaseConnector`: An abstract base class (`abc.ABC`) defining the standard contract: `authenticate()`, `fetch_data()`, and `normalize()`.
2. **Provider Implementations**: Each third-party system gets its own isolated file (e.g., `providers/procore.py`) containing a class that implements `BaseConnector`.
3. **Registry**: A `get_connector_for_provider(provider_name)` factory method that routes the string name from the database to the specific class implementation.

## Consequences
- **Positive**: Highly extensible. Adding a new provider only requires adding one file in `providers/` and a single line in the registry.
- **Positive**: Testing is deeply simplified; we can mock isolated providers without touching the core service logic.
- **Positive**: The core `trigger_sync` logic in `services.py` remains pristine, solely responsible for database transitions, job queuing, and error handling.
- **Negative**: Adds a slight layer of abstraction requiring developers to understand the contract before contributing a new integration.
