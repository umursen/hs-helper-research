from threadManager import ThreadManager
import threading
from copy import copy
from queue import Queue
import random

PLAYER_ONE = 1
PLAYER_TWO = 2

GAME_RESULT_PLAYER_ONE_WINNER = PLAYER_ONE
GAME_RESULT_PLAYER_TWO_WINNER = PLAYER_TWO
GAME_RESULT_NO_WINNER = -1
GAME_RESULT_DRAW = 3

THREAD_LEVEL = 1


class GameResult:
    def __init__(self, player_one_win_percentage=0, player_two_win_percentage=0, lethal_one=0, lethal_two=0, draw=0, unresolved=False):
        self.lethal_one = lethal_one
        self.lethal_two = lethal_two
        self.player_one_win_percentage = player_one_win_percentage
        self.player_two_win_percentage = player_two_win_percentage
        self.draw = draw
        self.unresolved = unresolved

    def __str__(self):
        return 'lethal one: ' + str(self.lethal_one) + \
            ', lethal_two: ' + str(self.lethal_two) + \
            ', player_one_win_percentage: ' + str(self.player_one_win_percentage) + \
            ', player_two_win_percentage: ' + str(self.player_two_win_percentage) + \
            ', draw: ' + str(self.draw) + \
            ', unresolved: ' + str(self.unresolved)


def join_results(densities):
    size = len(densities)
    return GameResult(
        lethal_one=sum([d.lethal_one for d in densities])/size,
        lethal_two=sum([d.lethal_two for d in densities])/size,
        player_one_win_percentage=sum([d.player_one_win_percentage for d in densities]) / size,
        player_two_win_percentage=sum([d.player_two_win_percentage for d in densities]) / size,
        draw=sum([d.draw for d in densities]) / size,
    )


class Scenario:

    PLAYER_ONE_ATTACKER_INDEX = 0
    PLAYER_TWO_ATTACKER_INDEX = 0
    level = 0

    def __init__(self):
        self.board = {PLAYER_ONE: list(), PLAYER_TWO: list()}
        self.player_turn = 1

    def set_board(self, player_one_cards: list, player_two_cards: list):
        self.board[PLAYER_ONE] = player_one_cards
        self.board[PLAYER_TWO] = player_two_cards

    def get_attacker_index(self, index):
        if index == PLAYER_ONE:
            return self.PLAYER_ONE_ATTACKER_INDEX
        elif index == PLAYER_TWO:
            return self.PLAYER_TWO_ATTACKER_INDEX
        else:
            raise Exception("Unknown player index")

    def increment_attacker_index(self, index):
        if index == PLAYER_ONE:
            self.PLAYER_ONE_ATTACKER_INDEX += 1
            return self.PLAYER_ONE_ATTACKER_INDEX % 7
        elif index == PLAYER_TWO:
            self.PLAYER_TWO_ATTACKER_INDEX += 1
            return self.PLAYER_TWO_ATTACKER_INDEX % 7
        else:
            raise Exception("Unknown player index")

    def get_winner(self):
        player_one_winner = any(self.board[PLAYER_ONE]) and not any(self.board[PLAYER_TWO])
        player_two_winner = not any(self.board[PLAYER_ONE]) and any(self.board[PLAYER_TWO])
        no_winner = any(self.board[PLAYER_ONE]) and any(self.board[PLAYER_TWO])
        draw = not any(self.board[PLAYER_ONE]) and not any(self.board[PLAYER_TWO])

        if player_one_winner:
            return GameResult(player_one_win_percentage=100)
        if player_two_winner:
            return GameResult(player_two_win_percentage=100)
        if no_winner:
            return GameResult(unresolved=True)
        if draw:
            return GameResult(draw=100)

    def summon_minion(self, minion, player, location):
        if len(self.board[player]) < 7:
            self.board[player].insert(location, minion)

    def copy(self):
        from copy import copy
        scenario = Scenario()
        scenario.player_turn = self.player_turn
        board_one = [
            copy(minion) for minion in self.board[PLAYER_ONE]
        ]
        board_two = [
            copy(minion) for minion in self.board[PLAYER_TWO]
        ]
        scenario.set_board(board_one, board_two)
        scenario.player_turn = self.player_turn
        scenario.level = self.level + 1
        return scenario

    def __str__(self):
        string = 'Level: ' + str(self.level) + '. Board One: '
        for m in self.board[PLAYER_ONE]:
            string += str(m)
        string += '\n          Board Two: '
        for m in self.board[PLAYER_TWO]:
            string += str(m)

        return string


class Oracle:

    MAXIMUM_THREADS = 32

    @staticmethod
    def next_player(player_index):
        return 3 - player_index

    def calculate_game_result_density(self, scenario, method='decision_tree', args=None):
        que = Queue()

        if method == 'decision_tree':
            if len(scenario.board[PLAYER_ONE]) != len(scenario.board[PLAYER_TWO]):

                if len(scenario.board[PLAYER_ONE]) > len(scenario.board[PLAYER_TWO]):
                    starter = PLAYER_ONE
                else:
                    starter = PLAYER_TWO

                scenario = copy(scenario)
                scenario.player_turn = starter
                density = self.solve_for_all_solutions(scenario)
            else:
                # player 1 starts
                scenario.player_turn = 1
                t1 = threading.Thread(target=lambda q, s: q.put(self.solve_for_all_solutions(s)), args=(que, scenario), name='thread-first')
                # density_one = self.calculate_game_result_density(scenario)
                t1.start()

                # player 2 starts
                scenario = copy(scenario)
                scenario.player_turn = 2
                t2 = threading.Thread(target=lambda q, s: q.put(self.solve_for_all_solutions(s)), args=(que, scenario), name='thread-second')
                # density_two = self.calculate_game_result_density(scenario)
                t2.start()

                t1.join()
                t2.join()

                densities = [que.get(), que.get()]
                # densities = [density_one, density_two]
                density = join_results(densities)

        elif method == 'sampling':
            sampling_amount = args['sampling_amount']
            densities = []
            threads = []
            for i in range(sampling_amount):
                if i < sampling_amount/2:
                    scenario.player_turn = 1
                else:
                    scenario.player_turn = 2

                if self.MAXIMUM_THREADS <= len(threads):
                    t = threads.pop(0)
                    t.join()

                t = threading.Thread(target=lambda q, s: q.put(self.solve_for_one_solution(s)),
                                      args=(que, scenario), name='thread-first')

                t.start()
                threads.append(t)

            while len(threads):
                t = threads.pop(0)
                t.join()

            while not que.empty():
                densities.append(que.get())

            density = join_results(densities)
        else:
            raise Exception('Unknown method!')

        return density

    def solve_for_one_solution(self, scenario):
        player_turn = scenario.player_turn
        child_scenario = self.execute_attack(player_turn, scenario)
        density = child_scenario.get_winner()
        if density.unresolved:
            child_scenario.player_turn = self.next_player(child_scenario.player_turn)
            return self.solve_for_one_solution(child_scenario)
        else:
            return density

    def solve_for_all_solutions(self, scenario):
        player_turn = scenario.player_turn

        densities = []

        if scenario.level < THREAD_LEVEL:
            tm = ThreadManager()

        for defender_index, defender in enumerate(scenario.board[self.next_player(player_turn)]):
            child_scenario = self.execute_attack(player_turn, scenario, defender_index=defender_index)
            density = child_scenario.get_winner()
            if density.unresolved:
                child_scenario.player_turn = self.next_player(child_scenario.player_turn)
                if scenario.level < THREAD_LEVEL:
                    thread = threading.Thread(
                        target=lambda manager, s: manager.density_queue.put(self.solve_for_all_solutions(s)),
                        args=(tm, child_scenario))
                    tm.thread_queue.put(thread)
                    thread.start()
                else:
                    density = self.solve_for_all_solutions(child_scenario)
                    densities.append(density)
            else:
                return density

        if scenario.level < THREAD_LEVEL:
            while not tm.thread_queue.empty():
                tm.thread_queue.get().join()
            while not tm.density_queue.empty():
                densities.append(tm.density_queue.get())

        return join_results(densities)

    def execute_attack(self, player: int, scenario: Scenario, defender_index: int = None):
        if defender_index is None:
            defender_index = random.randint(0, len(scenario.board[self.next_player(player)]) - 1)

        scenario = scenario.copy()
        attacker = scenario.board[player][scenario.get_attacker_index(player)]
        defender = scenario.board[self.next_player(player)][defender_index]
        attacker.perform_attack(defender)

        if not attacker.is_alive:
            scenario.board[player].remove(attacker)
            attacker.perform_deathrattle(scenario, player, scenario.get_attacker_index(player))
            # print(scenario)
        else:
            scenario.increment_attacker_index(player)

        if not defender.is_alive:
            scenario.board[self.next_player(player)].remove(defender)
            defender.perform_deathrattle(scenario, self.next_player(player), scenario.get_attacker_index(player))
            # print(scenario)

        scenario.player_turn = self.next_player(scenario.player_turn)
        return scenario
