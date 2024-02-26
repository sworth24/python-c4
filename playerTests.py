import unittest

from player import Player


class PlayerTests(unittest.TestCase):
    def testIsComputer(self):
        computerPlayer = Player(isPlayer1=True, isComputer=True)
        self.assertEqual(computerPlayer.isComputer, True)

        humanPlayer = Player(isPlayer1=True, isComputer=False)
        self.assertEqual(humanPlayer.isComputer, False)

    def testIsPlayer1(self):
        player1 = Player(isPlayer1=True, isComputer=False)
        self.assertEqual(player1.isPlayer1, True)

        player2 = Player(isPlayer1=False, isComputer=False)
        self.assertEqual(player2.isPlayer1, False)


unittest.main()
