import sys
import pygame
from networktables import NetworkTables
import os
import time
import math

NetworkTables.initialize(server='192.168.1.109')
nt = NetworkTables.getTable("localization")

from pygame.locals import (
    KEYDOWN,
    K_q
)

BLOCK_SIZE = 5

GRID_M_WIDTH = 5
GRID_M_HEIGHT = 3

GRID_Y_OFFSET = 0
GRID_MEASURE = 1

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

def draw_path(x, y):
    draw_pixel(x, y, GREEN)

def draw_pos(x, y):
    draw_pixel(x, y, RED)

def draw_carrot(x, y):
    draw_pixel(x, y, BLUE)

def draw_grid():
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if x % int(BLOCKS_PER_METER * GRID_MEASURE) == 0 or (y - int(BLOCKS_PER_METER * GRID_Y_OFFSET)) % int(BLOCKS_PER_METER * GRID_MEASURE) == 0:
                draw_pixel(x, y, GREY)

def motor_velocities(theta, magnitude):
    joy_x = math.sin(theta) * magnitude
    joy_y = math.cos(theta) * magnitude
    if abs(joy_x) > abs(joy_y):
        max_r = abs(magnitude / joy_x)
    else:
        max_r = abs(magnitude / joy_y)

    # this is the actual throttle  
    magnitude = magnitude / max_r
    turn_damping = 3.0 # for example
    right = (math.sin(theta) + math.cos(theta) / turn_damping)
    left = (math.sin(theta) - math.cos(theta) / turn_damping)
    
    print(tuple([left, right]))
    

def main():
    running = True

    path = [(i, int(math.sin(i*.05) * 50) + 75) for i in range(0, GRID_WIDTH)]
    i = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_q:
                    pygame.quit()
                    sys.exit(0)
        draw_grid()
        for point in path:
            draw_path(point[0], point[1])

        draw_pos(path[i][0], path[i][1])
        
        # todo: find first element from end of path within carrot distance
        p1 = (path[i][0], path[i][1])
        dst = None
        p2 = None
        # j = i + min(len(path) - i - 1, 5)
        for j in reversed(range(len(path))):
            p2 = (path[j][0], path[j][1])
            dst = math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
            if dst <= 20:
                break
        draw_carrot(p2[0], p2[1])
        try:
            theta = abs(math.degrees(math.atan((p1[1] - p2[1])/(p2[0] - p1[0]))))
        except ZeroDivisionError:
            theta = 0

        if p2[0] > p1[0] and p2[1] > p1[1]:
            theta = 90 + theta
        if p2[0] > p1[0] and p2[1] < p1[1]:
            theta = 90 - theta
        if p2[0] < p1[0] and p2[1] > p1[1]:
            theta = -90 + theta
        if p2[0] < p1[0] and p2[1] < p1[1]:
            theta = -90 - theta
        
        motor_velocities(math.radians(theta), dst)
        

        i = i + 1
        if i >= GRID_WIDTH:
            i = 0
        pygame.display.update()
        time.sleep(.05)

main()