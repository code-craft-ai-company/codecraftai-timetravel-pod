"""
    Provides the heartbeat sender for periodic health signaling.

    This module contains the :class:`HeartbeatSender` class which sends
    periodic heartbeat POST requests to a debugging service from a
    background daemon thread.
"""

import json
import time
import logging
import threading
import urllib.request


logger = logging.getLogger(__name__)

DEFAULT_HEARTBEAT_INTERVAL = 30.0  # seconds


class HeartbeatSender:
    """
        Sends periodic heartbeat to the debugging service.

        Uses ``threading.Event.wait(timeout)`` for interruptible sleeping,
        allowing clean shutdown via :meth:`stop`.
    """

    def __init__(self, service_url: str, service_credential: str,
                 instance_id: str,
                 interval: float = DEFAULT_HEARTBEAT_INTERVAL) -> None:
        """
            Create a HeartbeatSender.

            :param service_url: The base URL of the debugging service.
            :param service_credential: Bearer token for authentication.
            :param instance_id: The unique instance identifier.
            :param interval: The interval in seconds between heartbeats.
        """
        self._service_url = service_url.rstrip("/")
        self._service_credential = service_credential
        self._instance_id = instance_id
        self._interval = interval
        self._thread = None
        self._stop_event = threading.Event()
        return

    @property
    def interval(self) -> float:
        """
            The interval in seconds between heartbeats.
        """
        rtnval = self._interval
        return rtnval

    def start(self) -> None:
        """
            Start the heartbeat background thread.
        """
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
        self._thread.start()
        return

    def stop(self) -> None:
        """
            Stop the heartbeat background thread.
        """
        self._stop_event.set()
        if self._thread is not None:
            self._thread.join(timeout=self._interval + 2)
            self._thread = None
        return

    def _heartbeat_loop(self) -> None:
        """
            Main loop that sends heartbeats at the configured interval.
        """
        while not self._stop_event.is_set():
            self._send_heartbeat()
            self._stop_event.wait(timeout=self._interval)
        return

    def _send_heartbeat(self) -> None:
        """
            Send a single heartbeat POST request to the service.
        """
        payload = {
            "instance_id": self._instance_id,
            "timestamp": time.time(),
        }
        try:
            url = f"{self._service_url}/heartbeat"
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
                response.read()
        except Exception as exc:
            logger.warning("Heartbeat failed: %s", exc)
        return
