from typing import Dict, Any, List
from app.modules.connectors.base import BaseConnector

class GoogleSearchConsoleConnector(BaseConnector):
    def authenticate(self) -> None:
        pass

    def fetch_data(self) -> List[Dict[str, Any]]:
        project_id = self.config.get("project_id", 1)
        return [
            {
                "project_id": project_id,
                "date": "2023-01-01",
                "clicks": 420,
                "impressions": 12500,
                "ctr": 3.36,
                "position": 14.2
            },
            {
                "project_id": project_id,
                "date": "2023-01-02",
                "clicks": 480,
                "impressions": 13800,
                "ctr": 3.47,
                "position": 13.8
            }
        ]

    def normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        return raw
