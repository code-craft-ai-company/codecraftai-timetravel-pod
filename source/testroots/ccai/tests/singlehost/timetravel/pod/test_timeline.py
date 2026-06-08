"""
    Tests for the F6.2 Timeline Reconstruction module.
"""

import threading

from ccai.timetravel.pod.timeline import TimelineBuilder
from ccai.timetravel.pod.traceevents import CallEvent
from ccai.timetravel.pod.traceevents import LineEvent
from ccai.timetravel.pod.traceevents import ReturnEvent
from ccai.timetravel.pod.traceevents import EventType


def _make_event(event_cls, timestamp_ns, thread_id=None, **kwargs):
    """
        Helper to create events with minimal boilerplate.
    """
    if thread_id is None:
        thread_id = threading.get_ident()
    # LineEvent requires filename and lineno
    if event_cls is LineEvent and "filename" not in kwargs:
        kwargs.setdefault("filename", "test.py")
        kwargs.setdefault("lineno", 1)
    rtnval = event_cls(timestamp_ns=timestamp_ns, thread_id=thread_id, **kwargs)
    return rtnval


def test_single_source_sorted_by_timestamp() -> None:
    """
        Verify events from a single source are returned sorted by timestamp.
    """
    builder = TimelineBuilder()
    builder.add_events([
        _make_event(LineEvent, 300),
        _make_event(LineEvent, 100),
        _make_event(LineEvent, 200),
    ])

    timeline = builder.build()

    timestamps = [e.timestamp_ns for e in timeline]
    assert timestamps == [100, 200, 300]

    return


def test_multiple_sources_merge_sorted() -> None:
    """
        Verify events from multiple sources merge into sorted timeline.
    """
    builder = TimelineBuilder()
    builder.add_events([
        _make_event(LineEvent, 100),
        _make_event(LineEvent, 300),
    ])
    builder.add_events([
        _make_event(LineEvent, 150),
        _make_event(LineEvent, 250),
    ])

    timeline = builder.build()

    timestamps = [e.timestamp_ns for e in timeline]
    assert timestamps == [100, 150, 250, 300]

    return


def test_thread_id_filter() -> None:
    """
        Verify thread_id filter returns only matching events.
    """
    builder = TimelineBuilder()
    builder.add_events([
        _make_event(LineEvent, 100, thread_id=1),
        _make_event(LineEvent, 200, thread_id=2),
        _make_event(LineEvent, 300, thread_id=1),
    ])

    timeline = builder.build(thread_id=1)

    assert len(timeline) == 2
    for event in timeline:
        assert event.thread_id == 1

    return


def test_event_types_filter() -> None:
    """
        Verify event_types filter returns only matching types.
    """
    builder = TimelineBuilder()
    call_event = _make_event(
        CallEvent, 100,
        filename="test.py", lineno=1, function_name="f", args=(),
    )
    line_event = _make_event(LineEvent, 200)
    return_event = _make_event(
        ReturnEvent, 300,
        filename="test.py", lineno=1, function_name="f", return_value=0,
    )

    builder.add_events([call_event, line_event, return_event])

    timeline = builder.build(event_types=[EventType.CALL])

    assert len(timeline) == 1
    assert timeline[0].event_type == EventType.CALL

    return


def test_time_range_filter() -> None:
    """
        Verify time range filter returns events within bounds.
    """
    builder = TimelineBuilder()
    builder.add_events([
        _make_event(LineEvent, 100),
        _make_event(LineEvent, 200),
        _make_event(LineEvent, 300),
        _make_event(LineEvent, 400),
    ])

    timeline = builder.build(start_ns=150, end_ns=350)

    timestamps = [e.timestamp_ns for e in timeline]
    assert timestamps == [200, 300]

    return


def test_stable_sort_preserves_order_for_equal_timestamps() -> None:
    """
        Verify stable sort preserves source ordering for equal timestamps.
    """
    builder = TimelineBuilder()

    e1 = _make_event(LineEvent, 100, thread_id=1)
    e2 = _make_event(LineEvent, 100, thread_id=2)
    e3 = _make_event(LineEvent, 100, thread_id=3)

    builder.add_events([e1, e2, e3])

    timeline = builder.build()

    assert timeline[0] is e1
    assert timeline[1] is e2
    assert timeline[2] is e3

    return
