from typing import Dict, Any, List
from app.modules.connectors.base import BaseConnector

class ProcoreConnector(BaseConnector):
    def authenticate(self) -> None:
        pass

    def fetch_data(self) -> List[Dict[str, Any]]:
        import httpx
        try:
            # In a real implementation, make actual HTTP request here:
            # response = httpx.get("https://api.procore.com", timeout=self.timeout_seconds)
            pass
        except httpx.TimeoutException as e:
            from app.modules.connectors.exceptions import TransientSyncError
            raise TransientSyncError(f"Timeout after {self.timeout_seconds}s: {str(e)}")
            
        return [
            {"procore_id": 1, "name": "Project A"},
            {"procore_id": 2, "name": "Project B"}
        ]

    def normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        return {"id": raw.get("procore_id"), "name": raw.get("name")}
