# Problem Statement:
# Given a weighted directed graph, find the shortest path distance
# between every pair of vertices.
# The graph may contain negative edge weights, but it must not contain
# a negative-weight cycle.

# Import heapq because it provides a priority queue for Dijkstra's algorithm.
import heapq


# Define a function that calculates potential values using Bellman-Ford.
def bellman_ford(graph, source):
    # This docstring explains that the function returns distance potentials.
    """Return shortest-distance potentials for a graph with a super-source."""
    # Create a set to store every vertex found in the graph.
    vertices = set(graph)
    # Visit each list of outgoing edges in the graph.
    for edges in graph.values():
        # Visit every destination vertex in the current edge list.
        for destination, _ in edges:
            # Add the destination vertex to the vertex set.
            vertices.add(destination)

    # Initialize every vertex with a potential of zero for the super-source.
    distance = {vertex: 0 for vertex in vertices}

    # Run at most V - 1 relaxation rounds, where V is the vertex count.
    for _ in range(len(vertices) - 1):
        # Track whether any potential value was reduced in this round.
        changed = False
        # Visit each source vertex.
        for u in vertices:
            # Visit every outgoing edge from vertex u.
            for v, weight in graph.get(u, []):
                # Check whether the edge provides a shorter potential.
                if distance[u] + weight < distance[v]:
                    # Update the potential of destination vertex v.
                    distance[v] = distance[u] + weight
                    # Record that a potential value changed.
                    changed = True
        # Stop early if no potential value changed in the round.
        if not changed:
            break

    # Inspect the edges once more to detect a negative-weight cycle.
    for u in vertices:
        # Visit every outgoing edge from vertex u.
        for v, weight in graph.get(u, []):
            # A still-relaxable edge proves that a negative-weight cycle exists.
            if distance[u] + weight < distance[v]:
                # Report that Johnson's algorithm cannot process this graph.
                raise ValueError("Graph contains a negative-weight cycle")

    # Return the potentials that will be used for graph reweighting.
    return distance


# Define Dijkstra's function for finding shortest paths from one source.
def dijkstra(graph, source):
    # This docstring explains that edge weights must be non-negative.
    """Return shortest distances from source using a non-negative graph."""
    # Initialize the source distance to zero.
    distances = {source: 0}
    # Create a priority queue containing the source and its distance.
    queue = [(0, source)]

    # Continue until every reachable vertex with the best distance is processed.
    while queue:
        # Remove the vertex having the smallest known distance.
        current_distance, u = heapq.heappop(queue)
        # Ignore an outdated queue entry that is not the current best distance.
        if current_distance != distances[u]:
            continue

        # Visit each neighbor and edge weight of the current vertex.
        for v, weight in graph.get(u, []):
            # Calculate the distance obtained through vertex u.
            candidate = current_distance + weight
            # Check whether this route improves the known distance to v.
            if candidate < distances.get(v, float("inf")):
                # Store the newly improved shortest distance.
                distances[v] = candidate
                # Add the improved distance and vertex to the priority queue.
                heapq.heappush(queue, (candidate, v))

    # Return all shortest distances discovered from the source.
    return distances


# Define the main Johnson's algorithm function.
def johnson(graph):
    # This docstring describes the input and output of the function.
    """
    Compute all-pairs shortest paths.

    graph: dict mapping each vertex to [(neighbor, weight), ...]
    return: dict source -> dict destination -> shortest distance

    Johnson's algorithm supports negative edge weights but no
    negative-weight cycles.
    """
    # Create a set to collect all vertices in the graph.
    vertices = set(graph)
    # Visit every edge list to include destination-only vertices.
    for edges in graph.values():
        # Visit every destination and ignore the edge weight in this step.
        for destination, _ in edges:
            # Add destination-only vertices to the vertex set.
            vertices.add(destination)

    # Calculate reweighting potentials using Bellman-Ford.
    # Every vertex begins with a potential of zero, which models a super-source.
    potentials = bellman_ford(graph, None)

    # Create an empty dictionary for the reweighted graph.
    reweighted = {}
    # Visit each source vertex.
    for u in vertices:
        # Reweight every outgoing edge using h(u) and h(v).
        reweighted[u] = [
            # Convert w(u, v) into w'(u, v) = w(u, v) + h(u) - h(v).
            (v, weight + potentials[u] - potentials[v])
            # Iterate through every outgoing edge of vertex u.
            for v, weight in graph.get(u, [])
        ]

    # Create an empty dictionary that will hold all-pairs distances.
    all_pairs = {}
    # Run Dijkstra's algorithm once for every source vertex.
    for source in vertices:
        # Obtain shortest distances in the reweighted graph.
        reweighted_distances = dijkstra(reweighted, source)
        # Convert reweighted distances back to original graph distances.
        all_pairs[source] = {
            # Remove the reweighting contribution from each shortest distance.
            destination: reweighted_distances[destination]
            + potentials[destination]
            - potentials[source]
            # Iterate through every destination reached from this source.
            for destination in reweighted_distances
        }

    # Return the complete all-pairs shortest-distance mapping.
    return all_pairs


# Execute the example only when this file is run directly.
if __name__ == "__main__":
    # Store a directed graph containing negative edge weights.
    graph = {
        # Store vertex A and its outgoing edges.
        "A": [("B", -1), ("C", 4)],
        # Store vertex B and its outgoing edges.
        "B": [("C", 3), ("D", 2), ("E", 2)],
        # Store vertex C, which has no outgoing edges.
        "C": [],
        # Store vertex D and its outgoing edges.
        "D": [("B", 1), ("C", 5)],
        # Store vertex E and its outgoing edge.
        "E": [("D", -3)],
    }

    # Calculate the shortest distance from every vertex to every reachable vertex.
    shortest_distances = johnson(graph)
    # Print a heading that explains what the algorithm calculates.
    print("Johnson's Algorithm: shortest paths between every pair of vertices")
    # Explain that vertices are locations and edge weights are relationship costs.
    print("Each edge represents a one-way connection; its weight is the cost of using it.")
    # Explain that a shortest distance is the total weight of the cheapest route.
    print("Each result below gives the minimum total cost from one vertex to another.")
    # Explain that negative weights are allowed, but negative cycles are not.
    print("Negative edge weights are allowed, but a negative-weight cycle is not.")
    # Print a blank line to separate the explanation from the results.
    print("\nShortest-distance relationships:")
    # Visit each starting vertex and its calculated destination distances.
    for source, destinations in shortest_distances.items():
        # Visit each reachable destination and its shortest total distance.
        for destination, distance in destinations.items():
            # Explain that traveling from a vertex to itself costs zero.
            if source == destination:
                # Print the zero-distance relationship for the same vertex.
                print(f"From {source} to {destination}: distance is 0 (same vertex).")
            # Handle routes whose total weight is negative.
            elif distance < 0:
                # Print the negative shortest distance with a plain-language note.
                print(
                    f"From {source} to {destination}: the cheapest route has "
                    f"total weight {distance} (a negative total cost)."
                )
            # Handle routes whose total weight is zero or positive.
            else:
                # Print the shortest distance as the route's total weight.
                print(
                    f"From {source} to {destination}: the cheapest route has "
                    f"total weight {distance}."
                )
    # Explain that missing source-destination pairs have no available route.
    print("\nIf a destination is not listed for a source, no route exists between them.")