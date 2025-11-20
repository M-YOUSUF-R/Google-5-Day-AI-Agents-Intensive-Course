# Agent with MCP server

## What is MCP Server:

Model Context Protocol (MCP) is an open standard that lets agents use community-built integrations. Instead of writing your own integrations and API clients, just connect to an existing MCP server.

MCP enables agents to:

- Access live, external data from databases, APIs, and services without custom integration code
- Leverage community-built tools with standardized interfaces
- Scale capabilities by connecting to multiple specialized servers

## How MCP Works:

MCP connects the agent (the client) to external MCP servers that provide tools:

- MCP Server: Provides specific tools (like image generation, database access)
- MCP Client: Your agent that uses those tools
- All servers work the same way - standardized interface

### Architecture:

```
┌──────────────────┐
│       Agent      │
│   (MCP Client)   │
└────────┬─────────┘
         │
         │ Standard MCP Protocol
         │
    ┌────┴────┬────────┬────────┐
    │         │        │        │
    ▼         ▼        ▼        ▼
┌────────┐ ┌─────┐ ┌──────┐ ┌─────┐
│ GitHub │ │Slack│ │ Maps │ │ ... │
│ Server │ │ MCP │ │ MCP  │ │     │
└────────┘ └─────┘ └──────┘ └─────┘
```

### using MCP with Agent:

1. Choose an MCP server
2. Create the MCP toolset (configure connection)
3. Add it with Agent
4. Run & test the agent
