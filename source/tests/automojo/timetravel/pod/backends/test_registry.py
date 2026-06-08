"""
    Tests for the F2.4 Stream Backend Registry module.
"""

import os
import tempfile
import unittest

from ccai.timetravel.pod.backends.registry import StreamBackendRegistry
from ccai.timetravel.pod.backends.registry import create_default_registry
from ccai.timetravel.pod.backends.filebackend import FileStreamBackend


class TestStreamBackendRegistry(unittest.TestCase):
    """
        Tests for the StreamBackendRegistry class.
    """

    def test_register_and_create_backend(self):
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

        self.assertEqual(len(created_backends), 1)
        self.assertEqual(result["scheme"], "mock")
        self.assertEqual(result["path"], "/some/path")

        return

    def test_unknown_scheme_raises_value_error(self):
        """
            Verify creating a backend with an unknown scheme raises ValueError.
        """
        registry = StreamBackendRegistry()

        with self.assertRaises(ValueError) as ctx:
            registry.create_backend("unknown:///path")

        self.assertIn("unknown", str(ctx.exception))

        return

    def test_registered_schemes_returns_scheme_list(self):
        """
            Verify registered_schemes returns the list of registered schemes.
        """
        registry = StreamBackendRegistry()
        registry.register("alpha", lambda p: None)
        registry.register("beta", lambda p: None)

        schemes = registry.registered_schemes

        self.assertIn("alpha", schemes)
        self.assertIn("beta", schemes)
        self.assertEqual(len(schemes), 2)

        return


class TestCreateDefaultRegistry(unittest.TestCase):
    """
        Tests for the create_default_registry function.
    """

    def test_default_registry_has_file_tcp_unix_schemes(self):
        """
            Verify the default registry has file, tcp, and unix schemes.
        """
        registry = create_default_registry()

        schemes = registry.registered_schemes

        self.assertIn("file", schemes)
        self.assertIn("tcp", schemes)
        self.assertIn("unix", schemes)

        return

    def test_file_scheme_creates_file_backend(self):
        """
            Verify the file scheme creates a FileStreamBackend.
        """
        registry = create_default_registry()

        temp_dir = tempfile.mkdtemp()
        file_path = os.path.join(temp_dir, "test_trace.bin")
        uri = f"file://{file_path}"

        backend = registry.create_backend(uri)

        self.assertIsInstance(backend, FileStreamBackend)

        backend.write(b"test")
        backend.close()

        with open(file_path, "rb") as f:
            content = f.read()

        self.assertEqual(content, b"test")

        # Clean up
        os.remove(file_path)
        os.rmdir(temp_dir)

        return


if __name__ == "__main__":
    unittest.main()
