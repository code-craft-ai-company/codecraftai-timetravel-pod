"""
    Provides a buffered writer for batching serialized trace event bytes.

    This module contains the :class:`BufferedTraceWriter` class which accumulates
    serialized bytes in a ``bytearray`` and flushes to a stream backend when the
    buffer reaches a configurable threshold.
"""


DEFAULT_BUFFER_SIZE = 65536  # 64 KB


class BufferedTraceWriter:
    """
        Batches serialized event bytes and flushes to a stream backend in chunks.

        The stream argument must support ``write(data: bytes)`` and ``close()``.
    """

    __slots__ = ("_stream", "_buffer", "_max_size")

    def __init__(self, stream, max_buffer_size: int = DEFAULT_BUFFER_SIZE) -> None:
        """
            Create a BufferedTraceWriter.

            :param stream: An object with write(bytes) and close() methods.
            :param max_buffer_size: The buffer size threshold in bytes before auto-flush.
        """
        self._stream = stream
        self._buffer = bytearray()
        self._max_size = max_buffer_size
        return

    def write(self, data: bytes) -> None:
        """
            Append serialized bytes to the buffer, auto-flushing if full.

            :param data: The bytes to write.
        """
        self._buffer.extend(data)
        if len(self._buffer) >= self._max_size:
            self.flush()
        return

    def flush(self) -> None:
        """
            Write all buffered data to the stream backend.
        """
        if len(self._buffer) > 0:
            self._stream.write(bytes(self._buffer))
            self._buffer.clear()
        return

    def close(self) -> None:
        """
            Flush remaining data and close the stream backend.
        """
        self.flush()
        self._stream.close()
        return
