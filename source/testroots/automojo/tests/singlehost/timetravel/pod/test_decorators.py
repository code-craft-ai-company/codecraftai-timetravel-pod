"""
    Tests for the F4.2 Convenience Decorators module.
"""

import asyncio

from automojo.timetravel.pod.decorators import trace_portal
from automojo.timetravel.pod.decorators import create_gateway
from automojo.timetravel.pod.gateway import TimeTravelGateway


def test_preserves_function_name_and_docstring() -> None:
    """
        Verify @trace_portal on a sync function preserves name and docstring.
    """

    @trace_portal("test_portal")
    def my_function():
        """My docstring."""
        return 42

    assert my_function.__name__ == "my_function"
    assert my_function.__doc__ == "My docstring."

    return


def test_decorated_function_executes_normally() -> None:
    """
        Verify decorated function executes and returns normally.
    """

    @trace_portal("test_portal")
    def add(a, b):
        rtnval = a + b
        return rtnval

    result = add(3, 4)

    assert result == 7

    return


def test_async_function_works() -> None:
    """
        Verify @trace_portal on an async function works correctly.
    """

    @trace_portal("async_portal")
    async def async_func():
        """Async docstring."""
        rtnval = 42
        return rtnval

    assert async_func.__name__ == "async_func"
    assert async_func.__doc__ == "Async docstring."

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(async_func())
    finally:
        loop.close()
    assert result == 42

    return


def test_decorated_function_with_args_and_kwargs() -> None:
    """
        Verify decorated function correctly passes args and kwargs.
    """

    @trace_portal("test_portal")
    def greet(name, greeting="Hello"):
        rtnval = f"{greeting}, {name}!"
        return rtnval

    result = greet("World", greeting="Hi")

    assert result == "Hi, World!"

    return


def test_returns_gateway_with_correct_defaults() -> None:
    """
        Verify create_gateway returns a TimeTravelGateway with correct defaults.
    """
    gateway = create_gateway()

    assert isinstance(gateway, TimeTravelGateway)
    assert gateway.configuration.trace_calls
    assert not gateway.configuration.trace_lines
    assert not gateway.configuration.trace_variables
    assert not gateway.configuration.record_inner_portals
    assert gateway.backend_uri is None

    return


def test_custom_parameters_create_correct_configuration() -> None:
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

    assert isinstance(gateway, TimeTravelGateway)
    assert not gateway.configuration.trace_calls
    assert gateway.configuration.trace_lines
    assert gateway.configuration.trace_variables
    assert gateway.configuration.record_inner_portals
    assert gateway.backend_uri == "file:///tmp/test.bin"

    return
