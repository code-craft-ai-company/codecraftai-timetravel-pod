"""
    Tests for the MCP Server Tools.
"""

import asyncio
import json
import os

from ccai.timetravel.pod.remote.mcpserver import McpServer
from ccai.timetravel.pod.portalregistry import get_portal_registry


def _setup() -> McpServer:
    """
        Replicates the original ``setUp`` for the MCP Server Tools tests by
        acquiring the portal registry, deactivating all portals and creating a
        fresh :class:`McpServer` instance.

        :returns: A freshly constructed :class:`McpServer` instance.
    """
    registry = get_portal_registry()
    registry.deactivate_all()
    server = McpServer()

    return server


def _teardown() -> None:
    """
        Replicates the original ``tearDown`` for the MCP Server Tools tests by
        deactivating all portals in the portal registry.
    """
    registry = get_portal_registry()
    registry.deactivate_all()

    return


async def _call_tool(server: McpServer, name: str, arguments: dict) -> object:
    """
        Invokes the named MCP tool on the supplied server with the supplied
        arguments and returns the resulting content.

        :param server: The :class:`McpServer` instance to invoke the tool on.
        :param name: The name of the tool to invoke.
        :param arguments: The arguments to pass to the tool.

        :returns: The content from the tool call result.
    """
    import mcp.types as types
    handler = server._server.request_handlers[types.CallToolRequest]
    req = types.CallToolRequest(
        method="tools/call",
        params={"name": name, "arguments": arguments}
    )
    # The request_handlers[CallToolRequest] expects (request) only in recent MCP SDK versions
    res = await handler(req)
    # In newer MCP SDK, the result might be wrapped in a ServerResult which has a root
    if hasattr(res, "root"):
        rtnval = res.root.content
        return rtnval
    rtnval = res.content
    return rtnval


def test_create_session() -> None:
    """
        Verify that the ``create_session`` tool creates a session and reports
        the session id, directory and expiration.
    """
    server = _setup()
    try:
        async def _run() -> None:
            result = await _call_tool(server=server, name="create_session", arguments={})

            assert len(result) == 1
            res_data = json.loads(result[0].text if hasattr(result[0], 'text') else result[0]["text"])

            assert "session_id" in res_data
            assert "session_dir" in res_data
            assert "expires_at" in res_data

            session_id = res_data["session_id"]
            session_dir = res_data["session_dir"]

            assert os.path.exists(session_dir)
            assert session_id in server._sessions

            return

        asyncio.run(_run())
    finally:
        _teardown()

    return


def test_renew_session() -> None:
    """
        Verify that the ``renew_session`` tool extends the expiration of an
        existing session.
    """
    server = _setup()
    try:
        async def _run() -> None:
            res1 = await _call_tool(server=server, name="create_session", arguments={"timespan": 10})
            data1 = json.loads(res1[0].text if hasattr(res1[0], 'text') else res1[0]["text"])
            session_id = data1["session_id"]
            expires1 = data1["expires_at"]

            # Renew session
            res2 = await _call_tool(server=server, name="renew_session", arguments={"session_id": session_id, "timespan": 60})
            data2 = json.loads(res2[0].text if hasattr(res2[0], 'text') else res2[0]["text"])
            expires2 = data2["expires_at"]

            assert expires2 > expires1
            assert server._sessions[session_id]["expires_at"] == expires2

            return

        asyncio.run(_run())
    finally:
        _teardown()

    return


def test_close_session() -> None:
    """
        Verify that the ``close_session`` tool closes a session, removes its
        directory and drops it from the server session table.
    """
    server = _setup()
    try:
        async def _run() -> None:
            res1 = await _call_tool(server=server, name="create_session", arguments={"timespan": 10})
            data1 = json.loads(res1[0].text if hasattr(res1[0], 'text') else res1[0]["text"])
            session_id = data1["session_id"]
            session_dir = data1["session_dir"]

            assert os.path.exists(session_dir)
            assert session_id in server._sessions

            # Close session
            res2 = await _call_tool(server=server, name="close_session", arguments={"session_id": session_id})
            data2 = json.loads(res2[0].text if hasattr(res2[0], 'text') else res2[0]["text"])

            assert data2["status"] == "closed"
            assert not os.path.exists(session_dir)
            assert session_id not in server._sessions

            return

        asyncio.run(_run())
    finally:
        _teardown()

    return


def test_list_captures_empty() -> None:
    """
        Verify that the ``list_captures`` tool reports an empty capture list
        for a freshly created session.
    """
    server = _setup()
    try:
        async def _run() -> None:
            res1 = await _call_tool(server=server, name="create_session", arguments={})
            data1 = json.loads(res1[0].text if hasattr(res1[0], 'text') else res1[0]["text"])
            session_id = data1["session_id"]

            res2 = await _call_tool(server=server, name="list_captures", arguments={"session_id": session_id})
            data2 = json.loads(res2[0].text if hasattr(res2[0], 'text') else res2[0]["text"])
            assert data2["captures"] == []

            return

        asyncio.run(_run())
    finally:
        _teardown()

    return
