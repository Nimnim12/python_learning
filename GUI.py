import pygame
import sudoku_solver


class Board:
    BACKGROUND_COLOR = (250, 250, 250)

    def create_window(self,width,height):
        # Create first window
        screen = pygame.display.set_mode((width,height))
        pygame.display.set_caption("Sudoku")
        return screen

    def draw_lines(self,screen):
        width,height = pygame.display.get_surface().get_size()
        # draw vertical lines
        for i in range (1,9):
            pygame.draw.line(screen, (100, 100, 100), (i * (width // 9), 0), (i * (width // 9), height), 3)
        # draw horizontal lines
        for i in range (1,9):
            pygame.draw.line(screen, (100, 100, 100), (0, i*(height//9)), (width, i*(height//9)), 3)

        # draw bold lines
        for i in range (1,9):
            if i%3 == 0:
                pygame.draw.line(screen, (0, 0, 0), (i * (width // 9), 0), (i * (width // 9), height), 5)

        for i in range (1,9):
            if i%3 == 0:
                pygame.draw.line(screen, (0, 0, 0), (0, i*(height//9)), (width, i*(height//9)), 5)

    def draw_number(self,screen,row,col,value):
        width, height = pygame.display.get_surface().get_size()
        font = pygame.font.SysFont("ComicSans",150)
        number = font.render(str(value),1,(0,0,0))
        screen.blit(number,((col*(width//9))+(width//40),(row*(height//9))+(height//180)))

    def draw_board(self,screen,board):
        for i in range(9):
            for j in range(9):
                if(board[i][j] != 0):
                    self.draw_number(screen,i,j,board[i][j])

    def remove_number(self,screen,row,col):
        width, height = pygame.display.get_surface().get_size()
        pygame.draw.rect(screen,self.BACKGROUND_COLOR,((col * (width // 9))+10,(row * (height // 9))+10,(width//9)-20,(height//9)-20))


    def solve(self,screen,board):
        if(sudoku_solver.find_zero(board) == None): return
        row,col = sudoku_solver.find_zero(board)
        possible_answers = sudoku_solver.find_values(board,row,col)
        for i in possible_answers:
            board[row][col] = i
            self.draw_number(screen,row,col,i)
            pygame.display.update()
            self.solve(screen,board)
            if (sudoku_solver.find_zero(board) == None): return
            else :
                self.remove_number(screen,row,col)
                pygame.display.update()
        self.remove_number(screen, row, col)
        board[row][col] = 0
        pygame.display.update()


def main():
    sudoku = Board()
    screen = sudoku.create_window(1200,900)
    running = True
    board = sudoku_solver.example_board
    # Game Loop
    while(running):
        # Background options
        screen.fill(sudoku.BACKGROUND_COLOR)
        sudoku.draw_lines(screen)
        sudoku.draw_board(screen,board)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
            if event.type == pygame.MOUSEBUTTONDOWN:
                sudoku.solve(screen,board)
            #if event.type == pygame.KEYDOWN:
               # if event.key == pygame.K_r:

        # this method is necessary for anything to happen
        pygame.display.update()

if __name__ == '__main__':
    pygame.init()
    main()