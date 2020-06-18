
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

#TODO: add solved sudoku for reference

def board_print(board):
    for i in range(9):
        for j in range(9):
            print(str(board[i][j]) + " ", end='')
            if j == 2 or j == 5:
                print("| ", end='')
        print()
        if i == 2 or i == 5:
            print("---------------------")


# TODO: add solved sudoku for reference
def find_zero(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None


def find_row_values(board, row, col, values):
    for i in range(9):
        if i != col:
            if board[row][i] != 0:
                values[board[row][i]] += 1
    return None


def find_col_values(board, row, col, values):
    for i in range(9):
        if i != row:
            if board[i][col] != 0:
                values[board[i][col]] += 1
    return None


def find_square_values(board, row, col, values):
    for i in range(3 * (row // 3), 3 * (row // 3) + 3):
        for j in range(3 * (col // 3), 3 * (col // 3) + 3):
            if board[i][j] != 0:
                values[board[i][j]] += 1
    return None


def find_values(board, row, col):
    values = [0 for i in range(10)]
    find_row_values(board, row, col, values)
    find_col_values(board, row, col, values)
    find_square_values(board, row, col, values)
    possible_answers = []
    for i in range(1,10):
        if values[i] == 0:
            possible_answers.append(i)
    return possible_answers


def solve(board):
    if(find_zero(board) == None): return
    row,col = find_zero(board)
    possible_answers = find_values(example_board,row,col)
    for i in possible_answers:
        example_board[row][col] = i
        solve(example_board)
        if (find_zero(board) == None): return
    example_board[row][col] = 0


def main():
    solve(example_board)
    board_print(example_board)

if __name__ == '__main__':
    main()




