from fastapi import APIRouter
from app.modules.clients.router import router as clients_router

from app.api.health import router as health_router

api_router = APIRouter()
api_router.include_router(health_router)

from app.modules.auth.router import router as auth_router
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(clients_router, prefix="/clients", tags=["clients"])
from app.modules.projects.router import router as projects_router
api_router.include_router(projects_router, prefix="/projects", tags=["projects"])
from app.modules.locations.router import router as locations_router
from app.modules.integrations.router import router as integrations_router
from app.modules.connectors.router import router as connectors_router
from app.modules.metrics.router import router as metrics_router
from app.modules.dashboard.router import router as dashboard_router
from app.modules.reports.router import router as reports_router
api_router.include_router(locations_router, prefix="/locations", tags=["locations"])
api_router.include_router(integrations_router, prefix="/integrations", tags=["integrations"])
api_router.include_router(connectors_router, tags=["connectors"])
api_router.include_router(metrics_router)
api_router.include_router(dashboard_router)
api_router.include_router(reports_router)
