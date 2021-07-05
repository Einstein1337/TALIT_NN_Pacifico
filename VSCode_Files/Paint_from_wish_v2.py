import numpy as np
import pygame
from pygame.constants import KEYDOWN, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION

## VARIABLES ##
line_width = 2
image_res = 128  # image is square
image_res_factor = 5
drawing_surface_size = image_res*image_res_factor  # square width = height
extra_space = 150
WIN_WIDTH = drawing_surface_size + extra_space + line_width + 2
WIN_HEIGHT = drawing_surface_size + 2

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


def drawFigure(surface, lc):
    for i in range(len(lc) - 1):
        if lc[i] != "Unterbruch" and lc[i + 1] != "Unterbruch":
            if len(lc[i]) > 1:
                pygame.draw.line(
                    surface, BLACK, lc[i], lc[i + 1], pixel_size)


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
        line_coordinates = []
        draw = False
        erase = False
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
                            line_coordinates.append((x, y))

                if event.type == MOUSEBUTTONUP:
                    mouse_pressed = False
                    line_coordinates.append("Unterbruch")

                if event.type == MOUSEMOTION:
                    if mouse_pressed:
                        (x, y) = pygame.mouse.get_pos()
                        if x < WIN_WIDTH - extra_space - pixel_size/2 and x > 0 and y > 0 and y < WIN_HEIGHT:
                            line_coordinates.append((x, y))
                        else:
                            line_coordinates.append("Unterbruch")

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                self.exit()

            if keys[pygame.K_BACKSPACE] or keys[pygame.K_DELETE]:
                line_coordinates = []

            self.screen.fill(BG_COLOR)  # draw empty screen
            drawInterface(self.screen)
            drawFigure(self.screen, line_coordinates)
            # Update
            pygame.time.delay(TIME_DELAY)
            pygame.display.flip()
            pygame.display.update()
        pygame.quit()


if __name__ == "__main__":
    Game().play()
