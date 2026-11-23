from collections import deque
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class BFS(BaseSearch):

    def search(self, initial: State) -> SearchResult:
        frontier = deque([initial])
        visited = {initial}

        expanded_nodes = 0
        generated_nodes = 1
        max_frontier_size = 1

        while frontier:
            actual = frontier.popleft() # tira do comeco (FIFO)

            if actual.is_goal:
                return SearchResult(
                    solution=actual,
                    nodes_expanded=expanded_nodes,
                    nodes_generated=generated_nodes,
                    max_frontier_size=max_frontier_size,
                    depth=actual.cost
                )

            expanded_nodes += 1

            for child in actual.neighbors():
                generated_nodes += 1
                if child not in visited:
                    visited.add(child)
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
            