from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

# setp-1 : choose an MCP server & tools
"""
For the demo, we'll use the `Everything MCP Server` - an npm package `(@modelcontextprotocol/server-everything)` designed for testing MCP integrations.

It provides a 'getTinyImage' tool that returns a simple test image (16x16 pixels, Base64-encoded).
Find more servers: modelcontextprotocol.io/examples
"""
# step-2 : create the MCP toolset

mcp_image_server = McpToolset(
    connection_params= StdioConnectionParams(
        server_params=StdioServerParameters(
            command='npx',
            args=[
                '-y',
                "@modelcontextprotocol/server-everything",
            ],
            tool_filter=["getTinyImage"],
        ),
        timeout=30,
    )
)
