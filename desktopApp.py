import random
from tkinter import BOTH, Canvas, Frame, Label, StringVar, IntVar, Tk, messagebox, Checkbutton

from board import Board
from bot import Bot
from player import Player


class DesktopApp():

    def __init__(self, root):
        super().__init__()

        # We need to root to kill the game when its finished
        self.root = root

        # Set the title
        self.root.title("Connect 4")

        # Create the canvas child item which will draw the board
        self.boardCanvas = Canvas(root)
        # Size the canvas so it fits the parent
        self.boardCanvas.grid(row=0, column=0, rowspan=2, padx=20, pady=20, sticky="E")

        # Create the Player 1 options check button with label
        Label(root, text="Player 1").grid(row=0, column=1, sticky="W")
        p1Computer = IntVar()
        Checkbutton(root, text="Computer Controlled",
                    variable=p1Computer).grid(row=0, column=2, sticky="W")

        # Create the Player 2 options check button
        Label(root, text="Player 2").grid(row=1, column=1, sticky="W")
        p1Computer = IntVar()
        Checkbutton(root, text="Computer Controlled",
                    variable=p1Computer).grid(row=1, column=2, sticky="W")

        # Create the information label
        self.info = StringVar()
        infoLabel = Label(root, textvariable=self.info)
        infoLabel.grid(row=2, column=0, columnspan=3)

        # These are used for the drawing of the board
        self.chipSize = 20
        self.margin = 10

        # This is the AI for computer controller players
        self.bot = Bot()

        # Create the player objects and the board. We need to find a way of passing these in at some point
        self.player1 = Player(isPlayer1=True, isComputer=False)
        self.player2 = Player(isPlayer1=False, isComputer=True)
        self.board = Board(numberOfColumns=10, numberOfRows=10)

        # A human move is recorded by the user clicking on a column within the board
        self.waitingForHumanMove = False

        def callback(event):
            self.onMouseClick(event)
        self.boardCanvas.bind("<Button-1>", callback)

        # Start the game
        self.startGame()

    def drawBoard(self, board):
        rowCount = board.numberOfRows
        colCount = board.numberOfColumns

        width = (self.chipSize+self.margin)*colCount + self.margin
        height = (self.chipSize+self.margin) * rowCount + self.margin
        self.boardCanvas.create_rectangle(0, 0, width, height, fill="blue")
        # Resize the canvase so it is the same size as the board rectange
        self.boardCanvas.config(width=width,height=height)

        y = self.margin
        # We need to draw the columns from top to bottom
        row = rowCount - 1

        while row >= 0:
            x = self.margin
            for col in range(0, colCount):
                fill = "white"

                if (row < len(board.columns[col])):
                    if (board.columns[col][row] == True):
                        # Player 1 chip
                        fill = "red"
                    else:
                        # Player 2 chip
                        fill = "yellow"

                self.boardCanvas.create_oval(
                    x, y, x+self.chipSize, y+self.chipSize, fill=fill)
                x = x + self.chipSize + self.margin
            y = y + self.chipSize + self.margin
            row = row - 1

    def onMouseClick(self, event):
        if self.waitingForHumanMove:
            # Determine which column was clicked based on the event x position
            row = int((event.x - self.margin/2) /
                      (self.chipSize + self.margin))

            # Check if the move is valid. For example the column might be full up
            if self.board.isValidMove(row):
                if (self.board.isPlayer1Turn()):
                    player = self.player1
                    nextPlayer = self.player2
                else:
                    player = self.player2
                    nextPlayer = self.player1

                self.playMove(player, nextPlayer, row)

    def startGame(self):
        self.board.clear()
        self.drawBoard(self.board)
        self.makeNextMove(self.player1, self.player2)

    def makeNextMove(self, player, nextPlayer):
        if player.isComputer:
            nextMoves = self.bot.suggestNextMove(
                nextPlayer, player, self.board)
            # Choose a random move from nextMoves
            nextMove = random.choice(nextMoves)
            self.playMove(player, nextPlayer, nextMove)
        else:
            # Wait for human player to make move
            self.waitingForHumanMove = True
            if (player.isPlayer1):
                self.info.set("Player 1 - Make a Move")
            else:
                self.info.set("Player 2 - Make a Move")

    def playMove(self, player, nextPlayer, row):
        self.waitingForHumanMove = False
        self.board.makeMove(player, row)
        self.drawBoard(self.board)

        if (self.board.isWinner(player)):

            if (player.isPlayer1):
                winMessage = "Player 1 has won"

            else:
                winMessage = "Player 2 has won"

            anotherGame = messagebox.askquestion(
                self.root.title, "{}\n\nDo you want to play another game".format(winMessage))
            if (anotherGame == "yes"):
                self.startGame()
            else:
                self.root.destroy()
            return

        # Check if there are no move valid moves. In which case it is a draw
        validMoves = self.board.getValidMoves()

        if len(validMoves) == 0:
            anotherGame = messagebox.askquestion(
                self.root.title, "It's a draw\n\nDo you want to play another game")
            if (anotherGame == "yes"):
                self.startGame()
            else:
                self.root.destroy()
            return
        else:
            self.makeNextMove(nextPlayer, player)


def main():

    root = Tk()
    ex = DesktopApp(root)
    root.geometry("600x400")
    root.mainloop()


if __name__ == '__main__':
    main()
