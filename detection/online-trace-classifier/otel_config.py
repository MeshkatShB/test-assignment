from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter


def configure_tracer(service_name):
    """
    The function `configure_tracer` sets up a Jaeger exporter and tracer provider for tracing in a
    Python application.
    
    :param service_name: The `service_name` parameter is a string that represents the name of the
    service for which you are configuring the tracer. This name will be used to identify the service in
    the tracing system and in the exported traces
    :return: The `configure_tracer` function returns a tracer object that is created and configured with
    a Jaeger exporter, a tracer provider with specified service name, and span processors for batch
    processing with Jaeger exporter and ConsoleSpanExporter.
    """
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
