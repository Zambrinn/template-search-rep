from __future__ import annotations
from typing import List, Optional, Tuple


GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)


class State:
    """Representa um estado do 8-puzzle como tupla imutável de 9 inteiros (0 = espaço vazio)."""

    def __init__(self, tiles: Tuple[int, ...], parent: Optional["State"] = None, action: Optional[str] = None, cost: int = 0):
        if len(tiles) != 9 or set(tiles) != set(range(9)):
            raise ValueError("Estado inválido: deve conter exatamente os valores 0-8.")
        self.tiles = tiles
        self.parent = parent
        self.action = action
        self.cost = cost

    @property
    def is_goal(self) -> bool:
        return self.tiles == GOAL_STATE

    @property
    def blank_index(self) -> int:
        return self.tiles.index(0)

    def neighbors(self) -> List["State"]:
        """Retorna os estados filhos válidos a partir deste estado."""
        index = self.blank_index # encontrar o espaço em branco
        result = []

        moves = []
        if index not in (0, 1, 2):
            moves.append(("UP", index - 3))
        if index not in (6, 7, 8):
            moves.append(("DOWN", index + 3))
        if index not in (0, 3, 6):
            moves.append(("LEFT", index - 1))
        if index not in (2, 5, 8):
            moves.append(("RIGHT", index + 1))

        for action, new_index in moves:
            new = list(self.tiles)
            new[index], new[new_index] = new[new_index], new[index] 
            result.append(State(tuple(new), parent=self, action=action, cost=self.cost + 1)) 

        return result   

    def path(self) -> List["State"]:
        path = []
        actual = self
        while actual is not None:
            path.append(actual)
            actual = actual.parent
        path.reverse()
        return path
    
    def actions(self) -> List[str]:
        actions = []
        for state in self.path():
            if state.action is not None:
                actions.append(state.action)
        return actions

    def __eq__(self, other: object) -> bool:
        return isinstance(other, State) and self.tiles == other.tiles

    def __hash__(self) -> int:
        return hash(self.tiles)

    def __lt__(self, other: "State") -> bool:
        return self.cost < other.cost

    def __repr__(self) -> str:
        t = self.tiles
        return (
            f"+-------+\n"
            f"| {t[0]} {t[1]} {t[2]} |\n"
            f"| {t[3]} {t[4]} {t[5]} |\n"
            f"| {t[6]} {t[7]} {t[8]} |\n"
            f"+-------+"
        ).replace("0", " ")
