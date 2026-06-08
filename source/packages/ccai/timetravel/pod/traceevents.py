"""
    Provides the trace event model for the time travel pod.

    This module defines the :class:`EventType` constants and :class:`TraceEvent`
    base class along with all concrete event classes used to represent traced
    execution events.
"""

from typing import Optional


class EventType:
    """
        Integer tags for each trace event type, used in the struct
        serialization envelope.
    """

    CALL = 1
    RETURN = 2
    LINE = 3
    VARIABLE_SNAPSHOT = 4
    PORTAL_ENTER = 5
    PORTAL_EXIT = 6
    GATEWAY_START = 7
    GATEWAY_STOP = 8
    EXCEPTION = 9


class TraceEvent:
    """
        Base class for all trace events.

        Contains the common fields shared by every event: the event type tag,
        the nanosecond timestamp, and the thread ID.
    """

    __slots__ = ("event_type", "timestamp_ns", "thread_id")

    def __init__(self, event_type: int, timestamp_ns: int, thread_id: int) -> None:
        self.event_type = event_type
        self.timestamp_ns = timestamp_ns
        self.thread_id = thread_id
        return


class CallEvent(TraceEvent):
    """
        Represents a function call event.
    """

    __slots__ = ("filename", "lineno", "function_name", "args", "kwargs")

    def __init__(self, timestamp_ns: int, thread_id: int,
                 filename: str, lineno: int, function_name: str,
                 args: tuple = (), kwargs: Optional[dict] = None) -> None:
        super().__init__(EventType.CALL, timestamp_ns, thread_id)
        self.filename = filename
        self.lineno = lineno
        self.function_name = function_name
        self.args = args
        self.kwargs = kwargs
        return


class ReturnEvent(TraceEvent):
    """
        Represents a function return event.
    """

    __slots__ = ("filename", "lineno", "function_name", "return_value")

    def __init__(self, timestamp_ns: int, thread_id: int,
                 filename: str, lineno: int, function_name: str,
                 return_value=None) -> None:
        super().__init__(EventType.RETURN, timestamp_ns, thread_id)
        self.filename = filename
        self.lineno = lineno
        self.function_name = function_name
        self.return_value = return_value
        return


class LineEvent(TraceEvent):
    """
        Represents a line execution event.
    """

    __slots__ = ("filename", "lineno")

    def __init__(self, timestamp_ns: int, thread_id: int,
                 filename: str, lineno: int) -> None:
        super().__init__(EventType.LINE, timestamp_ns, thread_id)
        self.filename = filename
        self.lineno = lineno
        return


class VariableSnapshotEvent(TraceEvent):
    """
        Represents a variable snapshot captured at a traced line.
    """

    __slots__ = ("filename", "lineno", "local_variables")

    def __init__(self, timestamp_ns: int, thread_id: int,
                 filename: str, lineno: int, local_variables: dict) -> None:
        super().__init__(EventType.VARIABLE_SNAPSHOT, timestamp_ns, thread_id)
        self.filename = filename
        self.lineno = lineno
        self.local_variables = local_variables
        return


class ExceptionEvent(TraceEvent):
    """
        Represents an exception propagation event.
    """

    __slots__ = ("filename", "lineno", "function_name",
                 "exception_type", "exception_value", "traceback_str")

    def __init__(self, timestamp_ns: int, thread_id: int,
                 filename: str, lineno: int, function_name: str,
                 exception_type: str, exception_value: str,
                 traceback_str: str) -> None:
        super().__init__(EventType.EXCEPTION, timestamp_ns, thread_id)
        self.filename = filename
        self.lineno = lineno
        self.function_name = function_name
        self.exception_type = exception_type
        self.exception_value = exception_value
        self.traceback_str = traceback_str
        return


class PortalEnterEvent(TraceEvent):
    """
        Represents entering a nested portal scope.
    """

    __slots__ = ("portal_name",)

    def __init__(self, timestamp_ns: int, thread_id: int, portal_name: str) -> None:
        super().__init__(EventType.PORTAL_ENTER, timestamp_ns, thread_id)
        self.portal_name = portal_name
        return


class PortalExitEvent(TraceEvent):
    """
        Represents exiting a nested portal scope.
    """

    __slots__ = ("portal_name",)

    def __init__(self, timestamp_ns: int, thread_id: int, portal_name: str) -> None:
        super().__init__(EventType.PORTAL_EXIT, timestamp_ns, thread_id)
        self.portal_name = portal_name
        return


class GatewayStartEvent(TraceEvent):
    """
        Represents the gateway being entered.
    """

    __slots__ = ("wall_clock_time",)

    def __init__(self, timestamp_ns: int, thread_id: int, wall_clock_time: float) -> None:
        super().__init__(EventType.GATEWAY_START, timestamp_ns, thread_id)
        self.wall_clock_time = wall_clock_time
        return


class GatewayStopEvent(TraceEvent):
    """
        Represents the gateway being exited.
    """

    __slots__ = ("wall_clock_time",)

    def __init__(self, timestamp_ns: int, thread_id: int, wall_clock_time: float) -> None:
        super().__init__(EventType.GATEWAY_STOP, timestamp_ns, thread_id)
        self.wall_clock_time = wall_clock_time
        return
