# DevContainer Setup

This directory contains the configuration for a VS Code Dev Container with Python and uv.

## What's Included

- **Python 3.11**: Latest stable Python version
- **uv**: Fast Python package installer and resolver
- **VS Code Extensions**:
  - Python
  - Pylance
  - Black Formatter
  - Ruff

## Getting Started

1. Install [VS Code](https://code.visualstudio.com/) and the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
2. Open this repository in VS Code
3. When prompted, click "Reopen in Container" (or run the command "Dev Containers: Reopen in Container")
4. Wait for the container to build (first time only)

## Using uv

uv is a fast Python package installer and resolver. Here are some common commands:

### Install dependencies
```bash
uv pip install -r requirements.txt
```

### Install a package
```bash
uv pip install <package-name>
```

### Install dev dependencies
```bash
uv pip install -e ".[dev]"
```

### Create a virtual environment
```bash
uv venv
```

### Install project in editable mode with dependencies
```bash
uv pip install -e .
```

## Project Structure

- `.devcontainer/`: DevContainer configuration files
- `pyproject.toml`: Python project configuration and dependencies
- `README.md`: Project documentation

## Troubleshooting

If you encounter issues:

1. Rebuild the container: Command Palette → "Dev Containers: Rebuild Container"
2. Check the build logs for errors
3. Ensure Docker is running

For more information, see the [VS Code Dev Containers documentation](https://code.visualstudio.com/docs/devcontainers/containers).
