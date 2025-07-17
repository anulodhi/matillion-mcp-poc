#!/usr/bin/env python3

import asyncio
import os
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio
import requests

# Get credentials from environment variables
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
ACCOUNT_ID = os.getenv("ACCOUNT_ID")

# Create server instance
server = Server("matillion-api-server")

def get_access_token():
    """Get access token from Matillion API"""
    url = "https://id.core-dev.matillion.com/oauth/dpc/token"
    
    payload = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "audience": "https://api.matillion.com"
    }
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    response = requests.post(url, data=payload, headers=headers)
    response.raise_for_status()
    return response.json()

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools."""
    return [
        types.Tool(
            name="get_matillion_token",
            description="Get access token from Matillion API",
            inputSchema={
                "type": "object",
                "properties": {}
            },
        ),
        types.Tool(
            name="get_matillion_projects",
            description="Get projects from Matillion API",
            inputSchema={
                "type": "object",
                "properties": {
                    "page": {
                        "type": "integer",
                        "description": "Page number for pagination",
                        "default": 0
                    },
                    "size": {
                        "type": "integer", 
                        "description": "Number of items per page",
                        "default": 25
                    }
                }
            },
        ),
        types.Tool(
            name="get_project_environments",
            description="Get environments for a specific project from Matillion API",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {
                        "type": "string",
                        "description": "ID of the project to get environments for"
                    }
                },
                "required": ["project_id"]
            },
        ),
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool calls."""
        
    if name == "get_matillion_token":
        try:
            token_response = get_access_token()
            return [types.TextContent(
                type="text", 
                text=f"Access token obtained successfully. Token: {token_response.get('access_token', 'N/A')}"
            )]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error getting token: {str(e)}")]
    
    elif name == "get_matillion_projects":
        try:
            # Get token first
            token_response = get_access_token()
            token = token_response.get('access_token')
            
            if not token:
                return [types.TextContent(type="text", text="Error: Failed to get access token")]
            
            # Get projects
            page = arguments.get("page", 0) if arguments else 0
            size = arguments.get("size", 25) if arguments else 25
            
            url = f"https://eu1.api-dev.matillion.com/dpc/v1/projects?page={page}&size={size}"
            headers = {
                "Authorization": f"Bearer {token}",
                "account-id": ACCOUNT_ID
            }
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            projects_data = response.json()
            return [types.TextContent(
                type="text",
                text=f"Successfully retrieved projects: {projects_data}"
            )]
            
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error getting projects: {str(e)}")]
    
    elif name == "get_project_environments":
        try:
            # Validate required arguments
            if not arguments or "project_id" not in arguments:
                return [types.TextContent(type="text", text="Error: project_id is required")]
            
            project_id = arguments["project_id"]
            
            # Get token first
            token_response = get_access_token()
            token = token_response.get('access_token')
            
            if not token:
                return [types.TextContent(type="text", text="Error: Failed to get access token")]
            
            # Get environments for the specified project
            url = f"https://eu1.api-dev.matillion.com/dpc/v1/projects/{project_id}/environments"
            headers = {
                "Authorization": f"Bearer {token}",
                "account-id": ACCOUNT_ID
            }
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            environments_data = response.json()
            return [types.TextContent(
                type="text",
                text=f"Successfully retrieved environments for project {project_id}: {environments_data}"
            )]
            
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error getting environments: {str(e)}")]
    
    else:
        return [types.TextContent(type="text", text=f"Unknown tool: {name}")]

async def main():
    # Run the server using stdin/stdout
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="matillion-api-server",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())