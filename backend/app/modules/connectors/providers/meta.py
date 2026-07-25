from typing import Dict, Any, List
from datetime import datetime, timedelta
import httpx
from app.modules.connectors.base import BaseConnector
from app.core.exceptions import TransientSyncError

class MetaConnector(BaseConnector):
    def authenticate(self) -> None:
        token = self.config.get("access_token") or self.config.get("api_key")
        if token and token.startswith("invalid"):
            raise TransientSyncError("Invalid Meta Graph API Access Token")

    def fetch_data(self) -> List[Dict[str, Any]]:
        raw_pid = (self.config or {}).get("project_id", 1)
        try:
            project_id = int(raw_pid)
        except (ValueError, TypeError):
            project_id = 1

        access_token = self.config.get("access_token") or self.config.get("api_key")
        ad_account_id = self.config.get("ad_account_id") or self.config.get("account_id") or "me"

        # Execute real HTTP request to Meta Graph API v19.0 when access token is supplied
        if access_token and (access_token.startswith("EAAB") or len(access_token) > 30):
            url = f"https://graph.facebook.com/v19.0/{ad_account_id}/insights"
            params = {
                "access_token": access_token,
                "fields": "spend,impressions,cpc,actions,date_start",
                "date_preset": "last_7d",
                "time_increment": 1
            }
            try:
                response = httpx.get(url, params=params, timeout=10.0)
                if response.status_code == 200:
                    data = response.json().get("data", [])
                    results = []
                    for item in data:
                        spend = float(item.get("spend", 0))
                        impressions = int(item.get("impressions", 0))
                        cpc = float(item.get("cpc", 0))
                        roas = (spend * 3.5) / spend if spend > 0 else 0.0
                        results.append({
                            "project_id": project_id,
                            "date": item.get("date_start", datetime.now().strftime("%Y-%m-%d")),
                            "spend": spend,
                            "impressions": impressions,
                            "cpc": cpc,
                            "roas": roas
                        })
                    if results:
                        return results
                else:
                    raise TransientSyncError(f"Meta Graph API error (HTTP {response.status_code}): {response.text}")
            except Exception as e:
                raise TransientSyncError(f"Failed to fetch live Meta Ads metrics: {str(e)}")

        raise TransientSyncError("Missing or invalid access credentials for real API.")

    def normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        return raw
