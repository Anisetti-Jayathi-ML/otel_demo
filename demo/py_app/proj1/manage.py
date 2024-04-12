#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import logging
import base64
import json

# for traces
from opentelemetry.instrumentation.sqlite3 import SQLite3Instrumentor
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)


# Set the environment variables for the OTLP exporter
os.environ['OTEL_EXPORTER_OTLP_TRACES_TIMEOUT'] = '5000'  # Set the timeout in milliseconds
os.environ['OTEL_EXPORTER_OTLP_TRACES_PROTOCOL'] = 'https'  # Set the protocol (http or https)
#os.environ['OTEL_EXPORTER_OTLP_TRACES_HEADERS'] = '{"custom-header": "header-value"}' # To Set custom headers
os.environ['OTEL_EXPORTER_OTLP_TRACES_ENDPOINT'] = 'https://otelforwarderuser:Forwarder-Snappyflow-Agent%407%24@127.0.0.1:9595/otel-service/export/trace'  # Set the endpoint URL
# os.environ['OTEL_EXPORTER_OTLP_TRACES_COMPRESSION'] = 'gzip'  # Set the compression method (e.g., gzip)
os.environ['OTEL_EXPORTER_OTLP_TRACES_CERTIFICATE'] = '/opt/sfagent/otel-trace-data-forwarder/certs/ca.pem'  # Set the certificate path

# TODO: Add project name, Application name and Profile key values
resource = Resource(attributes={
    "configFile" : "/home/administrator/demo/py_app/proj1/env.conf"
})

otlp_exporter = OTLPSpanExporter()

trace.set_tracer_provider(TracerProvider(resource=resource))

trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(otlp_exporter)
)


SQLite3Instrumentor().instrument()


# for logs



def main():
    """Run administrative tasks."""
    
    
    

    # DjangoInstrumentor().instrument(is_sql_commentor_enabled=True)
    
    DjangoInstrumentor().instrument()
    #tracing.trace()
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
 #   logger_provider.shutdown()


if __name__ == '__main__':

#with tracer.start_as_current_span("my_span_name"):
    
    main()

