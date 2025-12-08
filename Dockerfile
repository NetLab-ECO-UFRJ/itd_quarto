# Multi-stage build for Quarto ebook
FROM ghcr.io/astral-sh/uv:python3.11-bookworm AS builder

# Install Quarto
ARG QUARTO_VERSION=1.6.42
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-amd64.deb && \
    dpkg -i quarto-${QUARTO_VERSION}-linux-amd64.deb && \
    rm quarto-${QUARTO_VERSION}-linux-amd64.deb

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock ./
COPY . .

# Install Python dependencies with uv
RUN uv sync --frozen

# Render the Quarto book
RUN uv run quarto render && \
    ls -la /app/_output && \
    test -f /app/_output/index.html || (echo "ERROR: Quarto render failed or index.html not found" && exit 1)

# Production stage with nginx
FROM nginx:alpine

# Install wget and apache2-utils for healthcheck and htpasswd
RUN apk add --no-cache wget apache2-utils

# Create htpasswd file with admin:password
RUN htpasswd -cb /etc/nginx/.htpasswd admin laguinho

# Copy rendered output to nginx html directory
COPY --from=builder /app/_output/. /usr/share/nginx/html/

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
