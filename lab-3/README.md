# Introduction-to-Artificial-Intelligence lab-3

Exercise 3

The task of the lab is to write a program/script that builds a tree of a given Isolation game and then plays with itself using the minimax algorithm. Two cases had to be tested:

1. one player plays randomly (i.e. does not use our algorithm) and the other player tries to optimise his moves (random vs minimax)
2. both players make optimal decisions (minimax vs minimax)

## Rules of the game

- each player starts with a pawn that can move 1 space per turn (vertically, horizontally and diagonally)
- players alternate moves, 1 move at a time
- a player cannot place a pawn on a previously visited field or on the opponent's field - the game ends if the opponent cannot move any more

## Assumptions

- I have adopted a version of the Isolation game in which there is no draw. The player who is the first to be unable to make a move loses
- The heuristics I have defined calculate, in a given board state, how many moves a player can make and how many moves his opponent can make. The function returns the difference between the number of possible moves for each player. The higher the score, the more favourable the board state for the Max player and the lower the score, the more favourable the board state for the Min player.
