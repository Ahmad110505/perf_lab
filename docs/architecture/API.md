# API Documentation

This document outlines the REST API for the Marketing Platform Backend. The API uses JSON for requests and responses, and JWT for authentication.

## Authentication (`/api/v1/auth`)
- **POST `/register`**: Register a new user. Expects `email` and `password`. Returns user details.
- **POST `/login`**: Authenticate and retrieve JWT tokens. Expects `email` and `password`. Returns `access_token` and `refresh_token`.
- **POST `/refresh`**: Refresh an expired access token.

## Clients (`/api/v1/clients`)
- **GET `/`**: List all clients.
- **GET `/{id}`**: Retrieve a specific client.
- **POST `/`**: Create a new client.
- **PATCH `/{id}`**: Update a client.
- **DELETE `/{id}`**: Delete a client (soft delete).
- **GET `/{id}/integrations`**: Retrieve all integrations configured for a specific client.

## Projects (`/api/v1/projects`)
- **GET `/`**: List all projects.
- **GET `/{id}`**: Retrieve a specific project.
- **POST `/`**: Create a new project. Requires `client_id`.
- **PATCH `/{id}`**: Update a project.
- **DELETE `/{id}`**: Delete a project (soft delete).

## Locations (`/api/v1/locations`)
- **GET `/`**: List all locations.
- **GET `/{id}`**: Retrieve a specific location.
- **POST `/`**: Create a new location. Requires `client_id` and optionally `project_id`.
- **PATCH `/{id}`**: Update a location.
- **DELETE `/{id}`**: Delete a location (soft delete).

## Integrations (`/api/v1/integrations`)
- **GET `/`**: List all integrations.
- **GET `/{id}`**: Retrieve a specific integration.
- **POST `/`**: Create a new integration. Requires `client_id`, `provider` (PROCORE, AUTODESK, GENERIC_WEBHOOK), and configuration. Note: `credentials_ref` is returned, raw secrets are never leaked.
- **PATCH `/{id}`**: Update an integration.
- **PATCH `/{id}/status`**: Update the status of an integration (e.g. connected, error).
- **DELETE `/{id}`**: Delete an integration.

## Connectors (`/api/v1/`)
- **POST `/integrations/{integration_id}/sync`**: Trigger a manual sync run for the specified integration. Returns a `ConnectorRun`.
- **GET `/integrations/{integration_id}/runs`**: Get the history of sync runs for a given integration.
- **GET `/connector-runs/{run_id}`**: Retrieve the status and audit details of a specific connector run.
