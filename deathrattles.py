import random
import numpy as np


def give_divine_shield(scenario, player, position):
    minions = scenario.board[player]
    indices_wo_ds = list()
    for i, minion in enumerate(minions):
        if not minion.divine_shield and i != position:
            indices_wo_ds.append(i)
    idx = random.choice(indices_wo_ds)
    scenario.board[player][idx].divine_shield = True


def give_attack(scenario, player, position, attack):
    minions = scenario.board[player].copy()
    indices = minions.remove(position)
    idx = random.choice(indices)
    scenario.board[player][idx].attack += attack
