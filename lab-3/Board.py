import numpy as np


class Board:
    def __init__(self, N = 10, min_x=None, min_y=None, max_x=None, max_y=None):
        self.N = N
        self.board = np.zeros((N, N), dtype=int)

        if min_x is None:
            min_x = 0
        if min_y is None:
            min_y = 0
        if max_x is None:
            max_x = N-1
        if max_y is None:
            max_y = N-1

        self.board[max_x][max_y] = 3
        self.board[min_x][min_y] = 2
        #self.board[N - 1][N - 1] =3
        #self.board[0][0] = 2

    def printBoard(self):
        for i in range(self.N):
            oneRow = ''
            for j in range(self.N):
                oneRow += str(self.board[i][j])
                oneRow += ' '
            print(oneRow)
        print()



