import pygame
from pygame.locals import *
import random

from PyGoL import PyRule, PyGoLEngine

pygame.init()

speed = 10  # How many iterations per second
squares = 0  # Size of squares: 0 = 8X8, 1 = 16X16, 2 = 32X32, 3 = 64X64
map_size = 64  # The width and height

sq_8 = 8 * 2**squares
imgs = [f"res/alive_{sq_8}.png", f"res/dead_{sq_8}.png", sq_8]


# -----CONFIG-----

width = map_size*imgs[2]
height = map_size*imgs[2]
screen_size = width, height
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
alive = pygame.image.load(imgs[0]).convert()
dead = pygame.image.load(imgs[1]).convert()
done = False

Conway = PyRule([3],[2,3])
#Labyrinth = PyRule([3], [1, 2, 3, 4, 5])
Board = PyGoLEngine(map_size, map_size, Conway)

random.seed(5)

for y in range(map_size):
    for x in range(map_size):
        Board.set(x, y, random.randint(0, 1))


def pygame_draw_board(brd: PyGoLEngine):
    for _y in range(brd.getYMax()):
        for _x in range(brd.getXMax()):
            if brd.get(_x, _y):
                screen.blit(alive, (_x * imgs[2], _y * imgs[2]))
            else:
                screen.blit(dead, (_x * imgs[2], _y * imgs[2]))


def get_pygame_cell_list():
    lst = []
    for _x in range(map_size):
        tmp = []
        for _y in range(map_size):
            tmp.append((_x * imgs[2], _y * imgs[2]))
        lst.append(tmp)
    return lst


pygame_draw_board(Board)
tp = 0
run = False

while not done:
    milliseconds = clock.tick(60)
    seconds = milliseconds / 1000.0
    tp += milliseconds

    for event in pygame.event.get():
        if event.type == QUIT:
            done = True

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                run = not run

        if event.type == KEYUP:
            if event.key == K_q:
                run = False
                Board.run()
                pygame_draw_board(Board)

    pressed = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
    pos = pygame.mouse.get_pos()

    if pressed[K_r]:
        Board.reset()
        pygame_draw_board(Board)
    if pressed[K_a]:
        for y in range(map_size):
            for x in range(map_size):
                Board.set(x, y, random.randint(0, 1))
        pygame_draw_board(Board)

    # Run the board at a specific frequency
    if run and tp > 1000/speed:
        tp = 0
        Board.run()
        pygame_draw_board(Board)

    if mouse[0]:  # Makes cells alive
        rects = get_pygame_cell_list()
        for y in range(map_size):
            for x in range(map_size):
                if rects[x][y][0] <= pos[0] < rects[x][y][0]+imgs[2] and \
                                        rects[x][y][1] <= pos[1] < rects[x][y][1] + imgs[2]:
                    Board.set(x, y, True)
                    pygame_draw_board(Board)

    if mouse[2]:  # Kills cells
        rects = get_pygame_cell_list()
        for y in range(map_size):
            for x in range(map_size):
                if rects[x][y][0] <= pos[0] < rects[x][y][0] + imgs[2] and \
                                        rects[x][y][1] <= pos[1] < rects[x][y][1] + imgs[2]:
                    Board.set(x, y, False)
                    pygame_draw_board(Board)

    pygame.display.flip()

pygame.quit()
