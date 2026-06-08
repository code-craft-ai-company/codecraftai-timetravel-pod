"""
    Tests for the F0.3 Timestamp and Clock Abstraction module.
"""

import unittest

from ccai.timetravel.pod.traceclock import TraceClock
from ccai.timetravel.pod.traceclock import get_trace_clock


class TestTraceClock(unittest.TestCase):
    """
        Tests for the TraceClock class.
    """

    def setUp(self):
        self._clock = TraceClock()
        return

    def tearDown(self):
        if self._clock.is_running:
            self._clock.stop()
        return

    def test_timestamp_before_start_raises_runtime_error(self):
        """
            Verify timestamp() before start() raises RuntimeError.
        """
        with self.assertRaises(RuntimeError):
            self._clock.timestamp()

        return

    def test_timestamp_after_start_returns_non_negative_integer(self):
        """
            Verify that after start(), timestamp() returns a non-negative integer.
        """
        self._clock.start()

        ts = self._clock.timestamp()

        self.assertIsInstance(ts, int)
        self.assertGreaterEqual(ts, 0)

        return

    def test_successive_timestamps_are_non_decreasing(self):
        """
            Verify two successive timestamp() calls return non-decreasing values.
        """
        self._clock.start()

        ts1 = self._clock.timestamp()
        ts2 = self._clock.timestamp()

        self.assertGreaterEqual(ts2, ts1)

        return

    def test_timestamp_after_stop_raises_runtime_error(self):
        """
            Verify that after stop(), timestamp() raises RuntimeError again.
        """
        self._clock.start()
        self._clock.stop()

        with self.assertRaises(RuntimeError):
            self._clock.timestamp()

        return

    def test_is_running_reflects_clock_state(self):
        """
            Verify is_running reflects the clock state correctly.
        """
        self.assertFalse(self._clock.is_running)

        self._clock.start()
        self.assertTrue(self._clock.is_running)

        self._clock.stop()
        self.assertFalse(self._clock.is_running)

        return


class TestGetTraceClock(unittest.TestCase):
    """
        Tests for the get_trace_clock() function.
    """

    def test_returns_same_instance_on_repeated_calls(self):
        """
            Verify get_trace_clock() returns the same instance on repeated calls.
        """
        clock_a = get_trace_clock()
        clock_b = get_trace_clock()

        self.assertIs(clock_a, clock_b)

        return

    def test_returns_trace_clock_instance(self):
        """
            Verify get_trace_clock() returns a TraceClock instance.
        """
        clock = get_trace_clock()

        self.assertIsInstance(clock, TraceClock)

        return


if __name__ == "__main__":
    unittest.main()
