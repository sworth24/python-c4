from board import Board
from player import Player


class FileStorage:
    # Save the board to a file. We use:
    #   'O' for player 1 chip
    #   'X' for player 2 chip
    #   '.' for no chip
    def saveBoard(self, board, filePath):
        # We write the lines from top to bottom the same way you would view the board
        boardString = ""
        i = board.numberOfRows - 1
        while i >= 0:
            # Append the new line if already written a line
            if len(boardString) > 0:
                boardString += "\n"
            boardString += self.getBoardRowString(board, i)
            i = i - 1
        file = open(filePath, "w")
        file.write(boardString)
        file.close()

    # Returns a board row as a string
    def getBoardRowString(self, board, row):
        textToWrite = ""
        for col in range(0, board.numberOfColumns):
            if len(board.columns[col]) > row:
                if (board.columns[col][row] == False):
                    textToWrite += "X"
                else:
                    textToWrite += "O"
            else:
                textToWrite += "."
        return textToWrite

    # Load the board from a file
    def loadBoard(self, filePath):
        file = open(filePath, "r")
        boardString = file.read()
        file.close()

        # Split the board into a series of row string using the line separator
        rowStrings = boardString.split("\n")

        # The number of rows is determined by the number of row lines.
        # One row for each line
        rows = len(rowStrings)

        # The number of columns is determined by the number of characters in any line.
        # One character for each column
        # All row lines should have the same number of characters
        cols = len(rowStrings[0])

        # Create the empty board
        board = Board(cols, rows)

        player1 = Player(True, False)
        player2 = Player(False, False)

        # The rows are ordered from top to bottom. We need to add the chips starting from the bottom
        # which is the last row
        row = rows - 1

        while(row >= 0):
            for col in range(0, len(rowStrings[row])):
                if rowStrings[row][col] == "O":
                    board.makeMove(player1, col)
                elif rowStrings[row][col] == "X":
                    board.makeMove(player2, col)
            row = row - 1

        return board
