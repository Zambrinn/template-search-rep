from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        frontier = [initial]
        visited = {initial: 0}

        expanded_nodes = 0
        generated_nodes = 1
        max_frontier_size = 1

        while frontier:
            actual = frontier.pop()

            if actual.is_goal:
                return SearchResult(
                    solution=actual,
                    nodes_expanded=expanded_nodes,
                    nodes_generated=generated_nodes,
                    max_frontier_size=max_frontier_size,
                    depth=actual.cost
                )

            if actual.cost >= self.depth_limit: continue

            expanded_nodes += 1

            for child in actual.neighbors():
                generated_nodes += 1
                if child not in visited or child.cost < visited[child]:
                    visited[child] = child.cost
                    frontier.append(child)

            if len(frontier) > max_frontier_size:
                max_frontier_size = len(frontier)

        return SearchResult(
            solution=None,
            nodes_expanded=expanded_nodes,
            nodes_generated=generated_nodes,
            max_frontier_size=max_frontier_size,
            depth=0
        )