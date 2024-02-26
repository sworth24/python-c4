import os
import unittest

from board import Board
from fileStorage import FileStorage
from player import Player


class FileStorageTests(unittest.TestCase):
    def testSave(self):
        board = Board(4, 4)
        player1 = Player(True, False)
        player2 = Player(False, False)
        tempFileName = "test.c4"

        board.makeMove(player1, 0)
        board.makeMove(player2, 1)
        board.makeMove(player1, 2)
        board.makeMove(player2, 3)
        board.makeMove(player2, 0)
        board.makeMove(player1, 1)
        board.makeMove(player2, 2)
        board.makeMove(player1, 0)
        board.makeMove(player2, 1)
        board.makeMove(player2, 0)

        storage = FileStorage()

        storage.saveBoard(board, tempFileName)

        loadedBoard = storage.loadBoard(tempFileName)

        self.assertTrue(board.isEqual(loadedBoard))

        os.remove(tempFileName)


unittest.main()
