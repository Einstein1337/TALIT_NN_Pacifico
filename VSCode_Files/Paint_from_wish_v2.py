import numpy as np
import pygame
import time
from pygame import draw
from pygame.constants import KEYDOWN, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION

## VARIABLES ##
line_width = 2
image_res = 128  # image is square
image_res_factor = 5
drawing_surface_size = image_res*image_res_factor  # square width = height
extra_space = 150
WIN_WIDTH = drawing_surface_size + extra_space + line_width + 2
WIN_HEIGHT = drawing_surface_size + 2

consol_height = WIN_HEIGHT/2.5
console_message_max_time = 5

convert_button_side_lenght = 55
convert_button_height = 20
convert_button_x = WIN_WIDTH - extra_space/2 - convert_button_side_lenght/2
convert_button_y = WIN_HEIGHT/2 - convert_button_height/2

pixel_size = image_res_factor
FPS = 1000
TIME_DELAY = int(1000/FPS)

text_size1 = 20
text_size2 = 15
# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
BG_COLOR = WHITE
## FUNCTIONS ##


def drawInterface(surface, f1, f2, cbp, consol_m):
    pygame.draw.line(
        surface, BLACK, (drawing_surface_size, 0), (drawing_surface_size, WIN_HEIGHT), line_width)

    if cbp:
        color = GRAY
    else:
        color = WHITE
    pygame.draw.rect(surface, color,  (
        convert_button_x, convert_button_y, convert_button_side_lenght, convert_button_height))
    pygame.draw.rect(surface, BLACK,  (
        convert_button_x, convert_button_y, convert_button_side_lenght, convert_button_height), line_width)
    img1 = f1.render('Convert', True, BLACK)
    img2 = f2.render('Clear Display: Backspace', True, BLACK)
    for k in range(len(consol_m)):
        msg = f2.render(consol_m[k].message, True, BLACK)
        surface.blit(msg, (WIN_WIDTH - extra_space +
                           1, WIN_HEIGHT - consol_height + k*text_size2))
    surface.blit(img1, (convert_button_x + 4, convert_button_y + 4))
    surface.blit(img2, (WIN_WIDTH - extra_space + 1, 5))


def drawFigure(surface, lc):
    for i in range(len(lc) - 1):
        if lc[i] != "Unterbruch" and lc[i + 1] != "Unterbruch":
            if len(lc[i]) > 1:
                pygame.draw.line(
                    surface, BLACK, lc[i], lc[i + 1], pixel_size)


def Convert(display, name, pos, size):
    image = pygame.Surface(size)  # Create image surface
    # Blit portion of the display to the image
    image.blit(display, (0, 0), (pos, size))
    pygame.image.save(image, name)  # Save the image to the disk


class ConsolMessage:
    def __init__(self, message, start_time):
        self.message = message
        self.st = start_time


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
        f = open('Image_int.txt', 'r')
        images = int(f.read())
        f.close()
        mouse_pressed = False
        convert_button_pressed = False
        font1 = pygame.font.SysFont('Arial.ttf', text_size1)
        font2 = pygame.font.SysFont('Arial.ttf', text_size2)
        consol_messages = []
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
                        if x >= convert_button_x and x <= convert_button_x + convert_button_side_lenght and y >= convert_button_y and y <= convert_button_y + convert_button_height:
                            convert_button_pressed = True
                            images += 1
                            f = open('Image_int.txt', 'w')
                            f.write(f"{images}")
                            f.close()
                            Convert(self.screen, f"Image_{images}.png",
                                    (0, 0), (drawing_surface_size, drawing_surface_size))
                            if len(consol_messages) >= consol_height/text_size2 - 1:
                                consol_messages = []
                            consol_messages.append(
                                ConsolMessage(f"Converted to Image_{images}.png", time.time()))

                if event.type == MOUSEBUTTONUP:
                    convert_button_pressed = False
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

            # updateConsol
            messages_in_overtime = 0
            time_now = time.time()
            for h in range(len(consol_messages)):
                if time_now - consol_messages[h].st >= console_message_max_time:
                    messages_in_overtime += 1

            for m in range(messages_in_overtime):
                del consol_messages[m]

            self.screen.fill(BG_COLOR)  # draw empty screen
            drawInterface(self.screen, font1, font2,
                          convert_button_pressed, consol_messages)
            drawFigure(self.screen, line_coordinates)
            # Update
            pygame.time.delay(TIME_DELAY)
            pygame.display.flip()
            pygame.display.update()
        pygame.quit()


if __name__ == "__main__":
    Game().play()
