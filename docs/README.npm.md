# UniFi MCP Server

A Model Context Protocol (MCP) server for UniFi Network Controller API.

## Installation

This npm package provides metadata for the MCP registry. The actual server is Python-based.

### Python Installation (Recommended)

```bash
pip install unifi-mcp-server==0.2.1
```

### Docker Installation

```bash
docker pull ghcr.io/seathegood/unifi-mcp-server:0.2.1
```

## Usage

```bash
# Run the MCP server
python -m src.main

# Or using Docker
docker run -e UNIFI_API_KEY=your-api-key \
  -e UNIFI_API_TYPE=cloud-v1 \
  ghcr.io/seathegood/unifi-mcp-server:0.2.1
```

## Documentation

Full documentation available at: https://github.com/seathegood/unifi-mcp-server

## Features

- 74 MCP tools for comprehensive UniFi network management
- Multi-site support
- QoS and traffic management
- Backup and restore operations
- Network topology visualization
- RADIUS authentication configuration

## License

Apache-2.0
