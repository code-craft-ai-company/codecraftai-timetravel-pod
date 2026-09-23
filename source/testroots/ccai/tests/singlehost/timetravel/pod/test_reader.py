"""
    Tests for the F6.1 Trace File Reader module.
"""

import io
import os
import tempfile
import threading

from typing import List
from typing import Tuple

from ccai.timetravel.pod.reader import TraceFileReader
from ccai.timetravel.pod.traceserializer import TraceSerializer
from ccai.timetravel.pod.traceevents import CallEvent
from ccai.timetravel.pod.traceevents import ReturnEvent
from ccai.timetravel.pod.traceevents import LineEvent


def _make_serialized_events() -> Tuple[List[object], bytes]:
    """
        Helper to create a list of events and their serialized bytes.

        :returns: A tuple of the original events list and their serialized bytes.
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
        data.extend(serializer.serialize(event=event))

    rtnval = (events, bytes(data))
    return rtnval


def test_round_trip_file() -> None:
    """
        Verify round-trip: serialize events to file, read back, compare.
    """
    events, data = _make_serialized_events()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".bin") as f:
        f.write(data)
        path = f.name

    try:
        reader = TraceFileReader(path)
        read_events = list(reader.read_events())

        assert len(read_events) == 3
        assert read_events[0].timestamp_ns == 100
        assert read_events[0].function_name == "foo"
        assert read_events[2].return_value == 42
    finally:
        os.unlink(path)

    return


def test_scan_headers() -> None:
    """
        Verify scan_headers returns envelope data without full deserialization.
    """
    events, data = _make_serialized_events()

    buf = io.BytesIO(data)
    reader = TraceFileReader(buf)
    headers = list(reader.scan_headers())

    assert len(headers) == 3

    return


def test_bytesio_source() -> None:
    """
        Verify reading from BytesIO works correctly.
    """
    events, data = _make_serialized_events()

    buf = io.BytesIO(data)
    reader = TraceFileReader(buf)
    read_events = list(reader.read_events())

    assert len(read_events) == 3
    assert read_events[1].timestamp_ns == 200

    return


def test_multiple_file_sources() -> None:
    """
        Verify reading rotated files (list of paths) concatenates events.
    """
    events, data = _make_serialized_events()

    paths = []
    for i in range(2):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".bin") as f:
            f.write(data)
            paths.append(f.name)

    try:
        reader = TraceFileReader(paths)
        read_events = list(reader.read_events())

        assert len(read_events) == 6  # 3 events x 2 files
    finally:
        for p in paths:
            os.unlink(p)

    return


def test_context_manager() -> None:
    """
        Verify context manager works properly.
    """
    events, data = _make_serialized_events()

    buf = io.BytesIO(data)
    with TraceFileReader(buf) as reader:
        read_events = list(reader.read_events())

    assert len(read_events) == 3

    return


def test_unsupported_source_raises_type_error() -> None:
    """
        Verify unsupported source type raises TypeError.
    """
    raised = False
    try:
        TraceFileReader(12345)
    except TypeError:
        raised = True

    assert raised

    return
