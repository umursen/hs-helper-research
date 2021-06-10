import unittest
from oracle import Oracle, Scenario
from minions import *


class TestOracle(unittest.TestCase):

    def test_game_result_basic_1_to_1_robot_kangaroo(self):
        minion1 = RobotKangaroo(1, 1)
        minion2 = Minion(2, 2)
        scenario = Scenario()
        scenario.set_board([minion1], [minion2])
        result = Oracle().calculate_game_result_density(scenario)
        print(result)
        self.assertEqual(result.player_one_win_percentage, 0)
        self.assertEqual(result.player_two_win_percentage, 0)
        self.assertEqual(result.lethal_one, 0)
        self.assertEqual(result.lethal_two, 0)
        self.assertEqual(result.draw, 100)

        minion1 = RobotKangaroo(1, 1)
        minion2 = Minion(1, 1)
        scenario = Scenario()
        scenario.set_board([minion1], [minion2])
        result = Oracle().calculate_game_result_density(scenario)

        self.assertEqual(result.player_one_win_percentage, 100)
        self.assertEqual(result.player_two_win_percentage, 0)
        self.assertEqual(result.lethal_one, 0)
        self.assertEqual(result.lethal_two, 0)
        self.assertEqual(result.draw, 0)

    def test_game_result_basic_1_to_2(self):
        minion1 = FiendishServant(1, 1)
        minion2 = Minion(1, 1)
        minion3 = Minion(1, 3)
        scenario = Scenario()
        scenario.set_board([minion1, minion2], [minion3])
        result = Oracle().calculate_game_result_density(scenario)
        print(result)
        self.assertEqual(result.player_one_win_percentage, 0)
        self.assertEqual(result.player_two_win_percentage, 0)
        self.assertEqual(result.lethal_one, 0)
        self.assertEqual(result.lethal_two, 0)
        self.assertEqual(result.draw, 100)
