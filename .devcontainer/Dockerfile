FROM mcr.microsoft.com/devcontainers/base:trixie
RUN apt-get update \
    && apt-get install -y --no-install-recommends ripgrep jq \
    && rm -rf /var/lib/apt/lists/*
USER vscode
RUN curl -LsSf https://astral.sh/uv/0.12.23/install.sh | sh
ENV PATH="/home/vscode/.local/bin:${PATH}"
