# The player class is used to hold whether they are the first player and whether it is a human or computer
class Player:
    def __init__(self, isPlayer1, isComputer):
        # isPlayer1 is True is they do first, False if player 2
        self.isPlayer1 = isPlayer1

        # isComputer is True is the player is a bot, False if a human
        self.isComputer = isComputer
