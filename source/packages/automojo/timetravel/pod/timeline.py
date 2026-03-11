"""
    Provides timeline reconstruction from trace events.

    This module contains the :class:`TimelineBuilder` which sorts and
    filters trace events into a chronologically ordered timeline.
"""

from typing import Optional


class TimelineBuilder:
    """
        Builds a sorted timeline from one or more event sources.

        Events can be added incrementally via :meth:`add_events`, and then
        :meth:`build` produces a sorted, optionally filtered timeline.
    """

    def __init__(self) -> None:
        """
            Create a TimelineBuilder.
        """
        self._events: list = []
        return

    def add_events(self, events) -> None:
        """
            Add an iterable of TraceEvent objects to the builder.

            :param events: An iterable of TraceEvent objects.
        """
        self._events.extend(events)
        return

    def build(self, thread_id: Optional[int] = None,
              event_types: Optional[list] = None,
              start_ns: Optional[int] = None,
              end_ns: Optional[int] = None) -> list:
        """
            Build the sorted, filtered timeline.

            Uses Python's stable sort to preserve source ordering for events
            with equal timestamps.

            :param thread_id: If set, only include events from this thread.
            :param event_types: If set, only include events with these event type values.
            :param start_ns: If set, only include events at or after this timestamp.
            :param end_ns: If set, only include events at or before this timestamp.

            :returns: A sorted, filtered list of TraceEvent objects.
        """
        # Sort by timestamp (stable sort preserves source ordering)
        self._events.sort(key=lambda e: e.timestamp_ns)

        filtered = self._events

        if thread_id is not None:
            filtered = [e for e in filtered if e.thread_id == thread_id]

        if event_types is not None:
            type_set = set(event_types)
            filtered = [e for e in filtered if e.event_type in type_set]

        if start_ns is not None:
            filtered = [e for e in filtered if e.timestamp_ns >= start_ns]

        if end_ns is not None:
            filtered = [e for e in filtered if e.timestamp_ns <= end_ns]

        rtnval = filtered
        return rtnval
