# for logs
# This custom logger configuration sets up OpenTelemetry to send traces to your backend using the OTLP exporter.
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
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj1.settings')

    logger_provider = LoggerProvider(
        resource=Resource.create(
            {
                "configFile":"/home/administrator/demo/py_app/proj1/env.conf"
    #             "service.name": "django-logs",
    #              "snappyflow/projectname" : "Banking",
    #     "snappyflow/appname": "flowlogs",
    #     "snappyflow/profilekey": "RLgmVLU7Vzi9mtbO6hKxtuKnXeU1/3OrxKu0dJqOCtq9TSHzCGBH0t/h7y0Lf4E6RhGu/RxWCZUTZ08tDKkEbFRVIZrPgwDYEketyBkiFEhJ7Gw1bFqKPqMk+9ZuHbOKesk/5TrSLQDK+S+OdI23mRvwqkaXlFoy5ifIdpDYaYP0yh1XxE7zEvEgCwAzyfujd08NIndes1sNXdVjBuNmnVvDuI6XXHx1YhBnfwpQZnpQXe964bgo4FBvG2MGhiEw6fv4YjRytq4uxMJQ/UmkO8PCa6YyW7kqI79OxWmF0gt4SqJ9g1t/rAKoYfAWCy1+P0I+6Gpz2uZ90rCDQMW7J/wyVZwGt+jUEG+dHgalLKWCrUKwSnbFzuBORaaYiCwyDCTcPeOPm8Y0n9uradBJsbVVFJnrPt6OTVI/Pb/JHHOlH+eJgLN59QamqujliZRVZoWmKTjiHWVHTSJUKBnzoZlwPjL/5uMilz9tKQfPoUrXvPr8UIWW6AauDETYB5K+TipBr9GLmjmKCPZZb6iZR0S+Y8QlXcqcA3GOyfERul6hqYnC5Zk744YCFaGygwvFZlOl4SdfkGJ8w9eCsQ/wMx+JEN0ZN7MTTU1zYsgek8Qdj08uuOymtuKTC2+LvIct68fTk+/l5WEwTJbtShlxPM13vMXjy88l5M22lWgvI1qU4NH45AlG8ETDDDNQtjg9dqbfhqfoPj1DMHuMeLl3maDoUlgvpuffE9PNJX3HVVPZNr1SmRyNX7mmvZJrveBLjFyTgNZWMKsW2T15OBIRIvin+XdaLDWG8lxRmVEY3GoaUxU4MzrtUhcoWG3LoPa76WfAZEY97DI2H2uT7Z/cP+DogbNwgtcHDey9DuvAanMka8x8u3HEs8tqABYejJQ1vbWUBttAYAY0AePPlN0A9w=="
    # # "snappyflow/projectname" : "test",
    #     "snappyflow/appname": "test",
    #     "snappyflow/profilekey": "LiF70Ps5ve5Gx1kb3BUm5dIVTRdNm3UbRRdCKiy5AAP1dAEWsp2PjpEfQ83debX+2NiQAeuXblA2cIMcyAEwYyqN5E2yCmX6oiwLL38/SkHThNYGByd5VPcuNukJH+UEJRgaGEWiHJReL7Hjr3zcao/Kw+y3DquDflWY0A43Z3CIeiysBGFmlBXiHI+77LPotGkep2F/DDM1MFQOaGumfg5n3U2rDSVQacNMRhbihPZgZIjkGgeWprXjLRCADj4fI/u4LF/r+quMOzHz62qjTmrPrH3nt1HaWp72WFEK9zC6CbzN8iZ9ld1x3pVPUb3IItT0LK5D499S+EMwTQolvMs2VD//wbzHfJwgpeJcEtiL5/EgqzcWoohiWG2eIyrK2mNTU5kHxnjd7WnG4hpmQpeBvK5UTfI456TYNzN18ON0Z1cwZdsdC4AL580a8FlewLjILJ2Wh988RDVK+j7K8Vc3m6pHQ20VUQo0GMO4+ToJJIsr2Sr1oMgE5662rx5cB6nnxAXlc6i2mtj8qQDbFw+QCicEj/d1y8QcPkSJ39O2bhMC8/C10BO5DKtxOaXrX6/LIPBeLepH8b0xWi5Z/eqxBmTVHERH9MJ8RizjYKlyo3TOdpK8wfDmedtWdnrq"
            }
        ),
    )
    set_logger_provider(logger_provider)

    exporter = OTLPLogExporter()
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
    
    handler = LoggingHandler(logger_provider=logger_provider)

# Attach OTLP handler to root logger

    logging.getLogger().addHandler(handler)

    logging.getLogger().setLevel(logging.INFO)

    logging.info("configured logging")


configure_logging()