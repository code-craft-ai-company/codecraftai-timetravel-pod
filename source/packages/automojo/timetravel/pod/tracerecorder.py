"""
    Provides the abstract base class for trace recorders.

    This module defines the :class:`TraceRecorder` interface that all concrete
    trace recorder implementations must satisfy.
"""

from abc import ABC
from abc import abstractmethod

from automojo.timetravel.pod.traceevents import TraceEvent


class TraceRecorder(ABC):
    """
        Abstract base class defining the contract for all trace recorders.
    """

    @abstractmethod
    def record(self, event: TraceEvent) -> None:
        """
            Accept a single trace event for recording.

            This method is called from the trace hook on the hot path and
            should be as fast as possible.

            :param event: The trace event to record.
        """
        ...

    @abstractmethod
    def flush(self) -> None:
        """
            Ensure all buffered data is written to the underlying stream.
        """
        ...

    @abstractmethod
    def close(self) -> None:
        """
            Finalize the recorder and release held resources.
        """
        ...
