"""
    Provides the main application gateway for time travel tracing.

    This module contains the :class:`TimeTravelGateway` class which marks
    the overall tracing timespan for the application, manages the trace clock,
    and provides access to the active gateway instance.
"""

import time
import threading

from typing import Optional

from ccai.timetravel.pod.traceclock import get_trace_clock
from ccai.timetravel.pod.tracingstate import set_gateway_active
from ccai.timetravel.pod.traceevents import GatewayStartEvent
from ccai.timetravel.pod.traceevents import GatewayStopEvent
from ccai.timetravel.pod.traceconfiguration import TraceConfiguration
from ccai.timetravel.pod.traceconfiguration import DEFAULT_TRACE_CONFIGURATION


class TimeTravelGateway:
    """
        Main application gateway that marks the tracing timespan.

        Used as a context manager. The gateway must be entered before any
        portals can activate tracing.
    """

    def __init__(self, configuration: Optional[TraceConfiguration] = None,
                 backend_uri: Optional[str] = None) -> None:
        """
            Create a TimeTravelGateway.

            :param configuration: The trace configuration. Defaults to DEFAULT_TRACE_CONFIGURATION.
            :param backend_uri: Optional URI for the stream backend.
        """
        if configuration is not None:
            self._configuration = configuration
        else:
            self._configuration = DEFAULT_TRACE_CONFIGURATION
        self._backend_uri = backend_uri
        self._clock = get_trace_clock()
        self._active_recorders: list = []
        return

    def __enter__(self):
        """
            Enter the gateway: start clock, set active flag, emit start event.

            :returns: This gateway instance.
        """
        # Start the clock
        self._clock.start()

        # Mark gateway as active
        set_gateway_active(True)

        # Set the active gateway reference
        set_active_gateway(self)

        # Emit gateway start event
        start_event = GatewayStartEvent(
            timestamp_ns=0,
            thread_id=threading.get_ident(),
            wall_clock_time=time.time(),
        )
        self._broadcast_event(start_event)

        rtnval = self
        return rtnval

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
            Exit the gateway: emit stop event, flush/close recorders, stop clock.

            :returns: False to propagate exceptions.
        """
        try:
            # Emit gateway stop event
            stop_event = GatewayStopEvent(
                timestamp_ns=self._clock.timestamp(),
                thread_id=threading.get_ident(),
                wall_clock_time=time.time(),
            )
            self._broadcast_event(stop_event)

            # Flush and close all active recorders
            for recorder in self._active_recorders:
                recorder.flush()
                recorder.close()
            self._active_recorders.clear()
        finally:
            # Always stop the clock and clear the gateway flag
            self._clock.stop()
            set_gateway_active(False)
            set_active_gateway(None)

        # Do not suppress exceptions
        rtnval = False
        return rtnval

    @property
    def configuration(self) -> TraceConfiguration:
        """
            The trace configuration for this gateway.
        """
        rtnval = self._configuration
        return rtnval

    @property
    def backend_uri(self) -> Optional[str]:
        """
            The backend URI for this gateway, or None.
        """
        rtnval = self._backend_uri
        return rtnval

    def register_recorder(self, recorder) -> None:
        """
            Register an active recorder for cleanup on gateway exit.

            :param recorder: A recorder implementing record/flush/close.
        """
        self._active_recorders.append(recorder)
        return

    def _broadcast_event(self, event) -> None:
        """
            Send an event to all active recorders.

            :param event: The trace event to broadcast.
        """
        for recorder in self._active_recorders:
            recorder.record(event)
        return


_active_gateway: Optional[TimeTravelGateway] = None


def get_active_gateway() -> Optional[TimeTravelGateway]:
    """
        Return the currently active gateway, or None if no gateway is active.

        :returns: The active TimeTravelGateway instance, or None.
    """
    rtnval = _active_gateway
    return rtnval


def set_active_gateway(gateway: Optional[TimeTravelGateway]) -> None:
    """
        Set the active gateway reference.

        :param gateway: The gateway instance, or None to clear.
    """
    global _active_gateway
    _active_gateway = gateway
    return
