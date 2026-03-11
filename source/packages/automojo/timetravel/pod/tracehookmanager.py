"""
    Provides the trace hook manager for sys.settrace integration.

    This module contains the :class:`TraceHookManager` class which installs
    a trace function on the current thread and dispatches trace events to
    a callback.
"""

import sys
import threading

from automojo.timetravel.pod.traceclock import get_trace_clock
from automojo.timetravel.pod.traceconfiguration import TraceConfiguration
from automojo.timetravel.pod.traceevents import CallEvent
from automojo.timetravel.pod.traceevents import ReturnEvent
from automojo.timetravel.pod.traceevents import LineEvent
from automojo.timetravel.pod.traceevents import VariableSnapshotEvent
from automojo.timetravel.pod.traceevents import ExceptionEvent


class TraceHookManager:
    """
        Manages sys.settrace installation and event dispatch for a single thread.

        Caches configuration booleans as instance attributes to avoid dictionary
        lookups on every trace callback invocation.
    """

    __slots__ = (
        "_record_callback", "_trace_calls", "_trace_lines",
        "_trace_variables", "_clock", "_thread_id",
    )

    def __init__(self, configuration: TraceConfiguration, record_callback) -> None:
        """
            Create a TraceHookManager.

            :param configuration: The trace configuration controlling granularity.
            :param record_callback: A callable that accepts a TraceEvent.
        """
        self._record_callback = record_callback
        self._trace_calls = configuration.trace_calls
        self._trace_lines = configuration.trace_lines
        self._trace_variables = configuration.trace_variables
        self._clock = get_trace_clock()
        self._thread_id = threading.get_ident()
        return

    def install(self) -> None:
        """
            Install the trace function on the current thread.
        """
        sys.settrace(self._trace_function)
        return

    def uninstall(self) -> None:
        """
            Remove the trace function from the current thread.
        """
        sys.settrace(None)
        return

    def _trace_function(self, frame, event, arg):
        """
            The trace function installed via sys.settrace.

            :param frame: The current stack frame.
            :param event: The trace event type string.
            :param arg: The event-specific argument.

            :returns: This trace function (to remain installed for sub-calls).
        """
        timestamp_ns = self._clock.timestamp()
        record = self._record_callback

        if event == "call":
            if self._trace_calls:
                call_event = CallEvent(
                    timestamp_ns=timestamp_ns,
                    thread_id=self._thread_id,
                    filename=frame.f_code.co_filename,
                    lineno=frame.f_lineno,
                    function_name=frame.f_code.co_name,
                )
                record(call_event)
            rtnval = self._trace_function
            return rtnval

        elif event == "return":
            if self._trace_calls:
                return_event = ReturnEvent(
                    timestamp_ns=timestamp_ns,
                    thread_id=self._thread_id,
                    filename=frame.f_code.co_filename,
                    lineno=frame.f_lineno,
                    function_name=frame.f_code.co_name,
                    return_value=arg,
                )
                record(return_event)

        elif event == "line":
            if self._trace_lines:
                line_event = LineEvent(
                    timestamp_ns=timestamp_ns,
                    thread_id=self._thread_id,
                    filename=frame.f_code.co_filename,
                    lineno=frame.f_lineno,
                )
                record(line_event)
            if self._trace_variables:
                var_event = VariableSnapshotEvent(
                    timestamp_ns=timestamp_ns,
                    thread_id=self._thread_id,
                    filename=frame.f_code.co_filename,
                    lineno=frame.f_lineno,
                    local_variables=dict(frame.f_locals),
                )
                record(var_event)

        elif event == "exception":
            exc_type, exc_value, exc_tb = arg
            exc_type_name = exc_type.__name__ if exc_type is not None else ""
            exc_value_str = str(exc_value) if exc_value is not None else ""
            exception_event = ExceptionEvent(
                timestamp_ns=timestamp_ns,
                thread_id=self._thread_id,
                filename=frame.f_code.co_filename,
                lineno=frame.f_lineno,
                function_name=frame.f_code.co_name,
                exception_type=exc_type_name,
                exception_value=exc_value_str,
                traceback_str="",
            )
            record(exception_event)

        rtnval = self._trace_function
        return rtnval
