import unittest

from board import Board
from bot import Bot
from player import Player


class BotTests(unittest.TestCase):
    def testSuggestedMoves(self):
        player1 = Player(True, True)
        player2 = Player(False, True)
        board = Board(7, 6)
        bot = Bot()

        # All moves are vald for an empty board
        moves = bot.suggestNextMove(player1, player2, board)
        self.assertEqual(moves, [0, 1, 2, 3, 4, 5, 6])

        # If player 1 has three in a row then the best move for player 1 is the winning move
        board.makeMove(player1, 0)
        board.makeMove(player2, 0)
        board.makeMove(player1, 1)
        board.makeMove(player2, 0)
        board.makeMove(player1, 2)
        winningMoves = bot.suggestNextMove(player1, player2, board)
        self.assertEqual(winningMoves, [3])
        notLosingMoves = bot.suggestNextMove(player2, player1, board)
        self.assertEqual(notLosingMoves, [3])


unittest.main()
