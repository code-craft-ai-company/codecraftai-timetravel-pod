"""
    Provides an MCP (Model Context Protocol) server for time travel pod management.

    This module contains the :class:`McpServer` which runs an MCP server, exposing
    tools that allow an agent to live debug Python applications by activating
    and deactivating time travel portals.
"""

import asyncio
import logging
import threading

from typing import Any, Optional

import mcp.server.stdio
from mcp.server import Server

import os
import tempfile
import uuid
import glob
import json

from automojo.timetravel.pod.portalregistry import get_portal_registry
from automojo.timetravel.pod.reader import TraceFileReader
from automojo.timetravel.pod.timeline import TimelineBuilder


logger = logging.getLogger(__name__)


class McpServer:
    """
        MCP Server for remote portal management via the Model Context Protocol.

        Exposes tools: list_portals, activate_portal, deactivate_portal.
    """

    def __init__(self, name: str = "timetravel-pod") -> None:
        """
            Create an McpServer.

            :param name: The name of the MCP server.
        """
        self._name = name
        self._server = Server(name)
        self._setup_tools()
        self._thread: Optional[threading.Thread] = None
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._running = False
        return

    def _setup_tools(self) -> None:
        """
            Setup the MCP tools exposed by this server.
        """
        @self._server.list_tools()
        async def handle_list_tools() -> list:
            return [
                {
                    "name": "create_session",
                    "description": "Create a new time travel session. Returns a session ID and creates a temporary directory for captures.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {}
                    }
                },
                {
                    "name": "list_captures",
                    "description": "List all captures within a given session.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "session_id": {
                                "type": "string",
                                "description": "The session ID."
                            }
                        },
                        "required": ["session_id"]
                    }
                },
                {
                    "name": "query_capture",
                    "description": "Query variables and states from a captured time travel trace.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "session_id": {
                                "type": "string",
                                "description": "The session ID."
                            },
                            "capture_id": {
                                "type": "string",
                                "description": "The capture ID."
                            },
                            "line_number": {
                                "type": "integer",
                                "description": "Optional line number to query state at."
                            },
                            "variable_name": {
                                "type": "string",
                                "description": "Optional variable name to query."
                            }
                        },
                        "required": ["session_id", "capture_id"]
                    }
                },
                {
                    "name": "list_portals",
                    "description": "List all registered time travel portals and their activation state.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {}
                    }
                },
                {
                    "name": "activate_portal",
                    "description": "Activate a time travel portal by name.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "The name of the portal to activate."
                            },
                            "expression": {
                                "type": "string",
                                "description": "Optional Python expression evaluated against the portal's locals to conditionally activate tracing."
                            },
                            "once": {
                                "type": "boolean",
                                "description": "If true, deactivate the portal immediately after a single trace activation."
                            },
                            "capture_id": {
                                "type": "string",
                                "description": "Optional unique ID for the capture. If not provided, a random UUID will be generated."
                            },
                            "session_id": {
                                "type": "string",
                                "description": "Optional session ID for the capture. If provided, the capture will be stored in the session directory."
                            }
                        },
                        "required": ["name"]
                    }
                },
                {
                    "name": "deactivate_portal",
                    "description": "Deactivate a time travel portal by name.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "The name of the portal to deactivate."
                            }
                        },
                        "required": ["name"]
                    }
                }
            ]

        @self._server.call_tool()
        async def handle_call_tool(name: str, arguments: dict) -> list:
            if name == "create_session":
                session_id = str(uuid.uuid4())
                session_dir = os.path.join(tempfile.gettempdir(), f"automojo_session_{session_id}")
                os.makedirs(session_dir, exist_ok=True)
                return [{"type": "text", "text": json.dumps({"session_id": session_id, "session_dir": session_dir})}]
            elif name == "list_captures":
                session_id = arguments.get("session_id")
                if not session_id:
                    raise ValueError("Missing 'session_id' argument")
                session_dir = os.path.join(tempfile.gettempdir(), f"automojo_session_{session_id}")
                if not os.path.exists(session_dir):
                    raise ValueError(f"Session directory not found: {session_dir}")
                captures = [os.path.basename(f) for f in glob.glob(os.path.join(session_dir, "*.bin"))]
                return [{"type": "text", "text": json.dumps({"captures": captures})}]
            elif name == "query_capture":
                session_id = arguments.get("session_id")
                capture_id = arguments.get("capture_id")
                line_number = arguments.get("line_number")
                variable_name = arguments.get("variable_name")

                if not session_id or not capture_id:
                    raise ValueError("Missing 'session_id' or 'capture_id' argument")

                if not capture_id.endswith(".bin"):
                    capture_id += ".bin"

                session_dir = os.path.join(tempfile.gettempdir(), f"automojo_session_{session_id}")
                capture_path = os.path.join(session_dir, capture_id)

                if not os.path.exists(capture_path):
                    raise ValueError(f"Capture file not found: {capture_path}")

                builder = TimelineBuilder()
                with TraceFileReader(capture_path) as reader:
                    builder.add_events(reader.read_events())

                timeline = builder.build()
                results = []

                # Find VariableSnapshot events
                from automojo.timetravel.pod.traceevents import VariableSnapshotEvent
                for event in timeline:
                    if isinstance(event, VariableSnapshotEvent):
                        if line_number is not None and event.lineno != line_number:
                            continue

                        locals_dict = event.local_variables
                        if variable_name is not None:
                            if variable_name in locals_dict:
                                results.append({
                                    "timestamp_ns": event.timestamp_ns,
                                    "filename": event.filename,
                                    "lineno": event.lineno,
                                    "variable": variable_name,
                                    "value": locals_dict[variable_name]
                                })
                        else:
                            results.append({
                                "timestamp_ns": event.timestamp_ns,
                                "filename": event.filename,
                                "lineno": event.lineno,
                                "variables": locals_dict
                            })

                return [{"type": "text", "text": json.dumps({"results": results})}]
            elif name == "list_portals":
                registry = get_portal_registry()
                portals = registry.list_portals()
                return [{"type": "text", "text": str(portals)}]
            elif name == "activate_portal":
                portal_name = arguments.get("name")
                if not portal_name:
                    raise ValueError("Missing 'name' argument")
                expression = arguments.get("expression")
                once = arguments.get("once", False)
                capture_id = arguments.get("capture_id")
                session_id = arguments.get("session_id")

                if session_id:
                    if not capture_id:
                        capture_id = str(uuid.uuid4())

                    if not capture_id.endswith(".bin"):
                        capture_id += ".bin"

                    session_dir = os.path.join(tempfile.gettempdir(), f"automojo_session_{session_id}")
                    if not os.path.exists(session_dir):
                        os.makedirs(session_dir, exist_ok=True)

                    capture_path = os.path.join(session_dir, capture_id)
                    capture_id = f"file://{capture_path}"

                registry = get_portal_registry()
                registry.activate_portal(portal_name, expression=expression, once=once, capture_id=capture_id)
                return [{"type": "text", "text": f"Activated portal: {portal_name} with capture_id: {capture_id}"}]
            elif name == "deactivate_portal":
                portal_name = arguments.get("name")
                if not portal_name:
                    raise ValueError("Missing 'name' argument")
                registry = get_portal_registry()
                registry.deactivate_portal(portal_name)
                return [{"type": "text", "text": f"Deactivated portal: {portal_name}"}]
            else:
                raise ValueError(f"Unknown tool: {name}")

        return

    def start_stdio(self) -> None:
        """
            Start the MCP server using standard I/O streams.
            This is a blocking call.
        """
        async def _run() -> None:
            async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
                await self._server.run(
                    read_stream,
                    write_stream,
                    self._server.create_initialization_options()
                )

        asyncio.run(_run())
        return

    def start_background_stdio(self) -> None:
        """
            Start the MCP server on a background thread using standard I/O streams.
        """
        self._running = True

        def _target() -> None:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            try:
                self._loop.run_until_complete(self._run_server())
            except Exception as e:
                logger.error("MCP Server error: %s", e)
            finally:
                self._loop.close()

        self._thread = threading.Thread(target=_target, daemon=True)
        self._thread.start()
        return

    async def _run_server(self) -> None:
        """
            Internal coroutine to run the MCP stdio server.
        """
        import sys

        # Save standard streams to restore them later if needed
        original_stdout = sys.stdout
        original_stdin = sys.stdin

        # Provide dup file descriptors to avoid closing sys.stdin/stdout when TextIOWrapper is garbage collected
        import os
        from io import TextIOWrapper
        import anyio

        fd_in = os.dup(sys.stdin.fileno())
        fd_out = os.dup(sys.stdout.fileno())

        stdin_stream = anyio.wrap_file(TextIOWrapper(open(fd_in, 'rb', buffering=0), encoding="utf-8"))
        stdout_stream = anyio.wrap_file(TextIOWrapper(open(fd_out, 'wb', buffering=0), encoding="utf-8"))

        try:
            async with mcp.server.stdio.stdio_server(stdin_stream, stdout_stream) as (read_stream, write_stream):
                # We would run this, but we need a way to stop it cleanly if requested
                # Since stdio_server blocks and consumes stdin, it usually runs until EOF
                await self._server.run(
                    read_stream,
                    write_stream,
                    self._server.create_initialization_options()
                )
        finally:
            # Reassign original stdout/stdin, preventing it from remaining closed in the main thread
            sys.stdout = original_stdout
            sys.stdin = original_stdin

        return

    def start_background_tcp(self, host: str, port: int) -> None:
        """
            Start the MCP server on a background thread using a TCP socket.
        """
        self._running = True

        def _target() -> None:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            try:
                self._loop.run_until_complete(self._run_tcp_server(host, port))
            except Exception as e:
                logger.error("MCP Server TCP error: %s", e)
            finally:
                self._loop.close()

        self._thread = threading.Thread(target=_target, daemon=True)
        self._thread.start()
        return

    async def _run_tcp_server(self, host: str, port: int) -> None:
        """
            Internal coroutine to run the MCP server over a TCP socket.
        """
        import anyio
        from anyio.streams.memory import MemoryObjectReceiveStream, MemoryObjectSendStream
        import json
        import mcp.types as types
        from mcp.shared.message import SessionMessage

        async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
            producer_read, consumer_read = anyio.create_memory_object_stream(100)
            producer_write, consumer_write = anyio.create_memory_object_stream(100)

            async def _read_from_socket():
                try:
                    while True:
                        line = await reader.readline()
                        if not line:
                            break
                        try:
                            msg = json.loads(line.decode('utf-8'))
                            parsed_msg = types.JSONRPCMessage.model_validate(msg)
                            await producer_read.send(
                                SessionMessage(message=parsed_msg, metadata=None)
                            )
                        except json.JSONDecodeError:
                            continue
                except anyio.ClosedResourceError:
                    pass
                finally:
                    producer_read.close()

            async def _write_to_socket():
                try:
                    async with consumer_write:
                        async for msg in consumer_write:
                            # msg is a SessionMessage, we want to write msg.message
                            msg_inner = getattr(msg, "message", msg)
                            if hasattr(msg_inner, "model_dump"):
                                data = msg_inner.model_dump(by_alias=True, exclude_none=True)
                                writer.write((json.dumps(data) + "\n").encode('utf-8'))
                            else:
                                writer.write((json.dumps(msg_inner) + "\n").encode('utf-8'))
                            await writer.drain()
                finally:
                    writer.close()
                    await writer.wait_closed()

            read_task = asyncio.create_task(_read_from_socket())
            write_task = asyncio.create_task(_write_to_socket())

            try:
                await self._server.run(
                    consumer_read,
                    producer_write,
                    self._server.create_initialization_options()
                )
            except Exception as e:
                logger.error("Error in TCP client: %s", e)
            finally:
                read_task.cancel()
                write_task.cancel()
                writer.close()
                await writer.wait_closed()

        server = await asyncio.start_server(handle_client, host, port)
        async with server:
            await server.serve_forever()

    def start_background_pipe(self, pipe_name: str) -> None:
        """
            Start the MCP server on a background thread using a named pipe / Unix domain socket.
        """
        self._running = True

        def _target() -> None:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            try:
                self._loop.run_until_complete(self._run_pipe_server(pipe_name))
            except Exception as e:
                logger.error("MCP Server Pipe error: %s", e)
            finally:
                self._loop.close()

        self._thread = threading.Thread(target=_target, daemon=True)
        self._thread.start()
        return

    async def _run_pipe_server(self, pipe_name: str) -> None:
        """
            Internal coroutine to run the MCP server over a named pipe / Unix domain socket.
        """
        import os
        import anyio
        import json
        import mcp.types as types
        from mcp.shared.message import SessionMessage

        # Ensure the socket is removed if it already exists
        if os.path.exists(pipe_name):
            try:
                os.remove(pipe_name)
            except OSError:
                pass

        async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
            producer_read, consumer_read = anyio.create_memory_object_stream(100)
            producer_write, consumer_write = anyio.create_memory_object_stream(100)

            async def _read_from_socket():
                try:
                    while True:
                        line = await reader.readline()
                        if not line:
                            break
                        try:
                            msg = json.loads(line.decode('utf-8'))
                            parsed_msg = types.JSONRPCMessage.model_validate(msg)
                            await producer_read.send(
                                SessionMessage(message=parsed_msg, metadata=None)
                            )
                        except json.JSONDecodeError:
                            continue
                except anyio.ClosedResourceError:
                    pass
                finally:
                    producer_read.close()

            async def _write_to_socket():
                try:
                    async with consumer_write:
                        async for msg in consumer_write:
                            msg_inner = getattr(msg, "message", msg)
                            if hasattr(msg_inner, "model_dump"):
                                data = msg_inner.model_dump(by_alias=True, exclude_none=True)
                                writer.write((json.dumps(data) + "\n").encode('utf-8'))
                            else:
                                writer.write((json.dumps(msg_inner) + "\n").encode('utf-8'))
                            await writer.drain()
                finally:
                    writer.close()
                    await writer.wait_closed()

            read_task = asyncio.create_task(_read_from_socket())
            write_task = asyncio.create_task(_write_to_socket())

            try:
                await self._server.run(
                    consumer_read,
                    producer_write,
                    self._server.create_initialization_options()
                )
            except Exception as e:
                logger.error("Error in Pipe client: %s", e)
            finally:
                read_task.cancel()
                write_task.cancel()
                writer.close()
                await writer.wait_closed()

        if not hasattr(asyncio, "start_unix_server"):
            raise NotImplementedError("Named pipes / Unix domain sockets are not supported on this platform.")

        server = await asyncio.start_unix_server(handle_client, path=pipe_name)
        async with server:
            await server.serve_forever()

    def stop(self) -> None:
        """
            Stop the background MCP server if running.
        """
        if self._running and self._loop is not None:
            self._running = False
            # Can't easily cancel stdin reading without closing stdin, but we signal
            # the thread to exit if it can.
            pass
        if self._thread is not None:
            # wait a short period since this blocks on standard in.
            self._thread.join(timeout=0.1)
            self._thread = None
        return
