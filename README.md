# Astrotel

Astrotel sending OpenTelemetry tracing and logging integration for Python applications into Signoz, Jaeger, OTEL Collector,... with support for FastAPI, Celery, MCP,... application


## Installation

Install with pip (requires Python 3.12+):

```sh
pip install astrotel[fastapi]
```

For FastAPI support:

```sh
pip install astrotel[fastapi]
```

## Usage

### Basic Usage

```python
from astrotel.provider.fastapi import FastAPIOpentelemetryTracing
from fastapi import FastAPI

app = FastAPI()
tracer = FastAPIOpentelemetryTracing()
tracer.configure_tracing(app)
```

### Logging Integration

```python
import logging

tracer = FastAPIOpentelemetryTracing()
logging_handler = tracer.configure_logging_handler()

# Attach handler to root logger
logging.basicConfig(
    level=logging.INFO, 
    handlers=[logging_handler, logging.StreamHandler()]  # also keep console logs
)

# Attach handler to FastAPI's logger too
uvicorn_logger = logging.getLogger("uvicorn")
uvicorn_logger.addHandler(logging_handler)

uvicorn_logger = logging.getLogger("uvicorn.access")
uvicorn_logger.addHandler(logging_handler)

fastapi_logger = logging.getLogger("fastapi")
fastapi_logger.addHandler(logging_handler)
```

## Configuration

You can configure Astrotel via environment variables or by creating environment variables:

### Meaning
- `OTEL_SERVICE_NAME`: Set service name
- `OTEL_DEPLOYMENT_ENVIRONMENT`: Set deployment environment name
- `OTEL_MODE`: Send to exporter by `http` or `grpc`
- `OTEL_GRPC_ENDPOINT`: gRPC OTEL collector endpoint (default: `http://localhost:4317`)
- `OTEL_HTTP_ENDPOINT`: HTTP OTEL collector endpoint (default: `http://localhost:4318`)
- `OTEL_LOGS_SHIP_LEVEL`: Minimum log level to ship (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`)

### For example

```
OTEL_SERVICE_NAME=my-service
OTEL_DEPLOYMENT_ENVIRONMENT=production
OTEL_MODE=grpc
OTEL_GRPC_ENDPOINT=http://otel-collector:4317
OTEL_HTTP_ENDPOINT=http://otel-collector:4318
OTEL_LOGS_SHIP_LEVEL=INFO
```

## Documentation

See the [docs/](docs/index.rst) or build the documentation locally:

```sh
make -C docs html
```

## Development

- Lint: `make lint`
- Format: `make format`

## License
MIT