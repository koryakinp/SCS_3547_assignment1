from game import Game
import numpy as np


def minimax(game, depth):
    if depth == 0 or game.is_terminal_state():
        return game.evaluate()

    if game.side_to_move == 1:
        maxEval = -99999
        for move in game.get_legal_moves():
            branch = Game(4, 4, 3, np.copy(game.board), game.side_to_move)
            branch.make_move(move)
            temp = minimax(branch, depth - 1)
            if temp > maxEval:
                maxEval = temp
        return maxEval

    if game.side_to_move == -1:
        minEval = 99999
        for move in game.get_legal_moves():
            branch = Game(4, 4, 3, np.copy(game.board), game.side_to_move)
            branch.make_move(move)
            temp = minimax(branch, depth - 1)
            if temp < minEval:
                minEval = temp
        return minEval


def minimax_withpruning(game, depth, alpha, beta):
    if depth == 0 or game.is_terminal_state():
        return game.evaluate()

    if game.side_to_move == 1:
        maxEval = -99999
        for move in game.get_legal_moves():
            branch = Game(4, 4, 3, np.copy(game.board), game.side_to_move)
            branch.make_move(move)
            temp = minimax_withpruning(branch, depth - 1, alpha, beta)
            maxEval = max(temp, maxEval)
            alpha = max(alpha, temp)
            if beta <= alpha:
                break

        return maxEval

    if game.side_to_move == -1:
        minEval = 99999
        for move in game.get_legal_moves():
            branch = Game(4, 4, 3, np.copy(game.board), game.side_to_move)
            branch.make_move(move)
            temp = minimax_withpruning(branch, depth - 1, alpha, beta)
            minEval = min(temp, minEval)
            beta = min(beta, temp)
            if beta <= alpha:
                break
        return minEval
