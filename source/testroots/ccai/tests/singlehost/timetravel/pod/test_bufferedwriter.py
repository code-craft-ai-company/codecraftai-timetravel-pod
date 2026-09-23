"""
    Tests for the F1.4 Buffered Writer module.
"""

from ccai.timetravel.pod.bufferedwriter import BufferedTraceWriter
from ccai.timetravel.pod.bufferedwriter import DEFAULT_BUFFER_SIZE


class MockStream:
    """
        A mock stream that records write and close calls.
    """

    def __init__(self):
        self.written_chunks = []
        self.closed = False
        return

    def write(self, data: bytes) -> None:
        self.written_chunks.append(data)
        return

    def close(self) -> None:
        self.closed = True
        return

    @property
    def total_bytes_written(self) -> int:
        rtnval = sum(len(chunk) for chunk in self.written_chunks)
        return rtnval


def test_small_write_does_not_trigger_stream_write() -> None:
    """
        Verify writing data smaller than buffer size does not trigger
        stream write.
    """
    stream = MockStream()
    writer = BufferedTraceWriter(stream, max_buffer_size=1024)

    writer.write(b"small data")

    assert len(stream.written_chunks) == 0

    return


def test_exceeding_buffer_triggers_auto_flush() -> None:
    """
        Verify writing data that exceeds buffer size triggers auto-flush.
    """
    stream = MockStream()
    writer = BufferedTraceWriter(stream, max_buffer_size=16)

    writer.write(b"x" * 20)

    assert len(stream.written_chunks) == 1
    assert len(stream.written_chunks[0]) == 20

    return


def test_flush_writes_buffered_data_immediately() -> None:
    """
        Verify flush() writes buffered data to stream immediately.
    """
    stream = MockStream()
    writer = BufferedTraceWriter(stream, max_buffer_size=1024)

    writer.write(b"buffered data")
    assert len(stream.written_chunks) == 0

    writer.flush()

    assert len(stream.written_chunks) == 1
    assert stream.written_chunks[0] == b"buffered data"

    return


def test_close_flushes_then_closes_stream() -> None:
    """
        Verify close() flushes remaining data then closes the stream.
    """
    stream = MockStream()
    writer = BufferedTraceWriter(stream, max_buffer_size=1024)

    writer.write(b"final data")
    writer.close()

    assert len(stream.written_chunks) == 1
    assert stream.written_chunks[0] == b"final data"
    assert stream.closed

    return


def test_multiple_small_writes_accumulate() -> None:
    """
        Verify multiple small writes accumulate in buffer until threshold.
    """
    stream = MockStream()
    writer = BufferedTraceWriter(stream, max_buffer_size=32)

    writer.write(b"aaaa")  # 4 bytes
    writer.write(b"bbbb")  # 8 total
    writer.write(b"cccc")  # 12 total

    assert len(stream.written_chunks) == 0

    # Now exceed threshold
    writer.write(b"x" * 25)  # 37 total, exceeds 32

    assert len(stream.written_chunks) == 1
    assert stream.total_bytes_written == 37

    return


def test_custom_buffer_size_is_respected() -> None:
    """
        Verify custom buffer size is respected.
    """
    stream = MockStream()
    writer = BufferedTraceWriter(stream, max_buffer_size=8)

    writer.write(b"1234567")  # 7 bytes, under 8

    assert len(stream.written_chunks) == 0

    writer.write(b"8")  # 8 bytes, at threshold

    assert len(stream.written_chunks) == 1

    return


def test_default_buffer_size_constant() -> None:
    """
        Verify the DEFAULT_BUFFER_SIZE constant is 64 KB.
    """
    assert DEFAULT_BUFFER_SIZE == 65536

    return
