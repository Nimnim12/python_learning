import unittest
import sudoku_solver


class TestSudokuSolver(unittest.TestCase):
    board = [
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

    def test_find_zero(self):
        row, col = sudoku_solver.find_zero(TestSudokuSolver.board)
        self.assertEqual(row, 0, "Found wrong row")
        self.assertEqual(col, 1, "Found wrong column")

    def test_find_row_values(self):
        values = [0 for i in range(10)]
        sudoku_solver.find_row_values(TestSudokuSolver.board, 2, 2, values)
        true_values = [0, 1, 0, 0, 0, 1, 0, 0, 0, 1]
        self.assertEqual(values, true_values, "Wrong possible values in row")

    def test_find_col_values(self):
        values = [0 for i in range(10)]
        sudoku_solver.find_col_values(TestSudokuSolver.board, 0, 4, values)
        true_values = [0, 1, 1, 1, 0, 0, 0, 0, 1, 0]
        self.assertEqual(values, true_values, "Wrong possible values in row")

    def test_find_square_values(self):
        values = [0 for i in range(10)]
        sudoku_solver.find_square_values(TestSudokuSolver.board, 0, 4, values)
        true_values = [0, 1, 0, 0, 0, 1, 0, 0, 0, 1]
        self.assertEqual(values, true_values, "Wrong possible values in row")


if __name__ == '__main__':
    unittest.main()
