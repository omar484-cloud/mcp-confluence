# MCP Confluence - API Reference

## Overview

This document provides detailed information about all available tools in the MCP Confluence Server.

## Tools

### Search Tools

#### `search_pages`

Search for pages in Confluence using CQL (Confluence Query Language).

**Parameters:**
- `query` (string, required): CQL query string
  - Examples: `title~"API"`, `space.key=DEV`, `author=admin`
- `limit` (integer, optional): Maximum results (1-100, default: 25)
- `start` (integer, optional): Pagination start (default: 0)

**Response:**
```json
{
  "success": true,
  "results": [
    {
      "id": "123",
      "type": "page",
      "title": "API Documentation",
      "space": {"key": "DEV"},
      "url": "..."
    }
  ],
  "total": 42,
  "start": 0,
  "limit": 25
}
```

**Example:**
```json
{
  "method": "call_tool",
  "params": {
    "name": "search_pages",
    "arguments": {
      "query": "title~\"API\" AND space.key=DEV",
      "limit": 10
    }
  }
}
```

---

#### `search_spaces`

Search for spaces in Confluence.

**Parameters:**
- `limit` (integer, optional): Maximum results (default: 25)
- `start` (integer, optional): Pagination start (default: 0)

**Response:**
```json
{
  "success": true,
  "spaces": [
    {
      "key": "DEV",
      "name": "Development",
      "type": "global",
      "status": "current"
    }
  ],
  "total": 5,
  "start": 0,
  "limit": 25
}
```

---

### Page Tools

#### `get_page`

Retrieve a specific page by its ID.

**Parameters:**
- `page_id` (string, required): The page ID

**Response:**
```json
{
  "success": true,
  "page": {
    "id": "123",
    "type": "page",
    "title": "Sample Page",
    "space": {"key": "DEV"},
    "status": "current",
    "body": {
      "storage": {
        "value": "<p>Page content...</p>"
      }
    },
    "version": {"number": 2},
    "url": "https://..."
  }
}
```

---

#### `create_page`

Create a new page in a Confluence space.

**Parameters:**
- `space_key` (string, required): The space key where page will be created
- `title` (string, required): Page title
- `body` (string, required): Page body content (in storage format - Wiki markup or HTML)
- `parent_id` (string, optional): Parent page ID (for child pages)

**Response:**
```json
{
  "success": true,
  "page_id": "456",
  "page": {
    "id": "456",
    "type": "page",
    "title": "New Page",
    "space": {"key": "DEV"},
    "status": "current"
  }
}
```

**Example:**
```json
{
  "method": "call_tool",
  "params": {
    "name": "create_page",
    "arguments": {
      "space_key": "DEV",
      "title": "API Guidelines",
      "body": "<p>These are our API guidelines...</p>"
    }
  }
}
```

---

#### `update_page`

Update the content and title of an existing page.

**Parameters:**
- `page_id` (string, required): The page ID
- `title` (string, required): New page title
- `body` (string, required): New page body content
- `version_number` (integer, optional): Current version number (auto-fetched if not provided)

**Response:**
```json
{
  "success": true,
  "page": {
    "id": "123",
    "title": "Updated Title",
    "version": {"number": 3}
  }
}
```

---

#### `delete_page`

Delete a page from Confluence.

**Parameters:**
- `page_id` (string, required): The page ID to delete

**Response:**
```json
{
  "success": true,
  "message": "Page 123 deleted successfully"
}
```

---

### Space Tools

#### `get_space`

Get information about a specific Confluence space.

**Parameters:**
- `space_key` (string, required): The space key

**Response:**
```json
{
  "success": true,
  "space": {
    "key": "DEV",
    "name": "Development",
    "type": "global",
    "status": "current",
    "description": "Development space for...",
    "url": "https://..."
  }
}
```

---

#### `list_spaces`

List all available Confluence spaces.

**Parameters:**
- `limit` (integer, optional): Maximum results (default: 25)
- `start` (integer, optional): Pagination start (default: 0)

**Response:**
```json
{
  "success": true,
  "spaces": [
    {
      "key": "DEV",
      "name": "Development",
      "type": "global"
    },
    {
      "key": "PROD",
      "name": "Production",
      "type": "global"
    }
  ],
  "total": 2,
  "start": 0,
  "limit": 25
}
```

---

#### `get_space_pages`

List all pages in a specific space.

**Parameters:**
- `space_key` (string, required): The space key
- `limit` (integer, optional): Maximum results (default: 25)
- `start` (integer, optional): Pagination start (default: 0)

**Response:**
```json
{
  "success": true,
  "pages": [
    {
      "id": "123",
      "type": "page",
      "title": "Page 1",
      "space": {"key": "DEV"}
    }
  ],
  "total": 15,
  "start": 0,
  "limit": 25
}
```

---

### Metadata Tools

#### `get_page_history`

Get the revision history of a page.

**Parameters:**
- `page_id` (string, required): The page ID
- `limit` (integer, optional): Maximum versions (default: 10)

**Response:**
```json
{
  "success": true,
  "versions": [
    {
      "number": 3,
      "by": {
        "displayName": "John Doe",
        "accountId": "user123"
      },
      "when": "2026-02-22T10:00:00Z",
      "message": "Updated API docs"
    }
  ],
  "total": 3
}
```

---

#### `get_page_attachments`

Get all attachments on a page.

**Parameters:**
- `page_id` (string, required): The page ID
- `limit` (integer, optional): Maximum attachments (default: 10)

**Response:**
```json
{
  "success": true,
  "attachments": [
    {
      "id": "att123",
      "title": "api-schema.json",
      "type": "application/json",
      "size": 2048,
      "url": "https://..."
    }
  ],
  "total": 1
}
```

---

#### `get_page_comments`

Get all comments on a page.

**Parameters:**
- `page_id` (string, required): The page ID
- `limit` (integer, optional): Maximum comments (default: 10)

**Response:**
```json
{
  "success": true,
  "comments": [
    {
      "id": "com123",
      "body": {
        "storage": {
          "value": "<p>Great documentation!</p>"
        }
      },
      "by": {
        "displayName": "Jane Smith"
      },
      "created": "2026-02-22T09:30:00Z"
    }
  ],
  "total": 1
}
```

---

## Error Handling

All tools return errors in the following format:

```json
{
  "success": false,
  "error": "Error message describing what went wrong"
}
```

### Common Error Codes

- `400` - Bad Request: Invalid parameters
- `401` - Unauthorized: Invalid credentials
- `403` - Forbidden: Insufficient permissions
- `404` - Not Found: Resource doesn't exist
- `429` - Rate Limited: Too many requests
- `500` - Server Error: Confluence server error

## Authentication

All requests are authenticated using HTTP Basic Authentication with:
- Username: Your Confluence email/username
- Password: Your Personal Access Token (PAT)

No additional authentication headers are needed in MCP requests.

## Rate Limiting

The server implements automatic retry logic with exponential backoff for rate-limited requests. If you receive a rate limit error, the server will automatically retry after the specified delay.

## Pagination

Many tools support pagination with `limit` and `start` parameters:
- `limit`: Maximum number of items to return (typically 1-100)
- `start`: Zero-based index to start from

Results include:
- `total`: Total number of items available
- `start`: Starting index of current results
- `limit`: Limit used in request

## CQL (Confluence Query Language)

The `search_pages` tool uses CQL for querying. Common CQL examples:

```
# Search by title
title ~ "API"

# Search by space
space.key = "DEV"

# Combined search
title ~ "API" AND space.key = "DEV"

# Search by author
author = "john@example.com"

# Search by content type
type = "page"

# Advanced filtering
created >= -7d AND updated >= -1d
```

For more CQL documentation, see: https://confluence.atlassian.com/confcloud/advanced-search-using-cql-791557401.html

