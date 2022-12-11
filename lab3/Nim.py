from collections import namedtuple

Nimply = namedtuple("Nimply", "row, num_objects")

class Nim:
    def __init__(self, num_rows: int, k: int = None) -> None:
        self._rows = [i * 2 + 1 for i in range(num_rows)]
        self._k = k

    # Example with k = 3, where k is the number of rows
    #   *
    #  ***
    # *****

    def __bool__(self):
        return sum(self._rows) > 0

    def __str__(self):
        return "<" + " ".join(str(_) for _ in self._rows) + ">"

    @property
    def rows(self) -> tuple:
        return tuple(self._rows)

    @property
    def k(self) -> int:
        return self._k

    # Make an action in the game (a ply is a move by one player)
    def nimming(self, ply: Nimply) -> None:
        row, num_objects = ply
        assert self._rows[row] >= num_objects
        assert self._k is None or num_objects <= self._k
        self._rows[row] -= num_objects

    # Given a Nim game, returns the possible moves in that state of the game
    def possible_moves(self):
        return [(r, o) for r, c in enumerate(self.rows) for o in range(1, c + 1) if self.k is None or o <= self.k]
    
    # Returns if a game is in a terminal state or not
    def is_over(self):
        if sum(elements > 0 for elements in self.rows) == 0:
            return True
        else:
            return False

    def get_state_and_reward(self):
        return self, self.give_reward()

    def give_reward(self):
        # if at end give 0 reward
        # if not at end give -1 reward
        return -1 * int(not self.is_over())