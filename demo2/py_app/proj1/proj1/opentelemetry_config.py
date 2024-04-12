from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider

# Define your OTLP collector endpoint.
otlp_endpoint = "http://localhost:4318/v1/trace"

# Create a resource for your application.
resource = Resource(attributes={"service.name": "your-django-app"})

# Create a span exporter.
span_exporter = OTLPSpanExporter(endpoint=otlp_endpoint)

# Create a TracerProvider and configure it.
trace.set_tracer_provider(TracerProvider(resource=resource))
trace.get_tracer_provider().add_span_processor(SimpleExportSpanProcessor(span_exporter))

# Instrument Django application.
DjangoInstrumentor().instrument()
