"""
    Tests for the F1.2 Trace Recorder Interface module.
"""

import unittest

from automojo.timetravel.pod.tracerecorder import TraceRecorder
from automojo.timetravel.pod.traceevents import TraceEvent


class TestTraceRecorder(unittest.TestCase):
    """
        Tests for the TraceRecorder abstract base class.
    """

    def test_cannot_instantiate_directly(self):
        """
            Verify TraceRecorder cannot be instantiated directly.
        """
        with self.assertRaises(TypeError):
            TraceRecorder()

        return

    def test_subclass_missing_abstract_method_cannot_be_instantiated(self):
        """
            Verify a subclass missing any abstract method cannot be instantiated.
        """
        class PartialRecorder(TraceRecorder):
            def record(self, event: TraceEvent) -> None:
                return

            def flush(self) -> None:
                return

            # missing close()

        with self.assertRaises(TypeError):
            PartialRecorder()

        return

    def test_complete_subclass_can_be_instantiated(self):
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

        self.assertEqual(len(recorder.events), 1)
        self.assertTrue(recorder.flushed)
        self.assertTrue(recorder.closed)

        return


if __name__ == "__main__":
    unittest.main()
