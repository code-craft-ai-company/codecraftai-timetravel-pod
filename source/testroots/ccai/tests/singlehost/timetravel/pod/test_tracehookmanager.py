"""
    Tests for the F1.1 Trace Hook Manager module.
"""

import threading

from typing import List

from ccai.timetravel.pod.tracehookmanager import TraceHookManager
from ccai.timetravel.pod.traceconfiguration import TraceConfiguration
from ccai.timetravel.pod.traceclock import TraceClock
from ccai.timetravel.pod.traceclock import get_trace_clock
from ccai.timetravel.pod.traceevents import CallEvent
from ccai.timetravel.pod.traceevents import ReturnEvent
from ccai.timetravel.pod.traceevents import LineEvent
from ccai.timetravel.pod.traceevents import VariableSnapshotEvent
from ccai.timetravel.pod.traceevents import ExceptionEvent


class TraceHookFixture:
    """
        Per-test fixture state replicating the original ``setUp`` for the
        ``TestTraceHookManager`` test case. Holds the started trace clock and
        the list of recorded events. The :meth:`record_callback` method stands
        in for the original ``_record_callback`` instance method.
    """

    def __init__(self, clock: TraceClock) -> None:
        self._clock = clock
        self._recorded_events: List[object] = []
        return

    @property
    def clock(self) -> TraceClock:
        return self._clock

    @property
    def recorded_events(self) -> List[object]:
        return self._recorded_events

    def record_callback(self, event: object) -> None:
        """
            Append a recorded trace event to the collected list.

            :param event: The trace event produced by the hook manager.
        """
        self._recorded_events.append(event)
        return


def _setup_trace_hook_fixture() -> TraceHookFixture:
    """
        Replicate the original ``setUp``: acquire the shared trace clock,
        start it, and create a fresh fixture holding an empty recorded-events
        list.

        :returns: A started :class:`TraceHookFixture` for a single test.
    """
    clock = get_trace_clock()
    clock.start()
    fixture = TraceHookFixture(clock=clock)
    return fixture


def _teardown_trace_hook_fixture(fixture: TraceHookFixture) -> None:
    """
        Replicate the original ``tearDown``: stop the trace clock if it is
        still running.

        :param fixture: The :class:`TraceHookFixture` instance to clean up.
    """
    if fixture.clock.is_running:
        fixture.clock.stop()
    return


def test_install_and_call_produces_call_and_return_events() -> None:
    """
        Verify installing the hook and calling a function produces
        CallEvent and ReturnEvent.
    """
    fixture = _setup_trace_hook_fixture()

    try:
        config = TraceConfiguration(trace_calls=True)
        manager = TraceHookManager(
            configuration=config, record_callback=fixture.record_callback
        )

        def simple_function():
            return 42

        manager.install()
        simple_function()
        manager.uninstall()

        call_events = [e for e in fixture.recorded_events if isinstance(e, CallEvent)]
        return_events = [e for e in fixture.recorded_events if isinstance(e, ReturnEvent)]

        assert len(call_events) > 0
        assert len(return_events) > 0

        # Find the call event for our function
        simple_calls = [e for e in call_events if e.function_name == "simple_function"]
        assert len(simple_calls) == 1
    finally:
        _teardown_trace_hook_fixture(fixture=fixture)

    return


def test_trace_lines_true_produces_line_events() -> None:
    """
        Verify with trace_lines=True, executing code produces LineEvent objects.
    """
    fixture = _setup_trace_hook_fixture()

    try:
        config = TraceConfiguration(trace_calls=True, trace_lines=True)
        manager = TraceHookManager(
            configuration=config, record_callback=fixture.record_callback
        )

        def multi_line():
            a = 1
            b = 2
            c = a + b
            return c

        manager.install()
        multi_line()
        manager.uninstall()

        line_events = [e for e in fixture.recorded_events if isinstance(e, LineEvent)]

        assert len(line_events) > 0
    finally:
        _teardown_trace_hook_fixture(fixture=fixture)

    return


def test_trace_lines_false_no_line_events() -> None:
    """
        Verify with trace_lines=False, no LineEvent objects are produced.
    """
    fixture = _setup_trace_hook_fixture()

    try:
        config = TraceConfiguration(trace_calls=True, trace_lines=False)
        manager = TraceHookManager(
            configuration=config, record_callback=fixture.record_callback
        )

        def multi_line():
            a = 1
            b = 2
            return a + b

        manager.install()
        multi_line()
        manager.uninstall()

        line_events = [e for e in fixture.recorded_events if isinstance(e, LineEvent)]

        assert len(line_events) == 0
    finally:
        _teardown_trace_hook_fixture(fixture=fixture)

    return


def test_trace_variables_produces_snapshot_events() -> None:
    """
        Verify with trace_variables=True, VariableSnapshotEvent contains local
        variable data.
    """
    fixture = _setup_trace_hook_fixture()

    try:
        config = TraceConfiguration(
            trace_calls=True, trace_lines=True, trace_variables=True
        )
        manager = TraceHookManager(
            configuration=config, record_callback=fixture.record_callback
        )

        def var_function():
            x = 42
            y = "hello"
            return x

        manager.install()
        var_function()
        manager.uninstall()

        snapshot_events = [
            e for e in fixture.recorded_events
            if isinstance(e, VariableSnapshotEvent)
        ]

        assert len(snapshot_events) > 0

        # At least one snapshot should have our variables
        has_x = False
        for snap in snapshot_events:
            if "x" in snap.local_variables:
                has_x = True
                break

        assert has_x
    finally:
        _teardown_trace_hook_fixture(fixture=fixture)

    return


def test_exceptions_produce_exception_events() -> None:
    """
        Verify exceptions produce ExceptionEvent objects.
    """
    fixture = _setup_trace_hook_fixture()

    try:
        config = TraceConfiguration(trace_calls=True)
        manager = TraceHookManager(
            configuration=config, record_callback=fixture.record_callback
        )

        def failing_function():
            raise ValueError("test error")

        manager.install()
        try:
            failing_function()
        except ValueError:
            # Expected: the test only needs the trace hook to observe the raised exception.
            pass
        manager.uninstall()

        exception_events = [
            e for e in fixture.recorded_events if isinstance(e, ExceptionEvent)
        ]

        assert len(exception_events) > 0

        # Find the exception for our ValueError
        value_errors = [
            e for e in exception_events if e.exception_type == "ValueError"
        ]
        assert len(value_errors) > 0
    finally:
        _teardown_trace_hook_fixture(fixture=fixture)

    return


def test_uninstall_stops_event_production() -> None:
    """
        Verify uninstall() stops all event production.
    """
    fixture = _setup_trace_hook_fixture()

    try:
        config = TraceConfiguration(trace_calls=True)
        manager = TraceHookManager(
            configuration=config, record_callback=fixture.record_callback
        )

        def func_a():
            return 1

        def func_b():
            return 2

        manager.install()
        func_a()
        manager.uninstall()

        count_after_uninstall = len(fixture.recorded_events)

        func_b()

        assert len(fixture.recorded_events) == count_after_uninstall
    finally:
        _teardown_trace_hook_fixture(fixture=fixture)

    return


def test_events_carry_correct_thread_id() -> None:
    """
        Verify events carry the correct thread ID.
    """
    fixture = _setup_trace_hook_fixture()

    try:
        config = TraceConfiguration(trace_calls=True)
        manager = TraceHookManager(
            configuration=config, record_callback=fixture.record_callback
        )
        expected_thread_id = threading.get_ident()

        def simple():
            return 1

        manager.install()
        simple()
        manager.uninstall()

        for event in fixture.recorded_events:
            assert event.thread_id == expected_thread_id
    finally:
        _teardown_trace_hook_fixture(fixture=fixture)

    return
