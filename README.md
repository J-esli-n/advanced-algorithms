# Advance Algorithms

A growing collection of algorithm implementations written in Python, with examples and notes on how to run them.

## Algorithms

| Category | Algorithm | File | Notes |
|---|---|---|---|
| Graphs | Johnson's algorithm | [`johnsons_algorithm.py`](johnsons_algorithm.py) | All-pairs shortest paths; supports negative edge weights, but not negative-weight cycles |

## Requirements

- Python 3
- No external packages required for the current implementation

## Run an example

```bash
python johnsons_algorithm.py
```

## Use Johnson's algorithm

```python
from johnsons_algorithm import johnson

graph = {
    "A": [("B", 2)],
    "B": [],
}

distances = johnson(graph)
print(distances)
```

The graph is represented as a dictionary where each vertex maps to a list of `(neighbor, weight)` pairs. The result maps each source vertex to the shortest distances for reachable destinations. A graph with a negative-weight cycle raises `ValueError`.

## Adding an algorithm

- Put each implementation in its own clearly named `.py` file.
- Include a short description, expected input, and a runnable example.
- Add the algorithm to the table above.
- Update the requirements if the implementation needs external packages.