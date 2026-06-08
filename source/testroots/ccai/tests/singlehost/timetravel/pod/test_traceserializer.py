"""
    Tests for the F1.3 Hybrid Serialization Format module.
"""

from ccai.timetravel.pod.traceserializer import TraceSerializer
from ccai.timetravel.pod.traceserializer import TraceDeserializer
from ccai.timetravel.pod.traceserializer import ENVELOPE_SIZE
from ccai.timetravel.pod.traceevents import EventType
from ccai.timetravel.pod.traceevents import CallEvent
from ccai.timetravel.pod.traceevents import ReturnEvent
from ccai.timetravel.pod.traceevents import LineEvent
from ccai.timetravel.pod.traceevents import VariableSnapshotEvent
from ccai.timetravel.pod.traceevents import ExceptionEvent
from ccai.timetravel.pod.traceevents import PortalEnterEvent
from ccai.timetravel.pod.traceevents import PortalExitEvent
from ccai.timetravel.pod.traceevents import GatewayStartEvent
from ccai.timetravel.pod.traceevents import GatewayStopEvent


def test_envelope_size_is_29_bytes() -> None:
    """
        Verify envelope size is exactly 29 bytes.
    """
    assert ENVELOPE_SIZE == 29

    return


def test_call_event_round_trips_with_all_fields() -> None:
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

    assert isinstance(restored, CallEvent)
    assert restored.event_type == EventType.CALL
    assert restored.timestamp_ns == 123456789
    assert restored.thread_id == 42
    assert restored.filename == "test_module.py"
    assert restored.lineno == 10
    assert restored.function_name == "my_func"
    assert restored.args == (1, "hello")
    assert restored.kwargs == {"key": "value"}
    assert offset == len(data)

    return


def test_return_event_preserves_return_value() -> None:
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

    assert isinstance(restored, ReturnEvent)
    assert restored.function_name == "get_value"
    assert restored.return_value == {"result": [1, 2, 3]}

    return


def test_line_event_has_zero_length_payload() -> None:
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
    assert payload_len == 0

    # Round-trip
    restored, _ = deserializer.deserialize(data)
    assert isinstance(restored, LineEvent)
    assert restored.filename == "script.py"
    assert restored.lineno == 42

    return


def test_preserves_local_variables_dict() -> None:
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

    assert isinstance(restored, VariableSnapshotEvent)
    assert restored.local_variables == local_vars

    return


def test_preserves_exception_details() -> None:
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

    assert isinstance(restored, ExceptionEvent)
    assert restored.exception_type == "ValueError"
    assert restored.exception_value == "invalid input"
    assert restored.traceback_str == "Traceback (most recent call last)..."

    return


def test_portal_enter_preserves_name() -> None:
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

    assert isinstance(restored, PortalEnterEvent)
    assert restored.portal_name == "auth_portal"

    return


def test_portal_exit_preserves_name() -> None:
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

    assert isinstance(restored, PortalExitEvent)
    assert restored.portal_name == "auth_portal"

    return


def test_gateway_start_preserves_wall_clock_time() -> None:
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

    assert isinstance(restored, GatewayStartEvent)
    assert round(restored.wall_clock_time - 1700000000.123456, 7) == 0

    return


def test_gateway_stop_preserves_wall_clock_time() -> None:
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

    assert isinstance(restored, GatewayStopEvent)
    assert round(restored.wall_clock_time - 1700000060.789, 7) == 0

    return


def test_read_header_returns_envelope_fields() -> None:
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

    assert event_type == EventType.CALL
    assert timestamp_ns == 1000
    assert thread_id == 5
    assert lineno == 7
    assert next_offset == ENVELOPE_SIZE

    return


def test_skip_event_advances_to_next_event() -> None:
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

    assert isinstance(restored, LineEvent)
    assert restored.timestamp_ns == 200
    assert restored.filename == "b.py"

    return
