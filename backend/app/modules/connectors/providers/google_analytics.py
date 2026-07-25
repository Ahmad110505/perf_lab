from typing import Dict, Any, List
from datetime import datetime, timedelta
import httpx
from app.modules.connectors.base import BaseConnector
from app.core.exceptions import TransientSyncError

class GoogleAnalyticsConnector(BaseConnector):
    def authenticate(self) -> None:
        token = self.config.get("access_token") or self.config.get("api_key")
        if token and token.startswith("invalid"):
            raise TransientSyncError("Invalid Google Analytics API token provided")

    def fetch_data(self) -> List[Dict[str, Any]]:
        raw_pid = (self.config or {}).get("project_id", 1)
        try:
            project_id = int(raw_pid)
        except (ValueError, TypeError):
            project_id = 1

        property_id = self.config.get("property_id") or self.config.get("measurement_id")
        access_token = self.config.get("access_token") or self.config.get("api_key")

        # Execute real HTTP request to GA4 Data API when OAuth access_token is supplied
        if property_id and access_token and access_token.startswith("ya29."):
            url = f"https://analyticsdata.googleapis.com/v1beta/properties/{property_id}:runReport"
            headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
            payload = {
                "dateRanges": [{"startDate": "7daysAgo", "endDate": "today"}],
                "dimensions": [{"name": "date"}],
                "metrics": [{"name": "sessions"}, {"name": "conversions"}, {"name": "bounceRate"}]
            }
            try:
                response = httpx.post(url, json=payload, headers=headers, timeout=10.0)
                if response.status_code == 200:
                    data = response.json()
                    rows = data.get("rows", [])
                    results = []
                    for row in rows:
                        d_raw = row.get("dimensionValues", [{}])[0].get("value", "")
                        d_str = datetime.strptime(d_raw, "%Y%m%d").strftime("%Y-%m-%d") if len(d_raw) == 8 else datetime.now().strftime("%Y-%m-%d")
                        mv = row.get("metricValues", [{}, {}, {}])
                        results.append({
                            "project_id": project_id,
                            "date": d_str,
                            "sessions": float(mv[0].get("value", 0)),
                            "conversions": float(mv[1].get("value", 0)),
                            "bounce_rate": float(mv[2].get("value", 0)) * 100 if float(mv[2].get("value", 0)) <= 1.0 else float(mv[2].get("value", 0))
                        })
                    if results:
                        return results
                else:
                    raise TransientSyncError(f"GA4 Data API returned HTTP {response.status_code}: {response.text}")
            except Exception as e:
                raise TransientSyncError(f"Failed to fetch live GA4 metrics: {str(e)}")

        raise TransientSyncError("Missing or invalid access credentials for real API.")

    def normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        return raw
