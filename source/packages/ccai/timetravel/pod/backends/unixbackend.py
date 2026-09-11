"""
    Provides the Unix domain socket stream backend for sending trace data.

    This module contains the :class:`UnixStreamBackend` class which sends
    serialized trace data over a Unix domain socket with reconnection support.
"""

import logging
import os
import socket
import sys
import time

from typing import Optional

from ccai.errors.exceptions import ConfigurationError


logger = logging.getLogger(__name__)

DEFAULT_CONNECT_TIMEOUT = 5.0
DEFAULT_MAX_RETRIES = 3
DEFAULT_RETRY_BACKOFF = 0.5


class UnixStreamBackend:
    """
        Stream backend that sends trace data over a Unix domain socket.

        Supports automatic reconnection with exponential backoff on failure.
    """

    def __init__(self, socket_path: str,
                 connect_timeout: float = DEFAULT_CONNECT_TIMEOUT,
                 max_retries: int = DEFAULT_MAX_RETRIES,
                 retry_backoff: float = DEFAULT_RETRY_BACKOFF) -> None:
        """
            Create a UnixStreamBackend.

            :param socket_path: The path to the Unix domain socket.
            :param connect_timeout: Connection timeout in seconds.
            :param max_retries: Maximum number of reconnection attempts.
            :param retry_backoff: Initial backoff in seconds (doubles each retry).
        """
        self._socket_path = socket_path
        self._connect_timeout = connect_timeout
        self._max_retries = max_retries
        self._retry_backoff = retry_backoff
        self._socket: Optional[socket.socket] = None

        # Unix domain sockets are only available where the 'socket' module exposes
        # 'AF_UNIX'.  Check this here, at the point of use, so that a 'unix://'
        # backend configured on a platform without them (such as Windows) fails
        # with a clear message rather than an AttributeError from deep inside the
        # connect path.
        if not hasattr(socket, "AF_UNIX"):
            errmsg_lines = [
                "Unix domain sockets are not supported on this platform.",
                f"    platform: {sys.platform}",
                f"    socket_path: {socket_path}",
                "Use a 'file://' or 'tcp://' stream backend on this platform instead.",
            ]
            errmsg = os.linesep.join(errmsg_lines)
            raise ConfigurationError(errmsg)

        self._connect()
        return

    def _connect(self) -> None:
        """
            Establish a Unix domain socket connection.
        """
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(self._connect_timeout)
        sock.connect(self._socket_path)
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
                    "Unix socket reconnect attempt %d/%d failed",
                    attempt + 1, self._max_retries
                )
                time.sleep(backoff)
                backoff *= 2

        rtnval = False
        return rtnval

    def write(self, data: bytes) -> None:
        """
            Send data over the Unix domain socket.

            On failure, attempts reconnection. If reconnection fails, the data
            is dropped and an error is logged.

            :param data: The bytes to send.
        """
        try:
            self._socket.sendall(data)
        except OSError:
            if not self._reconnect():
                logger.error(
                    "Failed to reconnect to %s, dropping trace data",
                    self._socket_path
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
                pass
            self._socket = None
        return

    def close(self) -> None:
        """
            Close the Unix domain socket connection.
        """
        self._close_socket()
        return
