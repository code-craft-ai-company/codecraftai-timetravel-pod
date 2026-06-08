"""
    Tests for the F6.1 Trace File Reader module.
"""

import io
import os
import tempfile
import threading
import unittest

from ccai.timetravel.pod.reader import TraceFileReader
from ccai.timetravel.pod.traceserializer import TraceSerializer
from ccai.timetravel.pod.traceserializer import TraceDeserializer
from ccai.timetravel.pod.traceevents import CallEvent
from ccai.timetravel.pod.traceevents import ReturnEvent
from ccai.timetravel.pod.traceevents import LineEvent


class TestTraceFileReader(unittest.TestCase):
    """
        Tests for the TraceFileReader class.
    """

    def _make_serialized_events(self):
        """
            Helper to create a list of events and their serialized bytes.
        """
        serializer = TraceSerializer()
        tid = threading.get_ident()

        events = [
            CallEvent(
                timestamp_ns=100, thread_id=tid,
                filename="test.py", lineno=10, function_name="foo",
                args=(1,),
            ),
            LineEvent(timestamp_ns=200, thread_id=tid, filename="test.py", lineno=11),
            ReturnEvent(
                timestamp_ns=300, thread_id=tid,
                filename="test.py", lineno=10, function_name="foo",
                return_value=42,
            ),
        ]

        data = bytearray()
        for event in events:
            data.extend(serializer.serialize(event))

        rtnval = (events, bytes(data))
        return rtnval

    def test_round_trip_file(self):
        """
            Verify round-trip: serialize events to file, read back, compare.
        """
        events, data = self._make_serialized_events()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".bin") as f:
            f.write(data)
            path = f.name

        try:
            reader = TraceFileReader(path)
            read_events = list(reader.read_events())

            self.assertEqual(len(read_events), 3)
            self.assertEqual(read_events[0].timestamp_ns, 100)
            self.assertEqual(read_events[0].function_name, "foo")
            self.assertEqual(read_events[2].return_value, 42)
        finally:
            os.unlink(path)

        return

    def test_scan_headers(self):
        """
            Verify scan_headers returns envelope data without full deserialization.
        """
        events, data = self._make_serialized_events()

        buf = io.BytesIO(data)
        reader = TraceFileReader(buf)
        headers = list(reader.scan_headers())

        self.assertEqual(len(headers), 3)

        return

    def test_bytesio_source(self):
        """
            Verify reading from BytesIO works correctly.
        """
        events, data = self._make_serialized_events()

        buf = io.BytesIO(data)
        reader = TraceFileReader(buf)
        read_events = list(reader.read_events())

        self.assertEqual(len(read_events), 3)
        self.assertEqual(read_events[1].timestamp_ns, 200)

        return

    def test_multiple_file_sources(self):
        """
            Verify reading rotated files (list of paths) concatenates events.
        """
        events, data = self._make_serialized_events()

        paths = []
        for i in range(2):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".bin") as f:
                f.write(data)
                paths.append(f.name)

        try:
            reader = TraceFileReader(paths)
            read_events = list(reader.read_events())

            self.assertEqual(len(read_events), 6)  # 3 events x 2 files
        finally:
            for p in paths:
                os.unlink(p)

        return

    def test_context_manager(self):
        """
            Verify context manager works properly.
        """
        events, data = self._make_serialized_events()

        buf = io.BytesIO(data)
        with TraceFileReader(buf) as reader:
            read_events = list(reader.read_events())

        self.assertEqual(len(read_events), 3)

        return

    def test_unsupported_source_raises_type_error(self):
        """
            Verify unsupported source type raises TypeError.
        """
        with self.assertRaises(TypeError):
            TraceFileReader(12345)

        return


if __name__ == "__main__":
    unittest.main()
