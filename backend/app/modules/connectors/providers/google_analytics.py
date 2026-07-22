from typing import Dict, Any, List
from app.modules.connectors.base import BaseConnector

class GoogleAnalyticsConnector(BaseConnector):
    def authenticate(self) -> None:
        pass

    def fetch_data(self) -> List[Dict[str, Any]]:
        # Mock payload injecting project_id from config
        project_id = self.config.get("project_id", 1)
        return [
            {
                "project_id": project_id,
                "date": "2023-01-01",
                "sessions": 1500,
                "bounce_rate": 45.2
            },
            {
                "project_id": project_id,
                "date": "2023-01-02",
                "sessions": 1600,
                "bounce_rate": 44.8
            }
        ]

    def normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        return raw
