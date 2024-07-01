import requests
import schedule
import time

from detection.utils import JAEGER_API_URL, SERVICES


def fetch_traces(service):
    response = requests.get(f"{JAEGER_API_URL}?service={service}")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch traces: {response.status_code}")
        return None


# Function to check for errors in traces
def check_for_errors(service):
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
    schedule.every(interval).seconds.do(check_for_errors, service)


if __name__ == "__main__":
    service_names = SERVICES
    interval = 10  # Check every 10 seconds

    for service_name in service_names:
        schedule_error_checking(service_name, interval)

    while True:
        schedule.run_pending()
        time.sleep(1)
