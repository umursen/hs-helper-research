import unittest
from minion import Minion
from oracle import Oracle


class TestOracle(unittest.TestCase):

    def test_game_result_basic_1_to_1(self):
        oracle = Oracle()
        minion1 = Minion(1, 1)
        minion2 = Minion(1, 1)
        oracle.set_board([minion1], [minion2])
        result = oracle.calculate_game_result()
        self.assertEqual(result, (0, 0, 100, 0, 0))

    def test_game_result_win(self):
        oracle = Oracle()
        minion1 = Minion(1, 2)
        minion2 = Minion(1, 1)
        oracle.set_board([minion1], [minion2])
        result = oracle.calculate_game_result()
        self.assertEqual(result, (100, 0, 0, 0, 0))

    def test_game_result_defeat(self):
        oracle = Oracle()
        minion1 = Minion(1, 1)
        minion2 = Minion(1, 2)
        oracle.set_board([minion1], [minion2])
        result = oracle.calculate_game_result()
        self.assertEqual(result, (0, 0, 0, 0, 100))