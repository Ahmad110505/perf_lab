# Software Architecture Design (SAD)
## Marketing Intelligence Platform - Version 1.0

## 1. Architecture Overview
The Marketing Intelligence Platform is designed using a **Modular Monolith** architecture. 
**Why Modular Monolith?**
- **Maintainability:** By strictly separating domain logic into self-contained modules, the codebase remains organized without the operational complexity of microservices.
- **Reliability (Decoupled Reads):** The dashboard (reads) operates independently of external API integrations. External APIs are queried via background Celery workers, pushing data into MySQL through a staged ingestion pipeline.
- **Scalability:** Background workers can be scaled horizontally independent of the API web servers.

## 2. Responsibilities of Every Module

### 2.1 Authentication
- **Purpose**: Manage system access and identity verification.
- **Responsibilities**: Login, Token Generation (JWT), Token Validation, Password Verification.
- **Dependencies**: None.
- **Data Owned**: Users, Passwords, Roles.
- **Data Consumed**: None.

### 2.2 Clients
- **Purpose**: Manage marketing clients.
- **Responsibilities**: CRUD for client entities, linking clients to projects.
- **Dependencies**: Authentication (for access control).
- **Data Owned**: Client profiles, Status, Contact info.
- **Data Consumed**: None.

### 2.3 Projects
- **Purpose**: Manage projects (Websites, Apps, Campaigns) owned by clients.
- **Responsibilities**: CRUD for projects, linking projects to locations and integrations.
- **Dependencies**: Clients.
- **Data Owned**: Project profiles, Types, Status.
- **Data Consumed**: Client IDs.

### 2.4 Locations
- **Purpose**: Manage physical business addresses linked to projects.
- **Responsibilities**: CRUD for physical locations (GEO data).
- **Dependencies**: Projects.
- **Data Owned**: Address, Coordinates, Region.
- **Data Consumed**: Project IDs.

### 2.5 Integrations (Connectors)
- **Purpose**: Manage credentials, configurations, and data ingestion for external platforms.
- **Responsibilities**: Dedicated connectors fetch data from third-party APIs. Each connector is completely isolated from every other connector and contains its own:
  - API Client
  - Mapper
  - Validation
  - Error Handling
- **Modules**:
  - `Google Analytics Connector`
  - `Google Search Console Connector`
  - `Meta Connector`
  - `Ahrefs Connector`
  - `SEMrush Connector`
- **Dependencies**: Projects, Security (Encryption).
- **Data Owned**: API Keys, Tokens (Encrypted), Provider details.
- **Data Consumed**: Project IDs.

### 2.6 Synchronization
- **Purpose**: Orchestrate data ingestion from Connectors.
- **Responsibilities**: Schedule background jobs, handle rate limits, manage retries across Connectors.
- **Dependencies**: Integrations (Connectors), Metrics.
- **Data Owned**: Sync Job Status, Last Sync Timestamps.
- **Data Consumed**: Integration Credentials.

### 2.7 Metrics
- **Purpose**: Multi-stage processing and storage for all marketing data.
- **Responsibilities**: 
  - **Raw Metrics**: Store the untouched JSON response directly from the Connector for audit and replayability.
  - **Normalization**: Transform raw data into a standardized schema.
  - **Normalized Metrics**: Serve as the core time-series store for all standardized data.
- **Dependencies**: Projects, Locations.
- **Data Owned**: Raw Metrics, Normalized Metrics (SEO, Meta, Content).
- **Data Consumed**: Project IDs, Location IDs.

### 2.8 Dashboard
- **Purpose**: Serve aggregated, high-level views of the platform state.
- **Responsibilities**: Provide lightning-fast read operations for the UI. The dashboard **must only read Dashboard Summary data whenever possible**.
- **Dashboard Summary Builder**: A dedicated background process that reads Normalized Metrics to compute aggregations, KPI calculations, and daily summaries.
- **Dashboard Summary Table**: Pre-calculated, heavily indexed tables optimized for the Dashboard UI.
- **Dependencies**: Clients, Projects, Metrics, Integrations.
- **Data Owned**: Dashboard Summary Table (Aggregations).
- **Data Consumed**: Normalized Metrics.

### 2.9 Reports
- **Purpose**: Generate structured outputs for the marketing team.
- **Responsibilities**: Export data (CSV/PDF), generate scheduled summaries.
- **Dependencies**: Metrics, Projects.
- **Data Owned**: Report templates, Generated report metadata.
- **Data Consumed**: Normalized Metrics.

## 3. Architecture Decision Records (ADR)
Located at `/docs/architecture/ADR/`
- `0001-use-biginteger-for-ids.md`
- `0002-connector-framework-pattern.md`
- `0003-mysql.md`
- `0004-celery.md`
- `0005-staged-metrics-ingestion.md`
