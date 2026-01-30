# Use the official Python 3.11 image as base
FROM mcr.microsoft.com/devcontainers/python:3.11-bullseye AS base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_VERSION=0.5.11

# Set working directory
WORKDIR /workspace

# Install uv
RUN pip install --no-cache-dir uv==${UV_VERSION}

# Install additional system dependencies
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

# Create/Configure non-root user 'vscode'
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN if ! id -u ${USERNAME} > /dev/null 2>&1; then \
        groupadd --gid $USER_GID $USERNAME \
        && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME; \
    fi

RUN chown -R $USERNAME:$USERNAME /workspace

# Switch to non-root user
USER ${USERNAME}

COPY --chown=$USERNAME:$USERNAME pyproject.toml uv.lock ./


RUN uv sync --no-install-project && uv cache prune --ci

ENV VIRTUAL_ENV=/workspace/.venv \
    PATH="/workspace/.venv/bin:$PATH"

# Copy the rest of the application code
COPY --chown=$USERNAME:$USERNAME . .


# Default command
CMD ["/bin/bash"]

FROM base AS runtime

CMD ["uvicorn", "clc3_project.backend.api_endpoints:app", "--host", "0.0.0.0", "--port", "8000"]