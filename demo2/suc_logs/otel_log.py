import logging
from opentelemetry import trace
from opentelemetry.log import LogRecord, LogRecordProcessor, LoggingHandler
from opentelemetry.sdk.logs import ConsoleLogExporter, SimpleLoggerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider

# Create a logger provider with a ConsoleLogExporter
logger_provider = SimpleLoggerProvider(
    resource=Resource(
        service="my-service",
        attributes={
            "my-attribute": "my-value",
        },
    ),
    log_record_processors=[ConsoleLogExporter()],
)

# Set the logger provider as the root logger provider
logger_provider.set_logger("otel_logger")

# Create an OTLPLogExporter
exporter = OTLPLogExporter(
    endpoint="https://otelforwarderuser:Forwarder-Snappyflow-Agent%407%24@127.0.0.1:9595/otel-service/export/trace",
    headers={
        "custom-header": "header-value",
    },
)

# Add the exporter to the logger provider
logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))

class OpenTelemetryHandler(LoggingHandler):
    def __init__(self, logger_provider):
        super().__init__(logger_provider=logger_provider)

    def emit(self, record):
        record = LogRecord(
            body=json.dumps(record.__dict__),
            name=record.name,
            severity_number=record.levelno,
            time=trace.as_datetime(record.created),
            attributes=record.args,
        )
        super().emit(record)