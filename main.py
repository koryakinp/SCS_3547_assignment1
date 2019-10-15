from game import Game
from minimax import minimax, minimax_withpruning

game = Game(5, 5, 4)
res = minimax_withpruning(game, 20, -99, 99)
print(res)
