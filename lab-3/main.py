from Game import Game
import random
if __name__ == '__main__':
    N = 10

    winCounterMax = 0
    winCounterMin = 0
    for i in range(10):
        #below version of the programme with random starting points and playing minimax vs minimax
        # min_x = random.randint(0, N - 1)
        # min_y = random.randint(0, N - 1)
        # max_x = random.randint(0, N - 1)
        # max_y = random.randint(0, N - 1)
        #game1 = Game(N, min_x, min_y, max_x, max_y)
        #status, howManyMoves = game1.playMiniMaxVsMiniMax()

        #below is a version of the programme playing random vs minimax,
        game1 = Game(N)
        status, howManyMoves = game1.playRandomVsMiniMax()

        if status == 3:
            winCounterMax += 1
        if status == 2:
            winCounterMin += 1

    print("winCounterMax: ", winCounterMax)
    print("winCounterMin: ", winCounterMin)



