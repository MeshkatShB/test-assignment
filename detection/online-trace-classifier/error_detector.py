import requests
import schedule
import time

from detection.utils import JAEGER_API_URL, SERVICES


def fetch_traces(service):
    """
    The function `fetch_traces` sends a GET request to a Jaeger API endpoint to retrieve traces for a
    specified service and returns the JSON response if successful.
    
    :param service: The `fetch_traces` function takes a `service` parameter, which is used to specify
    the service for which you want to fetch traces. The function then makes a GET request to a Jaeger
    API endpoint with the specified service name to retrieve traces related to that service. If the
    request is successful
    :return: The function `fetch_traces(service)` returns the JSON response if the status code is 200
    (OK). If the status code is not 200, it prints a message indicating the failure to fetch traces and
    returns `None`.
    """
    response = requests.get(f"{JAEGER_API_URL}?service={service}")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch traces: {response.status_code}")
        return None


# Function to check for errors in traces
def check_for_errors(service):
    """
    The function `check_for_errors` checks for errors and exceptions in the traces of a given service.
    
    :param service: The function `check_for_errors` takes a `service` parameter as input. It checks for
    errors in the specified service by fetching traces associated with that service. If any errors or
    exceptions are found within the traces, it will print out the details of the error or exception
    along with the corresponding span and
    """
    print(f"Checking for errors in service: {service}")
    traces = fetch_traces(service)
    if traces and 'data' in traces:
        for trace in traces['data']:
            for span in trace['spans']:
                if any(tag['key'] == 'error' and tag['value'] for tag in span['tags']):
                    print(f"Error detected in span {span['spanID']} of trace {trace['traceID']} in operation {span['operationName']}")
                for log in span['logs']:
                    for field in log['fields']:
                        if 'exception' in field['key']:
                            print(f"Exception detected in span {span['spanID']} of trace {trace['traceID']} in operation {span['operationName']}: {field['value']}")


def schedule_error_checking(service, interval):
    """
    The function `schedule_error_checking` schedules a task to check for errors in a service at
    specified intervals using the `schedule` library in Python.
    
    :param service: The `service` parameter likely refers to the specific service or function that needs
    error checking. This could be a web service, a database connection, or any other component of a
    software system that requires monitoring for errors
    :param interval: The `interval` parameter specifies the frequency at which the `check_for_errors`
    function will be executed for the given `service`. It is measured in seconds, so the function
    `check_for_errors` will be called every `interval` seconds to check for errors in the specified
    `service`
    """
    schedule.every(interval).seconds.do(check_for_errors, service)


if __name__ == "__main__":
    service_names = SERVICES
    interval = 10  # Check every 10 seconds

    for service_name in service_names:
        schedule_error_checking(service_name, interval)

    while True:
        schedule.run_pending()
        time.sleep(1)
