from typing import Dict, Any, List
from app.modules.connectors.base import BaseConnector

class ProcoreConnector(BaseConnector):
    def authenticate(self) -> None:
        pass

    def fetch_data(self) -> List[Dict[str, Any]]:
        return [{"procore_id": 1, "name": "Project A"}]

    def normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        return {"id": raw.get("procore_id"), "name": raw.get("name")}
