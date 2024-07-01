from otel_config import configure_tracer
from detection.utils import SERVICES

# tracer = configure_tracer("cat-api")
tracer = configure_tracer("cat-recommender-api")


def process():
    with tracer.start_as_current_span("cat-recommender-api-operation") as span:
        try:
            # Your cat-recommender-api code here
            span.add_event("Executing cat-recommender-api operation")
            # Simulate an error
            raise ValueError("An error occurred in cat-recommender-api")
        except Exception as e:

            span.set_attribute("error", True)
            span.add_event("exception", {"exception.message": str(e),
                                         "exception.type": type(e).__name__,
                                         'exception.start_time': span._start_time,
                                         'exception': str(span.__dict__),
                                         })
            print(f"Exception occurred: {e}")


# "exception": "{'_name': 'cat-recommender-api-operation', '_context':
# SpanContext(trace_id=0xc504039a473b009f71fb242cba7ffa25, span_id=0x3dc10025d22ce558, trace_flags=0x01, trace_state=[],
# is_remote=False), '_kind': <SpanKind.INTERNAL: 0>, '_instrumentation_info': InstrumentationInfo(otel_config, , ),
# '_instrumentation_scope': InstrumentationScope(otel_config, , ), '_parent': None, '_start_time': 1719847928833001800,
# '_end_time': None, '_attributes': {'error': True}, '_events': BoundedList([<opentelemetry.sdk.trace.Event object at
# 0x0000019C7FD39300>], maxlen=128), '_links': BoundedList([], maxlen=128), '_resource':
# <opentelemetry.sdk.resources.Resource object at 0x0000019C7FD38460>, '_status': <opentelemetry.trace.status.Status
# object at 0x0000019C7FCE5420>, '_sampler': <opentelemetry.sdk.trace.sampling.ParentBased object at
# 0x0000019C7FCE4DC0>, '_trace_config': None, '_record_exception': True, '_set_status_on_exception': True,
# '_span_processor': <opentelemetry.sdk.trace.SynchronousMultiSpanProcessor object at
# 0x0000019C7FD3A920>, '_limits': SpanLimits(max_span_attributes=128, max_events_attributes=128,
# max_link_attributes=128, max_attributes=128, max_events=128, max_links=128, max_attribute_length=None),
# '_lock': <unlocked _thread.lock object at 0x0000019C7FD6E780>}"


def main():
    while True:
        process()
        time.sleep(1)


if __name__ == "__main__":
    import time
    main()
