"""
    Tests for the MCP Server Tools.
"""

import json
import os
import tempfile
import unittest
import uuid

from ccai.timetravel.pod.remote.mcpserver import McpServer
from ccai.timetravel.pod.portalregistry import get_portal_registry
from ccai.timetravel.pod.traceevents import VariableSnapshotEvent
from ccai.timetravel.pod.traceserializer import TraceSerializer
from ccai.timetravel.pod.bufferedwriter import BufferedTraceWriter
from ccai.timetravel.pod.backends.filebackend import FileStreamBackend
from ccai.timetravel.pod.tracerecorder import TraceRecorder


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

    async def _call_tool(self, name: str, arguments: dict):
        import mcp.types as types
        handler = self._server._server.request_handlers[types.CallToolRequest]
        req = types.CallToolRequest(
            method="tools/call",
            params={"name": name, "arguments": arguments}
        )
        # The request_handlers[CallToolRequest] expects (request) only in recent MCP SDK versions
        res = await handler(req)
        # In newer MCP SDK, the result might be wrapped in a ServerResult which has a root
        if hasattr(res, "root"):
            return res.root.content
        return res.content

    async def test_create_session(self):
        result = await self._call_tool("create_session", {})

        self.assertEqual(len(result), 1)
        res_data = json.loads(result[0].text if hasattr(result[0], 'text') else result[0]["text"])

        self.assertIn("session_id", res_data)
        self.assertIn("session_dir", res_data)
        self.assertIn("expires_at", res_data)

        session_id = res_data["session_id"]
        session_dir = res_data["session_dir"]

        self.assertTrue(os.path.exists(session_dir))
        self.assertIn(session_id, self._server._sessions)

    async def test_renew_session(self):
        res1 = await self._call_tool("create_session", {"timespan": 10})
        data1 = json.loads(res1[0].text if hasattr(res1[0], 'text') else res1[0]["text"])
        session_id = data1["session_id"]
        expires1 = data1["expires_at"]

        # Renew session
        res2 = await self._call_tool("renew_session", {"session_id": session_id, "timespan": 60})
        data2 = json.loads(res2[0].text if hasattr(res2[0], 'text') else res2[0]["text"])
        expires2 = data2["expires_at"]

        self.assertGreater(expires2, expires1)
        self.assertEqual(self._server._sessions[session_id]["expires_at"], expires2)

    async def test_close_session(self):
        res1 = await self._call_tool("create_session", {"timespan": 10})
        data1 = json.loads(res1[0].text if hasattr(res1[0], 'text') else res1[0]["text"])
        session_id = data1["session_id"]
        session_dir = data1["session_dir"]

        self.assertTrue(os.path.exists(session_dir))
        self.assertIn(session_id, self._server._sessions)

        # Close session
        res2 = await self._call_tool("close_session", {"session_id": session_id})
        data2 = json.loads(res2[0].text if hasattr(res2[0], 'text') else res2[0]["text"])

        self.assertEqual(data2["status"], "closed")
        self.assertFalse(os.path.exists(session_dir))
        self.assertNotIn(session_id, self._server._sessions)

    async def test_list_captures_empty(self):
        res1 = await self._call_tool("create_session", {})
        data1 = json.loads(res1[0].text if hasattr(res1[0], 'text') else res1[0]["text"])
        session_id = data1["session_id"]

        res2 = await self._call_tool("list_captures", {"session_id": session_id})
        data2 = json.loads(res2[0].text if hasattr(res2[0], 'text') else res2[0]["text"])
        self.assertEqual(data2["captures"], [])
