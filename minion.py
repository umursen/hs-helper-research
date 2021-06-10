class Minion:

    def __init__(self, attack, health, divine_shield=None, active=True):
        self.attack = attack
        self.health = health
        self.divine_shield = divine_shield
        self.is_alive = True
        self.active = active

    def perform_attack(self, defender):
        attacker: Minion
        defender: Minion

        if not self.divine_shield:
            self.health -= defender.attack
        else:
            self.divine_shield = False

        if self.health <= 0:
            self.is_alive = False

        if not defender.divine_shield:
            defender.health -= self.attack
        else:
            defender.divine_shield = False

        if defender.health <= 0:
            defender.is_alive = False

    def perform_deathrattle(self, scenario, player, position):
        pass

    def __str__(self):
        return '(' + str(self.attack) + ',' + str(self.health) + ')'
