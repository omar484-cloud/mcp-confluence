# MCP Confluence - Usage Examples

This guide demonstrates how to use the MCP Confluence Server.

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd mcp-confluence
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp .env.example .env
# Edit .env with your Confluence credentials
```

## Running the Server

Start the MCP server:
```bash
python -m src.main
```

The server will start and listen for JSON requests on stdin.

## Making Requests

The server accepts JSON requests on stdin and returns JSON responses on stdout.

### Request Format

```json
{
  "request_id": "unique-request-id",
  "method": "call_tool",
  "params": {
    "name": "tool_name",
    "arguments": {
      "param1": "value1",
      "param2": "value2"
    }
  }
}
```

### Example 1: Search for Pages

```bash
# Send request
echo '{"request_id":"1","method":"call_tool","params":{"name":"search_pages","arguments":{"query":"space.key=DEV","limit":5}}}' | python -m src.main
```

Response:
```json
{
  "request_id": "1",
  "success": true,
  "data": {
    "success": true,
    "results": [
      {
        "id": "123",
        "title": "API Documentation",
        "type": "page",
        "space": {"key": "DEV"}
      }
    ],
    "total": 1,
    "start": 0,
    "limit": 5
  }
}
```

### Example 2: Create a Page

```bash
echo '{
  "request_id":"2",
  "method":"call_tool",
  "params":{
    "name":"create_page",
    "arguments":{
      "space_key":"DEV",
      "title":"New API Guidelines",
      "body":"<p>This page contains our API best practices</p>"
    }
  }
}' | python -m src.main
```

### Example 3: Get Page Details

```bash
echo '{
  "request_id":"3",
  "method":"call_tool",
  "params":{
    "name":"get_page",
    "arguments":{"page_id":"123"}
  }
}' | python -m src.main
```

### Example 4: List All Spaces

```bash
echo '{
  "request_id":"4",
  "method":"call_tool",
  "params":{
    "name":"list_spaces",
    "arguments":{}
  }
}' | python -m src.main
```

### Example 5: Get Server Information

```bash
echo '{
  "request_id":"5",
  "method":"get_server_info",
  "params":{}
}' | python -m src.main
```

### Example 6: List Available Tools

```bash
echo '{
  "request_id":"6",
  "method":"list_tools",
  "params":{}
}' | python -m src.main
```

## Python Integration

You can also use the server programmatically in Python:

```python
import asyncio
from src.config import Settings
from src.server import MCPConfluenceServer

async def main():
    # Load settings
    settings = Settings(
        confluence_url="https://your-domain.atlassian.net",
        confluence_username="your-email@example.com",
        confluence_api_token="your-token",
        confluence_deployment="cloud"
    )
    
    # Create server
    server = MCPConfluenceServer(settings)
    
    # Call a tool
    result = await server.call_tool(
        'search_pages',
        query='space.key=DEV',
        limit=10
    )
    
    print(result)

asyncio.run(main())
```

## Environment Configuration

The `.env` file controls server behavior:

```env
# Confluence Connection
CONFLUENCE_URL=https://your-domain.atlassian.net
CONFLUENCE_USERNAME=your-email@example.com
CONFLUENCE_API_TOKEN=your-api-token
CONFLUENCE_DEPLOYMENT=cloud  # 'cloud' or 'server'

# Logging
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL

# Request Settings
REQUEST_TIMEOUT=30
MAX_RETRIES=3
RATE_LIMIT_DELAY=1

# Optional: Proxy
HTTP_PROXY=
HTTPS_PROXY=
```

## Getting API Tokens

### Atlassian Cloud

1. Go to https://id.atlassian.com/manage/api-tokens
2. Click "Create API token"
3. Copy the generated token
4. Add to `.env` file as `CONFLUENCE_API_TOKEN`

### Confluence Server

1. Log in to your Confluence instance
2. Go to Settings > Personal Settings
3. Create or find your API token
4. Add to `.env` file as `CONFLUENCE_API_TOKEN`

## Testing

Run the test suite:

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_client.py -v

# Run specific test
pytest tests/test_client.py::test_client_initialization -v
```

## Integration with LLMs

The MCP Confluence Server is designed to work with LLM applications. Example integration:

```python
import asyncio
from src.config import get_settings
from src.server import MCPConfluenceServer

async def query_confluence(llm_request):
    settings = get_settings()
    server = MCPConfluenceServer(settings)
    
    # Get available tools for the LLM
    tools = server.list_tools()
    
    # Handle tool calls from LLM
    if llm_request.tool == "search_pages":
        result = await server.call_tool(
            'search_pages',
            **llm_request.arguments
        )
        return result
```

## Troubleshooting

### Authentication Error

**Error:** `Authentication failed (401)`

**Solution:** Check your credentials in `.env`:
- Verify `CONFLUENCE_USERNAME` is correct
- Ensure `CONFLUENCE_API_TOKEN` is valid
- Check `CONFLUENCE_URL` is correct

### Rate Limited

**Error:** `Rate limit exceeded (429)`

**Solution:** The server will automatically retry. You can adjust:
```env
RATE_LIMIT_DELAY=2
MAX_RETRIES=5
```

### Permission Denied

**Error:** `Insufficient permissions (403)`

**Solution:** Ensure your user account has permission to access the space or page.

### Page Not Found

**Error:** `Resource not found (404)`

**Solution:** Verify the page ID or space key exists.

## Performance Tips

1. **Limit results**: Always use `limit` parameter in search to reduce data transfer
2. **Pagination**: Use `start` and `limit` for large datasets
3. **Caching**: Cache frequently accessed pages at the LLM integration level
4. **Specific queries**: Use CQL to filter at the Confluence level rather than post-processing

## Security Considerations

1. **API Token**: Never commit `.env` to version control
2. **Credentials**: Use environment variables, not hardcoded values
3. **HTTPS**: Always use HTTPS URLs for Confluence
4. **Proxies**: Use proxies if needed for network security

## Next Steps

- See [API_REFERENCE.md](API_REFERENCE.md) for detailed tool documentation
- Check [README.md](README.md) for project overview
- Review test files for more usage examples

