from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Tuple, Optional
from app.shared.service import BaseService
from app.modules.integrations.repository import IntegrationRepository, integration_repository
from app.modules.integrations.schemas import IntegrationCreate, IntegrationUpdate
from app.modules.integrations.models import Integration, IntegrationProvider, IntegrationStatus
from app.modules.clients.repository import client_repository
from app.core.security import encrypt_credential

class IntegrationService(BaseService[IntegrationRepository]):
    def __init__(self):
        super().__init__(integration_repository)

    def get_integrations(self, db: Session, client_id: Optional[int] = None, provider: Optional[IntegrationProvider] = None, status: Optional[IntegrationStatus] = None, skip: int = 0, limit: int = 100) -> dict:
        items, total = self.repository.get_multi_with_count(db, client_id=client_id, provider=provider, status=status, skip=skip, limit=limit)
        return {"items": items, "total": total, "skip": skip, "limit": limit}

    def get_integration(self, db: Session, integration_id: int) -> Integration:
        integration = self.repository.get(db, id=integration_id)
        if not integration or integration.deleted_at:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Integration not found")
        return integration

    def create_integration(self, db: Session, integration_in: IntegrationCreate) -> Integration:
        # 1. Verify client exists
        client = client_repository.get(db, id=integration_in.client_id)
        if not client or client.deleted_at:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")

        # 2. Prevent duplicate provider per client
        existing = self.repository.get_by_provider(db, client_id=integration_in.client_id, provider=integration_in.provider)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Integration for provider {integration_in.provider.value} already exists for this client")

        obj_dict = integration_in.model_dump()
        obj_dict["status"] = IntegrationStatus.CONNECTED

        # Encrypt API Key at rest if provided in config and credentials_ref not explicitly provided
        if not obj_dict.get("credentials_ref") and integration_in.config and "api_key" in integration_in.config:
            obj_dict["credentials_ref"] = encrypt_credential(str(integration_in.config["api_key"]))

        return self.repository.create(db, obj_in=obj_dict)

    def update_integration(self, db: Session, integration_id: int, integration_in: IntegrationUpdate) -> Integration:
        integration = self.get_integration(db, integration_id)
        update_data = integration_in.model_dump(exclude_unset=True)
        if "config" in update_data and update_data["config"] and "api_key" in update_data["config"]:
            integration.credentials_ref = encrypt_credential(str(update_data["config"]["api_key"]))
        for field, value in update_data.items():
            setattr(integration, field, value)
        db.commit()
        db.refresh(integration)
        return integration

    def update_status(self, db: Session, integration_id: int, new_status: IntegrationStatus) -> Integration:
        integration = self.get_integration(db, integration_id)
        integration.status = new_status
        db.commit()
        db.refresh(integration)
        return integration

    def delete_integration(self, db: Session, integration_id: int) -> None:
        integration = self.get_integration(db, integration_id)
        self.repository.soft_delete(db, id=integration_id)

integration_service = IntegrationService()
