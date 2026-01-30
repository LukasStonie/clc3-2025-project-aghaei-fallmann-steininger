# Use the official Python 3.11 image as base
FROM mcr.microsoft.com/devcontainers/python:3.11-bullseye

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_VERSION=0.5.11


# Install uv - the fast Python package installer
# Using pip as the installation method since it's more reliable in restricted environments
RUN pip install --no-cache-dir uv==${UV_VERSION}

# Install additional system dependencies that might be needed for Python packages
RUN rm -f /etc/apt/sources.list.d/yarn.list \
    && apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
        git \
        build-essential \
        libssl-dev \
        libffi-dev \
        python3-dev \
        libqt5widgets5 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user 'vscode' if it doesn't exist
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# The base image already has vscode user, so we just ensure the proper setup
RUN if ! id -u ${USERNAME} > /dev/null 2>&1; then \
        groupadd --gid $USER_GID $USERNAME \
        && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME; \
    fi

# Switch to non-root user
USER ${USERNAME}

# Set working directory
WORKDIR /workspace

# Default command
CMD ["/bin/bash"]
