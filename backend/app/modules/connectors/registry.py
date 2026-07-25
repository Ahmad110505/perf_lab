from typing import Type
from app.modules.connectors.base import BaseConnector
from app.modules.connectors.providers.procore import ProcoreConnector
from app.modules.connectors.providers.autodesk import AutodeskConnector
from app.modules.connectors.providers.generic_webhook import GenericWebhookConnector
from app.modules.connectors.providers.google_analytics import GoogleAnalyticsConnector
from app.modules.connectors.providers.google_search_console import GoogleSearchConsoleConnector
from app.modules.connectors.providers.meta import MetaConnector
from app.modules.connectors.providers.ahrefs import AhrefsConnector
from app.modules.connectors.providers.semrush import SEMrushConnector
from app.modules.connectors.providers.google_tag_manager import GoogleTagManagerConnector
from app.modules.connectors.providers.google_business_profile import GoogleBusinessProfileConnector

def get_connector_for_provider(provider: str) -> Type[BaseConnector]:
    if provider == "procore":
        return ProcoreConnector
    elif provider == "autodesk":
        return AutodeskConnector
    elif provider == "generic_webhook":
        return GenericWebhookConnector
    elif provider == "google_analytics":
        return GoogleAnalyticsConnector
    elif provider == "google_search_console":
        return GoogleSearchConsoleConnector
    elif provider == "meta":
        return MetaConnector
    elif provider == "ahrefs":
        return AhrefsConnector
    elif provider == "semrush":
        return SEMrushConnector
    elif provider == "google_tag_manager":
        return GoogleTagManagerConnector
    elif provider == "google_business_profile":
        return GoogleBusinessProfileConnector
    raise ValueError(f"Unknown provider: {provider}")
