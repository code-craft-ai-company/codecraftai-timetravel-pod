"""
    Tests for the F3.1 TimeTravelGateway module.
"""

from automojo.timetravel.pod.gateway import TimeTravelGateway
from automojo.timetravel.pod.gateway import get_active_gateway
from automojo.timetravel.pod.tracingstate import is_gateway_active
from automojo.timetravel.pod.traceclock import get_trace_clock
from automojo.timetravel.pod.traceevents import GatewayStartEvent
from automojo.timetravel.pod.traceevents import GatewayStopEvent
from automojo.timetravel.pod.traceconfiguration import TraceConfiguration


class MockRecorder:
    """
        A mock recorder that collects events and tracks flush/close calls.
    """

    def __init__(self):
        self.events = []
        self.flushed = False
        self.closed = False
        return

    def record(self, event):
        self.events.append(event)
        return

    def flush(self):
        self.flushed = True
        return

    def close(self):
        self.closed = True
        return


def test_entering_starts_clock_and_sets_active_flag() -> None:
    """
        Verify entering the gateway starts the clock and sets the
        gateway-active flag.
    """
    clock = get_trace_clock()
    gateway = TimeTravelGateway()

    with gateway:
        assert is_gateway_active()
        assert clock.is_running

    return


def test_exiting_stops_clock_and_clears_active_flag() -> None:
    """
        Verify exiting the gateway stops the clock and clears the
        gateway-active flag.
    """
    clock = get_trace_clock()
    gateway = TimeTravelGateway()

    with gateway:
        pass

    assert not is_gateway_active()
    assert not clock.is_running

    return


def test_get_active_gateway_inside_and_outside() -> None:
    """
        Verify get_active_gateway returns the gateway inside the with
        block and None outside.
    """
    gateway = TimeTravelGateway()

    assert get_active_gateway() is None

    with gateway:
        active = get_active_gateway()
        assert active is gateway

    assert get_active_gateway() is None

    return


def test_exceptions_propagate_after_cleanup() -> None:
    """
        Verify exceptions inside the gateway propagate after cleanup.
    """
    gateway = TimeTravelGateway()

    raised = False
    try:
        with gateway:
            raise ValueError("test error")
    except ValueError:
        raised = True

    assert raised

    # Cleanup should still have happened
    assert not is_gateway_active()
    assert not get_trace_clock().is_running

    return


def test_registered_recorders_are_flushed_and_closed() -> None:
    """
        Verify registered recorders are flushed and closed on gateway exit.
    """
    gateway = TimeTravelGateway()
    recorder = MockRecorder()

    with gateway:
        gateway.register_recorder(recorder)

    assert recorder.flushed
    assert recorder.closed

    return


def test_gateway_start_event_has_timestamp_zero() -> None:
    """
        Verify the GatewayStartEvent has timestamp_ns=0.
    """
    gateway = TimeTravelGateway()
    recorder = MockRecorder()

    # Register before entering so the recorder catches the start event
    gateway.register_recorder(recorder)

    with gateway:
        pass

    start_events = [
        e for e in recorder.events if isinstance(e, GatewayStartEvent)
    ]

    assert len(start_events) == 1
    assert start_events[0].timestamp_ns == 0

    return


def test_gateway_stop_event_is_emitted() -> None:
    """
        Verify a GatewayStopEvent is emitted on exit.
    """
    gateway = TimeTravelGateway()
    recorder = MockRecorder()

    # Register before entering so the recorder catches both events
    gateway.register_recorder(recorder)

    with gateway:
        pass

    stop_events = [
        e for e in recorder.events if isinstance(e, GatewayStopEvent)
    ]

    assert len(stop_events) == 1
    assert stop_events[0].timestamp_ns > 0

    return


def test_configuration_property() -> None:
    """
        Verify configuration property returns the provided configuration.
    """
    config = TraceConfiguration(trace_calls=False, trace_lines=True)
    gateway = TimeTravelGateway(configuration=config)

    assert gateway.configuration is config

    return
