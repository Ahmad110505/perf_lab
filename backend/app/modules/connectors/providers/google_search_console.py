from typing import Dict, Any, List
from datetime import datetime, timedelta
import httpx
from app.modules.connectors.base import BaseConnector
from app.core.exceptions import TransientSyncError

class GoogleSearchConsoleConnector(BaseConnector):
    def authenticate(self) -> None:
        pass

    def fetch_data(self) -> List[Dict[str, Any]]:
        raw_pid = (self.config or {}).get("project_id", 1)
        try:
            project_id = int(raw_pid)
        except (ValueError, TypeError):
            project_id = 1

        access_token = self.config.get("access_token") or self.config.get("api_key")
        site_url = self.config.get("site_url") or self.config.get("domain")

        if access_token and site_url and access_token.startswith("ya29."):
            url = f"https://www.googleapis.com/webmasters/v3/sites/{site_url}/searchAnalytics/query"
            headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
            payload = {
                "startDate": (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),
                "endDate": datetime.now().strftime("%Y-%m-%d"),
                "dimensions": ["date"]
            }
            try:
                response = httpx.post(url, json=payload, headers=headers, timeout=10.0)
                if response.status_code == 200:
                    rows = response.json().get("rows", [])
                    results = []
                    for r in rows:
                        results.append({
                            "project_id": project_id,
                            "date": r.get("keys", [datetime.now().strftime("%Y-%m-%d")])[0],
                            "clicks": int(r.get("clicks", 0)),
                            "impressions": int(r.get("impressions", 0)),
                            "ctr": float(r.get("ctr", 0.0)) * 100,
                            "position": float(r.get("position", 0.0))
                        })
                    if results:
                        return results
                else:
                    raise TransientSyncError(f"Google Search Console API HTTP {response.status_code}: {response.text}")
            except Exception as e:
                raise TransientSyncError(f"Failed to fetch live Search Console metrics: {str(e)}")

        raise TransientSyncError("Missing or invalid access credentials for real API.")

    def normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        return raw
