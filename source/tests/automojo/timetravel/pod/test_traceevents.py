"""
    Tests for the F0.4 Trace Event Model module.
"""

import unittest

from ccai.timetravel.pod.traceevents import EventType
from ccai.timetravel.pod.traceevents import TraceEvent
from ccai.timetravel.pod.traceevents import CallEvent
from ccai.timetravel.pod.traceevents import ReturnEvent
from ccai.timetravel.pod.traceevents import LineEvent
from ccai.timetravel.pod.traceevents import VariableSnapshotEvent
from ccai.timetravel.pod.traceevents import ExceptionEvent
from ccai.timetravel.pod.traceevents import PortalEnterEvent
from ccai.timetravel.pod.traceevents import PortalExitEvent
from ccai.timetravel.pod.traceevents import GatewayStartEvent
from ccai.timetravel.pod.traceevents import GatewayStopEvent


class TestEventType(unittest.TestCase):
    """
        Tests for the EventType constants.
    """

    def test_all_constants_are_unique_integers(self):
        """
            Verify all EventType constants are unique integers.
        """
        constants = [
            EventType.CALL,
            EventType.RETURN,
            EventType.LINE,
            EventType.VARIABLE_SNAPSHOT,
            EventType.PORTAL_ENTER,
            EventType.PORTAL_EXIT,
            EventType.GATEWAY_START,
            EventType.GATEWAY_STOP,
            EventType.EXCEPTION,
        ]

        for constant in constants:
            self.assertIsInstance(constant, int)

        unique_values = set(constants)
        self.assertEqual(len(unique_values), len(constants))

        return

    def test_expected_type_values(self):
        """
            Verify the expected integer values for each event type.
        """
        self.assertEqual(EventType.CALL, 1)
        self.assertEqual(EventType.RETURN, 2)
        self.assertEqual(EventType.LINE, 3)
        self.assertEqual(EventType.VARIABLE_SNAPSHOT, 4)
        self.assertEqual(EventType.PORTAL_ENTER, 5)
        self.assertEqual(EventType.PORTAL_EXIT, 6)
        self.assertEqual(EventType.GATEWAY_START, 7)
        self.assertEqual(EventType.GATEWAY_STOP, 8)
        self.assertEqual(EventType.EXCEPTION, 9)

        return


class TestTraceEvent(unittest.TestCase):
    """
        Tests for the TraceEvent base class.
    """

    def test_base_fields_are_set_correctly(self):
        """
            Verify TraceEvent base fields are set correctly.
        """
        event = TraceEvent(event_type=1, timestamp_ns=12345, thread_id=99)

        self.assertEqual(event.event_type, 1)
        self.assertEqual(event.timestamp_ns, 12345)
        self.assertEqual(event.thread_id, 99)

        return

    def test_slots_prevents_arbitrary_attribute_addition(self):
        """
            Verify __slots__ prevents arbitrary attribute addition.
        """
        event = TraceEvent(event_type=1, timestamp_ns=0, thread_id=0)

        with self.assertRaises(AttributeError):
            event.arbitrary_attribute = "should_fail"

        return


class TestCallEvent(unittest.TestCase):
    """
        Tests for the CallEvent class.
    """

    def test_constructible_with_documented_fields(self):
        """
            Verify CallEvent is constructible with all documented fields.
        """
        event = CallEvent(
            timestamp_ns=1000,
            thread_id=42,
            filename="test.py",
            lineno=10,
            function_name="my_func",
            args=(1, 2),
            kwargs={"key": "value"},
        )

        self.assertEqual(event.event_type, EventType.CALL)
        self.assertEqual(event.timestamp_ns, 1000)
        self.assertEqual(event.thread_id, 42)
        self.assertEqual(event.filename, "test.py")
        self.assertEqual(event.lineno, 10)
        self.assertEqual(event.function_name, "my_func")
        self.assertEqual(event.args, (1, 2))
        self.assertEqual(event.kwargs, {"key": "value"})

        return

    def test_default_args_and_kwargs(self):
        """
            Verify default args is empty tuple and kwargs is None.
        """
        event = CallEvent(
            timestamp_ns=0,
            thread_id=0,
            filename="test.py",
            lineno=1,
            function_name="f",
        )

        self.assertEqual(event.args, ())
        self.assertIsNone(event.kwargs)

        return

    def test_slots_prevents_arbitrary_attribute(self):
        """
            Verify __slots__ prevents arbitrary attribute addition.
        """
        event = CallEvent(
            timestamp_ns=0, thread_id=0, filename="", lineno=0, function_name="",
        )

        with self.assertRaises(AttributeError):
            event.extra = "nope"

        return


class TestReturnEvent(unittest.TestCase):
    """
        Tests for the ReturnEvent class.
    """

    def test_constructible_with_documented_fields(self):
        """
            Verify ReturnEvent is constructible with all documented fields.
        """
        event = ReturnEvent(
            timestamp_ns=2000,
            thread_id=42,
            filename="test.py",
            lineno=20,
            function_name="my_func",
            return_value=42,
        )

        self.assertEqual(event.event_type, EventType.RETURN)
        self.assertEqual(event.return_value, 42)

        return


class TestLineEvent(unittest.TestCase):
    """
        Tests for the LineEvent class.
    """

    def test_constructible_with_documented_fields(self):
        """
            Verify LineEvent is constructible with all documented fields.
        """
        event = LineEvent(
            timestamp_ns=3000,
            thread_id=42,
            filename="test.py",
            lineno=30,
        )

        self.assertEqual(event.event_type, EventType.LINE)
        self.assertEqual(event.filename, "test.py")
        self.assertEqual(event.lineno, 30)

        return


class TestVariableSnapshotEvent(unittest.TestCase):
    """
        Tests for the VariableSnapshotEvent class.
    """

    def test_constructible_with_documented_fields(self):
        """
            Verify VariableSnapshotEvent stores local variables dict.
        """
        local_vars = {"x": 10, "y": "hello"}
        event = VariableSnapshotEvent(
            timestamp_ns=4000,
            thread_id=42,
            filename="test.py",
            lineno=40,
            local_variables=local_vars,
        )

        self.assertEqual(event.event_type, EventType.VARIABLE_SNAPSHOT)
        self.assertEqual(event.local_variables, local_vars)

        return


class TestExceptionEvent(unittest.TestCase):
    """
        Tests for the ExceptionEvent class.
    """

    def test_stores_exception_details_as_strings(self):
        """
            Verify ExceptionEvent stores exception type, value, and traceback
            as strings.
        """
        event = ExceptionEvent(
            timestamp_ns=5000,
            thread_id=42,
            filename="test.py",
            lineno=50,
            function_name="failing_func",
            exception_type="ValueError",
            exception_value="bad value",
            traceback_str="Traceback ...",
        )

        self.assertEqual(event.event_type, EventType.EXCEPTION)
        self.assertEqual(event.exception_type, "ValueError")
        self.assertEqual(event.exception_value, "bad value")
        self.assertEqual(event.traceback_str, "Traceback ...")

        return


class TestPortalEvents(unittest.TestCase):
    """
        Tests for PortalEnterEvent and PortalExitEvent.
    """

    def test_portal_enter_event(self):
        """
            Verify PortalEnterEvent is constructible with portal_name.
        """
        event = PortalEnterEvent(
            timestamp_ns=6000, thread_id=42, portal_name="auth_portal",
        )

        self.assertEqual(event.event_type, EventType.PORTAL_ENTER)
        self.assertEqual(event.portal_name, "auth_portal")

        return

    def test_portal_exit_event(self):
        """
            Verify PortalExitEvent is constructible with portal_name.
        """
        event = PortalExitEvent(
            timestamp_ns=7000, thread_id=42, portal_name="auth_portal",
        )

        self.assertEqual(event.event_type, EventType.PORTAL_EXIT)
        self.assertEqual(event.portal_name, "auth_portal")

        return


class TestGatewayEvents(unittest.TestCase):
    """
        Tests for GatewayStartEvent and GatewayStopEvent.
    """

    def test_gateway_start_event(self):
        """
            Verify GatewayStartEvent stores wall_clock_time.
        """
        event = GatewayStartEvent(
            timestamp_ns=0, thread_id=42, wall_clock_time=1700000000.123,
        )

        self.assertEqual(event.event_type, EventType.GATEWAY_START)
        self.assertAlmostEqual(event.wall_clock_time, 1700000000.123)

        return

    def test_gateway_stop_event(self):
        """
            Verify GatewayStopEvent stores wall_clock_time.
        """
        event = GatewayStopEvent(
            timestamp_ns=99999, thread_id=42, wall_clock_time=1700000060.456,
        )

        self.assertEqual(event.event_type, EventType.GATEWAY_STOP)
        self.assertAlmostEqual(event.wall_clock_time, 1700000060.456)

        return


if __name__ == "__main__":
    unittest.main()
