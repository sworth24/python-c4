import random

from board import Board
from bot import Bot
from player import Player
from fileStorage import FileStorage

saveFilePath = "save.py"

class ConsoleApp:
    def __init__(self):
        self.bot = Bot()
        self.fileStorage = FileStorage()

    def run(self):
        if self.getYesNoAnswer("Would you like to play a game of Connect 4") == False:
            return

        player1Name = input("What is the name of the first player?\n").capitalize()
        player1Computer = self.getYesNoAnswer(
            "Hello {}. Are you a computer player".format(player1Name))
        player1 = Player(name=player1Name, isPlayer1=True,
                        isComputer=player1Computer)

        player2Name = input(
            "What is the name of the second player?\n").capitalize()
        player2Computer = self.getYesNoAnswer(
            "Hello {}. Are you a computer player".format(player2Name))
        player2 = Player(name=player2Name, isPlayer1=False,
                        isComputer=player2Computer)

        loadFileExists = self.fileStorage.saveFileExists(saveFilePath)

        if (loadFileExists):
            loadGame = self.getYesNoAnswer("Do you want to load a previous game")
        else:
            loadGame = False

        if loadGame:
            board = self.fileStorage.loadBoard(saveFilePath)

            self.drawBoard(board)

            if (board.isPlayer1Turn()):
                self.makeMove(player1, player2, board)
            else:
                self.makeMove(player2, player1, board)
        else:
            board = Board(numberOfColumns=7, numberOfRows=6)
            self.makeMove(player1, player2, board)

    def makeMove(self, currentPlayer, nextPlayer, board):
        if currentPlayer.isComputer:
            nextMoves = self.bot.suggestNextMove(currentPlayer, nextPlayer, board)
            # Choose a random move from nextMoves
            nextMove = random.choice(nextMoves)
        else:
            nextMove = self.getHumanMove(currentPlayer, board)

        print("{} placed a chip in column {}".format(
            currentPlayer.name, nextMove + 1))

        winner = board.isWinningMove(currentPlayer, nextMove)
        board.makeMove(currentPlayer, nextMove)

        self.drawBoard(board)

        if (winner):
            playAgain = self.getYesNoAnswer("{} won. Do you want to play again".format(currentPlayer.name))

            if (playAgain):
                board.clear()
                if currentPlayer.isPlayer1:
                    self.makeMove(currentPlayer, nextPlayer, board)
                else:
                    self.makeMove(nextPlayer, currentPlayer, board)
            else:
                return
        elif (len(board.getValidMoves()) == 0):
            playAgain = self.getYesNoAnswer("Its a draw. Do you want to play again")

            if (playAgain):
                board.clear()
                if currentPlayer.isPlayer1:
                    self.makeMove(currentPlayer, nextPlayer, board)
                else:
                    self.makeMove(nextPlayer, currentPlayer, board)
            else:
                return
        else:
            self.makeMove(nextPlayer, currentPlayer, board)

    def drawBoard(self, board):
        print("\n")

        boardHeader = "|"
        boardMargin = "+"

        for col in range(0, board.numberOfColumns):
            boardHeader = "{}{}|".format(boardHeader, col + 1)
            boardMargin = "{}-+".format(boardMargin)

        print(boardHeader)
        print(boardMargin)

        i = board.numberOfRows - 1
        while i >= 0:
            print(self.getBoardRowString(board, i))
            i = i - 1

        print("\n")

    def getBoardRowString(self, board, row):
        rowString = "|"
        for col in range(0, board.numberOfColumns):
            if len(board.columns[col]) > row:
                if (board.columns[col][row] == False):
                    rowString += "X"
                else:
                    rowString += "O"
            else:
                rowString += " "

            rowString += "|"

        return rowString

    def getHumanMove(self, player, board):
        while True:
            nextMove = input("{} please enter the column or type 'exit' to save and quit\n".format(player.name))

            if nextMove.upper() == "EXIT":
                self.fileStorage.saveBoard(board, saveFilePath)
                return

            if nextMove.isdigit():
                # Human column is 1 based so we subtract 1 to make it 0 based
                nextMove = int(nextMove) - 1
                if board.isValidMove(nextMove):
                    return nextMove
                else:
                    print("{} is not a valid column\n".format(nextMove))
            else:
                print("Please enter a valid digit for the column\n")

    # Returns a boolean response from a question
    def getYesNoAnswer(self, question):
        while True:
            response = input('{}?\n'.format(question)).upper()

            if response == 'Y' or response == 'YES':
                return True
            elif response == 'N' or response == 'NO':
                return False
            else:
                print('Please enter \'Y\' or \'N\'')

def main():
    app = ConsoleApp()

    app.run()

main()
