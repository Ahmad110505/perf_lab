from typing import Dict, Any, List
from app.modules.connectors.base import BaseConnector

class SEMrushConnector(BaseConnector):
    def authenticate(self) -> None:
        pass

    def fetch_data(self) -> List[Dict[str, Any]]:
        project_id = self.config.get("project_id", 1)
        return [
            {
                "project_id": project_id,
                "date": "2023-01-01",
                "search_volume": 45000,
                "organic_keywords": 3200,
                "organic_traffic": 18500
            },
            {
                "project_id": project_id,
                "date": "2023-01-02",
                "search_volume": 45000,
                "organic_keywords": 3220,
                "organic_traffic": 18900
            }
        ]

    def normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        return raw
