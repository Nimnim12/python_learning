import pygame
from sudoku_solver import example_board
class Cell:
    def __init__(self,value):
        self.value = value
        self.potential_values =[]
        self.selected = False
        self.set=False
        if(value != 0):
            self.set = True


class Board:
    def __init__(self,board):
        self.cells = [[Cell(board[row][col]) for row in range(9)] for col in range(9)]

class Gui:
    BACKGROUND_COLOR = (250, 250, 250)
    LINE_COLOR = (100,100,100)
    BOLD_LINE_COLOR = (0,0,0)
    MARKED_COLOR = (255,0,0)
    POTENTIAL_VALUE_COLOR = (50,50,50)

    def __init__(self,board):
        self.board = board

    def create_window(self,width,height):
        # Create first window
        screen = pygame.display.set_mode((width,height))
        pygame.display.set_caption("Sudoku")
        return screen

    def mark_square(self,screen,row,col):
        width, height = pygame.display.get_surface().get_size()
        pygame.draw.line(screen,self.MARKED_COLOR,(col*(width//9),row*(height//9)),(col*(width//9),(row*(height//9))+(height//9)),5)
        pygame.draw.line(screen,self.MARKED_COLOR,((col*(width//9))+(width//9),row*(height//9)),((col*(width//9))+(width//9),(row*(height//9))+(height//9)),5)
        pygame.draw.line(screen,self.MARKED_COLOR,(col*(width//9),row*(height//9)),((col*(width//9))+(width//9),row*(height//9)),5)
        pygame.draw.line(screen,self.MARKED_COLOR,(col*(width//9),(row*(height//9))+(height//9)),((col*(width//9))+(width//9),(row*(height//9))+(height//9)),5)
    def draw_lines(self,screen):
        width,height = pygame.display.get_surface().get_size()
        # draw vertical lines
        for i in range (1,9):
            pygame.draw.line(screen, self.LINE_COLOR , (i * (width // 9), 0), (i * (width // 9), height), 3)
        # draw horizontal lines
        for i in range (1,9):
            pygame.draw.line(screen, self.LINE_COLOR, (0, i*(height//9)), (width, i*(height//9)), 3)

        # draw bold lines
        for i in range (1,9):
            if i%3 == 0:
                pygame.draw.line(screen, self.BOLD_LINE_COLOR, (i * (width // 9), 0), (i * (width // 9), height), 5)

        for i in range (1,9):
            if i%3 == 0:
                pygame.draw.line(screen, self.BOLD_LINE_COLOR, (0, i*(height//9)), (width, i*(height//9)), 5)

    def draw_number(self,screen,row,col):
        width, height = pygame.display.get_surface().get_size()
        font = pygame.font.SysFont("ComicSans",150)
        number = font.render(str(self.board.cells[row][col].value),1,(0,0,0))
        screen.blit(number,((col*(width//9))+(width//40),(row*(height//9))+(height//180)))

    def draw_potential_numbers(self,screen,row,col):
        width, height = pygame.display.get_surface().get_size()
        font = pygame.font.SysFont("ComicSans", 30)
        values = self.board.cells[row][col].potential_values
        strnumbers = [str(integer) for integer in values]
        toprint = " ".join(strnumbers)
        number = font.render(toprint, 1, self.POTENTIAL_VALUE_COLOR)
        screen.blit(number, ((col * (width // 9)+(width//100)), (row * (height // 9))+(height//180)))

    def draw_board(self,screen):
        for i in range(9):
            for j in range(9):
                if(self.board.cells[i][j].set == False):
                    self.draw_potential_numbers(screen,i,j)
                if(self.board.cells[i][j].value != 0):
                    self.draw_number(screen,i,j)

    def remove_number(self,screen,row,col):
        width, height = pygame.display.get_surface().get_size()
        pygame.draw.rect(screen,self.BACKGROUND_COLOR,((col * (width // 9))+10,(row * (height // 9))+10,(width//9)-20,(height//9)-20))

    def clicked(self,pos):
        width, height = pygame.display.get_surface().get_size()
        if(pos[0]<width and pos[1]<height):
            col = pos[0] / (width // 9)
            row = pos[1] / (height // 9)
            self.board.cells[int(row)][int(col)].selected = True
            return (int(row),int(col))
        else:
            return None

    def set_value(self,value,row,col):
        self.board.cells[row][col].value =value
        self.board.cells[row][col].set = True

    def add_possible_value(self,value,row,col):
        if(len(self.board.cells[row][col].potential_values)<4):
            self.board.cells[row][col].potential_values.append(value)

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

    def solve(self,screen):
        if(self.find_zero() == None): return
        row,col = self.find_zero()
        possible_answers = self.find_values(row,col)
        for i in possible_answers:
            self.board.cells[row][col].value = i
            self.draw_number(screen,row,col)
            pygame.display.update()
            self.solve(screen)
            if (self.find_zero() == None): return
            else :
                self.remove_number(screen,row,col)
                pygame.display.update()
        self.remove_number(screen, row, col)
        self.board.cells[row][col].value = 0
        pygame.display.update()


def main():
    board = Board(example_board)
    sudoku = Gui(board)
    screen = sudoku.create_window(1200,900)
    running = True
    clicked = False
    # Game Loop
    while(running):
        # Background options
        screen.fill(sudoku.BACKGROUND_COLOR)
        sudoku.draw_lines(screen)
        sudoku.draw_board(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row,col = sudoku.clicked(pos)
                clicked = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    sudoku.solve(screen)
                if event.key == pygame.K_1:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        sudoku.add_possible_value("1",row,col)
                    else:
                        sudoku.set_value("1",row,col)
                if event.key == pygame.K_2:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        sudoku.add_possible_value("2", row, col)
                    else:
                        sudoku.set_value("2", row, col)
                if event.key == pygame.K_3:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        sudoku.add_possible_value("3", row, col)
                    else:
                        sudoku.set_value("3", row, col)
                if event.key == pygame.K_4:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        sudoku.add_possible_value("4", row, col)
                    else:
                        sudoku.set_value("4", row, col)
                if event.key == pygame.K_5:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        sudoku.add_possible_value("5", row, col)
                    else:
                        sudoku.set_value("5", row, col)
                if event.key == pygame.K_6:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        sudoku.add_possible_value("6", row, col)
                    else:
                        sudoku.set_value("6", row, col)
                if event.key == pygame.K_7:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        sudoku.add_possible_value("7", row, col)
                    else:
                        sudoku.set_value("7", row, col)
                if event.key == pygame.K_8:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        sudoku.add_possible_value("8", row, col)
                    else:
                        sudoku.set_value("8", row, col)
                if event.key == pygame.K_9:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        sudoku.add_possible_value("9", row, col)
                    else:
                        sudoku.set_value("9", row, col)

        if clicked:
            sudoku.mark_square(screen, row, col)

        # this method is necessary for anything to happen
        pygame.display.update()

if __name__ == '__main__':
    pygame.init()
    main()