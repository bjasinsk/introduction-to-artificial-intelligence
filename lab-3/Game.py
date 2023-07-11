import copy
import random

from Board import Board
from Player import Player


class Game:
    def __init__(self, N=10, min_x=None, min_y=None, max_x=None, max_y=None):
        self.gameBoard = Board(N, min_x, min_y, max_x, max_y)
        if min_x is None:
            min_x = 0
        if min_y is None:
            min_y = 0
        if max_x is None:
            max_x = N-1
        if max_y is None:
            max_y = N-1

        self.MIN = Player(2, min_x, min_y)
        self.MAX = Player(3, max_x, max_y)

        self.actualPlayer = self.MAX

    #true -> move is possible
    #false -> move is not possible
    def gameStatus(self):
        possibleMovesVectors = self.possibleMoves()

        if len(possibleMovesVectors) != 0:
            return True
        else:
            return False

    def isGameOver(self, board, player):
        possibleMovesVectors = self.possibleMoves(board, player)

        if len(possibleMovesVectors) != 0:
            return False
        else:
            return True

    def possibleMoves(self, boardToCheck = None, playerToCheck = None):
        if boardToCheck is None:
            boardToCheck = self.gameBoard

        if playerToCheck is None:
            playerToCheck = self.actualPlayer

        possibleMovesVectors = []
        for vectorX in range(-1, 2):
            for vectorY in range(-1, 2):
                if vectorX == 0 and vectorY == 0:
                    continue
                newPositionX = playerToCheck.x + vectorX
                newPositionY = playerToCheck.y + vectorY

                if newPositionX < 0 or newPositionX > len(boardToCheck.board) - 1:
                    continue

                if newPositionY < 0 or newPositionY > len(boardToCheck.board[0]) - 1:
                    continue

                if boardToCheck.board[newPositionX][newPositionY] == 0:
                    possibleMovesVectors.append((vectorX, vectorY))

        return possibleMovesVectors

    def possibleBoardConfigurations(self, boardToCheck = None, playerToCheck = None):
        if boardToCheck is None:
            boardToCheck = self.gameBoard

        if playerToCheck is None:
            playerToCheck = self.actualPlayer

        configurations = []
        moves = self.possibleMoves(boardToCheck, playerToCheck)

        for moveFromPossiblePlace in moves:
            possibleBoard = boardToCheck
            possiblePlayer = playerToCheck
            newBoardConfig = copy.deepcopy(possibleBoard)
            playerToSimulateMove = copy.deepcopy(possiblePlayer)
            playerToSimulateMove.move(newBoardConfig, moveFromPossiblePlace[0], moveFromPossiblePlace[1])
            configurations.append(newBoardConfig)
        return configurations

    def switchPlayer(self):
        if self.actualPlayer == self.MAX:
            self.actualPlayer = self.MIN
        else:
            self.actualPlayer = self.MAX
        return

    def heuristics(self, board, player, opponent):

        playerPossibleMoves = len(self.possibleMoves(board, player))
        enemyPossibleMoves = len(self.possibleMoves(board, opponent))

        mark = playerPossibleMoves - enemyPossibleMoves
        return mark


    def miniMax(self, board, player, opponent, depth):
        if depth == 0:
            return self.heuristics(board, player, opponent)
        if self.isGameOver(board, player):
            return self.heuristics(board, player, opponent)



        if player.symbol == 3:  #symbol 3 means MAX player
            bestValue = -100000
            for newBoard in self.possibleBoardConfigurations(board, player):
                value = self.miniMax(newBoard, opponent, player, depth - 1)
                if value > bestValue:
                    bestValue = value

            return bestValue

        if player.symbol == 2:  #symbol 2 means MIN player
            bestValue = 100000
            for newBoard in self.possibleBoardConfigurations(board, player):
                value = self.miniMax(newBoard, opponent, player, depth - 1)
                if value < bestValue:
                    bestValue = value

            return bestValue


    def inWhichWayGo(self, board, player, depth):
        bestScoreMAX = -1000000
        bestScoreMIN = 1000000
        bestMove = None
        for move in self.possibleMoves(board, player):
            temporaryBoard = copy.deepcopy(board)
            playerToSimulateMove = copy.deepcopy(player)

            if playerToSimulateMove.symbol == 3:
                playerToSimulateMoveOpponent = copy.deepcopy(self.MIN)
            else:
                playerToSimulateMoveOpponent = copy.deepcopy(self.MAX)

            playerToSimulateMove.move(temporaryBoard, move[0], move[1])
            score = self.miniMax(temporaryBoard, playerToSimulateMove, playerToSimulateMoveOpponent, depth)
            if score is None:
                score = 0

            if playerToSimulateMove.symbol == 3:
                if score > bestScoreMAX:
                    bestMove = move

            if playerToSimulateMove.symbol == 2:
                if score < bestScoreMIN:
                    bestMove = move
        return bestMove



    def chooseRandomMove(self):
        possibleMovesVectors = self.possibleMoves()
        print(possibleMovesVectors)
        randomMove = random.choice(possibleMovesVectors)
        print(randomMove)
        return randomMove

    def playRandomVsMiniMax(self):

        self.gameBoard.printBoard()
        #self.gameStatus() -> True = movement is possible
        #self.gameStatus() -> False = no movement is possible

        howManyMoves = 0
        while True:
            if self.gameStatus() == False:
                if self.actualPlayer == self.MIN:
                    print("Wygrana gracza:", self.MAX)
                    print("howManyMoves: ", howManyMoves)
                    return 3, howManyMoves
                else:
                    print("Wygrana gracza:", self.MIN)
                    print("howManyMoves: ", howManyMoves)
                    return 2, howManyMoves

            if self.actualPlayer == self.MAX:
                vector1 = self.inWhichWayGo(self.gameBoard, self.actualPlayer, 4)
                #print(vector1)
                self.actualPlayer.move(self.gameBoard, vector1[0], vector1[1])
                howManyMoves += 1

            if self.actualPlayer == self.MIN:
                vector2 = self.chooseRandomMove()
                self.actualPlayer.move(self.gameBoard, vector2[0], vector2[1])
                howManyMoves += 1

            self.gameBoard.printBoard()
            self.switchPlayer()

    def playMiniMaxVsMiniMax(self):

        self.gameBoard.printBoard()

        howManyMoves = 0
        while True:
            if self.gameStatus() == False:
                if self.actualPlayer == self.MIN:
                    print("Wygrana gracza:", self.MAX)
                    print("howManyMoves: ", howManyMoves)
                    return 3, howManyMoves
                else:
                    print("Wygrana gracza:", self.MIN)
                    print("howManyMoves: ", howManyMoves)
                    return 2, howManyMoves

            if self.actualPlayer.symbol == 3:
                vector1 = self.inWhichWayGo(self.gameBoard, self.actualPlayer, 3)
                print(vector1)
                self.actualPlayer.move(self.gameBoard, vector1[0], vector1[1])
                howManyMoves += 1

            if self.actualPlayer.symbol == 2:
                vector2 = self.inWhichWayGo(self.gameBoard, self.actualPlayer, 2)
                print(vector2)
                self.actualPlayer.move(self.gameBoard, vector2[0], vector2[1])
                howManyMoves += 1

            self.gameBoard.printBoard()
            self.switchPlayer()
