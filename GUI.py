from tkinter import *
from tkinter import messagebox
import random

import pygame
import pygame_menu
import sudoku_solver
from sudoku_solver import example_board


class Cell:
    def __init__(self, value):
        self.value = value
        self.potential_values = []
        self.selected = False
        self.set = False
        if (value != 0):
            self.set = True


class Board:
    def __init__(self, board,width=1200,height=900):
        self.cells = [[Cell(board[row][col]) for row in range(9)] for col in range(9)]
        sudoku_solver.solve(board)
        self.solved = [[Cell(board[row][col]) for row in range(9)] for col in range(9)]
        self.size=(width,height)

    def check_if_done(self):
        for i in range(9):
            for j in range(9):
                if (self.cells[i][j].value != self.solved[i][j].value):
                    return False
        return True

    def find_zero(self):
        for i in range(9):
            for j in range(9):
                if self.cells[i][j].value == 0:
                    return i, j
        return None

    def find_row_values(self, row, col, values):
        for i in range(9):
            if i != col:
                if self.cells[row][i].value != 0:
                    values[self.cells[row][i].value] += 1
        return None

    def find_col_values(self, row, col, values):
        for i in range(9):
            if i != row:
                if self.cells[i][col].value != 0:
                    values[self.cells[i][col].value] += 1
        return None

    def find_square_values(self, row, col, values):
        for i in range(3 * (row // 3), 3 * (row // 3) + 3):
            for j in range(3 * (col // 3), 3 * (col // 3) + 3):
                if self.cells[i][j].value != 0:
                    values[self.cells[i][j].value] += 1
        return None

    def find_values(self, row, col):
        values = [0 for i in range(10)]
        self.find_row_values(row, col, values)
        self.find_col_values(row, col, values)
        self.find_square_values(row, col, values)
        possible_answers = []
        for i in range(1, 10):
            if values[i] == 0:
                possible_answers.append(i)
        return possible_answers

    def solve(self):
        if (self.find_zero() == None): return True
        row, col = self.find_zero()
        possible_answers = self.find_values(row, col)
        #To generate random sudoku board
        random.shuffle(possible_answers)
        for i in possible_answers:
            self.cells[row][col].value = i
            self.solve()
            if (self.find_zero() == None):
                return True
        self.cells[row][col].value = 0
        return False

    @staticmethod
    def generate_sudoku():
        board = Board([[0 for row in range(9)] for col in range(9)])
        board.solve()
        return board


class Gui:
    BACKGROUND_COLOR = (250, 250, 250)
    LINE_COLOR = (100, 100, 100)
    BOLD_LINE_COLOR = (0, 0, 0)
    MARKED_COLOR = (255, 0, 0)
    POTENTIAL_VALUE_COLOR = (50, 50, 50)

    def __init__(self, board):
        self.board = board

    def create_window(self, width, height):
        # Create first window
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sudoku")
        return screen

    def mark_square(self, screen, row, col):
        width, height = self.board.size
        pygame.draw.line(screen, self.MARKED_COLOR, (col * (width // 9), row * (height // 9)),
                         (col * (width // 9), (row * (height // 9)) + (height // 9)), 5)
        pygame.draw.line(screen, self.MARKED_COLOR, ((col * (width // 9)) + (width // 9), row * (height // 9)),
                         ((col * (width // 9)) + (width // 9), (row * (height // 9)) + (height // 9)), 5)
        pygame.draw.line(screen, self.MARKED_COLOR, (col * (width // 9), row * (height // 9)),
                         ((col * (width // 9)) + (width // 9), row * (height // 9)), 5)
        pygame.draw.line(screen, self.MARKED_COLOR, (col * (width // 9), (row * (height // 9)) + (height // 9)),
                         ((col * (width // 9)) + (width // 9), (row * (height // 9)) + (height // 9)), 5)

    def draw_lines(self, screen):
        width, height = self.board.size
        # draw vertical lines
        for i in range(1, 9):
            pygame.draw.line(screen, self.LINE_COLOR, (i * (width // 9), 0), (i * (width // 9), 9*(height//9)), 3)
        # draw horizontal lines
        for i in range(1, 9):
            pygame.draw.line(screen, self.LINE_COLOR, (0, i * (height // 9)), (9*(width//9), i * (height // 9)), 3)

        # draw bold lines
        for i in range(10):
            if i % 3 == 0:
                pygame.draw.line(screen, self.BOLD_LINE_COLOR, (i * (width // 9), 0), (i * (width // 9), 9*(height//9)), 5)
        for i in range(10):
            if i % 3 == 0:
                pygame.draw.line(screen, self.BOLD_LINE_COLOR, (0, i * (height // 9)), (9*(width//9), i * (height // 9)), 5)

    def draw_number(self, screen, row, col):
        width, height = self.board.size
        font = pygame.font.SysFont("ComicSans", height//6)
        number = font.render(str(self.board.cells[row][col].value), 1, (0, 0, 0))
        screen.blit(number, ((col * (width // 9)) + (width // 40), (row * (height // 9)) + (height // 180)))

    def draw_potential_numbers(self, screen, row, col):
        width, height = self.board.size
        font = pygame.font.SysFont("ComicSans", height//30)
        values = self.board.cells[row][col].potential_values
        strnumbers = [str(integer) for integer in values]
        toprint = " ".join(strnumbers)
        number = font.render(toprint, 1, self.POTENTIAL_VALUE_COLOR)
        screen.blit(number, ((col * (width // 9) + (width // 100)), (row * (height // 9)) + (height // 180)))

    def draw_board(self, screen):
        for i in range(9):
            for j in range(9):
                if (self.board.cells[i][j].set == False):
                    self.draw_potential_numbers(screen, i, j)
                if (self.board.cells[i][j].value != 0):
                    self.draw_number(screen, i, j)

    def remove_number(self, screen, row, col):
        width, height = self.board.size
        pygame.draw.rect(screen, self.BACKGROUND_COLOR,
                         ((col * (width // 9)) + 10, (row * (height // 9)) + 10, (width // 9) - 20, (height // 9) - 20))

    def clicked(self, pos):
        width, height = self.board.size
        if (pos[0] < width and pos[1] < height):
            col = pos[0] / (width // 9)
            row = pos[1] / (height // 9)
            row = int(row)
            col = int(col)
            if row == 9: row=8
            if col == 9: col=8
            self.board.cells[row][col].selected = True
            return (int(row), int(col))
        else:
            return None

    def set_value(self, value, row, col):
        self.board.cells[row][col].value = value
        self.board.cells[row][col].set = True

    def remove_value(self,row,col):
        self.board.cells[row][col].value = 0
        self.board.cells[row][col].set = False

    def add_possible_value(self, value, row, col):
        if (len(self.board.cells[row][col].potential_values) < 4):
            self.board.cells[row][col].potential_values.append(value)

    def remove_possible_value(self,row,col):
        position =len(self.board.cells[row][col].potential_values) - 1
        del self.board.cells[row][col].potential_values[position]

    def remove_all_possible_values(self, row, col):
        self.board.cells[row][col].potential_values = []

    def check_if_done(self):
        return self.board.check_if_done()

    def find_zero(self):
        for i in range(9):
            for j in range(9):
                if self.board.cells[i][j].value == 0:
                    return i, j
        return None

    def find_row_values(self, row, col, values):
        for i in range(9):
            if i != col:
                if self.board.cells[row][i].value != 0:
                    values[self.board.cells[row][i].value] += 1
        return None

    def find_col_values(self, row, col, values):
        for i in range(9):
            if i != row:
                if self.board.cells[i][col].value != 0:
                    values[self.board.cells[i][col].value] += 1
        return None

    def find_square_values(self, row, col, values):
        for i in range(3 * (row // 3), 3 * (row // 3) + 3):
            for j in range(3 * (col // 3), 3 * (col // 3) + 3):
                if self.board.cells[i][j].value != 0:
                    values[self.board.cells[i][j].value] += 1
        return None

    def find_values(self, row, col):
        values = [0 for i in range(10)]
        self.find_row_values(row, col, values)
        self.find_col_values(row, col, values)
        self.find_square_values(row, col, values)
        possible_answers = []
        for i in range(1, 10):
            if values[i] == 0:
                possible_answers.append(i)
        return possible_answers

    def solve(self, screen):
        if (self.find_zero() == None): return True
        row, col = self.find_zero()
        possible_answers = self.find_values(row, col)
        for i in possible_answers:
            self.board.cells[row][col].value = i
            self.draw_number(screen, row, col)
            pygame.display.update()
            self.solve(screen)
            if (self.find_zero() == None):
                return True
            else:
                self.remove_number(screen, row, col)
                pygame.display.update()
        self.remove_number(screen, row, col)
        self.board.cells[row][col].value = 0
        pygame.display.update()
        return False


def main():
    board = Board(sudoku_solver.example_board)
    sudoku = Gui(board)
    screen = sudoku.create_window(1200, 900)
    menu = pygame_menu.Menu(300, 400, 'Welcome',
                            theme=pygame_menu.themes.THEME_BLUE)
    menu.add_button('Play', start_game, sudoku, screen)
    menu.add_button("How to play",how_to_play)
    menu.add_button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(screen)
def start_game(sudoku,screen):
    running = True
    clicked = False
    # Game Loop
    while (running):
        # Background options
        screen.fill(sudoku.BACKGROUND_COLOR)
        sudoku.draw_lines(screen)
        sudoku.draw_board(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if(pos[0]<sudoku.board.size[0] and pos[1]<sudoku.board.size[1]):
                    row, col = sudoku.clicked(pos)
                    clicked = True
            if clicked:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DELETE:
                        sudoku.remove_value(row,col)
                        sudoku.remove_all_possible_values(row,col)
                    if event.key == pygame.K_BACKSPACE:
                        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                            sudoku.remove_possible_value(row, col)
                        else:
                            sudoku.remove_value(row, col)
                    if event.key == pygame.K_RETURN:
                        if sudoku.check_if_done():
                            Tk().wm_withdraw()
                            messagebox.showinfo("Ok","Sudoku complete!")
                        else:
                            Tk().wm_withdraw()
                            messagebox.showinfo("Ok", "Sudoku not complete properly")
                    if event.key == pygame.K_SPACE:
                        if sudoku.solve(screen):
                            Tk().wm_withdraw()
                            messagebox.showinfo("Ok", "Sudoku solved")
                        else:
                            Tk().wm_withdraw()
                            messagebox.showinfo("Ok", "Sudoku not solvable")
                    if event.key == pygame.K_1:
                        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                            sudoku.add_possible_value(1, row, col)
                        else:
                            sudoku.set_value(1, row, col)
                    if event.key == pygame.K_2:
                        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                            sudoku.add_possible_value(2, row, col)
                        else:
                            sudoku.set_value(2, row, col)
                    if event.key == pygame.K_3:
                        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                            sudoku.add_possible_value(3, row, col)
                        else:
                            sudoku.set_value(3, row, col)
                    if event.key == pygame.K_4:
                        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                            sudoku.add_possible_value(4, row, col)
                        else:
                            sudoku.set_value(4, row, col)
                    if event.key == pygame.K_5:
                        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                            sudoku.add_possible_value(5, row, col)
                        else:
                            sudoku.set_value(5, row, col)
                    if event.key == pygame.K_6:
                        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                            sudoku.add_possible_value(6, row, col)
                        else:
                            sudoku.set_value(6, row, col)
                    if event.key == pygame.K_7:
                        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                            sudoku.add_possible_value(7, row, col)
                        else:
                            sudoku.set_value(7, row, col)
                    if event.key == pygame.K_8:
                        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                            sudoku.add_possible_value(8, row, col)
                        else:
                            sudoku.set_value(8, row, col)
                    if event.key == pygame.K_9:
                        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                            sudoku.add_possible_value(9, row, col)
                        else:
                            sudoku.set_value(9, row, col)

        if clicked:
            sudoku.mark_square(screen, row, col)

        # this method is necessary for anything to happen
        pygame.display.update()

def how_to_play():
    screen = pygame.display.set_mode((1200,800))
    running = True
    help = ["1. Standard sudoku rules apply",
            "2. Press any number to write is as answer",
            "3. Press backspace to delete answer",
            "4. Press any number with Shift to add candidate",
            "5. Press backspace with Shift to delete candidate",
            "6. Press delete to delete all answers and candidates"]
    while(running):
        screen.fill((255,255,255))
        font = pygame.font.SysFont("ComicSans", 50)
        counter = 0
        for str in help:
            todraw = font.render(str, 1, (0, 0, 0))
            screen.blit(todraw, (0, counter*75))
            counter = counter +1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.update()

if __name__ == '__main__':
    pygame.init()
    main()
