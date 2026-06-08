"""
    Tests for the F6.3 Portal-Scoped Filtering module.
"""

import threading
import unittest

from ccai.timetravel.pod.portalfilter import filter_by_portal
from ccai.timetravel.pod.traceevents import PortalEnterEvent
from ccai.timetravel.pod.traceevents import PortalExitEvent
from ccai.timetravel.pod.traceevents import LineEvent
from ccai.timetravel.pod.traceevents import CallEvent


class TestFilterByPortal(unittest.TestCase):
    """
        Tests for the filter_by_portal function.
    """

    def _tid(self):
        rtnval = threading.get_ident()
        return rtnval

    def test_filters_events_within_enter_exit_markers(self):
        """
            Verify filtering by portal name returns only events within
            enter/exit markers.
        """
        events = [
            LineEvent(timestamp_ns=10, thread_id=self._tid(), filename="test.py", lineno=1),
            PortalEnterEvent(
                timestamp_ns=20, thread_id=self._tid(), portal_name="inner"
            ),
            LineEvent(timestamp_ns=30, thread_id=self._tid(), filename="test.py", lineno=1),
            LineEvent(timestamp_ns=40, thread_id=self._tid(), filename="test.py", lineno=1),
            PortalExitEvent(
                timestamp_ns=50, thread_id=self._tid(), portal_name="inner"
            ),
            LineEvent(timestamp_ns=60, thread_id=self._tid(), filename="test.py", lineno=1),
        ]

        result = filter_by_portal(events, "inner")

        self.assertEqual(len(result), 4)  # enter + 2 lines + exit
        self.assertIsInstance(result[0], PortalEnterEvent)
        self.assertIsInstance(result[1], LineEvent)
        self.assertIsInstance(result[2], LineEvent)
        self.assertIsInstance(result[3], PortalExitEvent)

        return

    def test_multiple_enter_exit_pairs(self):
        """
            Verify multiple enter/exit pairs return events from all occurrences.
        """
        events = [
            PortalEnterEvent(
                timestamp_ns=10, thread_id=self._tid(), portal_name="p"
            ),
            LineEvent(timestamp_ns=20, thread_id=self._tid(), filename="test.py", lineno=1),
            PortalExitEvent(
                timestamp_ns=30, thread_id=self._tid(), portal_name="p"
            ),
            LineEvent(timestamp_ns=40, thread_id=self._tid(), filename="test.py", lineno=1),  # outside
            PortalEnterEvent(
                timestamp_ns=50, thread_id=self._tid(), portal_name="p"
            ),
            LineEvent(timestamp_ns=60, thread_id=self._tid(), filename="test.py", lineno=1),
            PortalExitEvent(
                timestamp_ns=70, thread_id=self._tid(), portal_name="p"
            ),
        ]

        result = filter_by_portal(events, "p")

        # enter + line + exit + enter + line + exit = 6
        self.assertEqual(len(result), 6)
        # The outside LineEvent (ts=40) should not be included
        timestamps = [e.timestamp_ns for e in result]
        self.assertNotIn(40, timestamps)

        return

    def test_events_in_chronological_order(self):
        """
            Verify events are returned in chronological order.
        """
        events = [
            PortalEnterEvent(
                timestamp_ns=100, thread_id=self._tid(), portal_name="p"
            ),
            LineEvent(timestamp_ns=200, thread_id=self._tid(), filename="test.py", lineno=1),
            LineEvent(timestamp_ns=300, thread_id=self._tid(), filename="test.py", lineno=1),
            PortalExitEvent(
                timestamp_ns=400, thread_id=self._tid(), portal_name="p"
            ),
        ]

        result = filter_by_portal(events, "p")

        timestamps = [e.timestamp_ns for e in result]
        self.assertEqual(timestamps, [100, 200, 300, 400])

        return

    def test_nonexistent_portal_returns_empty(self):
        """
            Verify filtering by a portal name that doesn't appear returns empty list.
        """
        events = [
            LineEvent(timestamp_ns=10, thread_id=self._tid(), filename="test.py", lineno=1),
            LineEvent(timestamp_ns=20, thread_id=self._tid(), filename="test.py", lineno=1),
        ]

        result = filter_by_portal(events, "nonexistent")

        self.assertEqual(result, [])

        return


if __name__ == "__main__":
    unittest.main()
