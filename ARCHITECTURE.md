# Architecture & Design

This document describes the architecture and design decisions of the MCP Confluence Server.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    LLM / Client Application                  │
└────────────────────────────┬────────────────────────────────┘
                             │
                    JSON-RPC/MCP Protocol
                             │
┌────────────────────────────▼────────────────────────────────┐
│              MCP Confluence Server (main.py)                 │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            MCPConfluenceServer                       │  │
│  │  - Tool Registry                                     │  │
│  │  - Request Handler                                  │  │
│  │  - Response Builder                                 │  │
│  └────────────────┬─────────────────────────────────────┘  │
│                   │                                          │
│  ┌────────────────▼─────────────────────────────────────┐  │
│  │              Tool Layer                              │  │
│  │  ┌───────────────────────────────────────────────┐   │  │
│  │  │ Search Tools      Page Tools     Space Tools  │   │  │
│  │  │ - search_pages    - get_page     - get_space │   │  │
│  │  │ - search_spaces   - create_page  - list_*    │   │  │
│  │  │                   - update_page              │   │  │
│  │  │                   - delete_page              │   │  │
│  │  │                                              │   │  │
│  │  │ Metadata Tools                               │   │  │
│  │  │ - get_page_history                           │   │  │
│  │  │ - get_page_attachments                       │   │  │
│  │  │ - get_page_comments                          │   │  │
│  │  └───────────────────────────────────────────────┘   │  │
│  └────────────────┬─────────────────────────────────────┘  │
│                   │                                          │
│  ┌────────────────▼─────────────────────────────────────┐  │
│  │          ConfluenceClient Layer                       │  │
│  │  - HTTP Session Management                           │  │
│  │  - Request Building & Validation                     │  │
│  │  - Response Parsing & Error Handling                 │  │
│  │  - Retry Logic & Rate Limiting                       │  │
│  └────────────────┬─────────────────────────────────────┘  │
│                   │                                          │
│  ┌────────────────▼─────────────────────────────────────┐  │
│  │           Supporting Modules                          │  │
│  │  - config.py    (Settings & Configuration)           │  │
│  │  - models/      (Data Models & Type Safety)          │  │
│  │  - utils/       (Logging, Error Handling)            │  │
│  └────────────────┬─────────────────────────────────────┘  │
│                   │                                          │
└───────────────────┼──────────────────────────────────────────┘
                    │
                   HTTP/REST (with Basic Auth)
                    │
         ┌──────────▼───────────┐
         │ Confluence REST API   │
         │  (Cloud or Server)    │
         └──────────────────────┘
```

## Layer Breakdown

### 1. Presentation Layer (Server)
**File:** `src/server.py`

Responsibilities:
- Handle MCP protocol requests
- Manage tool registry
- Coordinate tool execution
- Format responses

Key class: `MCPConfluenceServer`

### 2. Tool Layer
**Directory:** `src/tools/`

Responsibilities:
- Define tool interface via `BaseTool`
- Implement specific tool functionality
- Parameter validation
- Tool discovery

Tool Organization:
- `search.py` - Search tools
- `page.py` - Page CRUD operations
- `space.py` - Space operations
- `metadata.py` - Metadata retrieval

### 3. Client Layer
**File:** `src/client.py`

Responsibilities:
- Confluence REST API communication
- Authentication handling
- Request/response processing
- Error handling and retry logic
- Rate limit management

Key class: `ConfluenceClient`

### 4. Configuration Layer
**File:** `src/config.py`

Responsibilities:
- Load and validate settings
- Environment variable handling
- Default value management
- Configuration validation

### 5. Data Models
**Directory:** `src/models/`

Responsibilities:
- Define data structures
- Type safety with Pydantic
- Serialization/deserialization

Models:
- `confluence.py` - Confluence domain models
- `mcp.py` - MCP protocol models

### 6. Utilities
**Directory:** `src/utils/`

Responsibilities:
- Logging configuration
- Custom exception definitions
- Shared utilities

## Design Patterns

### 1. Tool Factory Pattern
Tools are registered dynamically with a common interface:

```python
class BaseTool(ABC):
    @abstractmethod
    async def execute(self, **kwargs):
        pass

class SpecificTool(BaseTool):
    async def execute(self, **kwargs):
        # Implementation
```

### 2. Dependency Injection
`ConfluenceClient` is injected into tools:

```python
tool = SearchPagesTool(client)
result = await tool.execute(query="...")
```

### 3. Error Handling Strategy
Specific exception hierarchy for better error handling:

```python
ConfluenceError (base)
├── AuthenticationError (401)
├── AuthorizationError (403)
├── NotFoundError (404)
├── BadRequestError (400)
├── RateLimitError (429)
└── ConfluenceServerError (500)
```

### 4. Configuration Management
Pydantic settings for type-safe configuration:

```python
class Settings(BaseSettings):
    confluence_url: str
    confluence_api_token: str
    # ... validated automatically
```

### 5. Async/Await Pattern
All tool execution is async for scalability:

```python
result = await server.call_tool('search_pages', ...)
```

## Data Flow

### Request Processing Flow

```
1. MCP Request (JSON)
   ↓
2. MCPConfluenceServer.handle_request()
   ↓
3. Route to appropriate handler:
   - list_tools() → Return tool definitions
   - call_tool(name, args) → Execute tool
   - get_server_info() → Return server info
   ↓
4. Tool.execute() with parameters
   ↓
5. ConfluenceClient API calls
   ↓
6. HTTP request to Confluence REST API
   ↓
7. Parse & validate response
   ↓
8. Return formatted result to Tool
   ↓
9. Tool returns result
   ↓
10. MCPConfluenceServer formats MCP response
    ↓
11. Return JSON response
```

## API Integration Points

### Authentication
- HTTP Basic Auth (username + API token)
- Applied to all Confluence REST API calls
- Token stored in environment variable

### Confluence API Endpoints Used

**Cloud Deployment:**
```
Base: /rest/api/3
GET /content/search
GET /content/{id}
POST /content
PUT /content/{id}
DELETE /content/{id}
GET /spaces
GET /spaces/{key}
```

**Server Deployment:**
```
Base: /wiki/rest/api
(Same endpoints as Cloud)
```

## Scalability Considerations

### Horizontal Scaling
- Stateless design allows multiple instances
- Use load balancer to distribute requests
- Each instance has independent Confluence client

### Rate Limiting
- Automatic retry with exponential backoff
- Configurable delay and max retries
- Respects Confluence rate limit headers

### Caching Strategy
- Could be added at tool level
- Could be added at client level
- LRU cache for frequently accessed pages

## Security Architecture

### Authentication Flow
```
1. Load credentials from .env
2. Create HTTPBasicAuth with username + token
3. Attach to all requests
4. Confluence validates credentials
5. Continue or return 401/403
```

### Secrets Management
- Environment variables for sensitive data
- .env file (git ignored)
- Support for external secret managers

### Error Handling
- No credential leaking in error messages
- Generic error messages to clients
- Detailed logging for debugging

## Extension Points

### Adding New Tools
1. Create class inheriting from `BaseTool`
2. Implement required properties and methods
3. Add to tool registry in `MCPConfluenceServer`

### Custom API Calls
1. Extend `ConfluenceClient` methods
2. Use existing `_request_with_retry`
3. Handle errors appropriately

### Custom Configuration
1. Extend `Settings` class
2. Add environment variables
3. Use in client/server initialization

## Performance Optimization

### Response Time Optimization
- Use limit parameter in searches
- Implement pagination
- Cache results if applicable

### Memory Optimization
- Stream large responses
- Clear unused objects
- Use generators for large datasets

### Network Optimization
- Use expand parameter selectively
- Batch requests where possible
- Compress large payloads

## Testing Strategy

### Unit Tests
- Test individual tool execution
- Mock Confluence client
- Verify error handling

### Integration Tests
- Test with mocked API responses
- Test error scenarios
- Test edge cases

### Test Organization
```
tests/
├── test_client.py      - Client functionality
├── test_server.py      - Server functionality
├── test_tools.py       - Tool execution
└── fixtures.py         - Shared test data
```

## Dependencies

### Core Dependencies
- `requests` - HTTP client
- `pydantic` - Data validation
- `python-dotenv` - Environment config

### Development Dependencies
- `pytest` - Testing framework
- `pytest-asyncio` - Async test support
- `pytest-mock` - Mocking utilities

## Future Enhancements

1. **Caching Layer**
   - Redis for distributed caching
   - LRU cache for memory-based caching

2. **Metrics & Monitoring**
   - Prometheus integration
   - Performance tracking
   - Error rate monitoring

3. **Advanced Features**
   - Batch operations
   - Webhooks support
   - Custom filters
   - Full-text search enhancements

4. **Multi-Confluence Support**
   - Support multiple instances
   - Instance switching
   - Cross-instance queries

5. **Plugin System**
   - External tool plugins
   - Custom tool loading
   - Dynamic registration

## Conclusion

The architecture is designed to be:
- **Modular**: Clear separation of concerns
- **Extensible**: Easy to add new tools and features
- **Testable**: Well-defined interfaces and dependencies
- **Maintainable**: Clear code organization and patterns
- **Scalable**: Stateless design supports horizontal scaling
- **Secure**: Proper error handling and secrets management

