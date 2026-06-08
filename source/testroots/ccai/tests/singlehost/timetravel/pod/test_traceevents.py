"""
    Tests for the F0.4 Trace Event Model module.
"""

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


def test_all_constants_are_unique_integers() -> None:
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
        assert isinstance(constant, int)

    unique_values = set(constants)
    assert len(unique_values) == len(constants)

    return


def test_expected_type_values() -> None:
    """
        Verify the expected integer values for each event type.
    """
    assert EventType.CALL == 1
    assert EventType.RETURN == 2
    assert EventType.LINE == 3
    assert EventType.VARIABLE_SNAPSHOT == 4
    assert EventType.PORTAL_ENTER == 5
    assert EventType.PORTAL_EXIT == 6
    assert EventType.GATEWAY_START == 7
    assert EventType.GATEWAY_STOP == 8
    assert EventType.EXCEPTION == 9

    return


def test_base_fields_are_set_correctly() -> None:
    """
        Verify TraceEvent base fields are set correctly.
    """
    event = TraceEvent(event_type=1, timestamp_ns=12345, thread_id=99)

    assert event.event_type == 1
    assert event.timestamp_ns == 12345
    assert event.thread_id == 99

    return


def test_slots_prevents_arbitrary_attribute_addition() -> None:
    """
        Verify __slots__ prevents arbitrary attribute addition.
    """
    event = TraceEvent(event_type=1, timestamp_ns=0, thread_id=0)

    raised = False
    try:
        event.arbitrary_attribute = "should_fail"
    except AttributeError:
        raised = True

    assert raised

    return


def test_constructible_with_documented_fields_callevent() -> None:
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

    assert event.event_type == EventType.CALL
    assert event.timestamp_ns == 1000
    assert event.thread_id == 42
    assert event.filename == "test.py"
    assert event.lineno == 10
    assert event.function_name == "my_func"
    assert event.args == (1, 2)
    assert event.kwargs == {"key": "value"}

    return


def test_default_args_and_kwargs() -> None:
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

    assert event.args == ()
    assert event.kwargs is None

    return


def test_slots_prevents_arbitrary_attribute() -> None:
    """
        Verify __slots__ prevents arbitrary attribute addition.
    """
    event = CallEvent(
        timestamp_ns=0, thread_id=0, filename="", lineno=0, function_name="",
    )

    raised = False
    try:
        event.extra = "nope"
    except AttributeError:
        raised = True

    assert raised

    return


def test_constructible_with_documented_fields_returnevent() -> None:
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

    assert event.event_type == EventType.RETURN
    assert event.return_value == 42

    return


def test_constructible_with_documented_fields_lineevent() -> None:
    """
        Verify LineEvent is constructible with all documented fields.
    """
    event = LineEvent(
        timestamp_ns=3000,
        thread_id=42,
        filename="test.py",
        lineno=30,
    )

    assert event.event_type == EventType.LINE
    assert event.filename == "test.py"
    assert event.lineno == 30

    return


def test_constructible_with_documented_fields_variablesnapshotevent() -> None:
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

    assert event.event_type == EventType.VARIABLE_SNAPSHOT
    assert event.local_variables == local_vars

    return


def test_stores_exception_details_as_strings() -> None:
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

    assert event.event_type == EventType.EXCEPTION
    assert event.exception_type == "ValueError"
    assert event.exception_value == "bad value"
    assert event.traceback_str == "Traceback ..."

    return


def test_portal_enter_event() -> None:
    """
        Verify PortalEnterEvent is constructible with portal_name.
    """
    event = PortalEnterEvent(
        timestamp_ns=6000, thread_id=42, portal_name="auth_portal",
    )

    assert event.event_type == EventType.PORTAL_ENTER
    assert event.portal_name == "auth_portal"

    return


def test_portal_exit_event() -> None:
    """
        Verify PortalExitEvent is constructible with portal_name.
    """
    event = PortalExitEvent(
        timestamp_ns=7000, thread_id=42, portal_name="auth_portal",
    )

    assert event.event_type == EventType.PORTAL_EXIT
    assert event.portal_name == "auth_portal"

    return


def test_gateway_start_event() -> None:
    """
        Verify GatewayStartEvent stores wall_clock_time.
    """
    event = GatewayStartEvent(
        timestamp_ns=0, thread_id=42, wall_clock_time=1700000000.123,
    )

    assert event.event_type == EventType.GATEWAY_START
    assert round(event.wall_clock_time - 1700000000.123, 7) == 0

    return


def test_gateway_stop_event() -> None:
    """
        Verify GatewayStopEvent stores wall_clock_time.
    """
    event = GatewayStopEvent(
        timestamp_ns=99999, thread_id=42, wall_clock_time=1700000060.456,
    )

    assert event.event_type == EventType.GATEWAY_STOP
    assert round(event.wall_clock_time - 1700000060.456, 7) == 0

    return
