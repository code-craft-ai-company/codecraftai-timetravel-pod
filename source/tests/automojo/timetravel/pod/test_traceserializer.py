"""
    Tests for the F1.3 Hybrid Serialization Format module.
"""

import unittest

from automojo.timetravel.pod.traceserializer import TraceSerializer
from automojo.timetravel.pod.traceserializer import TraceDeserializer
from automojo.timetravel.pod.traceserializer import ENVELOPE_SIZE
from automojo.timetravel.pod.traceevents import EventType
from automojo.timetravel.pod.traceevents import CallEvent
from automojo.timetravel.pod.traceevents import ReturnEvent
from automojo.timetravel.pod.traceevents import LineEvent
from automojo.timetravel.pod.traceevents import VariableSnapshotEvent
from automojo.timetravel.pod.traceevents import ExceptionEvent
from automojo.timetravel.pod.traceevents import PortalEnterEvent
from automojo.timetravel.pod.traceevents import PortalExitEvent
from automojo.timetravel.pod.traceevents import GatewayStartEvent
from automojo.timetravel.pod.traceevents import GatewayStopEvent


class TestEnvelopeSize(unittest.TestCase):
    """
        Tests for the envelope size constant.
    """

    def test_envelope_size_is_29_bytes(self):
        """
            Verify envelope size is exactly 29 bytes.
        """
        self.assertEqual(ENVELOPE_SIZE, 29)

        return


class TestCallEventRoundTrip(unittest.TestCase):
    """
        Tests for CallEvent serialization round-trip.
    """

    def test_call_event_round_trips_with_all_fields(self):
        """
            Verify CallEvent round-trips through serialize -> deserialize.
        """
        serializer = TraceSerializer()
        deserializer = TraceDeserializer()

        original = CallEvent(
            timestamp_ns=123456789,
            thread_id=42,
            filename="test_module.py",
            lineno=10,
            function_name="my_func",
            args=(1, "hello"),
            kwargs={"key": "value"},
        )

        data = serializer.serialize(original)
        restored, offset = deserializer.deserialize(data)

        self.assertIsInstance(restored, CallEvent)
        self.assertEqual(restored.event_type, EventType.CALL)
        self.assertEqual(restored.timestamp_ns, 123456789)
        self.assertEqual(restored.thread_id, 42)
        self.assertEqual(restored.filename, "test_module.py")
        self.assertEqual(restored.lineno, 10)
        self.assertEqual(restored.function_name, "my_func")
        self.assertEqual(restored.args, (1, "hello"))
        self.assertEqual(restored.kwargs, {"key": "value"})
        self.assertEqual(offset, len(data))

        return


class TestReturnEventRoundTrip(unittest.TestCase):
    """
        Tests for ReturnEvent serialization round-trip.
    """

    def test_return_event_preserves_return_value(self):
        """
            Verify ReturnEvent round-trips correctly, including return_value.
        """
        serializer = TraceSerializer()
        deserializer = TraceDeserializer()

        original = ReturnEvent(
            timestamp_ns=200000,
            thread_id=99,
            filename="module.py",
            lineno=20,
            function_name="get_value",
            return_value={"result": [1, 2, 3]},
        )

        data = serializer.serialize(original)
        restored, _ = deserializer.deserialize(data)

        self.assertIsInstance(restored, ReturnEvent)
        self.assertEqual(restored.function_name, "get_value")
        self.assertEqual(restored.return_value, {"result": [1, 2, 3]})

        return


class TestLineEventRoundTrip(unittest.TestCase):
    """
        Tests for LineEvent serialization round-trip.
    """

    def test_line_event_has_zero_length_payload(self):
        """
            Verify LineEvent produces a zero-length payload.
        """
        serializer = TraceSerializer()
        deserializer = TraceDeserializer()

        original = LineEvent(
            timestamp_ns=300000,
            thread_id=1,
            filename="script.py",
            lineno=42,
        )

        data = serializer.serialize(original)

        # Read header to check payload_len
        header, _ = deserializer.read_header(data)
        event_type, timestamp_ns, thread_id, filename_len, lineno, payload_len = header
        self.assertEqual(payload_len, 0)

        # Round-trip
        restored, _ = deserializer.deserialize(data)
        self.assertIsInstance(restored, LineEvent)
        self.assertEqual(restored.filename, "script.py")
        self.assertEqual(restored.lineno, 42)

        return


class TestVariableSnapshotEventRoundTrip(unittest.TestCase):
    """
        Tests for VariableSnapshotEvent serialization round-trip.
    """

    def test_preserves_local_variables_dict(self):
        """
            Verify VariableSnapshotEvent preserves the local variables dict.
        """
        serializer = TraceSerializer()
        deserializer = TraceDeserializer()

        local_vars = {"x": 42, "name": "test", "data": [1, 2, 3]}
        original = VariableSnapshotEvent(
            timestamp_ns=400000,
            thread_id=7,
            filename="vars.py",
            lineno=15,
            local_variables=local_vars,
        )

        data = serializer.serialize(original)
        restored, _ = deserializer.deserialize(data)

        self.assertIsInstance(restored, VariableSnapshotEvent)
        self.assertEqual(restored.local_variables, local_vars)

        return


class TestExceptionEventRoundTrip(unittest.TestCase):
    """
        Tests for ExceptionEvent serialization round-trip.
    """

    def test_preserves_exception_details(self):
        """
            Verify ExceptionEvent preserves exception type, value, and traceback.
        """
        serializer = TraceSerializer()
        deserializer = TraceDeserializer()

        original = ExceptionEvent(
            timestamp_ns=500000,
            thread_id=3,
            filename="error.py",
            lineno=50,
            function_name="bad_func",
            exception_type="ValueError",
            exception_value="invalid input",
            traceback_str="Traceback (most recent call last)...",
        )

        data = serializer.serialize(original)
        restored, _ = deserializer.deserialize(data)

        self.assertIsInstance(restored, ExceptionEvent)
        self.assertEqual(restored.exception_type, "ValueError")
        self.assertEqual(restored.exception_value, "invalid input")
        self.assertEqual(restored.traceback_str, "Traceback (most recent call last)...")

        return


class TestPortalEventsRoundTrip(unittest.TestCase):
    """
        Tests for portal event serialization round-trip.
    """

    def test_portal_enter_preserves_name(self):
        """
            Verify PortalEnterEvent preserves portal name.
        """
        serializer = TraceSerializer()
        deserializer = TraceDeserializer()

        original = PortalEnterEvent(
            timestamp_ns=600000, thread_id=1, portal_name="auth_portal",
        )

        data = serializer.serialize(original)
        restored, _ = deserializer.deserialize(data)

        self.assertIsInstance(restored, PortalEnterEvent)
        self.assertEqual(restored.portal_name, "auth_portal")

        return

    def test_portal_exit_preserves_name(self):
        """
            Verify PortalExitEvent preserves portal name.
        """
        serializer = TraceSerializer()
        deserializer = TraceDeserializer()

        original = PortalExitEvent(
            timestamp_ns=700000, thread_id=1, portal_name="auth_portal",
        )

        data = serializer.serialize(original)
        restored, _ = deserializer.deserialize(data)

        self.assertIsInstance(restored, PortalExitEvent)
        self.assertEqual(restored.portal_name, "auth_portal")

        return


class TestGatewayEventsRoundTrip(unittest.TestCase):
    """
        Tests for gateway event serialization round-trip.
    """

    def test_gateway_start_preserves_wall_clock_time(self):
        """
            Verify GatewayStartEvent preserves wall clock time.
        """
        serializer = TraceSerializer()
        deserializer = TraceDeserializer()

        original = GatewayStartEvent(
            timestamp_ns=0, thread_id=1, wall_clock_time=1700000000.123456,
        )

        data = serializer.serialize(original)
        restored, _ = deserializer.deserialize(data)

        self.assertIsInstance(restored, GatewayStartEvent)
        self.assertAlmostEqual(restored.wall_clock_time, 1700000000.123456)

        return

    def test_gateway_stop_preserves_wall_clock_time(self):
        """
            Verify GatewayStopEvent preserves wall clock time.
        """
        serializer = TraceSerializer()
        deserializer = TraceDeserializer()

        original = GatewayStopEvent(
            timestamp_ns=9999999, thread_id=1, wall_clock_time=1700000060.789,
        )

        data = serializer.serialize(original)
        restored, _ = deserializer.deserialize(data)

        self.assertIsInstance(restored, GatewayStopEvent)
        self.assertAlmostEqual(restored.wall_clock_time, 1700000060.789)

        return


class TestHeaderAndSkip(unittest.TestCase):
    """
        Tests for read_header and skip_event methods.
    """

    def test_read_header_returns_envelope_fields(self):
        """
            Verify read_header returns correct envelope fields without
            deserializing payload.
        """
        serializer = TraceSerializer()
        deserializer = TraceDeserializer()

        event = CallEvent(
            timestamp_ns=1000, thread_id=5,
            filename="test.py", lineno=7,
            function_name="fn",
        )

        data = serializer.serialize(event)
        header, next_offset = deserializer.read_header(data)

        event_type, timestamp_ns, thread_id, filename_len, lineno, payload_len = header

        self.assertEqual(event_type, EventType.CALL)
        self.assertEqual(timestamp_ns, 1000)
        self.assertEqual(thread_id, 5)
        self.assertEqual(lineno, 7)
        self.assertEqual(next_offset, ENVELOPE_SIZE)

        return

    def test_skip_event_advances_to_next_event(self):
        """
            Verify skip_event advances offset to the next event in a
            multi-event buffer.
        """
        serializer = TraceSerializer()
        deserializer = TraceDeserializer()

        event1 = LineEvent(timestamp_ns=100, thread_id=1, filename="a.py", lineno=1)
        event2 = LineEvent(timestamp_ns=200, thread_id=1, filename="b.py", lineno=2)

        data = serializer.serialize(event1) + serializer.serialize(event2)

        offset_after_first = deserializer.skip_event(data, offset=0)
        restored, _ = deserializer.deserialize(data, offset=offset_after_first)

        self.assertIsInstance(restored, LineEvent)
        self.assertEqual(restored.timestamp_ns, 200)
        self.assertEqual(restored.filename, "b.py")

        return


if __name__ == "__main__":
    unittest.main()
