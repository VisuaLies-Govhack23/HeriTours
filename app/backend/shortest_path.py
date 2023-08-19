import heapq


def find_shortest_path(start: int, n: int, costs: list[list[float]]):
    """
    Find the shortest path through a graph.

    Computes shortest weighted Hamiltonian Path from a known starting point.

    start: the index of the start node
    n: the number of nodes
    costs: an n*n matrix of costs, the diagonal must be math.infinity
    """
    # Priority queue to perform a breadth first search.
    # Elements are tuples containing:
    # (heuristic lower bound, actual path cost, path so far)
    q = []

    # Use the smallest distance between places as a heuristic
    least = min(min(cost for cost in row) for row in costs)

    # Set up the first step
    for i in range(n):
        if i != start:
            past_cost = costs[start][i]
            path = (start, i)
            future_cost = (n - len(path)) * least
            heapq.heappush(q, (past_cost + future_cost, past_cost, path))

    # Keep iterating on the lowest-cost paths
    while True:
        _, past_cost, path = heapq.heappop(q)
        if len(path) == n:
            return past_cost, path
        for i in range(n):
            if i not in path:
                next_path = path + (i,)
                next_past_cost = past_cost + costs[path[-1]][i]
                next_future_cost = (n - len(path)) * least
                heapq.heappush(
                    q, (next_past_cost + next_future_cost, next_past_cost, next_path)
                )
