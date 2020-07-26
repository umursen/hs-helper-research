class Minion:

    def __init__(self, attack, health, divine_shield=None, deathrattle=None):
        self.attack = attack
        self.health = health
        self.divine_shield = divine_shield
        self.deathrattle = deathrattle
        self.is_alive = True

    def perform_attack(self, defender):
        attacker: Minion
        defender: Minion

        self.health -= defender.attack

        if self.health <= 0:
            self.is_alive = False

        defender.health -= self.attack
        if defender.health <= 0:
            defender.is_alive = False

    def __str__(self):
        return '(' + str(self.attack) + ',' + str(self.health) + ')'
