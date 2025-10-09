from abc import ABC, abstractmethod
import logging

from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter as GrpcLogExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter as GrpcTraceExporter,
)
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter as HttpLogExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter as HttpTraceExporter,
)
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, SpanExporter

from astrotel.config import AstrotelSettings, astrotel_default
from astrotel.error import InvalidOtelModeError


class OtelTracingBase(ABC):
    _settings: AstrotelSettings
    tracer_provider: TracerProvider
    logger_provider: LoggerProvider
    def __init__(
        self,
        settings: AstrotelSettings = astrotel_default
    ):
        self._settings = settings
        # Init resource with name and deploy environment
        resource = Resource.create({
            'service.name': settings.service_name,
            'deployment.environment': settings.deployment_environment,
        })

        # Init self.tracer_provider
        self.tracer_provider = TracerProvider(resource=resource)
        trace_exporter = self._get_trace_exporter()
        self.tracer_provider.add_span_processor(BatchSpanProcessor(trace_exporter))

        # Init self.logger_provider
        self.logger_provider = LoggerProvider(resource=resource)
        log_exporter = self._get_logs_exporter()
        self.logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))

    def _get_trace_exporter(self) -> SpanExporter:
        settings = self._settings
        """Init trace exporter"""
        if settings.mode == 'grpc':
            exporter = GrpcTraceExporter(endpoint=settings.grpc_endpoint, insecure=True)
        elif settings.mode == 'http':
            exporter = HttpTraceExporter(endpoint=settings.http_endpoint)
        else:
            raise InvalidOtelModeError(
                f"Unsupported OTEL mode: {settings.mode!r}. Expected 'grpc' or 'http'."
            )
        return exporter

    def _get_logs_exporter(self) -> SpanExporter:
        """Init logs exporter"""
        settings = self._settings
        if settings.mode == 'grpc':
            exporter = GrpcLogExporter(endpoint=settings.grpc_endpoint, insecure=True)
        elif settings.mode == 'http':
            exporter = HttpLogExporter(endpoint=settings.http_endpoint)
        else:
            raise InvalidOtelModeError(
                f"Unsupported OTEL mode: {settings.mode!r}. Expected 'grpc' or 'http'."
            )
        return exporter

    @abstractmethod
    def configure_tracing(self):
        pass

    def configure_logging_handler(self) -> LoggingHandler:
        level = getattr(logging, self._settings.logs_ship_level, logging.INFO)
        return LoggingHandler(level=level, logger_provider=self.logger_provider)
