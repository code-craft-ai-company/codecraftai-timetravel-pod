"""
    Provides the hybrid struct+pickle serialization format for trace events.

    This module contains the :class:`TraceSerializer` and :class:`TraceDeserializer`
    classes which convert :class:`TraceEvent` objects to and from a compact binary
    format using ``struct`` for fixed-size envelopes and ``pickle`` protocol 5
    for variable-size payloads.
"""

import pickle
import struct

from ccai.timetravel.pod.traceevents import EventType
from ccai.timetravel.pod.traceevents import TraceEvent
from ccai.timetravel.pod.traceevents import CallEvent
from ccai.timetravel.pod.traceevents import ReturnEvent
from ccai.timetravel.pod.traceevents import LineEvent
from ccai.timetravel.pod.traceevents import VariableSnapshotEvent
from ccai.timetravel.pod.traceevents import ExceptionEvent
from ccai.timetravel.pod.traceevents import PortalEnterEvent
from ccai.timetravel.pod.traceevents import PortalExitEvent
from ccai.timetravel.pod.traceevents import GatewayStartEvent
from ccai.timetravel.pod.traceevents import GatewayStopEvent

from typing import Optional


# Format: ! = network byte order (big-endian)
#   B  = event_type       (1 byte,  unsigned char)
#   Q  = timestamp_ns     (8 bytes, unsigned long long)
#   Q  = thread_id        (8 bytes, unsigned long long)
#   I  = filename_length  (4 bytes, unsigned int)
#   I  = lineno           (4 bytes, unsigned int)
#   I  = payload_length   (4 bytes, unsigned int)
ENVELOPE_FORMAT = "!BQQIII"
ENVELOPE_SIZE = struct.calcsize(ENVELOPE_FORMAT)  # 29 bytes


class TraceSerializer:
    """
        Serializes TraceEvent objects into the hybrid struct+pickle binary format.

        Uses a pre-compiled ``struct.Struct`` for maximum packing speed.
    """

    def __init__(self) -> None:
        self._struct = struct.Struct(ENVELOPE_FORMAT)
        self._pack = self._struct.pack
        return

    def serialize(self, event: TraceEvent) -> bytes:
        """
            Serialize a single TraceEvent to bytes.

            :param event: The trace event to serialize.

            :returns: The serialized bytes.
        """
        payload_data = self._extract_payload(event)

        if payload_data is not None:
            payload_bytes = pickle.dumps(payload_data, protocol=5)
        else:
            payload_bytes = b""

        filename = self._extract_filename(event)
        if filename:
            filename_bytes = filename.encode("utf-8")
        else:
            filename_bytes = b""

        lineno = self._extract_lineno(event)

        envelope = self._pack(
            event.event_type,
            event.timestamp_ns,
            event.thread_id,
            len(filename_bytes),
            lineno,
            len(payload_bytes),
        )

        rtnval = envelope + filename_bytes + payload_bytes
        return rtnval

    def _extract_filename(self, event: TraceEvent) -> str:
        """
            Extract filename from event, or empty string for events without one.

            :param event: The trace event.

            :returns: The filename string.
        """
        rtnval = getattr(event, "filename", "")
        return rtnval

    def _extract_lineno(self, event: TraceEvent) -> int:
        """
            Extract line number from event, or 0 for events without one.

            :param event: The trace event.

            :returns: The line number integer.
        """
        rtnval = getattr(event, "lineno", 0)
        return rtnval

    def _extract_payload(self, event: TraceEvent) -> Optional[dict]:
        """
            Extract the variable-length payload data for pickling.

            :param event: The trace event.

            :returns: A dict of payload data, or None for events with no payload.
        """
        event_type = event.event_type

        if event_type == EventType.CALL:
            rtnval = {
                "function_name": event.function_name,
                "args": event.args,
                "kwargs": event.kwargs,
            }
        elif event_type == EventType.RETURN:
            rtnval = {
                "function_name": event.function_name,
                "return_value": event.return_value,
            }
        elif event_type == EventType.LINE:
            rtnval = None
        elif event_type == EventType.VARIABLE_SNAPSHOT:
            rtnval = {
                "local_variables": event.local_variables,
            }
        elif event_type == EventType.EXCEPTION:
            rtnval = {
                "function_name": event.function_name,
                "exception_type": event.exception_type,
                "exception_value": event.exception_value,
                "traceback_str": event.traceback_str,
            }
        elif event_type == EventType.PORTAL_ENTER:
            rtnval = {
                "portal_name": event.portal_name,
            }
        elif event_type == EventType.PORTAL_EXIT:
            rtnval = {
                "portal_name": event.portal_name,
            }
        elif event_type == EventType.GATEWAY_START:
            rtnval = {
                "wall_clock_time": event.wall_clock_time,
            }
        elif event_type == EventType.GATEWAY_STOP:
            rtnval = {
                "wall_clock_time": event.wall_clock_time,
            }
        else:
            rtnval = None

        return rtnval


class TraceDeserializer:
    """
        Deserializes the hybrid struct+pickle binary format back into
        TraceEvent objects.

        Uses a pre-compiled ``struct.Struct`` for maximum unpacking speed.
    """

    def __init__(self) -> None:
        self._struct = struct.Struct(ENVELOPE_FORMAT)
        self._unpack = self._struct.unpack
        return

    def deserialize(self, data: bytes, offset: int = 0) -> tuple:
        """
            Deserialize one event starting at offset.

            :param data: The byte buffer containing serialized events.
            :param offset: The byte offset to start reading from.

            :returns: A tuple of (TraceEvent, next_offset).
        """
        header = self._unpack(data[offset:offset + ENVELOPE_SIZE])
        event_type, timestamp_ns, thread_id, filename_len, lineno, payload_len = header
        offset += ENVELOPE_SIZE

        if filename_len > 0:
            filename = data[offset:offset + filename_len].decode("utf-8")
        else:
            filename = ""
        offset += filename_len

        payload_data = None
        if payload_len > 0:
            payload_data = pickle.loads(data[offset:offset + payload_len])
        offset += payload_len

        event = self._reconstruct_event(
            event_type, timestamp_ns, thread_id, filename, lineno, payload_data
        )

        rtnval = (event, offset)
        return rtnval

    def read_header(self, data: bytes, offset: int = 0) -> tuple:
        """
            Read only the envelope header without deserializing the payload.

            :param data: The byte buffer containing serialized events.
            :param offset: The byte offset to start reading from.

            :returns: A tuple of (header_tuple, offset_after_header).
        """
        header = self._unpack(data[offset:offset + ENVELOPE_SIZE])
        rtnval = (header, offset + ENVELOPE_SIZE)
        return rtnval

    def skip_event(self, data: bytes, offset: int = 0) -> int:
        """
            Skip past one event, returning the offset of the next event.

            :param data: The byte buffer containing serialized events.
            :param offset: The byte offset to start reading from.

            :returns: The offset of the next event.
        """
        header = self._unpack(data[offset:offset + ENVELOPE_SIZE])
        _, _, _, filename_len, _, payload_len = header
        rtnval = offset + ENVELOPE_SIZE + filename_len + payload_len
        return rtnval

    def _reconstruct_event(self, event_type: int, timestamp_ns: int,
                           thread_id: int, filename: str, lineno: int,
                           payload_data: Optional[dict]) -> TraceEvent:
        """
            Reconstruct a TraceEvent from deserialized components.

            :param event_type: The integer event type tag.
            :param timestamp_ns: The nanosecond timestamp.
            :param thread_id: The thread identifier.
            :param filename: The source filename.
            :param lineno: The line number.
            :param payload_data: The deserialized payload dict, or None.

            :returns: The reconstructed TraceEvent subclass instance.
        """
        if event_type == EventType.CALL:
            rtnval = CallEvent(
                timestamp_ns=timestamp_ns,
                thread_id=thread_id,
                filename=filename,
                lineno=lineno,
                function_name=payload_data["function_name"],
                args=payload_data["args"],
                kwargs=payload_data["kwargs"],
            )
        elif event_type == EventType.RETURN:
            rtnval = ReturnEvent(
                timestamp_ns=timestamp_ns,
                thread_id=thread_id,
                filename=filename,
                lineno=lineno,
                function_name=payload_data["function_name"],
                return_value=payload_data["return_value"],
            )
        elif event_type == EventType.LINE:
            rtnval = LineEvent(
                timestamp_ns=timestamp_ns,
                thread_id=thread_id,
                filename=filename,
                lineno=lineno,
            )
        elif event_type == EventType.VARIABLE_SNAPSHOT:
            rtnval = VariableSnapshotEvent(
                timestamp_ns=timestamp_ns,
                thread_id=thread_id,
                filename=filename,
                lineno=lineno,
                local_variables=payload_data["local_variables"],
            )
        elif event_type == EventType.EXCEPTION:
            rtnval = ExceptionEvent(
                timestamp_ns=timestamp_ns,
                thread_id=thread_id,
                filename=filename,
                lineno=lineno,
                function_name=payload_data["function_name"],
                exception_type=payload_data["exception_type"],
                exception_value=payload_data["exception_value"],
                traceback_str=payload_data["traceback_str"],
            )
        elif event_type == EventType.PORTAL_ENTER:
            rtnval = PortalEnterEvent(
                timestamp_ns=timestamp_ns,
                thread_id=thread_id,
                portal_name=payload_data["portal_name"],
            )
        elif event_type == EventType.PORTAL_EXIT:
            rtnval = PortalExitEvent(
                timestamp_ns=timestamp_ns,
                thread_id=thread_id,
                portal_name=payload_data["portal_name"],
            )
        elif event_type == EventType.GATEWAY_START:
            rtnval = GatewayStartEvent(
                timestamp_ns=timestamp_ns,
                thread_id=thread_id,
                wall_clock_time=payload_data["wall_clock_time"],
            )
        elif event_type == EventType.GATEWAY_STOP:
            rtnval = GatewayStopEvent(
                timestamp_ns=timestamp_ns,
                thread_id=thread_id,
                wall_clock_time=payload_data["wall_clock_time"],
            )
        else:
            rtnval = TraceEvent(
                event_type=event_type,
                timestamp_ns=timestamp_ns,
                thread_id=thread_id,
            )

        return rtnval
