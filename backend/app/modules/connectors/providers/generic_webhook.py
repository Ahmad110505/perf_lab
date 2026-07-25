from typing import Dict, Any, List
from app.modules.connectors.base import BaseConnector

class GenericWebhookConnector(BaseConnector):
    def authenticate(self) -> None:
        raise NotImplementedError()

    def fetch_data(self) -> List[Dict[str, Any]]:
        raise NotImplementedError()

    def normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError()
