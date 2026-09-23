"""
    Provides the TCP socket stream backend for sending trace data over TCP.

    This module contains the :class:`TcpStreamBackend` class which sends
    serialized trace data to a remote TCP endpoint with reconnection support.
"""

import socket
import time
import logging

from typing import Optional


logger = logging.getLogger(__name__)

DEFAULT_CONNECT_TIMEOUT = 5.0
DEFAULT_MAX_RETRIES = 3
DEFAULT_RETRY_BACKOFF = 0.5


class TcpStreamBackend:
    """
        Stream backend that sends trace data to a TCP endpoint.

        Supports automatic reconnection with exponential backoff on failure.
    """

    def __init__(self, host: str, port: int,
                 connect_timeout: float = DEFAULT_CONNECT_TIMEOUT,
                 max_retries: int = DEFAULT_MAX_RETRIES,
                 retry_backoff: float = DEFAULT_RETRY_BACKOFF) -> None:
        """
            Create a TcpStreamBackend.

            :param host: The remote host to connect to.
            :param port: The remote port to connect to.
            :param connect_timeout: Connection timeout in seconds.
            :param max_retries: Maximum number of reconnection attempts.
            :param retry_backoff: Initial backoff in seconds (doubles each retry).
        """
        self._host = host
        self._port = port
        self._connect_timeout = connect_timeout
        self._max_retries = max_retries
        self._retry_backoff = retry_backoff
        self._socket: Optional[socket.socket] = None
        self._connect()
        return

    def _connect(self) -> None:
        """
            Establish a TCP connection to the remote endpoint.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self._connect_timeout)
        sock.connect((self._host, self._port))
        self._socket = sock
        return

    def _reconnect(self) -> bool:
        """
            Attempt to reconnect with exponential backoff.

            :returns: True if reconnection succeeded, False otherwise.
        """
        backoff = self._retry_backoff
        for attempt in range(self._max_retries):
            try:
                self._close_socket()
                self._connect()
                rtnval = True
                return rtnval
            except OSError:
                logger.warning(
                    "Reconnect attempt %d/%d failed, retrying in %.1fs",
                    attempt + 1, self._max_retries, backoff
                )
                time.sleep(backoff)
                backoff *= 2

        rtnval = False
        return rtnval

    def write(self, data: bytes) -> None:
        """
            Send data over the TCP connection.

            On failure, attempts reconnection. If reconnection fails, the data
            is dropped and an error is logged.

            :param data: The bytes to send.
        """
        try:
            self._socket.sendall(data)
        except OSError:
            if not self._reconnect():
                logger.error(
                    "Failed to reconnect to %s:%d, dropping trace data",
                    self._host, self._port
                )
                return
            try:
                self._socket.sendall(data)
            except OSError:
                logger.error("Write failed after reconnect, dropping trace data")
        return

    def _close_socket(self) -> None:
        """
            Close the socket if open.
        """
        if self._socket is not None:
            try:
                self._socket.close()
            except OSError:
                # Best-effort close; the socket is discarded either way and a failure to close it
                # must not prevent the backend from reconnecting or shutting down.
                pass
            self._socket = None
        return

    def close(self) -> None:
        """
            Close the TCP connection.
        """
        self._close_socket()
        return
