"""
    Tests for the F2.4 Stream Backend Registry module.
"""

import os
import tempfile

from automojo.timetravel.pod.backends.registry import StreamBackendRegistry
from automojo.timetravel.pod.backends.registry import create_default_registry
from automojo.timetravel.pod.backends.filebackend import FileStreamBackend


def test_register_and_create_backend() -> None:
    """
        Verify a registered factory can create a backend via URI.
    """
    registry = StreamBackendRegistry()

    created_backends = []

    def mock_factory(parsed):
        backend = {"scheme": parsed.scheme, "path": parsed.path}
        created_backends.append(backend)
        rtnval = backend
        return rtnval

    registry.register("mock", mock_factory)

    result = registry.create_backend("mock:///some/path")

    assert len(created_backends) == 1
    assert result["scheme"] == "mock"
    assert result["path"] == "/some/path"

    return


def test_unknown_scheme_raises_value_error() -> None:
    """
        Verify creating a backend with an unknown scheme raises ValueError.
    """
    registry = StreamBackendRegistry()

    raised = False
    exception_text = ""
    try:
        registry.create_backend("unknown:///path")
    except ValueError as err:
        raised = True
        exception_text = str(err)

    assert raised
    assert "unknown" in exception_text

    return


def test_registered_schemes_returns_scheme_list() -> None:
    """
        Verify registered_schemes returns the list of registered schemes.
    """
    registry = StreamBackendRegistry()
    registry.register("alpha", lambda p: None)
    registry.register("beta", lambda p: None)

    schemes = registry.registered_schemes

    assert "alpha" in schemes
    assert "beta" in schemes
    assert len(schemes) == 2

    return


def test_default_registry_has_file_tcp_unix_schemes() -> None:
    """
        Verify the default registry has file, tcp, and unix schemes.
    """
    registry = create_default_registry()

    schemes = registry.registered_schemes

    assert "file" in schemes
    assert "tcp" in schemes
    assert "unix" in schemes

    return


def test_file_scheme_creates_file_backend() -> None:
    """
        Verify the file scheme creates a FileStreamBackend.
    """
    registry = create_default_registry()

    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, "test_trace.bin")
    uri = "file://{}".format(file_path)

    backend = registry.create_backend(uri)

    assert isinstance(backend, FileStreamBackend)

    backend.write(b"test")
    backend.close()

    with open(file_path, "rb") as f:
        content = f.read()

    assert content == b"test"

    # Clean up
    os.remove(file_path)
    os.rmdir(temp_dir)

    return
