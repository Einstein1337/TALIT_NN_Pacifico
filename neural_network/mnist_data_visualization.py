import os
import sys
import numpy as np
import pygame
from pygame.constants import CONTROLLER_AXIS_INVALID

WIN_HEIGHT = 280
WIN_WIDTH = 280

FPS = 60
TIME_DELAY = int(1000/FPS)

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
BG_COLOR = WHITE

class Game:
    """
    Main GAME class
    """

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode(
            (WIN_WIDTH, WIN_HEIGHT)
        )  # create screen which will display everything
        self.win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption("Paint from wish")  # Game title
        self.game_play = False
        self.living_cells = []

    def play(self):
        # Update
        with open(os.path.join(sys.path[0], "data\mnist_test.csv"), 'r') as fts:
            input_list_mnist_test = fts.readlines()

        split_input_list = input_list_mnist_test[1].split(",")
        split_input_list = [float(i) for i in split_input_list]
        v_list = split_input_list[1:len(split_input_list)]
        
        self.screen.fill(BG_COLOR)  # draw empty screen
        color = 0
        for y in range(28):
            for x in range(28):
                pygame.draw.rect(self.screen, (v_list[color], v_list[color], v_list[color]),  (10*x, 10*y, 10, 10))
                color += 1
                pygame.time.delay(TIME_DELAY)
                pygame.display.flip()
                pygame.display.update()

        
        while True:
            for event in pygame.event.get():
                # Exit app if click quit button
                if event.type == pygame.QUIT:
                    run = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                self.exit()


        pygame.quit()


if __name__ == "__main__":
    Game().play()