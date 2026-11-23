import heapq
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        positions = (
            (0, 0), (0, 1), (0, 2),
            (1, 0), (1, 1), (1, 2),
            (2, 0), (2, 1), (2, 2),
        )

        total = 0
        for index, value in enumerate(state.tiles):
            if value == 0:
                continue
            current_row, current_column = positions[index]
            goal_row, goal_column = positions[value - 1]
            total += abs(current_row - goal_row) + abs(current_column - goal_column)

        return total

    def search(self, initial: State) -> SearchResult:
        frontier = []
        heapq.heappush(frontier, (self.heuristic(initial), initial))
        visited = {initial: 0}

        expanded_nodes = 0
        generated_nodes = 1
        max_frontier_size = 1

        while frontier:
            _, actual = heapq.heappop(frontier)

            if actual.cost > visited[actual]:
                continue

            if actual.is_goal:
                return SearchResult(
                    solution=actual,
                    nodes_expanded=expanded_nodes,
                    nodes_generated=generated_nodes,
                    max_frontier_size=max_frontier_size,
                    depth=actual.cost,
                )

            expanded_nodes += 1

            for child in actual.neighbors():
                generated_nodes += 1
                if child not in visited or child.cost < visited[child]:
                    visited[child] = child.cost
                    f = child.cost + self.heuristic(child)
                    heapq.heappush(frontier, (f, child))

            if len(frontier) > max_frontier_size:
                max_frontier_size = len(frontier)

        return SearchResult(
            solution=None,
            nodes_expanded=expanded_nodes,
            nodes_generated=generated_nodes,
            max_frontier_size=max_frontier_size,
            depth=0,
        )
