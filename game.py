#!/usr/bin/env python3
import sys
from window import create_window
from curses import KEY_UP, KEY_DOWN, KEY_RIGHT, KEY_LEFT
from collections import deque, namedtuple
from time import sleep
from random import randint

Tile = namedtuple("Tile", "y x chr")
snake = deque([Tile(8,15, "→")], maxlen=1)
start_key = KEY_RIGHT

HEIGHT, WIDTH = 6*3,10*3
FPS = 5
"""
    This is the "map"
"""
def create_grid(width, height):
    return [["░" for x in range(width-1)] for y in range(height-1)]

"""
    create food on a random segment in level
    it can't be placed on a segment, where the snake is
"""
def create_food(grid, snake):
    while True:
        x, y = randint(0, len(grid[0])-1), randint(0, len(grid)-1)
        for segment in snake:
            sy, sx, _ = segment
            if (x, y) == (sx, sy):
                break
        else:
            return Tile(y, x, "+")

"""
    Check if there is a collision on this segment
"""
def collision(a, b):
    return a[:2] == b[:2]


"""
    draw the grid, including background, snake and food
"""
def render(screen, grid):
    for y, row in enumerate(grid):
       for x, chr in enumerate(row):
               screen.addch(y,x,chr)

"""
    handle key events,
    check for collision on key event,
    move the snake
"""
def movement(key, snake, food, grid, old_key):
    head, *tail = snake
    y,x,chr = head
    if key == KEY_UP:
        y -= 1
        chr = "↑"
        if y < 0:
            y = len(grid) - 1

    if key == KEY_DOWN:
        y+= 1
        chr = "↓"
        if y > len(grid) - 1:
            y = 0

    if key == KEY_LEFT :
        x -= 1
        chr = "←"
        if x < 0:
            x = len(grid[0]) - 1

    if key == KEY_RIGHT:
        x += 1
        chr = "→"
        if x > len(grid[0]) -1:
            x = 0

    # only append when user presses any button
    _head = Tile(y,x,chr)
    if _head != head:
        for segment in tail:
            if collision(_head, segment):
                return None, food
        if collision(head, food):
            snake = deque(snake, maxlen=snake.maxlen+1)
            food = None

        snake.appendleft(Tile(y,x,chr))

    return snake, food


"""
    main function which has a while/True, here some events happen:
    - draw the level_grid
    - Check if User want's to exit by ESC
    - move snake, draw create_food
    - check if game is over
    - calculate speed of snake depending on its length
"""
with create_window(WIDTH, HEIGHT) as screen:
    old_key = start_key
    food = None
    while True:
        level_grid = create_grid(WIDTH, HEIGHT)
        key = screen.getch()

        # No key was pressed yet
        if key == -1:
            key = old_key

        # stop game on ESC-Button
        if key == 27:
            break

        if food is None:
            food = create_food(level_grid, snake)

        level_grid[food.y][food.x] = food.chr

        snake, food = movement(key, snake, food, level_grid, old_key)

        # snake bites itself
        if snake is None:
            break

        for segment in snake:
            level_grid[segment.y][segment.x] = segment.chr

        render(screen, level_grid)
        old_key = key

        # wait some time for the next loop iteration
        sleep(max(1 / (FPS + len(snake)), 1/30))
