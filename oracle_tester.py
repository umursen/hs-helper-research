import unittest
from minion import Minion
from oracle import Oracle


class TestOracle(unittest.TestCase):

    def test_game_result_basic_1_to_1(self):
        minion1 = Minion(1, 1)
        minion2 = Minion(1, 1)
        oracle = Oracle([minion1], [minion2])
        result = oracle.calculate_game_result_density()

        self.assertEqual(result.player_one_win_percentage, 0)
        self.assertEqual(result.player_two_win_percentage, 0)
        self.assertEqual(result.lethal_one, 0)
        self.assertEqual(result.lethal_two, 0)
        self.assertEqual(result.draw, 100)

    def test_game_result_win(self):
        minion1 = Minion(1, 2)
        minion2 = Minion(1, 1)
        oracle = Oracle([minion1], [minion2])
        result = oracle.calculate_game_result_density()

        self.assertEqual(result.player_one_win_percentage, 100)
        self.assertEqual(result.player_two_win_percentage, 0)
        self.assertEqual(result.lethal_one, 0)
        self.assertEqual(result.lethal_two, 0)
        self.assertEqual(result.draw, 0)

    def test_game_result_defeat(self):
        minion1 = Minion(1, 1)
        minion2 = Minion(1, 2)
        oracle = Oracle([minion1], [minion2])
        result = oracle.calculate_game_result_density()

        self.assertEqual(result.player_one_win_percentage, 0)
        self.assertEqual(result.player_two_win_percentage, 100)
        self.assertEqual(result.lethal_one, 0)
        self.assertEqual(result.lethal_two, 0)
        self.assertEqual(result.draw, 0)

    def test_game_result_2x2(self):
        minion1 = Minion(10, 15)
        minion2 = Minion(1, 2)
        board_one = [minion1, minion2]
        minion3 = Minion(5, 5)
        minion4 = Minion(1, 2)
        board_two = [minion3, minion4]
        oracle = Oracle(board_one, board_two)
        result = oracle.calculate_game_result_density()

        self.assertEqual(result.player_one_win_percentage, 100)
        self.assertEqual(result.player_two_win_percentage, 0)
        self.assertEqual(result.lethal_one, 0)
        self.assertEqual(result.lethal_two, 0)
        self.assertEqual(result.draw, 0)

    def test_game_result_7x7(self):
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
