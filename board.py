# The board class is used to store a game at any one time
class Board:
    def __init__(self, numberOfColumns, numberOfRows):
        # The number of columns being used. Will be 7 in a traditional game of C4.
        self.numberOfColumns = numberOfColumns

        # The number of rows being used. Will be 6 in a traditional game of C4
        self.numberOfRows = numberOfRows

        # The board is a stored as an array of columns, where each column is an array of rows.
        # A move is made by specifying the column. This will append to this array giving a column and a row.
        # So to begin with we start with each column being empty
        self.columns = []

        for x in range(0, numberOfColumns):
            self.columns.append([])  # appending the empty

    # Check if is valid to make a move in the specified column. The column is zero based.
    # Returns True or False
    def isValidMove(self, column):
        return column >= 0 and column < self.numberOfColumns and len(self.columns[column]) < self.numberOfRows

    # Make a move with the specified player and column. For performance we do not check if the move is valid
    # so you should call isValidMove() before calling makeMove()
    def makeMove(self, player, column):
        self.columns[column].append(player.isPlayer1)

    # Clear the board in preparation for a new game
    def clear(self):
        for col in range(0, self.numberOfColumns):
            self.columns[col] = []

    # Check if it is player 1's turn. Will return True if it player 1 to go next. Will return False if it is player 2
    def isPlayer1Turn(self):
        # count the number of moves which have been made. If this is even then player 1 should make the next move
        moveCount = 0

        for col in range(0, self.numberOfColumns):
            moveCount = moveCount + len(self.columns[col])

        if moveCount % 2 == 0:
            return True
        else:
            return False

    # Get a list of all valid moves
    def getValidMoves(self):
        validMoves = []

        # Try each column to see if it a valid move
        for col in range(0, self.numberOfColumns):
            if (self.isValidMove(col)):
                validMoves.append(col)

        return validMoves

    # Check whether this move will win the game
    def isWinningMove(self, player, column):
        # This can be optimised later to just check the moves from the new chip, but for now check the whole board
        self.columns[column].append(player.isPlayer1)
        isWinningMove = self.isWinner(player)
        self.columns[column].pop()

        return isWinningMove

    # Check if the specified player has won the game
    def isWinner(self, player):
        # first check vertically for each column for 4 in a row
        for col in range(0, self.numberOfColumns):
            rowCount = len(self.columns[col])

            if rowCount >= 4:
                matchCount = 0
                for row in range(0, rowCount):
                    if row >= len(self.columns[col]):
                        break
                    elif self.columns[col][row] == player.isPlayer1:
                        matchCount = matchCount + 1
                        if matchCount >= 4:
                            return True
                    else:
                        matchCount = 0

        # now check horizontally for each row
        for row in range(0, self.numberOfRows):
            matchCount = 0
            for col in range(0, self.numberOfColumns):
                if len(self.columns[col]) > row and self.columns[col][row] == player.isPlayer1:
                    matchCount = matchCount + 1
                    if matchCount >= 4:
                        return True
                else:
                    matchCount = 0

        # Now check diagonally SW to NE starting on y axis
        # Do not check after numberOfRows - 4 because you cannot get 4 in a row with only 3 chips
        for startRow in range(0, self.numberOfRows - 3):
            matchCount = 0
            row = startRow
            col = 0
            while(row < self.numberOfRows and col < self.numberOfColumns):
                if len(self.columns[col]) > row and self.columns[col][row] == player.isPlayer1:
                    matchCount = matchCount + 1
                    if matchCount >= 4:
                        return True
                else:
                    matchCount = 0
                row = row + 1
                col = col + 1

        # Now check diagonally SW to NE starting on x axis
        # Do not check after numberOfCols - 4 because you cannot get 4 in a row with only 3 chips
        # Start on col 1 because col 0 is the same as row 0 which has already been checked
        for startCol in range(1, self.numberOfColumns - 3):
            matchCount = 0
            row = 0
            col = startCol
            while(row < self.numberOfRows and col < self.numberOfColumns):
                if len(self.columns[col]) > row and self.columns[col][row] == player.isPlayer1:
                    matchCount = matchCount + 1
                    if matchCount >= 4:
                        return True
                else:
                    matchCount = 0
                row = row + 1
                col = col + 1

        # Now check diagonally SE to NW starting on y axis
        # Do not check after numberOfRows - 4 because you cannot get 4 in a row with only 3 chips
        for startRow in range(0, self.numberOfRows - 3):
            matchCount = 0
            row = startRow
            col = self.numberOfColumns - 1
            while(row < self.numberOfRows and col >= 0):
                if len(self.columns[col]) > row and self.columns[col][row] == player.isPlayer1:
                    matchCount = matchCount + 1
                    if matchCount >= 4:
                        return True
                else:
                    matchCount = 0
                row = row + 1
                col = col - 1

        # Now check diagonally SE to NW starting on x axis
        # Start on col 4 because you cannot get 3 in a row with only 3 chips
        # Finish on numberOfColumns - 1 because col numberOfColumns is the same as row 0 which has already been checked
        for startCol in range(3, self.numberOfColumns - 1):
            matchCount = 0
            row = 0
            col = startCol
            while(row < self.numberOfRows and col >= 0):
                if len(self.columns[col]) > row and self.columns[col][row] == player.isPlayer1:
                    matchCount = matchCount + 1
                    if matchCount >= 4:
                        return True
                else:
                    matchCount = 0
                row = row + 1
                col = col - 1

        return False

    # Check if 2 boards are the same
    def isEqual(self, otherBoard):
        # Must have same number of columns
        if self.numberOfColumns != otherBoard.numberOfColumns:
            return False
        # Must have same number of rows
        if self.numberOfRows != otherBoard.numberOfRows:
            return False

        # Check each column
        for col in range(0, self.numberOfColumns):
            # Column length must match
            if len(self.columns[col]) != len(otherBoard.columns[col]):
                return False

            # And each column chip must match
            for row in range(0, len(self.columns[col])):
                if self.columns[col][row] != otherBoard.columns[col][row]:
                    return False

        # The boards are identical
        return True
