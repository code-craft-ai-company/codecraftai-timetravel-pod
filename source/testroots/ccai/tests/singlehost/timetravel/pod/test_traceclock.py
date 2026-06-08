"""
    Tests for the F0.3 Timestamp and Clock Abstraction module.
"""

from ccai.timetravel.pod.traceclock import TraceClock
from ccai.timetravel.pod.traceclock import get_trace_clock


def _setup_trace_clock() -> TraceClock:
    """
        Create a fresh :class:`TraceClock` instance for a single test.

        :returns: A newly constructed :class:`TraceClock`.
    """
    clock = TraceClock()
    return clock


def _teardown_trace_clock(clock: TraceClock) -> None:
    """
        Stop the supplied clock if it is still running.

        :param clock: The :class:`TraceClock` instance to clean up.
    """
    if clock.is_running:
        clock.stop()
    return


def test_timestamp_before_start_raises_runtime_error() -> None:
    """
        Verify timestamp() before start() raises RuntimeError.
    """
    clock = _setup_trace_clock()

    try:
        raised = False
        try:
            clock.timestamp()
        except RuntimeError:
            raised = True

        assert raised
    finally:
        _teardown_trace_clock(clock=clock)

    return


def test_timestamp_after_start_returns_non_negative_integer() -> None:
    """
        Verify that after start(), timestamp() returns a non-negative integer.
    """
    clock = _setup_trace_clock()

    try:
        clock.start()

        ts = clock.timestamp()

        assert isinstance(ts, int)
        assert ts >= 0
    finally:
        _teardown_trace_clock(clock=clock)

    return


def test_successive_timestamps_are_non_decreasing() -> None:
    """
        Verify two successive timestamp() calls return non-decreasing values.
    """
    clock = _setup_trace_clock()

    try:
        clock.start()

        ts1 = clock.timestamp()
        ts2 = clock.timestamp()

        assert ts2 >= ts1
    finally:
        _teardown_trace_clock(clock=clock)

    return


def test_timestamp_after_stop_raises_runtime_error() -> None:
    """
        Verify that after stop(), timestamp() raises RuntimeError again.
    """
    clock = _setup_trace_clock()

    try:
        clock.start()
        clock.stop()

        raised = False
        try:
            clock.timestamp()
        except RuntimeError:
            raised = True

        assert raised
    finally:
        _teardown_trace_clock(clock=clock)

    return


def test_is_running_reflects_clock_state() -> None:
    """
        Verify is_running reflects the clock state correctly.
    """
    clock = _setup_trace_clock()

    try:
        assert not clock.is_running

        clock.start()
        assert clock.is_running

        clock.stop()
        assert not clock.is_running
    finally:
        _teardown_trace_clock(clock=clock)

    return


def test_returns_same_instance_on_repeated_calls() -> None:
    """
        Verify get_trace_clock() returns the same instance on repeated calls.
    """
    clock_a = get_trace_clock()
    clock_b = get_trace_clock()

    assert clock_a is clock_b

    return


def test_returns_trace_clock_instance() -> None:
    """
        Verify get_trace_clock() returns a TraceClock instance.
    """
    clock = get_trace_clock()

    assert isinstance(clock, TraceClock)

    return
