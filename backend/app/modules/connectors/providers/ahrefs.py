from typing import Dict, Any, List
from app.modules.connectors.base import BaseConnector

class AhrefsConnector(BaseConnector):
    def authenticate(self) -> None:
        pass

    def fetch_data(self) -> List[Dict[str, Any]]:
        project_id = self.config.get("project_id", 1)
        return [
            {
                "project_id": project_id,
                "date": "2023-01-01",
                "domain_rating": 58,
                "backlinks": 12400,
                "referring_domains": 850
            },
            {
                "project_id": project_id,
                "date": "2023-01-02",
                "domain_rating": 58,
                "backlinks": 12450,
                "referring_domains": 855
            }
        ]

    def normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        return raw
