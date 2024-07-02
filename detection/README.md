# Detection Service


##  About this project

The Detection Service is designed to classify and detect errors in online traces. It is composed of several components organized into different directories. Below is an overview of the structure and functionality of each component.

## Project Structure

```
detection
├── online-trace-classifier
│ ├── error_detector.py
│ ├── main.py
│ └── otel_config.py
├── test
│ ├── trace-classifier
│ │ ├── test_n_plus_one.py
│ │ └── test_trace_error.py
│ └── trace_classifier
│ ├── dependency_analysis.py
│ ├── error_correlation.py
│ ├── long_traces.py
│ ├── n_plus_one.py
│ ├── trace_error.py
│ └── tracer.py
├── data_loader.py
├── README.md
└── utils.py
```
   
## Components

### online-trace-classifier

In this folder, exists two separate implementation of error detections.
1. Jaeger API with `requests` python library. [Implemented in `error_detector.py`]

- For running with this method, only use the snippet code below after changing directory to `online-trace-classifier`:
```bash
   python error_detector.py
```
2. Jarger API with `OpenTelemetry` which didn't have any result. [Implemented in `main.py` and the OTel config file in `otel_config.py`]
- For running with this method, See the `Getting Started` section, `part 2`.
- **error_detector.py**: Contains the logic to detect errors in online traces. With a scheduler, it dispatches both `cat-api` and `cat-recommender-api` services to receive logs. 
- **main.py**: The main entry point for the online trace classifier service. [The `OpenTelemetry API` is not as accurate as Jaeger API requests.]
- **otel_config.py**: Configuration file for `OpenTelemetry` integration.

### trace_classifier

In this folder, there are multiple analytic tools implemented to detect errors which are contained in a `.json` file.
Unlike the `online-trace-classifier`, these files only run on static datasets which are presented to us in `trace_exploration/traces/*.json`.

All the files in this folder can be run by the below structure:
```bash
   python <FILE_NAME.py>
```

Detailed descriptions of each file are as below:

- **dependency_analysis.py**: Analyzes dependencies within the trace data, depicts the graph of `spanIDs` regarding the `service` and save the output graph as a `.png` file to `test-assignment/docs` folder. 
- **error_correlation.py**: Correlates different types of errors found in traces with development time. [It can be implemented to use any other variable for finding correlation]
- **long_traces.py**: Identifies and handles traces that are unusually long.
- **n_plus_one.py**: Detects the `N+1 query` problem in traces.
- **trace_error.py**: Detects `error`, `warning`, and `exception` in spans regarding the traces.
- **tracer.py**: An example of how `OpenTelemetry` library works. [straight from the documentation]

### test

#### trace-classifier

- **test_n_plus_one.py**: Tests for the `N+1 query` problem detection.
- **test_trace_error.py**: Tests for error trace detection.


### Root Directory

- **data_loader.py**: Handles loading of trace data for processing.
- **utils.py**: Utility functions used across the service which contains `JAEGER_API_URL` and Jaeger paths.
- **README.md**: This document.

## Plugins
### .live-plugins
There are 5 plugins that can identify the developer for errors using LivePlugin format.
In this folder, we have Kotlin Scripts regarding all detections which includes: `dependency_analysis.kts`,
`error_correlations.kts`, `long_traces.kts`, `n_plus_one.kts` , and `trace_error.kts`. The LivePlugin will load all the `.live-plugins`
folder in startup since it is noted in the LivePlugin documentation.

## Getting Started

To get started with the Detection Service, follow these steps:

1. **Install Dependencies**: Ensure you have all the necessary dependencies installed. You can install them using:
   ```bash
   pip install -r requirements.txt
   ```
2. **Run the Service**: Navigate to the `online-trace-classifier` directory and run the `main.py` file or use below to run:
   ```bash
   python detection/online-trace-classifier/main.py
   ```
3. **Run Tests**: Navigate to the `test` directory and run the test files to ensure everything is working correctly:
   ```bash
   python -m unittest discover -s test
   ```

## Note:
Unfortunately there is no `main.py` for `trace_classifier` but it's not hard to implement it. It can be a menu and run the dedicated error detection but time was limited.
