from typing import Dict, Any, List
from app.modules.connectors.base import BaseConnector

class GoogleTagManagerConnector(BaseConnector):
    def authenticate(self) -> None:
        pass

    def fetch_data(self) -> List[Dict[str, Any]]:
        project_id = self.config.get("project_id", 1)
        container_id = self.config.get("container_id", "GTM-5W89X22")
        return [
            {
                "project_id": project_id,
                "container_id": container_id,
                "event_name": "lead_form_submit",
                "trigger_count": 320,
                "date": "2026-07-22"
            },
            {
                "project_id": project_id,
                "container_id": container_id,
                "event_name": "phone_call_click",
                "trigger_count": 145,
                "date": "2026-07-22"
            }
        ]

    def normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        return raw
