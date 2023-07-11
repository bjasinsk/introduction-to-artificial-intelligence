class Player:
    def __init__(self, symbol, x, y):
        self.x = x
        self.y = y
        self.symbol = symbol

    def __str__(self):
        if self.symbol == 2:
            return "MIN"
        if self.symbol == 3:
            return "MAX"

    def move(self, gameBoard, vectorX, vectorY):
        newPositionX = self.x + vectorX
        newPositionY = self.y + vectorY

        if newPositionX < 0 or newPositionX > len(gameBoard.board) - 1:
            print("Movement is not possible")
            return False

        if newPositionY < 0 or newPositionY > len(gameBoard.board[0] - 1):
            print("Movement is not possible")
            return False

        if gameBoard.board[newPositionX][newPositionY] != 0:
            print("Movement is not possible")
            return False

        gameBoard.board[self.x][self.y] = 1
        gameBoard.board[newPositionX][newPositionY] = self.symbol
        self.x = newPositionX
        self.y = newPositionY
        return True
