# Matillion API MCP Server

This is a Python-based MCP (Model Context Protocol) server that interacts with the Matillion API. It provides a convenient interface for AI assistants to access Matillion resources through standardized tool calls.

## Features

- Authentication with Matillion API
- Fetch projects from Matillion
- Get environments for specific projects
- Extensible framework for adding more Matillion API interactions

## Prerequisites

- Python 3.8+
- Matillion account with API access
- Client credentials (Client ID, Client Secret, Account ID)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd mcp-server-hyd
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Create and Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## Running the Server

To start the MCP server:

```bash
python server.py
```

The server runs on stdin/stdout, making it compatible with MCP clients.

## Available Tools

The server provides the following tools:

1. **get_matillion_token**
   - Description: Get access token from Matillion API
   - Parameters: None

2. **get_matillion_projects**
   - Description: Get projects from Matillion API
   - Parameters:
     - `page` (optional, default: 0): Page number for pagination
     - `size` (optional, default: 25): Number of items per page

3. **get_project_environments**
   - Description: Get environments for a specific project from Matillion API
   - Parameters:
     - `project_id` (required): ID of the project to get environments for

## Integration with AI Assistants

This MCP server can be integrated with AI assistants that support the Model Context Protocol. The assistant can then make tool calls to interact with the Matillion API.

## MCP Server Configuration

To configure an MCP client to use this server, you'll need to add it to your MCP configuration. Here's a sample configuration:

```json
{
  "mcpServers": {
    "your_mcp_server_name": {
      "command": "/path/to/venv/bin/python3",
      "args": [
        "/path/to/mcp-server/server.py"
      ],
      "env": {
        "CLIENT_ID": "your-client-id",
        "CLIENT_SECRET": "your-client-secret",
        "ACCOUNT_ID": "your-account-id"
      }
    }
  }
}
```

### Configuration Options:

- **mcpServers**: Object containing all MCP server configurations
- **matillion mcp server**: A unique name for the server
- **command**: Path to the Python interpreter in your virtual environment
- **args**: Array of arguments to pass to the command (path to server.py)
- **env**: Environment variables for authentication (CLIENT_ID, CLIENT_SECRET, ACCOUNT_ID)

