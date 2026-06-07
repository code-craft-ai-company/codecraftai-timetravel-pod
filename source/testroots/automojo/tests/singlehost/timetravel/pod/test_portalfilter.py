"""
    Tests for the F6.3 Portal-Scoped Filtering module.
"""

import threading

from automojo.timetravel.pod.portalfilter import filter_by_portal
from automojo.timetravel.pod.traceevents import PortalEnterEvent
from automojo.timetravel.pod.traceevents import PortalExitEvent
from automojo.timetravel.pod.traceevents import LineEvent
from automojo.timetravel.pod.traceevents import CallEvent


def _tid() -> int:
    """
        Return the identifier of the current thread.

        :returns: The current thread identifier.
    """
    rtnval = threading.get_ident()
    return rtnval


def test_filters_events_within_enter_exit_markers() -> None:
    """
        Verify filtering by portal name returns only events within
        enter/exit markers.
    """
    events = [
        LineEvent(timestamp_ns=10, thread_id=_tid(), filename="test.py", lineno=1),
        PortalEnterEvent(
            timestamp_ns=20, thread_id=_tid(), portal_name="inner"
        ),
        LineEvent(timestamp_ns=30, thread_id=_tid(), filename="test.py", lineno=1),
        LineEvent(timestamp_ns=40, thread_id=_tid(), filename="test.py", lineno=1),
        PortalExitEvent(
            timestamp_ns=50, thread_id=_tid(), portal_name="inner"
        ),
        LineEvent(timestamp_ns=60, thread_id=_tid(), filename="test.py", lineno=1),
    ]

    result = filter_by_portal(events, "inner")

    assert len(result) == 4  # enter + 2 lines + exit
    assert isinstance(result[0], PortalEnterEvent)
    assert isinstance(result[1], LineEvent)
    assert isinstance(result[2], LineEvent)
    assert isinstance(result[3], PortalExitEvent)

    return


def test_multiple_enter_exit_pairs() -> None:
    """
        Verify multiple enter/exit pairs return events from all occurrences.
    """
    events = [
        PortalEnterEvent(
            timestamp_ns=10, thread_id=_tid(), portal_name="p"
        ),
        LineEvent(timestamp_ns=20, thread_id=_tid(), filename="test.py", lineno=1),
        PortalExitEvent(
            timestamp_ns=30, thread_id=_tid(), portal_name="p"
        ),
        LineEvent(timestamp_ns=40, thread_id=_tid(), filename="test.py", lineno=1),  # outside
        PortalEnterEvent(
            timestamp_ns=50, thread_id=_tid(), portal_name="p"
        ),
        LineEvent(timestamp_ns=60, thread_id=_tid(), filename="test.py", lineno=1),
        PortalExitEvent(
            timestamp_ns=70, thread_id=_tid(), portal_name="p"
        ),
    ]

    result = filter_by_portal(events, "p")

    # enter + line + exit + enter + line + exit = 6
    assert len(result) == 6
    # The outside LineEvent (ts=40) should not be included
    timestamps = [e.timestamp_ns for e in result]
    assert 40 not in timestamps

    return


def test_events_in_chronological_order() -> None:
    """
        Verify events are returned in chronological order.
    """
    events = [
        PortalEnterEvent(
            timestamp_ns=100, thread_id=_tid(), portal_name="p"
        ),
        LineEvent(timestamp_ns=200, thread_id=_tid(), filename="test.py", lineno=1),
        LineEvent(timestamp_ns=300, thread_id=_tid(), filename="test.py", lineno=1),
        PortalExitEvent(
            timestamp_ns=400, thread_id=_tid(), portal_name="p"
        ),
    ]

    result = filter_by_portal(events, "p")

    timestamps = [e.timestamp_ns for e in result]
    assert timestamps == [100, 200, 300, 400]

    return


def test_nonexistent_portal_returns_empty() -> None:
    """
        Verify filtering by a portal name that doesn't appear returns empty list.
    """
    events = [
        LineEvent(timestamp_ns=10, thread_id=_tid(), filename="test.py", lineno=1),
        LineEvent(timestamp_ns=20, thread_id=_tid(), filename="test.py", lineno=1),
    ]

    result = filter_by_portal(events, "nonexistent")

    assert result == []

    return
