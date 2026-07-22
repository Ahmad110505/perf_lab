from typing import Type
from app.modules.connectors.base import BaseConnector
from app.modules.connectors.providers.procore import ProcoreConnector
from app.modules.connectors.providers.autodesk import AutodeskConnector
from app.modules.connectors.providers.generic_webhook import GenericWebhookConnector

def get_connector_for_provider(provider: str) -> Type[BaseConnector]:
    if provider == "procore":
        return ProcoreConnector
    elif provider == "autodesk":
        return AutodeskConnector
    elif provider == "generic_webhook":
        return GenericWebhookConnector
    raise ValueError(f"Unknown provider: {provider}")
