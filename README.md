# <img src="https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/png/unifi-dark.png" alt="UniFi Dark Logo" width="40" /> UniFi MCP Server (seathegood fork)

This fork explores MCP development patterns for AI workflows while maintaining a robust UniFi API integration and a container-first delivery model. It is not intended to maintain backward compatibility with the upstream project.

- Maintained at: `github.com/seathegood/unifi-mcp-server`
- Upstream reference: `github.com/enuno/unifi-mcp-server` (acknowledged with thanks)
- License: Apache-2.0 (preserved)
- Publishing: GHCR (and mirrored to Docker Hub under seathegood); upstream PyPI/npm are not targets for this fork

## What this is
- A Model Context Protocol (MCP) server and docs for UniFi network automation, tuned for AI agents and automation workflows.
- A container-first distribution with a harmonized environment contract: `UNIFI_API_TYPE`, `UNIFI_CLOUD_API_URL`, `UNIFI_LOCAL_*`, `UNIFI_RATE_LIMIT_REQUESTS`/`PERIOD`, `UNIFI_REQUEST_TIMEOUT`, caching/logging/audit flags.
- A foundation for experimenting with MCP tooling patterns and production-ready deployment practices.

## What this is not
- Not backward compatible with the upstream release history or legacy env names beyond transitional shims.
- Not a commitment to publish on upstream registries (PyPI/npm) or to preserve upstream version numbering.
- Not a drop-in replacement for upstream; capabilities and APIs may diverge.

## Current status
- Pre-release fork bootstrap; first forked release is planned under `seathegood` GHCR/Docker Hub.
- Legacy release history and coverage claims from upstream are intentionally removed here; see `docs/` for any legacy references.

## Running (container-first)
```bash
# pull (replace tag as needed when first forked release is cut)
docker pull ghcr.io/seathegood/unifi-mcp-server:latest

# run with env contract (example: local gateway)
docker run -i --rm \
  -e UNIFI_API_KEY=your-api-key \
  -e UNIFI_API_TYPE=local \
  -e UNIFI_LOCAL_HOST=192.168.1.1 \
  ghcr.io/seathegood/unifi-mcp-server:latest
```

For Compose-based deployment with Redis/Toolbox, see `docker-compose.yml` and `.env.example` (contract uses the harmonized env names).

## Configuration (harmonized)
- `UNIFI_API_TYPE`: `cloud-v1` | `cloud-ea` | `local`
- `UNIFI_CLOUD_API_URL`: base URL for cloud APIs
- `UNIFI_LOCAL_*`: `UNIFI_LOCAL_HOST`, `UNIFI_LOCAL_PORT`, `UNIFI_LOCAL_VERIFY_SSL`
- `UNIFI_DEFAULT_SITE`, `UNIFI_SITE_MANAGER_ENABLED`
- Reliability: `UNIFI_RATE_LIMIT_REQUESTS`, `UNIFI_RATE_LIMIT_PERIOD`, `UNIFI_MAX_RETRIES`, `UNIFI_RETRY_BACKOFF_FACTOR`, `UNIFI_REQUEST_TIMEOUT`
- Cache/Logging/Audit: `UNIFI_CACHE_ENABLED`, `UNIFI_CACHE_TTL`, `LOG_LEVEL`, `LOG_API_REQUESTS`, `UNIFI_AUDIT_LOG_ENABLED`

## Roadmap (fork)
- MCP patterns for AI workflows (promptable automation, robust validation).
- Container-first hardening (health checks, minimal env surface, secrets hygiene).
- Documentation refresh aligned to the new contract and deployment model.
- Maintain UniFi API integration parity while simplifying scope as needed.

## Contributing
- Branch protections will be enforced on `main`; use PRs with checks.
- Issues/Discussions: https://github.com/seathegood/unifi-mcp-server

## Credits
- Original project by `enuno` and contributors: https://github.com/enuno/unifi-mcp-server
- Licensed under Apache-2.0 (see LICENSE)
- **MCP Protocol**: Standard Model Context Protocol for AI agent integration
- **Comprehensive Testing**: 990 unit tests with 78.18% coverage (4,865 of 6,105 statements)
- **CI/CD Pipelines**: Automated testing, security scanning, and Docker builds (18 checks)
- **Multi-Architecture**: Docker images for amd64, arm64, arm/v7 (32-bit ARM), and arm64/v8
- **Zero Security Issues**: Clean scans from Bandit, Trivy, OSV Scanner, and Socket Security
- **Quality Metrics**: Black formatting, Ruff linting, comprehensive type hints

## Quick Start

### Prerequisites

- Python 3.10 or higher
- A UniFi account at [unifi.ui.com](https://unifi.ui.com)
- UniFi API key (obtain from Settings → Control Plane → Integrations)
- Access to UniFi Cloud API or local gateway

### Installation

#### Using PyPI (Recommended)

The UniFi MCP Server is published on PyPI and can be installed with pip or uv:

```bash
# Install from PyPI
pip install unifi-mcp-server

# Or using uv (faster)
uv pip install unifi-mcp-server

# Install specific version
pip install unifi-mcp-server==0.2.0
```

After installation, the `unifi-mcp-server` command will be available globally.

**PyPI Package**: <https://pypi.org/project/unifi-mcp-server/>

#### Using Docker (Alternative)

```bash
# Pull the latest release
docker pull ghcr.io/enuno/unifi-mcp-server:0.2.0

# Multi-architecture support: amd64, arm64, arm/v7
```

#### Build from Source (Development)

##### Using uv (Recommended)

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/enuno/unifi-mcp-server.git
cd unifi-mcp-server

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"
```

#### Using pip

```bash
# Clone the repository
git clone https://github.com/enuno/unifi-mcp-server.git
cd unifi-mcp-server

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"
```

#### Using Docker Compose (Recommended for Production)

The recommended way to run the UniFi MCP Server with full monitoring capabilities:

```bash
# 1. Copy and configure environment variables
cp .env.docker.example .env
# Edit .env with your UNIFI_API_KEY and AGNOST_ORG_ID

# 2. Start all services (MCP Server + Redis + MCP Toolbox)
docker-compose up -d

# 3. Check service status
docker-compose ps

# 4. View logs
docker-compose logs -f unifi-mcp

# 5. Access MCP Toolbox dashboard
open http://localhost:8080

# 6. Stop all services
docker-compose down
```

**Included Services:**

- **UniFi MCP Server**: Main MCP server with 77 tools (69 functional, 8 deprecated)
- **MCP Toolbox**: Web-based analytics dashboard (port 8080)
- **Redis**: High-performance caching layer

See [MCP_TOOLBOX.md](MCP_TOOLBOX.md) for detailed Toolbox documentation.

#### Using Docker (Standalone)

For standalone Docker usage (not with MCP clients):

```bash
# Pull the image
docker pull ghcr.io/enuno/unifi-mcp-server:latest

# Run the container in background (Cloud API)
# Note: -i flag keeps stdin open for STDIO transport
docker run -i -d \
  --name unifi-mcp \
  -e UNIFI_API_KEY=your-api-key \
  -e UNIFI_API_TYPE=cloud-v1 \
  ghcr.io/enuno/unifi-mcp-server:latest

# OR run with local gateway proxy
docker run -i -d \
  --name unifi-mcp \
  -e UNIFI_API_KEY=your-api-key \
  -e UNIFI_API_TYPE=local \
  -e UNIFI_LOCAL_HOST=192.168.1.1 \
  ghcr.io/enuno/unifi-mcp-server:latest

# Check container status
docker ps --filter name=unifi-mcp

# View logs
docker logs unifi-mcp

# Stop and remove
docker rm -f unifi-mcp
```

**Note**: For MCP client integration (Claude Desktop, etc.), see the [Usage](#usage) section below for the correct configuration without `-d` flag.

## Build from Source

### Prerequisites

- **Python 3.10+**: Required for running the server
- **Git**: For cloning the repository
- **uv** (recommended) or **pip**: For dependency management
- **Docker** (optional): For containerized builds
- **Node.js & npm** (optional): For npm package publishing

### Development Build

#### 1. Clone the Repository

```bash
git clone https://github.com/enuno/unifi-mcp-server.git
cd unifi-mcp-server
```

#### 2. Set Up Development Environment

**Using uv (Recommended):**

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
# Or on Windows: .venv\Scripts\activate

# Install development dependencies
uv pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
pre-commit install --hook-type commit-msg
```

**Using pip:**

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
# Or on Windows: .venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
pre-commit install --hook-type commit-msg
```

#### 3. Configure Environment

```bash
# Copy example configuration
cp .env.example .env

# Edit .env with your UniFi credentials
# Required: UNIFI_API_KEY
# Recommended: UNIFI_API_TYPE=local, UNIFI_LOCAL_HOST=<gateway-ip>
```

#### 4. Run Tests

```bash
# Run all unit tests
pytest tests/unit/ -v

# Run with coverage report
pytest tests/unit/ --cov=src --cov-report=html --cov-report=term-missing

# View coverage report
open htmlcov/index.html  # macOS
# Or: xdg-open htmlcov/index.html  # Linux
```

#### 5. Run the Server

```bash
# Development mode with MCP Inspector
uv run mcp dev src/main.py

# Production mode
uv run python -m src.main

# The MCP Inspector will be available at http://localhost:5173
```

### Production Build

#### Build Python Package

```bash
# Install build tools
uv pip install build

# Build wheel and source distribution
python -m build

# Output: dist/unifi_mcp_server-0.2.0-py3-none-any.whl
#         dist/unifi_mcp_server-0.2.0.tar.gz
```

#### Build Docker Image

```bash
# Build for current architecture
docker build -t unifi-mcp-server:0.2.0 .

# Build multi-architecture (requires buildx)
docker buildx create --use
docker buildx build \
  --platform linux/amd64,linux/arm64,linux/arm/v7 \
  -t ghcr.io/enuno/unifi-mcp-server:0.2.0 \
  --push .

# Test the image
docker run -i --rm \
  -e UNIFI_API_KEY=your-key \
  -e UNIFI_API_TYPE=cloud \
  unifi-mcp-server:0.2.0
```

### Publishing

#### Publish to PyPI

```bash
# Install twine
uv pip install twine

# Check distribution
twine check dist/*

# Upload to PyPI (requires PyPI account and token)
twine upload dist/*

# Or upload to Test PyPI first
twine upload --repository testpypi dist/*
```

#### Publish to npm (Metadata Wrapper)

```bash
# Ensure package.json is up to date
cat package.json

# Login to npm (if not already)
npm login

# Publish package
npm publish --access public

# Verify publication
npm view unifi-mcp-server
```

#### Publish to MCP Registry

```bash
# Install mcp-publisher
brew install mcp-publisher
# Or: curl -L "https://github.com/modelcontextprotocol/registry/releases/latest/download/mcp-publisher_$(uname -s | tr '[:upper:]' '[:lower:]')_$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/').tar.gz" | tar xz mcp-publisher && sudo mv mcp-publisher /usr/local/bin/

# Authenticate with GitHub (for io.github.enuno namespace)
mcp-publisher login github

# Publish to registry (requires npm package published first)
mcp-publisher publish

# Verify
curl "https://registry.modelcontextprotocol.io/v0.1/servers?search=io.github.enuno/unifi-mcp-server"
```

### Release Process

See [docs/RELEASE_PROCESS.md](docs/RELEASE_PROCESS.md) for the complete release workflow, including automated GitHub Actions, manual PyPI/npm publishing, and MCP registry submission.

### Configuration

#### Obtaining Your API Key

1. Log in to [UniFi Site Manager](https://unifi.ui.com)
2. Navigate to **Settings → Control Plane → Integrations**
3. Click **Create API Key**
4. **Save the key immediately** - it's only shown once!
5. Store it securely in your `.env` file

#### Configuration File

Create a `.env` file in the project root:

```env
# Required: Your UniFi API Key
UNIFI_API_KEY=your-api-key-here

# API Mode Selection (choose one):
# - 'local': Full access via local gateway (RECOMMENDED)
# - 'cloud-ea': Early Access cloud API (limited to statistics)
# - 'cloud-v1': Stable v1 cloud API (limited to statistics)
UNIFI_API_TYPE=local

# Local Gateway Configuration (for UNIFI_API_TYPE=local)
UNIFI_LOCAL_HOST=192.168.1.1
UNIFI_LOCAL_PORT=443
UNIFI_LOCAL_VERIFY_SSL=false

# Cloud API Configuration (for cloud-ea or cloud-v1)
# UNIFI_CLOUD_API_URL=https://api.ui.com

# Optional settings
UNIFI_DEFAULT_SITE=default

# Redis caching (optional - improves performance)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
# REDIS_PASSWORD=your-password  # If Redis requires authentication

# Webhook support (optional - for real-time events)
WEBHOOK_SECRET=your-webhook-secret-here

# Performance tracking with agnost.ai (optional - for analytics)
# Get your Organization ID from https://app.agnost.ai
# AGNOST_ENABLED=true
# AGNOST_ORG_ID=your-organization-id-here
# AGNOST_ENDPOINT=https://api.agnost.ai
# AGNOST_DISABLE_INPUT=false  # Set to true to disable input tracking
# AGNOST_DISABLE_OUTPUT=false # Set to true to disable output tracking
```

See `.env.example` for all available options.

### Running the Server

```bash
# Development mode with MCP Inspector
uv run mcp dev src/main.py

# Production mode
uv run python src/main.py
```

The MCP Inspector will be available at `http://localhost:5173` for interactive testing.

## Usage

### With Claude Desktop

Add to your Claude Desktop configuration (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

#### Option 1: Using PyPI Package (Recommended)

After installing via `pip install unifi-mcp-server`:

```json
{
  "mcpServers": {
    "unifi": {
      "command": "unifi-mcp-server",
      "env": {
        "UNIFI_API_KEY": "your-api-key-here",
        "UNIFI_API_TYPE": "local",
        "UNIFI_LOCAL_HOST": "192.168.1.1"
      }
    }
  }
}
```

For cloud API access, use:

```json
{
  "mcpServers": {
    "unifi": {
      "command": "unifi-mcp-server",
      "env": {
        "UNIFI_API_KEY": "your-api-key-here",
        "UNIFI_API_TYPE": "cloud-v1"
      }
    }
  }
}
```

#### Option 2: Using uv with PyPI Package

```json
{
  "mcpServers": {
    "unifi": {
      "command": "uvx",
      "args": ["unifi-mcp-server"],
      "env": {
        "UNIFI_API_KEY": "your-api-key-here",
        "UNIFI_API_TYPE": "local",
        "UNIFI_LOCAL_HOST": "192.168.1.1"
      }
    }
  }
}
```

#### Option 3: Using Docker

```json
{
  "mcpServers": {
    "unifi": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e",
        "UNIFI_API_KEY=your-api-key-here",
        "-e",
        "UNIFI_API_TYPE=cloud",
        "ghcr.io/enuno/unifi-mcp-server:latest"
      ]
    }
  }
}
```

**Important**: Do NOT use `-d` (detached mode) in MCP client configurations. The MCP client needs to maintain a persistent stdin/stdout connection to the container.

### With Cursor

Add to your Cursor MCP configuration (`mcp.json` via "View: Open MCP Settings → New MCP Server"):

#### Option 1: Using PyPI Package (Recommended)

After installing via `pip install unifi-mcp-server`:

```json
{
  "mcpServers": {
    "unifi-mcp": {
      "command": "unifi-mcp-server",
      "env": {
        "UNIFI_API_KEY": "your-api-key-here",
        "UNIFI_API_TYPE": "local",
        "UNIFI_LOCAL_HOST": "192.168.1.1",
        "UNIFI_LOCAL_VERIFY_SSL": "false"
      },
      "disabled": false
    }
  }
}
```

#### Option 2: Using uv with PyPI Package

```json
{
  "mcpServers": {
    "unifi-mcp": {
      "command": "uvx",
      "args": ["unifi-mcp-server"],
      "env": {
        "UNIFI_API_KEY": "your-api-key-here",
        "UNIFI_API_TYPE": "local",
        "UNIFI_LOCAL_HOST": "192.168.1.1"
      },
      "disabled": false
    }
  }
}
```

#### Option 3: Using Docker

```json
{
  "mcpServers": {
    "unifi-mcp": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "--name", "unifi-mcp-server",
        "-e", "UNIFI_API_KEY=your_unifi_api_key_here",
        "-e", "UNIFI_API_TYPE=local",
        "-e", "UNIFI_LOCAL_HOST=192.168.1.1",
        "-e", "UNIFI_LOCAL_VERIFY_SSL=false",
        "ghcr.io/enuno/unifi-mcp-server:latest"
      ],
      "disabled": false
    }
  }
}
```

**Configuration Notes:**

- Replace `UNIFI_API_KEY` with your actual UniFi API key
- For local gateway access, set `UNIFI_API_TYPE=local` and provide `UNIFI_LOCAL_HOST`
- For cloud API access, use `UNIFI_API_TYPE=cloud-v1` or `cloud-ea`
- After saving, restart Cursor to activate the server
- Invoke tools in the Chat sidebar (e.g., "List my UniFi devices")

### With Other MCP Clients

The UniFi MCP Server works with any MCP-compatible client. Here are generic configuration patterns:

#### Using the Installed Command

After installing from PyPI (`pip install unifi-mcp-server`):

```json
{
  "mcpServers": {
    "unifi": {
      "command": "unifi-mcp-server",
      "env": {
        "UNIFI_API_KEY": "your-api-key-here",
        "UNIFI_API_TYPE": "local",
        "UNIFI_LOCAL_HOST": "192.168.1.1"
      }
    }
  }
}
```

#### Using uvx (Run from PyPI without installation)

```json
{
  "mcpServers": {
    "unifi": {
      "command": "uvx",
      "args": ["unifi-mcp-server"],
      "env": {
        "UNIFI_API_KEY": "your-api-key-here",
        "UNIFI_API_TYPE": "local",
        "UNIFI_LOCAL_HOST": "192.168.1.1"
      }
    }
  }
}
```

#### Using Python Module Directly

```json
{
  "mcpServers": {
    "unifi": {
      "command": "python3",
      "args": ["-m", "src.main"],
      "env": {
        "UNIFI_API_KEY": "your-api-key-here",
        "UNIFI_API_TYPE": "local",
        "UNIFI_LOCAL_HOST": "192.168.1.1"
      }
    }
  }
}
```

**Environment Variables (All Clients):**

- `UNIFI_API_KEY` (required): Your UniFi API key from unifi.ui.com
- `UNIFI_API_TYPE` (required): `local`, `cloud-v1`, or `cloud-ea`
- **For Local Gateway API**:
  - `UNIFI_LOCAL_HOST`: Gateway IP (e.g., 192.168.1.1)
  - `UNIFI_LOCAL_PORT`: Gateway port (default: 443)
  - `UNIFI_LOCAL_VERIFY_SSL`: SSL verification (default: false)
- **For Cloud APIs**:
  - `UNIFI_CLOUD_API_URL`: Cloud API URL (default: <https://api.ui.com>)
  - `UNIFI_DEFAULT_SITE`: Default site ID (default: default)

### Programmatic Usage

```python
from mcp import MCP
import asyncio

async def main():
    mcp = MCP("unifi-mcp-server")

    # List all devices
    devices = await mcp.call_tool("list_devices", {
        "site_id": "default"
    })

    for device in devices:
        print(f"{device['name']}: {device['status']}")

    # Get network information via resource
    networks = await mcp.read_resource("sites://default/networks")
    print(f"Networks: {len(networks)}")

    # Create a guest WiFi network with VLAN isolation
    wifi = await mcp.call_tool("create_wlan", {
        "site_id": "default",
        "name": "Guest WiFi",
        "security": "wpapsk",
        "password": "GuestPass123!",
        "is_guest": True,
        "vlan_id": 100,
        "confirm": True  # Required for safety
    })
    print(f"Created WiFi: {wifi['name']}")

    # Get DPI statistics for top bandwidth users
    top_apps = await mcp.call_tool("list_top_applications", {
        "site_id": "default",
        "limit": 5,
        "time_range": "24h"
    })

    for app in top_apps:
        gb = app['total_bytes'] / 1024**3
        print(f"{app['application']}: {gb:.2f} GB")

    # Create Zone-Based Firewall zones (UniFi Network 9.0+)
    lan_zone = await mcp.call_tool("create_firewall_zone", {
        "site_id": "default",
        "name": "LAN",
        "description": "Trusted local network",
        "confirm": True
    })

    iot_zone = await mcp.call_tool("create_firewall_zone", {
        "site_id": "default",
        "name": "IoT",
        "description": "Internet of Things devices",
        "confirm": True
    })

    # Set zone-to-zone policy (LAN can access IoT, but IoT cannot access LAN)
    await mcp.call_tool("update_zbf_policy", {
        "site_id": "default",
        "source_zone_id": lan_zone["_id"],
        "destination_zone_id": iot_zone["_id"],
        "action": "accept",
        "confirm": True
    })

asyncio.run(main())
```

## API Documentation

See [docs/API.md](docs/API.md) for complete API documentation, including:

- Available MCP tools
- Resource URI schemes
- Request/response formats
- Error handling
- Examples

## Development

### Setup Development Environment

```bash
# Install development dependencies
uv pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
pre-commit install --hook-type commit-msg
```

### Running Tests

```bash
# Run all tests
pytest tests/unit/

# Run with coverage report
pytest tests/unit/ --cov=src --cov-report=html --cov-report=term-missing

# Run specific test file
pytest tests/unit/test_zbf_tools.py -v

# Run tests for new v0.2.0 features
pytest tests/unit/test_new_models.py tests/unit/test_zbf_tools.py tests/unit/test_traffic_flow_tools.py

# Run only unit tests (fast)
pytest -m unit

# Run only integration tests (requires UniFi controller)
pytest -m integration
```

**Current Test Coverage (v0.2.0)**:

- **Overall**: 78.18% (990 tests passing)
- **Total Statements**: 6,105 statements, 4,865 covered
- **Branch Coverage**: 75.03%

[![Coverage Sunburst](https://codecov.io/github/enuno/unifi-mcp-server/graphs/sunburst.svg?token=ZD314B59CE)](https://codecov.io/github/enuno/unifi-mcp-server)

**By Module Category:**

- **Models**: 98%+ coverage (Excellent)
- **Core Tools**: 90-100% coverage (Excellent)
- **v0.2.0 Features**: 70-96% coverage (Good to Excellent)
  - Topology: 95.83% (29 tests)
  - Backup & Restore: 86.32% (10 tests)
  - Multi-Site Aggregation: 92.95% (10 tests)
  - QoS: 82.43% (46 tests)
  - RADIUS: 69.77% (17 tests)
- **Utilities**: 90%+ coverage (Excellent)

**Top Coverage Performers** (>95%):

- clients.py: 98.72%
- devices.py: 98.44%
- device_control.py: 99.10%
- topology.py: 95.83% ⭐ (v0.2.0)
- vouchers.py: 96.36%
- firewall.py: 96.11%

See [VERIFICATION_REPORT.md](VERIFICATION_REPORT.md) for complete coverage details and [TESTING_PLAN.md](TESTING_PLAN.md) for testing strategy.

### Code Quality

```bash
# Format code
black src/ tests/
isort src/ tests/

# Lint code
ruff check src/ tests/ --fix

# Type check
mypy src/

# Run all pre-commit checks
pre-commit run --all-files
```

### Testing with MCP Inspector

```bash
# Start development server with inspector
uv run mcp dev src/main.py

# Open http://localhost:5173 in your browser
```

## Project Structure

```
unifi-mcp-server/
├── .github/
│   └── workflows/          # CI/CD pipelines (CI, security, release)
├── .claude/
│   └── commands/          # Custom slash commands for development
├── src/
│   ├── main.py            # MCP server entry point (77 tools registered)
│   ├── cache.py           # Redis caching implementation
│   ├── config/            # Configuration management
│   ├── api/               # UniFi API client with rate limiting
│   ├── models/            # Pydantic data models
│   │   └── zbf.py         # Zone-Based Firewall models
│   ├── tools/             # MCP tool definitions
│   │   ├── clients.py     # Client query tools
│   │   ├── devices.py     # Device query tools
│   │   ├── networks.py    # Network query tools
│   │   ├── sites.py       # Site query tools
│   │   ├── firewall.py    # Firewall management (Phase 4)
│   │   ├── firewall_zones.py  # Zone-Based Firewall zone management (v0.1.4)
│   │   ├── zbf_matrix.py  # Zone-Based Firewall policy matrix (v0.1.4)
│   │   ├── network_config.py  # Network configuration (Phase 4)
│   │   ├── device_control.py  # Device control (Phase 4)
│   │   ├── client_management.py  # Client management (Phase 4)
│   │   ├── wifi.py        # WiFi/SSID management (Phase 5)
│   │   ├── port_forwarding.py  # Port forwarding (Phase 5)
│   │   └── dpi.py         # DPI statistics (Phase 5)
│   ├── resources/         # MCP resource definitions
│   ├── webhooks/          # Webhook receiver and handlers (Phase 5)
│   └── utils/             # Utility functions and validators
├── tests/
│   ├── unit/              # Unit tests (213 tests, 37% coverage)
│   ├── integration/       # Integration tests (planned)
│   └── performance/       # Performance benchmarks (planned)
├── docs/                  # Additional documentation
│   └── AI-Coding/         # AI coding guidelines
├── .env.example           # Environment variable template
├── pyproject.toml         # Project configuration
├── README.md              # This file
├── docs/                  # Documentation (API.md, CONTRIBUTING.md, SECURITY.md, plans, reports)
└── LICENSE                # Apache 2.0 License
```

## Contributing

We welcome contributions from both human developers and AI coding assistants! Please see:

- [CONTRIBUTING.md](docs/CONTRIBUTING.md) - Contribution guidelines
- [AGENTS.md](docs/AGENTS.md) - AI agent-specific guidelines
- [AI_CODING_ASSISTANT.md](docs/AI-Coding/AI_CODING_ASSISTANT.md) - AI coding standards
- [AI_GIT_PRACTICES.md](docs/AI-Coding/AI_GIT_PRACTICES.md) - AI Git practices

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Run tests and linting: `pytest && pre-commit run --all-files`
5. Commit with conventional commits: `feat: add new feature`
6. Push and create a pull request

## Security

Security is a top priority. Please see [SECURITY.md](SECURITY.md) for:

- Reporting vulnerabilities
- Security best practices
- Supported versions

**Never commit credentials or sensitive data!**

## Roadmap

### Version 0.2.0 (Current - Complete ✅ 2026-01-25)

**All 7 Feature Phases Complete - 74 MCP Tools**

**Phase 3: Read-Only Operations (16 tools)**

- [x] Device management (list, details, statistics, search by type)
- [x] Client management (list, details, statistics, search)
- [x] Network information (details, VLANs, subnets, statistics)
- [x] Site management (list, details, statistics)
- [x] MCP resources (sites, devices, clients, networks)

**Phase 4: Mutating Operations with Safety (13 tools)**

- [x] Firewall rule management (create, update, delete)
- [x] Network configuration (create, update, delete networks/VLANs)
- [x] Device control (restart, locate, upgrade)
- [x] Client management (block, unblock, reconnect)
- [x] Safety mechanisms (confirmation, dry-run, audit logging)

**Phase 5: Advanced Features (11 tools)**

- [x] WiFi/SSID management (create, update, delete, statistics)
- [x] Port forwarding configuration (create, delete, list)
- [x] DPI statistics (site-wide, top apps, per-client)
- [x] Redis caching with automatic invalidation
- [x] Webhook support for real-time events

**Phase 6: Zone-Based Firewall (12 working tools)**

- [x] Zone management (create, update, delete, list, assign networks) - 7 tools ✅ WORKING
- [x] **Zone-to-zone policies via Firewall Policies v2 API** - 5 tools ✅ WORKING (PR #13)
- [x] Legacy zone matrix endpoints - 5 tools ❌ ENDPOINTS DO NOT EXIST (use v2 API instead)
- [x] Application blocking per zone (DPI-based blocking) - 2 tools ❌ ENDPOINTS DO NOT EXIST
- [x] Zone statistics and monitoring - 1 tool ❌ ENDPOINT DOES NOT EXIST
- [x] Type-safe Pydantic models for ZBF and Firewall Policies
- [x] Comprehensive unit tests (84% coverage)
- [x] Endpoint verification on U7 Express and UDM Pro (v10.0.156)

**Phase 7: Traffic Flow Monitoring (15 tools) ✅ COMPLETE**

- [x] Real-time traffic flow monitoring and analysis
- [x] Flow filtering by IP, protocol, application, time range
- [x] Connection state tracking (active, closed, timed-out)
- [x] Client traffic aggregation with top applications/destinations
- [x] Bandwidth rate calculations for streaming flows
- [x] Security quick-response capabilities (block suspicious IPs)
- [x] Type-safe Pydantic models for traffic flows
- [x] Comprehensive unit tests (86.62% coverage)
- [x] Advanced analytics and reporting capabilities

**ZBF Implementation Notes (Verified 2025-11-18):**

- ✅ Zone CRUD operations work (local gateway API only)
- ✅ **Zone-to-zone policies work via Firewall Policies v2 API** (local gateway API only)
- ❌ Legacy zone matrix endpoints NOT available via API (use v2 API instead)
- ❌ Application blocking per zone NOT available via API
- ❌ Zone statistics NOT available via API
- See ZBF_STATUS.md for complete details and examples

**Phase 1: QoS Enhancements (11 tools) ✅**

- [x] QoS profile management (CRUD operations)
- [x] Reference profiles and ProAV templates
- [x] Traffic routing with time-based schedules
- [x] Application-based QoS configuration
- [x] Coverage: 82.43% (46 tests passing)

**Phase 2: Backup & Restore (8 tools) ✅**

- [x] Manual and automated backup creation
- [x] Backup listing, download, and verification
- [x] Backup restore functionality
- [x] Automated scheduling with cron expressions
- [x] Cloud synchronization tracking
- [x] Coverage: 86.32% (10 tests passing)

**Phase 3: Multi-Site Aggregation (4 tools) ✅**

- [x] Cross-site device and client analytics
- [x] Site health monitoring with scoring
- [x] Side-by-side site comparison
- [x] Consolidated reporting across locations
- [x] Coverage: 92.95% (10 tests passing)

**Phase 4: ACL & Traffic Filtering (7 tools) ✅**

- [x] Layer 3/4 access control list management
- [x] Traffic matching lists (IP, MAC, domain, port)
- [x] Firewall policy automation
- [x] Rule ordering and priority
- [x] Coverage: 89.30-93.84%

**Phase 5: Site Management Enhancements (9 tools) ✅**

- [x] Multi-site provisioning and configuration
- [x] Site-to-site VPN setup
- [x] Device migration between sites
- [x] Advanced site settings management
- [x] Configuration export for backup
- [x] Coverage: 92.95% (10 tests passing)

**Phase 6: RADIUS & Guest Portal (6 tools) ✅**

- [x] RADIUS profile configuration (802.1X)
- [x] RADIUS accounting server support
- [x] Guest portal customization
- [x] Hotspot billing and voucher management
- [x] Session timeout and redirect control
- [x] Coverage: 69.77% (17 tests passing)

**Phase 7: Network Topology (5 tools) ✅**

- [x] Complete topology graph retrieval
- [x] Multi-format export (JSON, GraphML, DOT)
- [x] Device interconnection mapping
- [x] Port-level connection tracking
- [x] Network depth analysis
- [x] Coverage: 95.83% (29 tests passing)

**Quality Achievements:**

- [x] 990 tests passing (78.18% coverage)
- [x] 18/18 CI/CD checks passing
- [x] Zero security vulnerabilities
- [x] 30+ AI assistant example prompts
- [x] Comprehensive documentation (docs/VERIFICATION_REPORT.md, docs/API.md)

**Total: 74 MCP tools + Comprehensive documentation and verification**

### Version 0.3.0 (Future - Planned)

- [ ] VPN Management (site_vpn.py - 0% coverage currently)
- [ ] WAN Management (wans.py - 0% coverage currently)
- [ ] Enhanced ZBF Matrix (zbf_matrix.py - improve 65% coverage)
- [ ] Integration tests for caching and webhooks
- [ ] Performance benchmarks and optimization
- [ ] Additional DPI analytics (historical trends)
- [ ] Bulk device/client operations
- [ ] Advanced traffic flow analytics

### Version 1.0.0 (Future)

- [ ] Complete UniFi API coverage (remaining endpoints)
- [ ] Advanced analytics dashboard
- [ ] VPN configuration management
- [ ] Alert and notification management
- [ ] Bulk operations for devices
- [ ] Traffic shaping and QoS management

## Acknowledgments

This project is inspired by and builds upon:

- [sirkirby/unifi-network-mcp](https://github.com/sirkirby/unifi-network-mcp) - Reference implementation
- [MakeWithData UniFi MCP Guide](https://www.makewithdata.tech/p/build-a-mcp-server-for-ai-access) - Tutorial and guide
- [Anthropic MCP](https://github.com/anthropics/mcp) - Model Context Protocol specification
- [FastMCP](https://github.com/jlowin/fastmcp) - MCP server framework

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/seathegood/unifi-mcp-server/issues)
- **Discussions**: [GitHub Discussions](https://github.com/seathegood/unifi-mcp-server/discussions)
- **Documentation**: See [docs/API.md](docs/API.md) and other docs in this repository

## Links

- **Repository**: <https://github.com/seathegood/unifi-mcp-server>
- **Releases**: <https://github.com/seathegood/unifi-mcp-server/releases>
- **Docker Registry**: <https://ghcr.io/enuno/unifi-mcp-server> *(upstream images; update when fork registry is published)*
- **npm Package**: <https://www.npmjs.com/package/unifi-mcp-server>
- **MCP Registry**: Search for `io.github.enuno/unifi-mcp-server` at <https://registry.modelcontextprotocol.io>
- **Documentation**: [docs/API.md](docs/API.md) | [docs/VERIFICATION_REPORT.md](docs/VERIFICATION_REPORT.md)
- **UniFi Official**: <https://www.ui.com/>

## 🌟 Star History

If you find this project useful, please consider starring it on GitHub to help others discover it!

[![Star History Chart](https://api.star-history.com/svg?repos=enuno/unifi-mcp-server&type=date&legend=top-left)](https://www.star-history.com/#enuno/unifi-mcp-server&type=date&legend=top-left)

---

Made with ❤️ for the UniFi and AI communities
