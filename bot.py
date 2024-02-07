# The Bot class is the AI to suggest the next move
class Bot:
    # Return an array of the suggested next moves
    def suggestNextMove(self, player, opponentPlayer, board):
        # Get the list of valid moves
        validMoves = board.getValidMoves()
        print("valid moves = {}".format(validMoves))

        if len(validMoves) == 0:
            # There are no valid moves - so the game is a draw
            return []
        elif len(validMoves) == 1:
            # If there is only one valid move then this is the only move we can make.
            # No point checking to see if it is a good move
            return validMoves

        # First check if we can win in the next move
        winningMoves = self.getWinningMoves(player, board, validMoves)
        print("winning moves = {}".format(winningMoves))

        if len(winningMoves) > 0:
            return winningMoves

        # Now get an array of the moves for which the opponent will win next if that move is made
        opponentWinningMoves = self.getWinningMoves(
            opponentPlayer, board, validMoves)
        print("opponentWinningMoves moves = {}".format(opponentWinningMoves))

        # If there are any moves in which the opponent will win then we must try and stop them with the same move
        if (len(opponentWinningMoves)):
            return opponentWinningMoves

        # So we have found multiple moves in which the opponent will not win in the next turn
        # For now just return this list of moves
        # But we will improve this with recursion later
        return validMoves

    # Returns an array of all the columns which will win th game if this is the next move
    def getWinningMoves(self, player, board, validMoves):
        winningMoves = []

        # Iterate over the columns and test if the move is valid and a winning move
        for col in validMoves:
            if (board.isWinningMove(player, col)):
                winningMoves.append(col)

        return winningMoves
