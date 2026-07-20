#!/usr/bin/env python
import logging
import math
from collections.abc import Mapping
from typing import Any

import requests
from agent_utilities.core.config import setting
from agent_utilities.core.exceptions import ApiError, AuthError

logger = logging.getLogger(__name__)


class BaseApiClient:
    def __init__(
        self,
        public_key: str,
        secret_key: str,
        host: str,
        timeout: float | None = None,
        transport_kwargs: Mapping[str, Any] | None = None,
    ):
        self.public_key = public_key
        self.secret_key = secret_key
        self.host = host.rstrip("/")
        configured = timeout
        if configured is None:
            try:
                configured = float(setting("LANGFUSE_REQUEST_TIMEOUT_SECONDS", "30"))
            except (TypeError, ValueError):
                configured = 30.0
        if not math.isfinite(configured):
            configured = 30.0
        self.timeout = min(120.0, max(1.0, configured))
        supplied_transport = dict(transport_kwargs or {})
        if not supplied_transport.keys() <= {"verify", "cert", "proxies"}:
            raise ValueError("langfuse_transport_contract_invalid")
        self._transport_kwargs = supplied_transport

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
                timeout=self.timeout,
                **self._transport_kwargs,
            )
            if response.status_code == 401:
                raise AuthError("langfuse_authentication_failed")
            response.raise_for_status()
            if response.text:
                return response.json()
            return {"success": True}
        except requests.exceptions.RequestException as e:
            raise ApiError(f"langfuse_api_request_failed:{type(e).__name__}") from None
