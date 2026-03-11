"""
    Tests for the F3.1 TimeTravelGateway module.
"""

import unittest

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


class TestTimeTravelGateway(unittest.TestCase):
    """
        Tests for the TimeTravelGateway class.
    """

    def test_entering_starts_clock_and_sets_active_flag(self):
        """
            Verify entering the gateway starts the clock and sets the
            gateway-active flag.
        """
        clock = get_trace_clock()
        gateway = TimeTravelGateway()

        with gateway:
            self.assertTrue(is_gateway_active())
            self.assertTrue(clock.is_running)

        return

    def test_exiting_stops_clock_and_clears_active_flag(self):
        """
            Verify exiting the gateway stops the clock and clears the
            gateway-active flag.
        """
        clock = get_trace_clock()
        gateway = TimeTravelGateway()

        with gateway:
            pass

        self.assertFalse(is_gateway_active())
        self.assertFalse(clock.is_running)

        return

    def test_get_active_gateway_inside_and_outside(self):
        """
            Verify get_active_gateway returns the gateway inside the with
            block and None outside.
        """
        gateway = TimeTravelGateway()

        self.assertIsNone(get_active_gateway())

        with gateway:
            active = get_active_gateway()
            self.assertIs(active, gateway)

        self.assertIsNone(get_active_gateway())

        return

    def test_exceptions_propagate_after_cleanup(self):
        """
            Verify exceptions inside the gateway propagate after cleanup.
        """
        gateway = TimeTravelGateway()

        with self.assertRaises(ValueError):
            with gateway:
                raise ValueError("test error")

        # Cleanup should still have happened
        self.assertFalse(is_gateway_active())
        self.assertFalse(get_trace_clock().is_running)

        return

    def test_registered_recorders_are_flushed_and_closed(self):
        """
            Verify registered recorders are flushed and closed on gateway exit.
        """
        gateway = TimeTravelGateway()
        recorder = MockRecorder()

        with gateway:
            gateway.register_recorder(recorder)

        self.assertTrue(recorder.flushed)
        self.assertTrue(recorder.closed)

        return

    def test_gateway_start_event_has_timestamp_zero(self):
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

        self.assertEqual(len(start_events), 1)
        self.assertEqual(start_events[0].timestamp_ns, 0)

        return

    def test_gateway_stop_event_is_emitted(self):
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

        self.assertEqual(len(stop_events), 1)
        self.assertGreater(stop_events[0].timestamp_ns, 0)

        return

    def test_configuration_property(self):
        """
            Verify configuration property returns the provided configuration.
        """
        config = TraceConfiguration(trace_calls=False, trace_lines=True)
        gateway = TimeTravelGateway(configuration=config)

        self.assertIs(gateway.configuration, config)

        return


if __name__ == "__main__":
    unittest.main()
