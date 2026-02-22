# Quick Start Guide

Get your MCP Confluence Server running in 5 minutes!

## Step 1: Get Your API Token

### For Confluence Cloud:
1. Go to https://id.atlassian.com/manage/api-tokens
2. Click "Create API token"
3. Copy the token

### For Confluence Server:
1. Log in to your Confluence instance
2. Go to Settings > Personal Settings
3. Create or find your API token

## Step 2: Configure the Server

```bash
# Clone and setup
git clone <repo-url>
cd mcp-confluence
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create configuration
cp .env.example .env
```

Edit `.env`:
```env
CONFLUENCE_URL=https://your-domain.atlassian.net
CONFLUENCE_USERNAME=your-email@example.com
CONFLUENCE_API_TOKEN=your-copied-token
CONFLUENCE_DEPLOYMENT=cloud
LOG_LEVEL=INFO
```

## Step 3: Run the Server

```bash
python -m src.main
```

You should see output like:
```
2026-02-22 10:00:00 - mcp_confluence - INFO - Starting MCP Confluence Server
{
  "name": "MCP Confluence Server",
  "version": "1.0.0",
  "deployment": "cloud",
  "confluence_url": "https://your-domain.atlassian.net"
}
Available tools: 12
2026-02-22 10:00:00 - mcp_confluence - INFO - Server ready for requests
```

## Step 4: Test a Request

In another terminal:

```bash
# Test search
echo '{"request_id":"1","method":"call_tool","params":{"name":"list_spaces","arguments":{}}}' | python -m src.main
```

You should get a response with your spaces!

## Available Tools

Once running, you can use these tools:

### Search
- `search_pages` - Find pages by text
- `search_spaces` - List spaces

### Pages
- `get_page` - Get page details
- `create_page` - Create new page
- `update_page` - Update page content
- `delete_page` - Delete a page

### Spaces
- `get_space` - Get space info
- `list_spaces` - List all spaces
- `get_space_pages` - List pages in space

### Metadata
- `get_page_history` - Page revisions
- `get_page_attachments` - Page files
- `get_page_comments` - Page comments

## Useful Resources

- **[API_REFERENCE.md](API_REFERENCE.md)** - Full documentation of all tools
- **[USAGE.md](USAGE.md)** - Detailed usage examples
- **[README.md](README.md)** - Project overview

## Troubleshooting

**"Authentication failed"**
- Check username and token in `.env`
- Verify token hasn't expired

**"Rate limited"**
- Server retries automatically
- Increase `RATE_LIMIT_DELAY` if needed

**"Resource not found"**
- Verify page/space IDs or keys exist
- Check you have permission to access them

## Next Steps

1. Integrate with your LLM application
2. Create custom tools by extending the framework
3. Set up CI/CD pipeline
4. Deploy with Docker (see DEPLOYMENT.md)

Happy coding! 🚀

