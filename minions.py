from minion import Minion
from deathrattles import give_divine_shield, give_attack


class RobotKangaroo(Minion):

    def __init__(self, attack, health):
        super().__init__(attack, health)
        self.active = False

    def perform_deathrattle(self, scenario, player, position):
        scenario.summon_minion(Minion(1, 1), player, position)


class Scallywag(Minion):
    def __init__(self, attack, health):
        super().__init__(attack, health)
        self.active = False

    def perform_deathrattle(self, scenario, player, position):
        scenario.summon_minion(Minion(1, 1), player, position)


class FiendishServant(Minion):

    def __init__(self, attack, health):
        super().__init__(attack, health)

    def perform_deathrattle(self, scenario, player, position):
        give_attack(scenario, player, position, self.attack)


class SelflessHero(Minion):
    def __init__(self, attack, health):
        super().__init__(attack, health)

    def perform_deathrattle(self, scenario, player, position):
        give_divine_shield(scenario, player, position)
