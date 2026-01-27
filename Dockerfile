# Multi-stage build for smaller final image
FROM python:3.11-slim AS builder

WORKDIR /build

# Copy only necessary files for installation
COPY pyproject.toml MANIFEST.in README.md LICENSE ./
COPY junit_html_report_generator/ ./junit_html_report_generator/

# Install the package
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir build && \
    python -m build && \
    pip wheel --no-cache-dir --wheel-dir /build/wheels dist/*.whl

# Final stage
FROM python:3.11-slim

LABEL org.opencontainers.image.source="https://github.com/gorkalertxundi/junit-report-generator"
LABEL org.opencontainers.image.description="CLI tool to convert JUnit XML test results into HTML dashboards"
LABEL org.opencontainers.image.licenses="MIT"

WORKDIR /workspace

# Copy wheels from builder and install
COPY --from=builder /build/wheels /tmp/wheels
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir /tmp/wheels/*.whl && \
    rm -rf /tmp/wheels

# Verify installation
RUN junit-html-report-generator --list-templates

# Set entrypoint to the CLI tool
ENTRYPOINT ["junit-html-report-generator"]

# Default command shows help
CMD ["--help"]
