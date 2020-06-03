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
