"""
    Provides convenience decorators and factory functions for time travel tracing.

    This module contains the :func:`trace_portal` decorator for wrapping
    functions in a :class:`TimeTravelPortal` context, and the :func:`create_gateway`
    factory for easily creating :class:`TimeTravelGateway` instances.
"""

import functools
import inspect

from typing import Optional

from ccai.timetravel.pod.portal import TimeTravelPortal
from ccai.timetravel.pod.gateway import TimeTravelGateway
from ccai.timetravel.pod.traceconfiguration import TraceConfiguration


def trace_portal(name: str):
    """
        Decorator that wraps a function body in a TimeTravelPortal.

        Supports both sync and async functions.

        :param name: The portal name.

        :returns: A decorator function.
    """

    def decorator(func):
        if inspect.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                with TimeTravelPortal(name):
                    rtnval = await func(*args, **kwargs)
                return rtnval
            return async_wrapper
        else:
            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs):
                with TimeTravelPortal(name):
                    rtnval = func(*args, **kwargs)
                return rtnval
            return sync_wrapper

    return decorator


def create_gateway(
    trace_calls: bool = True,
    trace_lines: bool = False,
    trace_variables: bool = False,
    record_inner_portals: bool = False,
    backend_uri: Optional[str] = None,
) -> TimeTravelGateway:
    """
        Create a TimeTravelGateway with common defaults.

        Flattens the most common configuration parameters into keyword
        arguments, avoiding the need to construct TraceConfiguration manually.

        :param trace_calls: Whether to trace call/return events.
        :param trace_lines: Whether to trace line events.
        :param trace_variables: Whether to trace variable snapshots.
        :param record_inner_portals: Whether to record inner portal events.
        :param backend_uri: Optional URI for the stream backend.

        :returns: A configured TimeTravelGateway.
    """
    configuration = TraceConfiguration(
        trace_calls=trace_calls,
        trace_lines=trace_lines,
        trace_variables=trace_variables,
        record_inner_portals=record_inner_portals,
    )
    rtnval = TimeTravelGateway(
        configuration=configuration,
        backend_uri=backend_uri,
    )
    return rtnval
