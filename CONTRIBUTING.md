# Contributing Guide

We welcome contributions to MCP Confluence Server! This guide will help you get started.

## Getting Started

### Fork and Clone
```bash
git clone https://github.com/yourusername/mcp-confluence.git
cd mcp-confluence
git remote add upstream https://github.com/original/mcp-confluence.git
```

### Setup Development Environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Install development tools
pip install pytest pytest-cov black pylint mypy
```

### Create Feature Branch
```bash
git checkout -b feature/your-feature-name
```

## Development Workflow

### 1. Write Tests First
```python
# tests/test_your_feature.py
def test_your_feature():
    # Test implementation
    pass
```

### 2. Implement Feature
```python
# src/your_module.py
# Implementation code
```

### 3. Run Tests
```bash
pytest tests/ -v
pytest tests/ --cov=src  # With coverage
```

### 4. Code Quality
```bash
# Format code
black src/ tests/

# Check style
pylint src/ tests/

# Type checking
mypy src/ tests/
```

### 5. Commit Changes
```bash
git add .
git commit -m "feat: add your feature description"
```

### 6. Push and Create PR
```bash
git push origin feature/your-feature-name
```

## Code Standards

### Python Style Guide
- Follow PEP 8
- Use type hints
- Docstrings for all public functions
- Comments for complex logic

### Example Function
```python
def search_pages(
    self,
    query: str,
    limit: int = 25,
    start: int = 0
) -> Dict[str, Any]:
    """
    Search for pages using CQL.
    
    Args:
        query: CQL query string
        limit: Maximum results (1-100)
        start: Pagination start
        
    Returns:
        Dictionary containing search results
        
    Raises:
        BadRequestError: If CQL query is invalid
        ConfluenceServerError: If Confluence returns error
    """
    # Implementation
```

### Testing Standards
- Minimum 80% code coverage
- Test happy paths and error cases
- Use fixtures for reusable test data
- Mock external API calls

## Adding New Tools

### 1. Create Tool Class

```python
# src/tools/my_feature.py
from src.tools.base import BaseTool, ToolParameter

class MyNewTool(BaseTool):
    @property
    def name(self) -> str:
        return "my_new_tool"
    
    @property
    def description(self) -> str:
        return "Description of what the tool does"
    
    @property
    def parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="param1",
                type="string",
                description="Description",
                required=True
            ),
        ]
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        self.validate_parameters(**kwargs)
        # Implementation
        return {'success': True, 'data': result}
```

### 2. Add Tests

```python
# tests/test_my_feature.py
@pytest.mark.asyncio
async def test_my_new_tool(mock_client):
    tool = MyNewTool(mock_client)
    result = await tool.execute(param1="value")
    assert result['success']
```

### 3. Register Tool

```python
# src/server.py - Add to _initialize_tools()
MyNewTool(self.client),
```

### 4. Document Tool

Update `API_REFERENCE.md` with tool documentation.

## Adding Client Methods

### 1. Add to ConfluenceClient

```python
# src/client.py
def new_api_method(self, param: str) -> Dict[str, Any]:
    """
    Description of the method.
    
    Args:
        param: Parameter description
        
    Returns:
        API response
    """
    params = {'key': param}
    return self._request_with_retry('GET', '/endpoint', params=params)
```

### 2. Add Tests

```python
# tests/test_client.py
def test_new_api_method(client):
    with patch.object(client, '_request_with_retry', return_value={}):
        result = client.new_api_method('value')
        assert result
```

## Documentation

### Update README
- Document new features
- Add examples
- Update feature list

### Update API_REFERENCE
- Document new tools
- Include examples
- List parameters and responses

### Update ARCHITECTURE
- Document design patterns
- Update data flow diagrams
- Note extension points

## Git Commit Convention

Follow conventional commits:
```
feat: add new search capability
fix: handle rate limit errors correctly
docs: update API documentation
test: add tests for search functionality
refactor: simplify error handling
chore: update dependencies
```

## Pull Request Process

1. **Create PR** with clear title and description
2. **Provide Context**
   - What problem does it solve?
   - How does it work?
   - Any breaking changes?
3. **Include Tests**
   - Unit tests for new code
   - Integration tests if applicable
   - Minimum 80% coverage
4. **Update Documentation**
   - README if user-facing
   - API_REFERENCE for new tools
   - Code comments for complex logic
5. **Code Review**
   - Address reviewer feedback
   - Push review changes
   - Get approval

## Reporting Issues

### Bug Reports
Include:
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages/logs
- Confluence deployment type

### Feature Requests
Include:
- Use case description
- Expected behavior
- Examples if possible
- Potential implementation approach

## Development Tips

### Debugging
```python
# Add logging
import logging
logger = logging.getLogger(__name__)
logger.debug(f"Variable value: {var}")

# Print debugging
print(f"Debug: {variable}")

# Use pdb
import pdb; pdb.set_trace()
```

### Testing with Real API
```python
# Create test.py for manual testing
import asyncio
from src.config import get_settings
from src.server import MCPConfluenceServer

async def test():
    settings = get_settings()
    server = MCPConfluenceServer(settings)
    result = await server.call_tool('list_spaces')
    print(result)

asyncio.run(test())
```

### Common Tasks

**Run specific test:**
```bash
pytest tests/test_client.py::test_search_pages -v
```

**Run with debug output:**
```bash
pytest tests/ -v -s
```

**Check test coverage:**
```bash
pytest tests/ --cov=src --cov-report=html
# Open htmlcov/index.html
```

**Format all code:**
```bash
black src/ tests/
```

## Architecture Guidelines

When making structural changes:

1. **Maintain Layer Separation**
   - Tools shouldn't directly call HTTP
   - Client shouldn't know about tools

2. **Keep Tools Stateless**
   - Tools should be reusable
   - State in client/server

3. **Error Handling**
   - Use specific exceptions
   - Handle at appropriate layer

4. **Async/Await**
   - Keep async for scalability
   - Don't mix sync/async

## Performance Considerations

- Profile code for bottlenecks
- Cache expensive operations
- Batch operations when possible
- Use pagination for large datasets
- Minimize API calls

## Security Considerations

- Never log credentials
- Validate all inputs
- Use HTTPS for API calls
- Follow security best practices
- Report security issues privately

## Resources

- [Python Docs](https://docs.python.org/3/)
- [Pydantic Docs](https://docs.pydantic.dev/)
- [Pytest Docs](https://docs.pytest.org/)
- [Confluence API](https://developer.atlassian.com/cloud/confluence/)
- [MCP Protocol](https://spec.modelcontextprotocol.io/)

## Questions?

- Check existing issues/discussions
- Review documentation
- Ask in pull request
- Open an issue for discussion

Thank you for contributing! 🎉

