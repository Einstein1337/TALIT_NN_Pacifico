import numpy as np
import pygame
from pygame.constants import KEYDOWN, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION

## VARIABLES ##
line_width = 2
image_res = 128  # image is square
image_res_factor = 5
drawing_surface_size = image_res*image_res_factor  # square width = height
extra_space = 150
WIN_WIDTH = drawing_surface_size + extra_space + line_width
WIN_HEIGHT = drawing_surface_size

convert_button_side_lenght = 70
convert_button_height = 50
convert_button_x = WIN_WIDTH - extra_space/2 - convert_button_side_lenght/2
convert_button_y = WIN_HEIGHT/2 - convert_button_height/2

pixel_size = image_res_factor
FPS = 1000
TIME_DELAY = int(1000/FPS)

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
BG_COLOR = WHITE
## FUNCTIONS ##


def drawInterface(surface):
    pygame.draw.line(
        surface, BLACK, (drawing_surface_size, 0), (drawing_surface_size, WIN_HEIGHT), line_width)
    pygame.draw.rect(surface, BLACK,  (
        convert_button_x, convert_button_y, convert_button_side_lenght, convert_button_height), line_width)


def displayMatrix(surface, matrix):
    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            if matrix[y][x] == 0:
                color = WHITE
            else:
                color = BLACK
            pygame.draw.rect(surface, color,  (
                x*pixel_size, y*pixel_size, pixel_size, pixel_size))


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
        matrix = []
        draw = False
        erase = False
        for row in range(image_res):
            matrix.append([])
            for column in range(image_res):
                matrix[row].append(0)
        mouse_pressed = False
        while True:
            # key events
            for event in pygame.event.get():
                # Exit app if click quit button
                if event.type == pygame.QUIT:
                    run = False

                if event.type == MOUSEBUTTONDOWN:
                    mouse_pressed = True
                    if event.button == 1:  # Leftclick
                        (x, y) = pygame.mouse.get_pos()
                        if x < WIN_WIDTH - extra_space:
                            if matrix[int(y/pixel_size)][int(x/pixel_size)] == 0:
                                draw = True
                                matrix[int((y/pixel_size))
                                       ][int(x/pixel_size)] = 1
                            else:
                                erase = True
                                matrix[int((y/pixel_size))
                                       ][int(x/pixel_size)] = 0

                if event.type == MOUSEBUTTONUP:
                    mouse_pressed = False
                    draw = False
                    erase = False

                if event.type == MOUSEMOTION:
                    if mouse_pressed:
                        (x, y) = pygame.mouse.get_pos()
                        if x < WIN_WIDTH - extra_space:
                            if draw:
                                if matrix[int(y/pixel_size)][int(x/pixel_size)] == 0:
                                    matrix[int(y/pixel_size)
                                           ][int(x/pixel_size)] = 1
                            if erase:
                                if matrix[int(y/pixel_size)][int(x/pixel_size)] == 1:
                                    matrix[int(y/pixel_size)
                                           ][int(x/pixel_size)] = 0

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                self.exit()

            if keys[pygame.K_BACKSPACE] or keys[pygame.K_DELETE]:
                matrix = []
                for i in range(image_res):
                    matrix.append([])
                    for j in range(image_res):
                        matrix[i].append(0)

            self.screen.fill(BG_COLOR)  # draw empty screen
            drawInterface(self.screen)
            displayMatrix(self.screen, matrix)
            # Update
            pygame.time.delay(TIME_DELAY)
            pygame.display.flip()
            pygame.display.update()
        pygame.quit()


if __name__ == "__main__":
    Game().play()
