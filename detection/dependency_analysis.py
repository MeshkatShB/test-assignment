import networkx as nx
import matplotlib.pyplot as plt
from detection.data_loader import DataLoader

JAEGER_LOG_PATH_WITH_ERROR = '../trace_exploration/traces/trace_generate_pairs_with_error.json'

# Create a directed graph
G = nx.DiGraph()
traces = DataLoader(JAEGER_LOG_PATH_WITH_ERROR).get_traces()


# Extract services and their dependencies
for trace in traces:
    for span in trace["spans"]:
        for ref in span.get("references", []):
            if ref["refType"] == "CHILD_OF":
                parent_span_id = ref["spanID"]
                child_span_id = span["spanID"]
                parent_operation = next((s for s in trace["spans"] if s["spanID"] == parent_span_id), None)
                if parent_operation:
                    parent_service = parent_operation["operationName"]
                    child_service = span["operationName"]
                    G.add_edge(parent_service, child_service)

# Draw the graph
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=3000, node_color="skyblue", font_size=10, font_weight="bold")
plt.title("Service Dependency Graph")
plt.savefig('../docs/Service Dependency Graph.png')
plt.show()

# Identify services with high error rates
error_services = set()
for trace in traces:
    for span in trace["spans"]:
        if any(tag["key"] == "error" and tag["value"] is True for tag in span["tags"]):
            error_services.add(span["operationName"])

print("Services with high error rates:")
print(error_services)
