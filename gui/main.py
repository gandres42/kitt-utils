import sys
import pygame
from networktables import NetworkTables

NetworkTables.initialize(server='100.71.254.107')
nt = NetworkTables.getTable("localization")

from pygame.locals import (
    KEYDOWN,
    K_q
)

BLOCK_SIZE = 8

GRID_M_WIDTH = 4
GRID_M_HEIGHT = 3

BLOCKS_PER_METER = 50
GRID_WIDTH = (GRID_M_WIDTH * BLOCKS_PER_METER) + 1
GRID_HEIGHT = (GRID_M_HEIGHT * BLOCKS_PER_METER) + 1



BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
DARK_GREEN = (0, 125, 0)
WHITE = (255, 255, 255)
GREY = (90, 90, 90)

screen = pygame.display.set_mode([GRID_WIDTH * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE])
pygame.display.set_caption('KITT Monitor')

pygame.init()
clock = pygame.time.Clock()

def draw_pixel(x, y, color):
    rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
    pygame.draw.rect(screen, color, rect)

def draw_grid():
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if x % BLOCKS_PER_METER == 0 or y % BLOCKS_PER_METER == 0:
                draw_pixel(x, y, GREY)

def main():
    global sd
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_q:
                    pygame.quit()
                    sys.exit(0)
        screen.fill(BLACK)
        draw_grid()
        draw_pixel(nt.getNumber('x', -1), nt.getNumber('y', -1), RED)
        pygame.display.update()

main()