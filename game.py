import numpy as np
import matplotlib.pyplot as plt


class Game:

    def __init__(
            self,
            height=6,
            width=7,
            win_condition=4,
            position=None,
            side_to_move=1):
        self.height = height
        self.width = width
        self.win_condition = win_condition
        if position is None:
            self.board = np.zeros((height, width), dtype='b')
        else:
            self.board = position
        self.side_to_move = side_to_move

    def get_state(self):
        return self.board, self.side_to_move

    def make_move(self, move):
        row = np.where(self.board[:, move] == 0)[0].min()
        self.board[row, move] = self.side_to_move
        self.side_to_move = self.side_to_move * -1

    def get_legal_moves(self):
        return np.where(self.board[self.height - 1] == 0)[0]

    def print_board(self):
        print(np.flipud(self.board))

    def draw_board(self):
        arr1 = np.where(self.board == 1)
        arr2 = np.where(self.board == -1)
        arr3 = np.where(self.board == 0)

        x_new = np.concatenate([arr1[0], arr2[0], arr3[0]])
        y_new = np.concatenate([arr1[1], arr2[1], arr3[1]])

        red = np.full(len(arr1[0]), 'red')
        green = np.full(len(arr2[0]), 'blue')
        white = np.full(len(arr3[0]), 'lightgrey')

        colors = np.concatenate([red, green, white])
        area = np.full(len(colors), 1000)

        plt.scatter(y_new, x_new, s=area, c=colors)
        plt.xlim(-0.5, 6.5)
        plt.ylim(-0.5, 5.5)
        plt.axis('off')
        plt.show()

    def evaluate(self):
        temp1 = np.where(self.board == 1)
        white_pieces = list(zip(temp1[0], temp1[1]))
        temp2 = np.where(self.board == -1)
        black_pieces = list(zip(temp2[0], temp2[1]))

        w_score = 0
        for piece in white_pieces:
            score = self.__get_max_in_a_row(piece[1], piece[0], 1)
            if score > w_score:
                w_score = score

        b_score = 0
        for piece in black_pieces:
            score = self.__get_max_in_a_row(piece[1], piece[0], -1)
            if score > b_score:
                b_score = score

        b_score = b_score * -1
        return w_score + b_score

    def __get_max_in_a_row(self, x, y, color):
        i = 1

        arr1 = [True]
        arr2 = [True]
        arr3 = [True]
        arr4 = [True]

        while i < self.win_condition:

            up = y + i
            down = y - i
            right = x + i
            left = x - i

            if up < self.height:
                arr1.append(self.board[up, x] == color)
            if down >= 0:
                arr1.insert(0, self.board[down, x] == color)

            if right < self.width:
                arr2.append(self.board[y, right] == color)
            if left >= 0:
                arr2.insert(0, self.board[y, left] == color)

            if up < self.height and right < self.width:
                arr3.append(self.board[up, right] == color)

            if down >= 0 and left >= 0:
                arr3.insert(0, self.board[down, left] == color)

            if up < self.height and left >= 0:
                arr4.append(self.board[up, left] == color)

            if down >= 0 and right < self.width:
                arr4.insert(0, self.board[down, right] == color)

            i += 1

        max_in_a_row = [
            self.__get_max_in_a_row_for_direction(arr1),
            self.__get_max_in_a_row_for_direction(arr2),
            self.__get_max_in_a_row_for_direction(arr3),
            self.__get_max_in_a_row_for_direction(arr4)
        ]

        return max(max_in_a_row)

    def __get_max_in_a_row_for_direction(self, arr):
        temp = 0
        cur_max_in_a_row = 0
        for square in arr:
            if square:
                cur_max_in_a_row += 1
                if cur_max_in_a_row > temp:
                    temp = cur_max_in_a_row
            else:
                cur_max_in_a_row = 0
        return temp

    def is_terminal_state(self):
        temp = np.where(self.board == self.side_to_move)
        pieces = list(zip(temp[0], temp[1]))
        score = 0
        for p in pieces:
            temp_score = self.__get_max_in_a_row(p[1], p[0], self.side_to_move)
            if score > score:
                score = temp_score

        return score == self.win_condition
