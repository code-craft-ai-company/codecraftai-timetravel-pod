"""
    Provides a monotonic high-resolution clock abstraction for the time travel pod.

    This module contains the :class:`TraceClock` class which produces nanosecond
    timestamps relative to the gateway start using ``time.perf_counter_ns()``.
"""

import time

from typing import Optional


class TraceClock:
    """
        Monotonic high-resolution clock for trace event timestamps.

        Uses ``time.perf_counter_ns()`` to provide nanosecond-resolution
        timestamps relative to the gateway start time.
    """

    def __init__(self) -> None:
        self._origin_ns: Optional[int] = None
        return

    def start(self) -> None:
        """
            Record the origin timestamp. Called when the gateway is entered.
        """
        self._origin_ns = time.perf_counter_ns()
        return

    def stop(self) -> None:
        """
            Clear the origin. Called when the gateway is exited.
        """
        self._origin_ns = None
        return

    def timestamp(self) -> int:
        """
            Return nanosecond offset from origin.

            :returns: An integer representing nanoseconds since the clock was started.

            :raises: RuntimeError
        """
        if self._origin_ns is None:
            errmsg = "TraceClock has not been started. Enter the TimeTravelGateway first."
            raise RuntimeError(errmsg)

        rtnval = time.perf_counter_ns() - self._origin_ns
        return rtnval

    @property
    def is_running(self) -> bool:
        """
            Whether the clock is currently running.
        """
        rtnval = self._origin_ns is not None
        return rtnval


_trace_clock = TraceClock()


def get_trace_clock() -> TraceClock:
    """
        Return the process-wide singleton TraceClock instance.

        :returns: The singleton TraceClock.
    """
    rtnval = _trace_clock
    return rtnval
