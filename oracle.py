import random
from minion import Minion


class Scenario:

    PLAYER_ONE = 1
    PLAYER_TWO = 2

    def __init__(self, attacker_index):
        self.board = {self.PLAYER_ONE: list(), self.PLAYER_TWO: list()}
        self.attacker_index = attacker_index

    def set_board(self, player_one_cards: list, player_two_cards: list):
        self.board[self.PLAYER_ONE] = player_one_cards
        self.board[self.PLAYER_TWO] = player_two_cards

    def is_winner(self, player_index):
        if player_index == self.PLAYER_ONE:
            return any(self.board[self.PLAYER_TWO])
        if player_index == self.PLAYER_TWO:
            return any(self.board[self.PLAYER_ONE])


class Oracle:

    def __init__(self, player_one_board, player_two_board):
        self.board = Scenario(0)
        self.board.set_board(player_one_board, player_two_board)

    def calculate_game_result(self):
        # Player starts first
        attacker_minion = self.player_board[0]

        densities = []
        for enemy in self.enemy_board:

            scenarios =

        densities = self.get_density_for_attack()

    def solve_scenario(self, attacker: Minion, defender: Minion, round_attacker: int):
        attacker.perform_attack(defender)

        if not attacker.is_alive:
            if round_attacker:
                self.player_board.remove(attacker)
            else:
                self.enemy_board.remove(attacker)

        if not defender.is_alive:
            if round_attacker:
                self.player_board.remove(defender)
            else:
                self.enemy_board.remove(defender)
