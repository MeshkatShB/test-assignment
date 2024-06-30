from opentelemetry import trace, context
from opentelemetry.trace import NonRecordingSpan, SpanContext, TraceFlags
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, BatchSpanProcessor
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

# Set up a simple processor to write spans out to the console so we can see what's happening.
trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))

tracer = trace.get_tracer("my.tracer")

# A TextMapPropagator works with any dict-like object as its Carrier by default. You can also implement custom getters and setters.
with tracer.start_as_current_span('first-trace'):
    carrier = {}
    # Write the current context into the carrier.
    TraceContextTextMapPropagator().inject(carrier)

# The below might be in a different thread, on a different machine, etc.
# As a typical example, it would be on a different microservice and the carrier would
# have been forwarded via HTTP headers.

# Extract the trace context from the carrier.
# Here's what a typical carrier might look like, as it would have been injected above.
carrier = {'traceparent': '00-a9c3b99a95cc045e573e163c3ac80a77-d99d251a8caecd06-01'}
# Then we use a propagator to get a context from it.
ctx = TraceContextTextMapPropagator().extract(carrier=carrier)

# Instead of extracting the trace context from the carrier, if you have a SpanContext
# object already you can get a trace context from it like this.
span_context = SpanContext(
    trace_id=2604504634922341076776623263868986797,
    span_id=5213367945872657620,
    is_remote=True,
    trace_flags=TraceFlags(0x01)
)
ctx = trace.set_span_in_context(NonRecordingSpan(span_context))

# Now there are a few ways to make use of the trace context.

# You can pass the context object when starting a span.
with tracer.start_as_current_span('child', context=ctx) as span:
    span.set_attribute('primes', [2, 3, 5, 7])

# Or you can make it the current context, and then the next span will pick it up.
# The returned token lets you restore the previous context.
token = context.attach(ctx)
try:
    with tracer.start_as_current_span('child') as span:
        span.set_attribute('evens', [2, 4, 6, 8])
finally:
    context.detach(token)