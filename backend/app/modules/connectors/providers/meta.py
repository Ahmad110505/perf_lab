from typing import Dict, Any, List
from app.modules.connectors.base import BaseConnector

class MetaConnector(BaseConnector):
    def authenticate(self) -> None:
        pass

    def fetch_data(self) -> List[Dict[str, Any]]:
        project_id = self.config.get("project_id", 1)
        return [
            {
                "project_id": project_id,
                "date": "2023-01-01",
                "spend": 350.0,
                "impressions": 25000,
                "cpc": 1.25,
                "roas": 4.10
            },
            {
                "project_id": project_id,
                "date": "2023-01-02",
                "spend": 400.0,
                "impressions": 28000,
                "cpc": 1.18,
                "roas": 4.35
            }
        ]

    def normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        return raw
