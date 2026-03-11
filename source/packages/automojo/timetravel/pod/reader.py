"""
    Provides the trace file reader for deserializing trace files.

    This module contains the :class:`TraceFileReader` which reads and
    deserializes trace files or BytesIO objects into TraceEvent objects.
"""

import io

from automojo.timetravel.pod.traceserializer import TraceDeserializer


class TraceFileReader:
    """
        Reads and deserializes trace files into TraceEvent objects.

        Accepts a single file path, a list of file paths (for rotated files),
        or a ``BytesIO`` object as input.
    """

    def __init__(self, source) -> None:
        """
            Create a TraceFileReader.

            :param source: A file path (str), list of file paths, or BytesIO object.

            :raises TypeError: If source is not a supported type.
        """
        self._deserializer = TraceDeserializer()
        self._sources = []

        if isinstance(source, str):
            self._sources = [source]
        elif isinstance(source, list):
            self._sources = source
        elif isinstance(source, io.BytesIO):
            self._sources = [source]
        else:
            raise TypeError(f"Unsupported source type: {type(source)}")

        return

    def __enter__(self):
        """
            Enter the context manager.

            :returns: This reader instance.
        """
        rtnval = self
        return rtnval

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
            Exit the context manager.

            :returns: False to propagate exceptions.
        """
        self.close()
        rtnval = False
        return rtnval

    def read_events(self):
        """
            Yield all TraceEvent objects from the source(s).

            Events are yielded in the order they appear in the source files.
        """
        for source in self._sources:
            data = self._read_source(source)
            offset = 0
            while offset < len(data):
                event, offset = self._deserializer.deserialize(data, offset)
                yield event

        return

    def scan_headers(self):
        """
            Yield envelope-only tuples without deserializing payloads.

            This is more efficient than ``read_events()`` when you only
            need the envelope metadata (event type, timestamp, etc.).
        """
        for source in self._sources:
            data = self._read_source(source)
            offset = 0
            while offset < len(data):
                header, _ = self._deserializer.read_header(data, offset)
                yield header
                offset = self._deserializer.skip_event(data, offset)

        return

    def _read_source(self, source) -> bytes:
        """
            Read the raw bytes from a source.

            :param source: A file path string or BytesIO object.

            :returns: The raw bytes.
        """
        if isinstance(source, str):
            with open(source, "rb") as f:
                rtnval = f.read()
        elif isinstance(source, io.BytesIO):
            rtnval = source.getvalue()
        else:
            rtnval = b""
        return rtnval

    def close(self) -> None:
        """
            Close the reader.

            File handles are opened and closed per read, so this is a no-op.
        """
        return
