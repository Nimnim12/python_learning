import pygame
from sudoku_solver import example_board

def create_window(width,height):
    # Create first window
    screen = pygame.display.set_mode((width,height))
    pygame.display.set_caption("Sudoku")
    return screen

def draw_lines(screen):
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

def draw_number(screen,row,col,value):
    width, height = pygame.display.get_surface().get_size()
    font = pygame.font.SysFont("ComicSans",150,True)
    number = font.render(str(value),1,(0,0,0))
    screen.blit(number,((col*(width//9))+(width//40),(row*(height//9))+(height//180)))

def draw_board(screen,board):
    for i in range(9):
        for j in range(9):
            if(board[i][j] != 0):
                draw_number(screen,i,j,board[i][j])


def main():
    screen = create_window(1200,900)
    running = True
    # Game Loop
    while(running):
        # Background options
        screen.fill((250,250,250))
        draw_lines(screen)
        draw_board(screen,example_board)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
        # this method is necessary for anything to happen
        pygame.display.update()

if __name__ == '__main__':
    pygame.init()
    main()