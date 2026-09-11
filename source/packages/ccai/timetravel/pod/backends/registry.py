"""
    Provides the stream backend registry for URI-based backend creation.

    This module contains the :class:`StreamBackendRegistry` class which maps
    URI schemes to backend factory functions, and the default registry
    factory that pre-registers the file, TCP, and Unix backends.
"""

from urllib.parse import urlparse
from urllib.request import url2pathname

from ccai.timetravel.pod.backends.filebackend import FileStreamBackend
from ccai.timetravel.pod.backends.tcpbackend import TcpStreamBackend
from ccai.timetravel.pod.backends.unixbackend import UnixStreamBackend


class StreamBackendRegistry:
    """
        Registry mapping URI schemes to stream backend factory functions.
    """

    def __init__(self) -> None:
        self._factories: dict = {}
        return

    def register(self, scheme: str, factory) -> None:
        """
            Register a factory function for a URI scheme.

            :param scheme: The URI scheme (e.g. "file", "tcp", "unix").
            :param factory: A callable that accepts a ParseResult and returns a backend.
        """
        self._factories[scheme] = factory
        return

    def create_backend(self, uri: str):
        """
            Parse a URI and create the corresponding stream backend.

            :param uri: A URI string such as "file:///tmp/trace.bin" or "tcp://host:9090".

            :returns: A stream backend instance.

            :raises: ValueError
        """
        parsed = urlparse(uri)
        scheme = parsed.scheme

        if scheme not in self._factories:
            errmsg = (
                f"Unknown stream backend scheme: '{scheme}'. "
                f"Known schemes: {list(self._factories.keys())}"
            )
            raise ValueError(errmsg)

        factory = self._factories[scheme]
        rtnval = factory(parsed)
        return rtnval

    @property
    def registered_schemes(self) -> list:
        """
            Return the list of registered URI schemes.

            :returns: A list of scheme strings.
        """
        rtnval = list(self._factories.keys())
        return rtnval


def _create_file_backend(parsed) -> FileStreamBackend:
    """
        Factory function for creating a FileStreamBackend from a parsed URI.

        The URI path is converted back into a native filesystem path with
        :func:`urllib.request.url2pathname` so that a URI produced by
        :meth:`pathlib.Path.as_uri` round-trips on every platform.  On Windows
        ``file:///C:/traces/trace.bin`` parses to the path ``/C:/traces/trace.bin``,
        which is not a usable filesystem path until the leading slash is removed
        and the separators are converted.

        :param parsed: A urllib.parse.ParseResult.

        :returns: A FileStreamBackend instance.
    """
    file_path = url2pathname(parsed.path)
    rtnval = FileStreamBackend(file_path=file_path)
    return rtnval


def _create_tcp_backend(parsed) -> TcpStreamBackend:
    """
        Factory function for creating a TcpStreamBackend from a parsed URI.

        :param parsed: A urllib.parse.ParseResult.

        :returns: A TcpStreamBackend instance.
    """
    host = parsed.hostname or "localhost"
    port = parsed.port or 9090
    rtnval = TcpStreamBackend(host=host, port=port)
    return rtnval


def _create_unix_backend(parsed) -> UnixStreamBackend:
    """
        Factory function for creating a UnixStreamBackend from a parsed URI.

        :param parsed: A urllib.parse.ParseResult.

        :returns: A UnixStreamBackend instance.
    """
    socket_path = parsed.path
    rtnval = UnixStreamBackend(socket_path=socket_path)
    return rtnval


def create_default_registry() -> StreamBackendRegistry:
    """
        Create and return a pre-configured StreamBackendRegistry with the
        built-in file, TCP, and Unix backend factories.

        :returns: A StreamBackendRegistry with "file", "tcp", and "unix" registered.
    """
    registry = StreamBackendRegistry()
    registry.register("file", _create_file_backend)
    registry.register("tcp", _create_tcp_backend)
    registry.register("unix", _create_unix_backend)
    rtnval = registry
    return rtnval
