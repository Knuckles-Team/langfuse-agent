#!/usr/bin/env python
import logging
from typing import Any

import requests
from agent_utilities.core.exceptions import ApiError, AuthError

logger = logging.getLogger(__name__)


class BaseApiClient:
    def __init__(self, public_key: str, secret_key: str, host: str):
        self.public_key = public_key
        self.secret_key = secret_key
        self.host = host.rstrip("/")

    def _request(
        self,
        method: str,
        endpoint: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        url = f"{self.host}{endpoint}"
        try:
            response = requests.request(
                method,
                url,
                auth=(self.public_key, self.secret_key),
                json=data,
                params=params,
                headers={"Content-Type": "application/json"},
            )
            if response.status_code == 401:
                raise AuthError(f"Unauthorized: {response.text}")
            response.raise_for_status()
            if response.text:
                return response.json()
            return {"success": True}
        except requests.exceptions.RequestException as e:
            raise ApiError(f"API request failed: {e}") from e
