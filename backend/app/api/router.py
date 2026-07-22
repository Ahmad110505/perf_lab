from fastapi import APIRouter
from app.modules.clients.router import router as clients_router

api_router = APIRouter()

from app.modules.auth.router import router as auth_router
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(clients_router, prefix="/clients", tags=["clients"])
from app.modules.projects.router import router as projects_router
api_router.include_router(projects_router, prefix="/projects", tags=["projects"])
from app.modules.locations.router import router as locations_router
api_router.include_router(locations_router, prefix="/locations", tags=["locations"])
