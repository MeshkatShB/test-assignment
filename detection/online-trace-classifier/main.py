from otel_config import configure_tracer
from detection.utils import SERVICES

# tracer = configure_tracer("cat-api")
tracer = configure_tracer("cat-recommender-api")


def process():
    """
    The `process` function simulates an error in a cat-recommender API operation and logs details of the exception.
    """
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


def main():
    while True:
        process()
        time.sleep(1)


if __name__ == "__main__":
    import time
    main()
