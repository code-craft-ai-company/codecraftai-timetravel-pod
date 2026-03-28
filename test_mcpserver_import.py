import asyncio
from automojo.timetravel.pod.remote.mcpserver import McpServer

async def test_tcp():
    server = McpServer()
    server.start_background_tcp("127.0.0.1", 9998)
    await asyncio.sleep(1)

    import socket
    import json
    s = socket.socket()
    s.connect(("127.0.0.1", 9998))
    s.send(b'{"jsonrpc": "2.0", "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0"}}, "id": 1}\n')

    data = s.recv(1024)
    print("RECV", data.decode())
    s.close()
    server.stop()

if __name__ == "__main__":
    asyncio.run(test_tcp())
