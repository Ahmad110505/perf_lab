import abc
from typing import Dict, Any, List

class BaseConnector(abc.ABC):
    def __init__(self, config: Dict[str, Any], credentials_ref: str | None = None):
        self.config = config
        self.credentials_ref = credentials_ref

    @abc.abstractmethod
    def authenticate(self) -> None:
        pass

    @abc.abstractmethod
    def fetch_data(self) -> List[Dict[str, Any]]:
        # Returning a list as standard contract for now
        pass

    @abc.abstractmethod
    def normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        pass
