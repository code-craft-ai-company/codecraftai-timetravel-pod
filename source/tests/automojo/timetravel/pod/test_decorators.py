"""
    Tests for the F4.2 Convenience Decorators module.
"""

import asyncio
import unittest

from automojo.timetravel.pod.decorators import trace_portal
from automojo.timetravel.pod.decorators import create_gateway
from automojo.timetravel.pod.gateway import TimeTravelGateway


class TestTracePortalDecorator(unittest.TestCase):
    """
        Tests for the trace_portal decorator.
    """

    def test_preserves_function_name_and_docstring(self):
        """
            Verify @trace_portal on a sync function preserves name and docstring.
        """

        @trace_portal("test_portal")
        def my_function():
            """My docstring."""
            return 42

        self.assertEqual(my_function.__name__, "my_function")
        self.assertEqual(my_function.__doc__, "My docstring.")

        return

    def test_decorated_function_executes_normally(self):
        """
            Verify decorated function executes and returns normally.
        """

        @trace_portal("test_portal")
        def add(a, b):
            rtnval = a + b
            return rtnval

        result = add(3, 4)

        self.assertEqual(result, 7)

        return

    def test_async_function_works(self):
        """
            Verify @trace_portal on an async function works correctly.
        """

        @trace_portal("async_portal")
        async def async_func():
            """Async docstring."""
            rtnval = 42
            return rtnval

        self.assertEqual(async_func.__name__, "async_func")
        self.assertEqual(async_func.__doc__, "Async docstring.")

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(async_func())
        finally:
            loop.close()
        self.assertEqual(result, 42)

        return

    def test_decorated_function_with_args_and_kwargs(self):
        """
            Verify decorated function correctly passes args and kwargs.
        """

        @trace_portal("test_portal")
        def greet(name, greeting="Hello"):
            rtnval = f"{greeting}, {name}!"
            return rtnval

        result = greet("World", greeting="Hi")

        self.assertEqual(result, "Hi, World!")

        return


class TestCreateGateway(unittest.TestCase):
    """
        Tests for the create_gateway factory function.
    """

    def test_returns_gateway_with_correct_defaults(self):
        """
            Verify create_gateway returns a TimeTravelGateway with correct defaults.
        """
        gateway = create_gateway()

        self.assertIsInstance(gateway, TimeTravelGateway)
        self.assertTrue(gateway.configuration.trace_calls)
        self.assertFalse(gateway.configuration.trace_lines)
        self.assertFalse(gateway.configuration.trace_variables)
        self.assertFalse(gateway.configuration.record_inner_portals)
        self.assertIsNone(gateway.backend_uri)

        return

    def test_custom_parameters_create_correct_configuration(self):
        """
            Verify create_gateway with custom parameters creates correct config.
        """
        gateway = create_gateway(
            trace_calls=False,
            trace_lines=True,
            trace_variables=True,
            record_inner_portals=True,
            backend_uri="file:///tmp/test.bin",
        )

        self.assertIsInstance(gateway, TimeTravelGateway)
        self.assertFalse(gateway.configuration.trace_calls)
        self.assertTrue(gateway.configuration.trace_lines)
        self.assertTrue(gateway.configuration.trace_variables)
        self.assertTrue(gateway.configuration.record_inner_portals)
        self.assertEqual(gateway.backend_uri, "file:///tmp/test.bin")

        return


if __name__ == "__main__":
    unittest.main()
