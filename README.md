# 📊 PerfLab — Performance & Analytics Platform

PerfLab is a modular analytics engineering platform designed for aggregating, normalizing, and reporting performance metrics from diverse backend connectors (e.g., Google Analytics, custom API integrations, and database telemetry).

---

## 🌟 Core Features

- **Modular Connector Architecture:** Plug-and-play integrations for third-party analytics sources.
- **Metrics Normalization Engine:** Standardizes telemetry data across diverse formats into unified analytics schemas.
- **RESTful API Backend:** Built on FastAPI for high performance, dynamic filtering, and quick metric retrieval.
- **Client & Project Management:** Multi-tenant support for tracking performance metrics by client, location, and project.

---

## 🏗 System Architecture

```
backend/
├── app/
│   ├── api/             # API routes & endpoint controllers
│   ├── core/            # Config, security, and database sessions
│   ├── db/              # ORM models & database migrations
│   └── modules/
│       ├── connectors/  # Integration registry & external connectors
│       └── metrics/     # Normalizers, repositories, and services
```

---

## 🛠 Getting Started

### Prerequisites

- **Python 3.11+**
- **Virtual Environment (`venv`)**

### Setup Instructions

```bash
# 1. Clone the repository
git clone https://github.com/Ahmad110505/perf_lab.git
cd perf_lab

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install backend dependencies
cd backend
pip install -r requirements.txt

# 4. Run application server
uvicorn app.main:app --reload --port 8000
```

---

## 📄 License

Distributed under the MIT License.
