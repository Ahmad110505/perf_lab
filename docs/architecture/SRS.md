# Software Requirements Specification (SRS)

## 1. Introduction
The Marketing Platform is a multi-tenant B2B application designed to manage hierarchical organizational data and seamlessly sync with third-party providers (e.g., Procore, Autodesk).

## 2. Core Functional Requirements
- **Hierarchical Data Management**: Must support an overarching hierarchy: Clients -> Projects -> Locations.
- **Authentication**: Must provide secure JWT-based authentication with access and refresh tokens.
- **Integration Management**: Users must be able to configure third-party integrations securely. Raw credentials must never be exposed via the API.
- **Connector Framework**: The system must have an extensible framework for running sync jobs against third-party APIs.
- **Audit Logging**: All sync runs must be audited with success/failure statuses and processed record counts.

## 3. Non-Functional Requirements
- **Architecture**: Layered architecture (Models -> Schemas -> Repository -> Services -> Router).
- **Extensibility**: Adding a new third-party connector should not require modifying core integration routing or database schema logic; it should adhere to the `BaseConnector` contract.
- **Performance**: Heavy integration syncing must be delegated to background async workers (e.g., Celery) to avoid blocking HTTP requests.
- **Database Consistency**: Soft-delete mechanisms must be strictly respected across foreign keys. BigInteger IDs must be standard to avoid scaling limitations and FK mismatch errors.
