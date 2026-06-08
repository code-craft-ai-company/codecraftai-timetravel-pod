"""
    Tests for the F1.2 Trace Recorder Interface module.
"""

from ccai.timetravel.pod.tracerecorder import TraceRecorder
from ccai.timetravel.pod.traceevents import TraceEvent


def test_cannot_instantiate_directly() -> None:
    """
        Verify TraceRecorder cannot be instantiated directly.
    """
    raised = False
    try:
        TraceRecorder()
    except TypeError:
        raised = True

    assert raised

    return


def test_subclass_missing_abstract_method_cannot_be_instantiated() -> None:
    """
        Verify a subclass missing any abstract method cannot be instantiated.
    """
    class PartialRecorder(TraceRecorder):
        def record(self, event: TraceEvent) -> None:
            return

        def flush(self) -> None:
            return

        # missing close()

    raised = False
    try:
        PartialRecorder()
    except TypeError:
        raised = True

    assert raised

    return


def test_complete_subclass_can_be_instantiated() -> None:
    """
        Verify a complete subclass can be instantiated and its methods called.
    """
    class MockRecorder(TraceRecorder):
        def __init__(self):
            self.events = []
            self.flushed = False
            self.closed = False
            return

        def record(self, event: TraceEvent) -> None:
            self.events.append(event)
            return

        def flush(self) -> None:
            self.flushed = True
            return

        def close(self) -> None:
            self.closed = True
            return

    recorder = MockRecorder()

    event = TraceEvent(event_type=1, timestamp_ns=100, thread_id=42)
    recorder.record(event)
    recorder.flush()
    recorder.close()

    assert len(recorder.events) == 1
    assert recorder.flushed
    assert recorder.closed

    return
