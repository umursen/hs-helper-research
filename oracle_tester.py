import unittest
from minion import Minion
from oracle import Oracle, Scenario


class TestOracle(unittest.TestCase):

    def test_game_result_basic_1_to_1(self):
        minion1 = Minion(1, 1)
        minion2 = Minion(1, 1)
        scenario = Scenario()
        scenario.set_board([minion1], [minion2])
        result = Oracle().calculate_game_result_density(scenario)

        self.assertEqual(result.player_one_win_percentage, 0)
        self.assertEqual(result.player_two_win_percentage, 0)
        self.assertEqual(result.lethal_one, 0)
        self.assertEqual(result.lethal_two, 0)
        self.assertEqual(result.draw, 100)

    def test_game_result_basic_1_to_1_sampling(self):
        minion1 = Minion(1, 1)
        minion2 = Minion(1, 1)
        scenario = Scenario()
        scenario.set_board([minion1], [minion2])
        args = {'sampling_amount': 200}
        result = Oracle().calculate_game_result_density(scenario, method='sampling', args=args)

        self.assertEqual(result.player_one_win_percentage, 0)
        self.assertEqual(result.player_two_win_percentage, 0)
        self.assertEqual(result.lethal_one, 0)
        self.assertEqual(result.lethal_two, 0)
        self.assertEqual(result.draw, 100)

    def test_game_result_win(self):
        minion1 = Minion(1, 2)
        minion2 = Minion(1, 1)
        scenario = Scenario()
        scenario.set_board([minion1], [minion2])
        result = Oracle().calculate_game_result_density(scenario)

        self.assertEqual(result.player_one_win_percentage, 100)
        self.assertEqual(result.player_two_win_percentage, 0)
        self.assertEqual(result.lethal_one, 0)
        self.assertEqual(result.lethal_two, 0)
        self.assertEqual(result.draw, 0)

    def test_game_result_defeat(self):
        minion1 = Minion(1, 1)
        minion2 = Minion(1, 2)

        scenario = Scenario()
        scenario.set_board([minion1], [minion2])
        result = Oracle().calculate_game_result_density(scenario)

        self.assertEqual(result.player_one_win_percentage, 0)
        self.assertEqual(result.player_two_win_percentage, 100)
        self.assertEqual(result.lethal_one, 0)
        self.assertEqual(result.lethal_two, 0)
        self.assertEqual(result.draw, 0)

    def test_game_result_2x1(self):
        minion1 = Minion(10, 15)
        minion2 = Minion(1, 2)
        board_one = [minion1, minion2]
        minion3 = Minion(5, 5)
        board_two = [minion3]

        scenario = Scenario()
        scenario.set_board(board_one, board_two)
        result = Oracle().calculate_game_result_density(scenario)

        self.assertEqual(result.player_one_win_percentage, 100)
        self.assertEqual(result.player_two_win_percentage, 0)
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

        scenario = Scenario()
        scenario.set_board(board_one, board_two)
        result = Oracle().calculate_game_result_density(scenario)

        self.assertEqual(result.player_one_win_percentage, 100)
        self.assertEqual(result.player_two_win_percentage, 0)
        self.assertEqual(result.lethal_one, 0)
        self.assertEqual(result.lethal_two, 0)
        self.assertEqual(result.draw, 0)

    def test_game_result_2x2_win_and_tie(self):
        minion1 = Minion(2, 1)
        minion2 = Minion(1, 1)
        board_one = [minion1, minion2]
        minion3 = Minion(2, 2)
        minion4 = Minion(1, 1)
        board_two = [minion3, minion4]

        scenario = Scenario()
        scenario.set_board(board_one, board_two)
        result = Oracle().calculate_game_result_density(scenario)

        self.assertEqual(result.player_one_win_percentage, 0)
        self.assertEqual(result.player_two_win_percentage, 50)
        self.assertEqual(result.lethal_one, 0)
        self.assertEqual(result.lethal_two, 0)
        self.assertEqual(result.draw, 50)

    def test_game_result_2x2_win_and_tie_sampling(self):
        minion1 = Minion(2, 1)
        minion2 = Minion(1, 1)
        board_one = [minion1, minion2]
        minion3 = Minion(2, 2)
        minion4 = Minion(1, 1)
        board_two = [minion3, minion4]

        scenario = Scenario()
        scenario.set_board(board_one, board_two)
        args = {'sampling_amount': 20000}
        result = Oracle().calculate_game_result_density(scenario, method='sampling', args=args)

        print('error: ', abs(50 - result.player_two_win_percentage))
        self.assertEqual(result.player_one_win_percentage, 0)
        self.assertGreater(5, abs(50 - result.player_two_win_percentage))
        self.assertEqual(result.lethal_one, 0)
        self.assertEqual(result.lethal_two, 0)
        self.assertGreater(5, abs(50 - result.draw))

    def test_game_result_7x7(self):
        board_one = []
        board_two = []
        for i in range(7):
            board_one.append(Minion(10, 10))
        for i in range(7):
            board_two.append(Minion(1, 1))

        scenario = Scenario()
        scenario.set_board(board_one, board_two)
        result = Oracle().calculate_game_result_density(scenario)

        self.assertEqual(result.player_one_win_percentage, 100)
        self.assertEqual(result.player_two_win_percentage, 0)
        self.assertEqual(result.lethal_one, 0)
        self.assertEqual(result.lethal_two, 0)
        self.assertEqual(result.draw, 0)

    def test_game_result_7x7_sampling(self):
        board_one = []
        board_two = []
        for i in range(7):
            board_one.append(Minion(10, 10))
        for i in range(7):
            board_two.append(Minion(1, 1))

        scenario = Scenario()
        scenario.set_board(board_one, board_two)
        args = {'sampling_amount': 2000}
        result = Oracle().calculate_game_result_density(scenario, method='sampling', args=args)

        print('error: ', abs(100 - result.player_one_win_percentage))
        self.assertGreater(5, abs(100 - result.player_one_win_percentage))
        self.assertGreater(5, abs(0 - result.player_two_win_percentage))
        self.assertEqual(result.lethal_one, 0)
        self.assertEqual(result.lethal_two, 0)
        self.assertEqual(result.draw, 0)
