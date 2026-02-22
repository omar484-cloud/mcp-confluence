# MCP Confluence Server
# Model Context Protocol implementation for Atlassian Confluence

A Python-based MCP (Model Context Protocol) server that enables Large Language Models to interact with Confluence spaces, pages, and content through a standardized tool interface.

## Features

- **Tool-based Interface**: Implements standardized MCP tools for Confluence operations
- **Full CRUD Operations**: Create, read, update, and delete pages and spaces
- **Advanced Search**: CQL-based search with filtering and pagination
- **Authentication**: Support for Personal Access Tokens (PAT) and OAuth2
- **Error Handling**: Comprehensive error handling and logging
- **Type Safety**: Pydantic models for request/response validation
- **Testing**: Full test coverage with mocked API calls

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```env
CONFLUENCE_URL=https://your-domain.atlassian.net
CONFLUENCE_USERNAME=your-email@example.com
CONFLUENCE_API_TOKEN=your-api-token
CONFLUENCE_DEPLOYMENT=cloud  # 'cloud' or 'server'
LOG_LEVEL=INFO
```

### Running the Server

```bash
python -m src.main
```

## Project Structure

```
mcp-confluence/
├── src/
│   ├── __init__.py
│   ├── main.py                 # Entry point
│   ├── server.py               # MCP Server implementation
│   ├── client.py               # Confluence API client
│   ├── config.py               # Configuration management
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── base.py             # Base tool class
│   │   ├── search.py           # Search tools
│   │   ├── page.py             # Page CRUD tools
│   │   ├── space.py            # Space tools
│   │   └── metadata.py         # Metadata tools
│   ├── models/
│   │   ├── __init__.py
│   │   ├── confluence.py       # Confluence data models
│   │   └── mcp.py              # MCP protocol models
│   └── utils/
│       ├── __init__.py
│       ├── logger.py           # Logging configuration
│       └── errors.py           # Custom exceptions
├── tests/
│   ├── __init__.py
│   ├── test_client.py
│   ├── test_server.py
│   ├── test_tools.py
│   └── fixtures.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Supported Tools

### Search Tools
- `search_pages`: Search for pages using CQL
- `search_spaces`: Find spaces by name or key

### Page Tools
- `get_page`: Retrieve a specific page by ID or title
- `create_page`: Create a new page in a space
- `update_page`: Update page content and metadata
- `delete_page`: Delete a page

### Space Tools
- `get_space`: Retrieve space information
- `list_spaces`: List all available spaces
- `get_space_pages`: List pages in a space

### Metadata Tools
- `get_page_history`: Get page revision history
- `get_page_attachments`: List page attachments
- `get_page_comments`: Get page comments

## API Reference

See [API_REFERENCE.md](API_REFERENCE.md) for detailed documentation on each tool and its parameters.

## Development

### Running Tests

```bash
pytest tests/ -v
```

### Running Tests with Coverage

```bash
pytest tests/ --cov=src --cov-report=html
```

## Authentication

### Cloud Deployment
1. Create a Personal Access Token: https://id.atlassian.com/manage/api-tokens
2. Add to `.env` file

### Server Deployment
1. Use your account password or generate an API token
2. Configure via `.env` file

## Error Handling

The server implements comprehensive error handling with the following error codes:
- `400`: Bad Request (invalid parameters)
- `401`: Unauthorized (invalid credentials)
- `403`: Forbidden (insufficient permissions)
- `404`: Not Found (resource doesn't exist)
- `429`: Rate Limit (too many requests)
- `500`: Internal Server Error

## License

MIT

