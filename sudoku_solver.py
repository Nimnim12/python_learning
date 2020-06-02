import math

example_board = [
    [1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 4, 0, 0],
    [0, 0, 0, 9, 1, 5, 0, 0, 0],
    [0, 0, 4, 5, 3, 0, 0, 0, 0],
    [8, 0, 0, 0, 0, 0, 3, 0, 0],
    [0, 0, 6, 4, 8, 2, 1, 5, 0],
    [0, 8, 0, 0, 2, 1, 6, 0, 0],
    [0, 3, 0, 0, 0, 6, 0, 0, 0],
    [2, 0, 5, 3, 0, 0, 8, 0, 1],
]


# TODO: add solved sudoku for reference
def find_zero(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j


def find_row_values(board, row, col, values):
    for i in range(9):
        if i != col:
            if board[row][i] != 0:
                values[board[row][i]] += 1


def find_col_values(board, row, col, values):
    for i in range(9):
        if i != row:
            if board[i][col] != 0:
                values[board[i][col]] += 1


def find_square_values(board, row, col, values):
    for i in range(3 * math.floor(row / 3), 3 * math.floor(row / 3) + 3):
        for j in range(3 * math.floor(col / 3), 3 * math.floor(col / 3) + 3):
            if board[i][j] != 0:
                values[board[i][j]] += 1

