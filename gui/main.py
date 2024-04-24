import sys
import pygame
from networktables import NetworkTables
import os
import time

NetworkTables.initialize(server='192.168.1.109')
nt = NetworkTables.getTable("localization")

from pygame.locals import (
    KEYDOWN,
    K_q
)

BLOCK_SIZE = 5

GRID_M_WIDTH = 3
GRID_M_HEIGHT = 3

GRID_Y_OFFSET = 0.08
# GRID_Y_OFFSET = 0
GRID_MEASURE = .61

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

def draw_fuse(x, y):
    draw_pixel(x * BLOCKS_PER_METER, y * BLOCKS_PER_METER, GREEN)

def draw_dwm(x, y):
    draw_pixel(x * BLOCKS_PER_METER, y * BLOCKS_PER_METER, RED)

def draw_vive(x, y):
    draw_pixel(x * BLOCKS_PER_METER, y * BLOCKS_PER_METER, BLUE)

def draw_grid():
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if x % int(BLOCKS_PER_METER * GRID_MEASURE) == 0 or (y - int(BLOCKS_PER_METER * GRID_Y_OFFSET)) % int(BLOCKS_PER_METER * GRID_MEASURE) == 0:
                draw_pixel(x, y, GREY)

def main():
    running = True

    vive = []
    dwm = []
    fuse = []
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_q:
                    pygame.quit()
                    print('\nvive')
                    print(vive)
                    print('\nfuse')
                    print(fuse)
                    print('\ndwm')
                    print(dwm)
                    sys.exit(0)
        draw_grid()
        draw_fuse(nt.getNumber('fuse_x', -1000) + 3.8, (-1 * nt.getNumber('fuse_y', -1000)) + .8)
        draw_dwm(nt.getNumber('dwm_x', -1000) + 3.8, (-1 * nt.getNumber('dwm_y', -1000)) + .8)
        draw_vive(nt.getNumber('vive_x', -1000) + 3.8, (-1 * nt.getNumber('vive_y', -1000)) + .8)

        fuse.append((nt.getNumber('fuse_x', -1000) + 3.8, (-1 * nt.getNumber('fuse_y', -1000)) + .8))
        dwm.append((nt.getNumber('dwm_x', -1000) + 3.8, (-1 * nt.getNumber('dwm_y', -1000)) + .8))
        vive.append((nt.getNumber('vive_x', -1000) + 3.8, (-1 * nt.getNumber('vive_y', -1000)) + .8))
        pygame.display.update()

main()