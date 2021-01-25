import pygame
import random
from types import *

WIDTH = 600
HEIGHT = 600
FPS = 10

window = GAME_WINDOW(WIDTH, HEIGHT, FPS, "Snake")
field = FIELD(window, 30)
snake = SNAKE(field)
snake.create()

while window.running:
    def update():
        ctrl = False
        window.update()

        snake.move("MAIN")

        if pygame.key.get_pressed()[pygame.K_UP]:
            snake.move("UP")

        if pygame.key.get_pressed()[pygame.K_LEFT]:
            snake.move("LEFT")

        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            snake.move("RIGHT")

        if pygame.key.get_pressed()[pygame.K_DOWN]:
            snake.move("DOWN")

    def draw():
        for block in field.blocks:
            block.draw()

        pygame.display.flip()

    if snake.live:
        update()
        draw()
    else:
        print("YOU LOSE")
        window.running = False

window.stop()
