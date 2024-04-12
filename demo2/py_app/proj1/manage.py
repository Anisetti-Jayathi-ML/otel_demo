#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import logging
import base64
import json

# for traces

from opentelemetry.instrumentation.sqlite3 import SQLite3Instrumentor
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
from Crypto.Cipher import AES
from opentelemetry.instrumentation.django import DjangoInstrumentor


os.environ['OTEL_EXPORTER_OTLP_TRACES_ENDPOINT'] = 'https://otelforwarderuser:Forwarder-Snappyflow-Agent%407%24@127.0.0.1:9595/otel-service/export/trace'  # Set the endpoint URL
os.environ['OTEL_EXPORTER_OTLP_TRACES_CERTIFICATE'] = '/opt/sfagent/otel-trace-data-forwarder/certs/ca.pem'  # Set the certificate path
# os.environ['OTEL_EXPORTER_OTLP_LOGS_CERTIFICATE'] = '/opt/sfagent/otel-trace-data-forwarder/certs/ca.pem'  # Set the certificate path
# os.environ['OTEL_EXPORTER_OTLP_TRACES_CERTIFICATE'] = True
# print(os.environ.get('SNAPPYFLOW_PROJECTNAME'))
# print(os.environ.get('OTEL_EXPORTER_OTLP_TRACES_ENDPOINT'))
# print(os.environ.get('OTEL_EXPORTER_OTLP_TRACES_CERTIFICATE'))
resource = Resource(attributes={
    #service name appears in dashboard
    # "service.name": "test-project",
    # "snappyflow/projectname" : "Banking",
    # "snappyflow/appname": "flowlogs",
    # "snappyflow/profilekey": "RLgmVLU7Vzi9mtbO6hKxtuKnXeU1/3OrxKu0dJqOCtq9TSHzCGBH0t/h7y0Lf4E6RhGu/RxWCZUTZ08tDKkEbFRVIZrPgwDYEketyBkiFEhJ7Gw1bFqKPqMk+9ZuHbOKesk/5TrSLQDK+S+OdI23mRvwqkaXlFoy5ifIdpDYaYP0yh1XxE7zEvEgCwAzyfujd08NIndes1sNXdVjBuNmnVvDuI6XXHx1YhBnfwpQZnpQXe964bgo4FBvG2MGhiEw6fv4YjRytq4uxMJQ/UmkO8PCa6YyW7kqI79OxWmF0gt4SqJ9g1t/rAKoYfAWCy1+P0I+6Gpz2uZ90rCDQMW7J/wyVZwGt+jUEG+dHgalLKWCrUKwSnbFzuBORaaYiCwyDCTcPeOPm8Y0n9uradBJsbVVFJnrPt6OTVI/Pb/JHHOlH+eJgLN59QamqujliZRVZoWmKTjiHWVHTSJUKBnzoZlwPjL/5uMilz9tKQfPoUrXvPr8UIWW6AauDETYB5K+TipBr9GLmjmKCPZZb6iZR0S+Y8QlXcqcA3GOyfERul6hqYnC5Zk744YCFaGygwvFZlOl4SdfkGJ8w9eCsQ/wMx+JEN0ZN7MTTU1zYsgek8Qdj08uuOymtuKTC2+LvIct68fTk+/l5WEwTJbtShlxPM13vMXjy88l5M22lWgvI1qU4NH45AlG8ETDDDNQtjg9dqbfhqfoPj1DMHuMeLl3maDoUlgvpuffE9PNJX3HVVPZNr1SmRyNX7mmvZJrveBLjFyTgNZWMKsW2T15OBIRIvin+XdaLDWG8lxRmVEY3GoaUxU4MzrtUhcoWG3LoPa76WfAZEY97DI2H2uT7Z/cP+DogbNwgtcHDey9DuvAanMka8x8u3HEs8tqABYejJQ1vbWUBttAYAY0AePPlN0A9w=="
    # 
    #   "snappyflow/projectname" : os.environ.get("snappyflow_projectname"),
    # "snappyflow/appname": os.environ.get("snappyflow_appname"),
    # "snappyflow/profilekey": os.environ.get("snappyflow_profilekey")
"configFile":"/home/administrator/demo/py_app/proj1/env.conf"

    })
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj1.settings')


otlp_exporter = OTLPSpanExporter(
    # endpoint="https://otelforwarderuser:Forwarder-Snappyflow-Agent%407%24@127.0.0.1:9595/otel-service/export/trace",
    #  insecure=True  # Set to True to disable certificate verification
        # http_emitter=insecure_https_transport  # Use the custom HTTP transport)
)

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
    logger_provider.shutdown()
