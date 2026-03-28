"""
    Tests for the MCP Server Tools.
"""

import json
import os
import tempfile
import unittest
import uuid

from automojo.timetravel.pod.remote.mcpserver import McpServer
from automojo.timetravel.pod.portalregistry import get_portal_registry
from automojo.timetravel.pod.traceevents import VariableSnapshotEvent
from automojo.timetravel.pod.traceserializer import TraceSerializer
from automojo.timetravel.pod.bufferedwriter import BufferedTraceWriter
from automojo.timetravel.pod.backends.filebackend import FileStreamBackend
from automojo.timetravel.pod.tracerecorder import TraceRecorder


class TestMcpServerTools(unittest.IsolatedAsyncioTestCase):
    """
        Tests for the MCP Server Tools.
    """

    def setUp(self):
        self._registry = get_portal_registry()
        self._registry.deactivate_all()
        self._server = McpServer()

    def tearDown(self):
        self._registry.deactivate_all()

    async def test_create_session(self):
        response = await self._server._server.request_context.session.call_tool("create_session", {})
        data = json.loads(response.content[0].text)
        self.assertIn("session_id", data)
        self.assertIn("session_dir", data)
        self.assertTrue(os.path.exists(data["session_dir"]))

    async def test_list_captures_empty(self):
        # Create session
        session_id = str(uuid.uuid4())
        session_dir = os.path.join(tempfile.gettempdir(), f"automojo_session_{session_id}")
        os.makedirs(session_dir, exist_ok=True)

        # We need to simulate the tools call manually since we are not running a real client
        # In McpServer, handle_call_tool is wrapped by self._server.call_tool

        # Since _server is a mcp.server.Server, testing the internal router is difficult without a client.
        # We will directly test the logic by extracting the tool handler or refactoring.
        pass
