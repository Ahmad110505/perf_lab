from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.shared.service import BaseService
from app.modules.clients.repository import ClientRepository, client_repository
from app.modules.clients.schemas import ClientCreate, ClientUpdate, ClientResponse, ClientListResponse
from app.modules.clients.models import Client

class ClientService(BaseService[ClientRepository]):
    def __init__(self):
        super().__init__(client_repository)

    def get_client(self, db: Session, client_id: int) -> Client:
        client = self.repository.get(db, client_id)
        if not client:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
        return client

    def get_clients(self, db: Session, skip: int = 0, limit: int = 100) -> ClientListResponse:
        items, total = self.repository.get_multi_with_count(db, skip=skip, limit=limit)
        return ClientListResponse(
            items=[ClientResponse.model_validate(item) for item in items],
            total=total
        )

    def create_client(self, db: Session, client_in: ClientCreate, user_id: int) -> Client:
        existing = self.repository.get_by_name(db, client_in.name)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Client with this name already exists")
        
        obj_in = client_in.model_dump()
        obj_in["created_by"] = user_id
        
        client = self.repository.create(db, obj_in=obj_in)
        return client

    def update_client(self, db: Session, client_id: int, client_in: ClientUpdate, user_id: int) -> Client:
        client = self.get_client(db, client_id)
        
        update_data = client_in.model_dump(exclude_unset=True)
        if "name" in update_data:
            existing = self.repository.get_by_name(db, update_data["name"])
            if existing and existing.id != client_id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Client with this name already exists")
                
        for field, value in update_data.items():
            setattr(client, field, value)
            
        client.updated_by = user_id
        db.commit()
        db.refresh(client)
        return client

    def delete_client(self, db: Session, client_id: int, user_id: int) -> None:
        client = self.get_client(db, client_id)
        client.updated_by = user_id
        db.commit()
        self.repository.soft_delete(db, id=client_id)

client_service = ClientService()
