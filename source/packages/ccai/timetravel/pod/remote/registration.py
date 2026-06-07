"""
    Provides service registration with an external debugging service.

    This module contains the :class:`ServiceRegistration` class which manages
    registering and unregistering application instances with a remote debugging
    service using JSON POST requests via ``urllib.request``.
"""

import json
import logging
import urllib.request
import uuid

from typing import Optional


logger = logging.getLogger(__name__)


class ServiceRegistration:
    """
        Manages registration with an external debugging service.

        Sends JSON payloads to ``/register`` and ``/unregister`` endpoints
        with a Bearer token for authentication.
    """

    def __init__(self, service_url: str, service_credential: str,
                 remote_host: str, remote_port: int,
                 instance_credential: str) -> None:
        """
            Create a ServiceRegistration.

            :param service_url: The base URL of the debugging service.
            :param service_credential: Bearer token for authenticating with the service.
            :param remote_host: The host this instance's remote control server listens on.
            :param remote_port: The port this instance's remote control server listens on.
            :param instance_credential: The credential for connecting to this instance.
        """
        self._service_url = service_url.rstrip("/")
        self._service_credential = service_credential
        self._remote_host = remote_host
        self._remote_port = remote_port
        self._instance_credential = instance_credential
        self._instance_id = str(uuid.uuid4())
        self._registered = False
        return

    @property
    def instance_id(self) -> str:
        """
            The unique instance identifier (UUID string).
        """
        rtnval = self._instance_id
        return rtnval

    @property
    def registered(self) -> bool:
        """
            Whether this instance is currently registered.
        """
        rtnval = self._registered
        return rtnval

    def register(self) -> bool:
        """
            Register this application instance with the debugging service.

            :returns: True if registration succeeded, False otherwise.
        """
        payload = {
            "instance_id": self._instance_id,
            "remote_host": self._remote_host,
            "remote_port": self._remote_port,
            "instance_credential": self._instance_credential,
        }
        try:
            self._send_request("/register", payload)
            self._registered = True
            logger.info(
                "Registered with debugging service: %s (instance: %s)",
                self._service_url, self._instance_id
            )
            rtnval = True
            return rtnval
        except Exception as exc:
            logger.error("Failed to register with debugging service: %s", exc)
            rtnval = False
            return rtnval

    def unregister(self) -> None:
        """
            Unregister this application instance from the debugging service.
        """
        if not self._registered:
            return

        payload = {"instance_id": self._instance_id}
        try:
            self._send_request("/unregister", payload)
            self._registered = False
            logger.info(
                "Unregistered from debugging service: %s",
                self._service_url
            )
        except Exception as exc:
            logger.error(
                "Failed to unregister from debugging service: %s", exc
            )
        return

    def _send_request(self, path: str, payload: dict) -> bytes:
        """
            Send a JSON POST request to the debugging service.

            :param path: The URL path (e.g. "/register").
            :param payload: The JSON payload to send.

            :returns: The response body as bytes.
        """
        url = f"{self._service_url}{path}"
        data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._service_credential}",
            },
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=10) as response:
            rtnval = response.read()
        return rtnval
