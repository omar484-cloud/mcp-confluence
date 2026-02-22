"""
Main entry point for MCP Confluence Server
"""

import sys
import logging
import asyncio
import json
from typing import Dict, Any

from src.config import get_settings
from src.server import MCPConfluenceServer
from src.utils import setup_logging


async def main():
    """Main entry point"""

    # Load settings
    try:
        settings = get_settings()
    except Exception as e:
        print(f"Error loading settings: {e}", file=sys.stderr)
        print("Please ensure .env file is configured correctly", file=sys.stderr)
        sys.exit(1)

    # Setup logging
    logger = setup_logging(settings.log_level)
    logger.info("Starting MCP Confluence Server")

    # Initialize server
    try:
        server = MCPConfluenceServer(settings)
        logger.info("MCP Server initialized successfully")
        logger.info(f"Confluence URL: {settings.confluence_url}")
        logger.info(f"Deployment: {settings.confluence_deployment}")
    except Exception as e:
        logger.error(f"Failed to initialize server: {e}")
        sys.exit(1)

    # Print server info
    print(json.dumps(server.get_server_info(), indent=2))
    print(f"Available tools: {len(server.list_tools())}")

    # Start reading requests from stdin
    logger.info("Server ready for requests")

    try:
        while True:
            # Read request from stdin
            line = sys.stdin.readline()
            if not line:
                break

            try:
                request = json.loads(line.strip())
                logger.debug(f"Received request: {request}")

                # Process request
                response = await server.handle_request(request)

                # Send response
                print(json.dumps(response))
                sys.stdout.flush()
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON: {e}")
                print(json.dumps({
                    'success': False,
                    'error': f'Invalid JSON: {e}'
                }))
                sys.stdout.flush()
            except Exception as e:
                logger.error(f"Error processing request: {e}")
                print(json.dumps({
                    'success': False,
                    'error': str(e)
                }))
                sys.stdout.flush()
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())

