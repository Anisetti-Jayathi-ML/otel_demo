# opentelemetry_config.py


# for logs
# This custom logger configuration sets up OpenTelemetry to send traces to backend using the OTLP exporter.

from opentelemetry import trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.http._log_exporter import (
    OTLPLogExporter,
)
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource

import logging
import os

def configure_logging():

    # Set the environment variables for the OTLP exporter
    os.environ['OTEL_EXPORTER_OTLP_LOGS_TIMEOUT'] = '5000'  # Set the timeout in milliseconds
    os.environ['OTEL_EXPORTER_OTLP_LOGS_PROTOCOL'] = 'https'  # Set the protocol (http or https)
    #os.environ['OTEL_EXPORTER_OTLP_TRACES_HEADERS'] = '{"custom-header": "header-value"}' # To Set custom headers
    os.environ['OTEL_EXPORTER_OTLP_LOGS_ENDPOINT'] = 'https://otelforwarderuser:Forwarder-Snappyflow-Agent%407%24@127.0.0.1:9595/otel-service/export/log'  # Set the endpoint URL
    # os.environ['OTEL_EXPORTER_OTLP_TRACES_COMPRESSION'] = 'gzip'  # Set the compression method (e.g., gzip)
    os.environ['OTEL_EXPORTER_OTLP_LOGS_CERTIFICATE'] = '/opt/sfagent/otel-trace-data-forwarder/certs/ca.pem'  # Set the certificate path

    logger_provider = LoggerProvider(
        resource=Resource.create(
            {
            	"configFile":"/home/administrator/demo/py_app_logs/proj1/env.conf"
       
            }
        ),
    )
    set_logger_provider(logger_provider)

    exporter = OTLPLogExporter()
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
    
    handler = LoggingHandler(logger_provider=logger_provider)

# Attach OTLP handler to root logger

    logging.getLogger().addHandler(handler)

   # TODO : Add level as required
    logging.getLogger().setLevel(logging.INFO)

    logging.info("configured logging")


configure_logging()