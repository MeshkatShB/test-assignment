from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter


def configure_tracer(service_name):
    # Set up Jaeger exporter
    jaeger_exporter = JaegerExporter(
        agent_host_name="localhost",
        agent_port=16686,
    )

    # Set up the tracer provider
    trace.set_tracer_provider(
        TracerProvider(resource=Resource.create({"service.name": service_name}))
    )
    tracer_provider = trace.get_tracer_provider()

    # Add span processors
    tracer_provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))
    tracer_provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))

    return trace.get_tracer(__name__)
