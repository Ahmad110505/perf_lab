import logging
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from app.shared.models import Base
from app.modules.auth.models import User
from app.modules.clients.models import Client
from app.modules.projects.models import Project
from app.modules.locations.models import Location
from app.modules.integrations.models import Integration
from app.modules.connectors.models import ConnectorRun
from app.modules.metrics.models import RawMetric, NormalizedMetric
from app.modules.dashboard.models import DashboardSummary
from app.modules.reports.models import Report
from app.core.config import settings

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Ensure models are imported so Alembic can read metadata
target_metadata = Base.metadata

def get_url():
    return settings.SQLALCHEMY_DATABASE_URI

def run_migrations_offline() -> None:
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
