# Asana MCP Server

A Model Context Protocol (MCP) server that provides comprehensive tools for interacting with the Asana API. This server enables AI assistants and other MCP-compatible clients to manage Asana projects, tasks, teams, workspaces, and more through a standardized interface.

## Features

- **Comprehensive Asana API Coverage**: Access to a wide range of Asana operations including:
  - Projects and tasks management
  - Teams and workspaces
  - Custom fields and tags
  - Allocations and resource management
  - Attachments and stories
  - Portfolios and goals
  - Batch operations for efficient parallel requests

- **OAuth2 Authentication**: Secure authentication with Asana using OAuth2 flow with automatic token refresh
- **Dynamic Tool Registration**: Tools are loaded from a manifest file, making it easy to add or modify tools
- **FastMCP Integration**: Built on FastMCP for efficient MCP server implementation
- **Type-Safe Schemas**: All tools include proper input/output schemas for validation

## Prerequisites

- Python 3.10 or higher
- An Asana account
- An Asana OAuth app (create one at https://app.asana.com/0/my-apps)

## Installation

1. Clone or download this repository

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or use the script dependencies:
```bash
python run_server.py
```

## Configuration

### Step 1: Create Asana OAuth App

1. Go to https://app.asana.com/0/my-apps
2. Click **"Create New App"** or **"Create Custom App"**
3. Fill in the app details:
   - **App Name**: Choose a name (e.g., "MCP Server" or "Asana MCP Integration")
   - **App URL**: Can be your project URL or leave blank
   - **Redirect URI**: Set to `http://localhost:8338/callback`
     - This must match exactly what you use in your `.env` file
   - **Manage distribution**: Set to **\"Any workspace\"** so the app can be installed and used from any Asana workspace in your account
4. Click **"Create App"**

### Step 2: Configure App Permissions

After creating the app, you need to configure permissions:

1. In your app settings, go to the **"Permissions"** or **"Scopes"** section
2. Add the following permissions/scopes:
   - **default** - Full access (recommended for full API functionality)
   - Or select specific scopes based on your needs:
     - Read and write access to tasks
     - Read and write access to projects
     - Read and write access to teams
     - Read and write access to workspaces
     - Read and write access to users
     - Access to custom fields
     - Access to portfolios and goals (if needed)

3. **Save** the permissions settings

### Step 3: Get OAuth Credentials

1. In your app settings, find the **"Credentials"** or **"OAuth"** section
2. Copy the following values:
   - **Client ID** (also called "App ID")
   - **Client Secret** (keep this secure!)

### Step 4: Create .env File

Create a `.env` file in the project root with the following variables:

```env
ASANA_CLIENT_ID=your_client_id_here
ASANA_CLIENT_SECRET=your_client_secret_here
ASANA_REDIRECT_URI=http://localhost:8338/callback
ASANA_SCOPES=default
```

**Important Notes:**
- Replace `your_client_id_here` and `your_client_secret_here` with the actual values from your Asana app
- The `ASANA_REDIRECT_URI` must **exactly match** the redirect URI you set in your Asana app settings
- The `ASANA_SCOPES=default` provides full access; you can use specific scopes if preferred

## Usage

### Running the Server

Start the MCP server:

```bash
python run_server.py
```

Or directly:

```bash
python -m src.main
```

### First-Time Authentication

You have two options for authentication:

#### Option 1: Test Authentication Script (Recommended)

Run the authentication test script to handle OAuth and store tokens:

```bash
python test_auth.py
```

This script will:
1. Open a browser window for OAuth authentication
2. Prompt you to authorize the application
3. Store the access token in `.token_cache.json`
4. Verify the connection by fetching your user profile

This is useful for testing your OAuth setup before running the main server.

#### Option 2: Automatic Authentication on Server Start

Alternatively, the server will automatically handle authentication on first run:
1. Open a browser window for OAuth authentication
2. Prompt you to authorize the application
3. Store the access token for future use

The token is cached in `.token_cache.json` and will be automatically refreshed when needed.

### Available Tools

The server currently exposes **142 tools** for interacting with Asana. All tools follow the naming convention `<ACTION>_<RESOURCE>`. Here are some examples:

#### User & Workspace Tools
- `GET_CURRENT_USER` - Get the authenticated user's information
- `GET_MULTIPLE_WORKSPACES` - List accessible workspaces
- `GET_MULTIPLE_USERS` - Get user information

#### Project Tools
- `CREATE_A_PROJECT` - Create a new project
- `UPDATE_PROJECT` - Update an existing project
- `GET_MULTIPLE_PROJECTS` - List projects
- `GET_A_PROJECT` - Get project details

#### Task Tools
- `CREATE_A_TASK` - Create a new task
- `UPDATE_A_TASK` - Update an existing task
- `GET_MULTIPLE_TASKS` - List tasks
- `GET_A_TASK` - Get task details

#### Team Tools
- `GET_TEAMS_IN_WORKSPACE` - List teams in a workspace
- `UPDATE_TEAM` - Update team details
- `GET_A_TEAM` - Get team information

#### Custom Field Tools
- `UPDATE_CUSTOM_FIELD` - Update a custom field
- `GET_MULTIPLE_CUSTOM_FIELDS` - List custom fields

#### Tag Tools
- `UPDATE_TAG` - Update a tag
- `GET_MULTIPLE_TAGS` - List tags

#### Batch Operations
- `SUBMIT_PARALLEL_REQUESTS` - Submit multiple API requests in parallel

For a complete, always up-to-date list of all **142 tools**, see `tools_manifest.json`.

#### No need to enter user/workspace every time

After you authenticate, the server gets your **user GID** and **default workspace GID** from the Asana API (via the token session) and caches them in `.token_cache.json`. Tools that accept `workspace_gid`, `workspace`, or `assignee` will use these defaults when you omit the value, so you don’t need to enter them—server fills from your session. The default workspace is the first workspace in your account.

## Project Structure

```
asana/
├── src/
│   ├── main.py              # Main entry point and tool registration
│   ├── client.py            # Asana API client with OAuth2
│   ├── config.py            # Configuration settings
│   └── tools/               # Tool implementations
│       ├── attachment_tools.py
│       ├── batch_tools.py
│       ├── custom_field_tools.py
│       ├── event_tools.py
│       ├── goal_tools.py
│       ├── membership_tools.py
│       ├── portfolio_tools.py
│       ├── project_tools.py
│       ├── story_tools.py
│       ├── tag_tools.py
│       ├── task_tools.py
│       ├── team_tools.py
│       ├── user_tools.py
│       └── workspace_tools.py
├── tools_manifest.json      # Tool definitions and schemas
├── requirements.txt         # Python dependencies
├── run_server.py           # Server entry point script
├── mcp-config.json         # MCP configuration
└── README.md               # This file
```

## How It Works

1. **Tool Registration**: Tools are defined in `tools_manifest.json` with their target functions, descriptions, and input schemas
2. **Dynamic Loading**: The server dynamically imports and registers tools from the manifest at startup
3. **Client Injection**: Each tool function receives an `AsanaClient` instance for making API calls
4. **Schema Cleaning**: Input schemas are processed to remove null types for MCP compatibility
5. **OAuth Management**: The client handles authentication, token refresh, and caching automatically

## Development

### Adding New Tools

1. Create a function in the appropriate tool module (e.g., `src/tools/project_tools.py`)
2. The function should accept `client: AsanaClient` as the first parameter
3. Add the tool definition to `tools_manifest.json`:
   ```json
   {
     "id": "YOUR_TOOL_NAME",
     "target": "src.tools.your_module:your_function",
     "description": "Description of what the tool does",
     "input_schema": {
       "type": "object",
       "properties": {
         "param1": {"type": "string", "description": "..."}
       },
       "required": ["param1"]
     }
   }
   ```

### Testing Authentication

You can test the authentication flow independently. This script handles OAuth authentication and stores tokens in `.token_cache.json`:

```bash
python test_auth.py
```

This is useful for:
- Verifying your OAuth credentials are correct
- Pre-authenticating before running the main server
- Testing the connection to Asana API

## Dependencies

- `fastmcp>=0.1.0` - MCP server framework
- `requests>=2.31.0` - HTTP client for API calls
- `python-dotenv>=1.0.0` - Environment variable management
- `aiohttp>=3.9.0` - Async HTTP support

## Troubleshooting

### Authentication Issues

#### Invalid Client ID or Secret
- Ensure your `.env` file has correct `ASANA_CLIENT_ID` and `ASANA_CLIENT_SECRET`
- Double-check that you copied the values correctly from https://app.asana.com/0/my-apps
- Make sure there are no extra spaces or quotes in the `.env` file

#### Redirect URI Mismatch
- The redirect URI in your `.env` file must **exactly match** the one configured in your Asana app
- Common default: `http://localhost:8338/callback`
- Check both places:
  1. Your `.env` file: `ASANA_REDIRECT_URI=http://localhost:8338/callback`
  2. Your Asana app settings (under "Redirect URIs")

#### Permission/Scope Errors
- If you get "insufficient permissions" errors, verify your app has the required scopes:
  - Go to your app settings at https://app.asana.com/0/my-apps
  - Check the "Permissions" or "Scopes" section
  - Ensure "default" scope is enabled (or add specific scopes you need)
  - Save the changes and try authenticating again

#### Token Issues
- If authentication fails, delete `.token_cache.json` to force re-authentication
- Make sure the token cache file is not corrupted (delete it if unsure)
- Run `python test_auth.py` to test authentication independently

### Import Errors

- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Verify Python version is 3.10 or higher: `python --version`

### Tool Registration Issues

- Check `tools_manifest.json` for valid JSON syntax
- Verify target module paths match actual file structure
- Check logs for specific import errors

## License

This project is provided as-is. Please refer to Asana's API terms of service for usage guidelines.

## Support

For issues related to:
- **Asana API**: See [Asana API Documentation](https://developers.asana.com/docs)
- **MCP Protocol**: See [Model Context Protocol Documentation](https://modelcontextprotocol.io)
- **This Server**: Open an issue in the project repository

