# 1MCP Agent Integration Guide

## Overview

The `rest-chatbot-mcp` has been enhanced to support connections to the 1MCP Agent running on `http://localhost:3051/sse`. This integration allows the chatbot to use the 1MCP Agent's tools and resources through HTTP/SSE connections.

## Changes Made

### 1. Enhanced MCP Client Support

- **HTTPMCPClient**: New class that handles HTTP/SSE connections to 1MCP Agent
- **HTTPMCPAgent**: Enhanced agent that supports both traditional MCP clients and HTTP-based clients
- **Automatic Detection**: The system automatically detects URL-based server configurations

### 2. Configuration Updates

The `mcp_config.json` now supports both traditional MCP servers and URL-based connections:

```json
{
  "mcpServers": {
    "1mcp-agent": {
      "url": "http://localhost:3051/sse",
      "headers": {},
      "description": "1MCP Agent via HTTP/SSE",
      "disabled": false
    },
    "postgres-server": {
      "command": "npx",
      "args": [
        "-y", 
        "@modelcontextprotocol/server-postgres",
        "postgresql://postgres:postgres@localhost:5432/mydb"
      ],
      "disabled": true
    }
  }
}
```

### 3. New Dependencies

Added to `requirements.txt`:
- `aiohttp>=3.8.0` - For HTTP/SSE connections

### 4. API Endpoints

The 1MCP Agent is expected to provide these endpoints:
- `GET /health` - Health check
- `GET /tools` - List available tools
- `GET /resources` - List available resources
- `POST /call_tool` - Call a specific tool
- `POST /get_resource` - Get a specific resource

## Usage

### 1. Start the 1MCP Agent

```bash
cd /workspace/db-ready/1MCP-proxy
./start-sse.sh
```

This will start the 1MCP Agent on `http://localhost:3051/sse`.

### 2. Configure the Rest-Chatbot

Ensure your `mcp_config.json` includes the 1MCP Agent configuration:

```json
{
  "mcpServers": {
    "1mcp-agent": {
      "url": "http://localhost:3051/sse",
      "headers": {},
      "disabled": false
    }
  }
}
```

### 3. Start the Rest-Chatbot

```bash
cd /workspace/db-ready/rest-chatbot-mcp
./start.sh
```

### 4. Test the Integration

Run the test script:

```bash
python3 test_1mcp_integration.py
```

## API Usage Examples

### Query with 1MCP Agent

```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "List the files in the current directory",
    "provider": "gemini",
    "max_steps": 5
  }'
```

### Check Available Tools

```bash
curl "http://localhost:8000/health"
```

## Configuration Options

### Server Configuration

- `url`: The URL of the 1MCP Agent (e.g., `http://localhost:3051/sse`)
- `headers`: Optional HTTP headers for authentication
- `disabled`: Set to `true` to disable this server

### Headers Example (if using NGINX proxy)

```json
{
  "mcpServers": {
    "1mcp-agent": {
      "url": "http://localhost:4080/sse",
      "headers": {
        "Authorization": "Bearer mcp-token-secret-2025"
      },
      "disabled": false
    }
  }
}
```

## Troubleshooting

### 1. Connection Issues

If you get connection errors:

1. Check if the 1MCP Agent is running:
   ```bash
   curl http://localhost:3051/health
   ```

2. Verify the URL in the configuration matches the running service

3. Check the logs for detailed error messages

### 2. Authentication Issues

If using the NGINX proxy with authentication:

1. Ensure the correct Bearer token is in the headers
2. Use the correct proxy URL (e.g., `http://localhost:4080/sse`)

### 3. Tools Not Available

If no tools are available:

1. Check the 1MCP Agent configuration
2. Verify the `/tools` endpoint returns data
3. Check the rest-chatbot logs for MCP client errors

## Technical Details

### HTTP MCP Client

The `HTTPMCPClient` class provides:
- Async HTTP connections using aiohttp
- Support for authentication headers
- Error handling and fallback mechanisms
- Compatible interface with the existing MCP system

### Agent Integration

The `HTTPMCPAgent` class:
- Supports both traditional MCP clients and HTTP clients
- Automatically detects the client type
- Provides fallback to LLM-only mode if MCP is unavailable
- Builds context from available tools and resources

### Backward Compatibility

The system maintains full backward compatibility with existing MCP configurations. Traditional command-based MCP servers continue to work as before.

## Performance Considerations

- HTTP connections add latency compared to direct subprocess communication
- The system uses async HTTP clients for better performance
- Connection pooling is handled by aiohttp
- Error handling includes timeouts and retry logic

## Future Enhancements

Possible future improvements:
1. Caching of tool and resource lists
2. WebSocket support for real-time updates
3. Load balancing for multiple 1MCP Agent instances
4. Enhanced error recovery mechanisms
