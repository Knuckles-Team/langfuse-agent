import os
from typing import Dict, Any, Optional
import requests
from agent_utilities.exceptions import AuthError, ApiError

class LangfuseApi:
    def __init__(self, public_key: str, secret_key: str, host: str):
        self.public_key = public_key
        self.secret_key = secret_key
        self.host = host.rstrip("/")

    def _request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.host}{endpoint}"
        try:
            response = requests.request(
                method, 
                url, 
                auth=(self.public_key, self.secret_key), 
                json=data, 
                params=params,
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 401:
                raise AuthError(f"Unauthorized: {response.text}")
            response.raise_for_status()
            if response.text:
                return response.json()
            return {"success": True}
        except requests.exceptions.RequestException as e:
            raise ApiError(f"API request failed: {e}")

    def get_annotation_queues(self, page: int = 1, limit: int = 50) -> Dict[str, Any]:
        """Get all annotation queues"""
        return self._request("GET", "/api/public/annotation-queues", params={"page": page, "limit": limit})

    def get_metrics(self) -> Dict[str, Any]:
        """Get metrics"""
        return self._request("GET", "/api/public/metrics/daily")

    def get_traces(self, page: int = 1, limit: int = 50) -> Dict[str, Any]:
        """Get traces"""
        return self._request("GET", "/api/public/traces", params={"page": page, "limit": limit})
