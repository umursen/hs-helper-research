from minion import Minion
from oracle import Oracle
from numba import jit, cuda


@jit(target="cuda")
def run(self):
    board_one = []
    board_two = []
    for i in range(7):
        board_one.append(Minion(10, 10))
    for i in range(7):
        board_two.append(Minion(1, 1))

    oracle = Oracle(board_one, board_two)
    result = oracle.calculate_game_result_density()

    self.assertEqual(result.player_one_win_percentage, 100)
    self.assertEqual(result.player_two_win_percentage, 0)
    self.assertEqual(result.lethal_one, 0)
    self.assertEqual(result.lethal_two, 0)
    self.assertEqual(result.draw, 0)


if __name__ == '__main__':
    run()
