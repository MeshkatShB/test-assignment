BASE_PATH = 'H:/Documents/Apply/Applications/TU Delft/Assessment/test-assignment'
TRACES = '/trace_exploration/traces'

JAEGER_LOG_PATH_ADD_CAT = BASE_PATH + TRACES + '/trace_add_cat.json'

JAEGER_LOG_PATH_FIND_CAT = BASE_PATH + TRACES + '/trace_find_cats_by_name.json'

JAEGER_LOG_PATH_PAIRS = BASE_PATH + TRACES + '/trace_generate_pairs.json'

JAEGER_LOG_PATH_WITH_ERROR = BASE_PATH + TRACES + '/trace_generate_pairs_with_error.json'

JAEGER_LOG_PATH_GET_ALL_CATS = BASE_PATH + TRACES + '/trace_get_all_cats.json'

TRACE_DURATION_THRESHOLD = 1000

JAEGER_PORT = '16686'
JAEGER_DOMAIN = 'localhost'
JAEGER_API_URL = 'http://' + JAEGER_DOMAIN + ':' + JAEGER_PORT + '/api/traces'

SERVICES = [
    "cat-api",
    "cat-recommender-api",
]
