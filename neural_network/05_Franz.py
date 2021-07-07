import numpy as np
from numpy.core.fromnumeric import transpose
from numpy.core.numeric import outer
import os
import pygame
import time
from pygame import draw
from pygame.constants import KEYDOWN, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION

## VARIABLES ##
line_width = 2
image_res = 28  # image is square
image_res_factor = 10
drawing_surface_size = image_res*image_res_factor  # square width = height
extra_space = 150
WIN_WIDTH = drawing_surface_size + extra_space + line_width + 2
WIN_HEIGHT = drawing_surface_size + 2

space_between_buttons = 10
button_lenght = 55
button_height = 20
input_fiel_lenght = 100

consol_height = WIN_HEIGHT/2
console_message_max_time = 5

drawing_line_width = 3
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
def drawIntroducingScreen(surface, bl, font):
    img_list = [font.render('This is a handwriting recognition software. It can detect numbers', True, BLACK),
                font.render('written by hand between 0 and 9. But first of all, you need to', True, BLACK),
                font.render('create and train a neuronal network. For that you need to tell', True, BLACK),
                font.render('the programm the number of hidden layers and the number of neurons', True, BLACK),
                font.render('per hidden layer. You can also select a learning rate for your AI.', True, BLACK),
                font.render('The better numbers you choose the smarter your AI will be. Have fun', True, BLACK)]
    for img in range(len(img_list)):
        surface.blit(img_list[img], (WIN_WIDTH/10, WIN_HEIGHT/4+text_size2*img))

    for button in range(len(bl)):
        if bl[button].scene == 1:
            bl[button].drawButton(surface)

def drawHiddenLayerScreen(surface, bl, font):
    img_list = [font.render('Name:', True, BLACK),
                font.render('Learning rate:', True, BLACK),
                font.render('Hidden layers:', True, BLACK),]
    for img in range(len(img_list)):
        surface.blit(img_list[img], (WIN_WIDTH/10, WIN_HEIGHT/4+(button_height+space_between_buttons)*img + 4))

    for button in range(len(bl)):
        if bl[button].scene == 2:
            bl[button].drawButton(surface)


def drawNeuronScreen(surface):
    pass

# cbp = convert button pressed, cdbp = clear display button pressed
def drawDrawingScreen(surface, f, button_list, consol_m):
    pygame.draw.line(
        surface, BLACK, (drawing_surface_size, 0), (drawing_surface_size, WIN_HEIGHT), line_width)

    for btn in range(len(button_list)):
        button_list[btn].drawButton(surface)

    #text in consol
    for k in range(len(consol_m)):
        msg = f.render(consol_m[k].message, True, BLACK)
        surface.blit(msg, (WIN_WIDTH - extra_space +
                           5, WIN_HEIGHT - consol_height + k*text_size2))


def drawFigure(surface, lc):
    for i in range(len(lc) - 1):
        if lc[i] != "break" and lc[i + 1] != "break":
            if len(lc[i]) > 1:
                pygame.draw.line(
                    surface, BLACK, lc[i], lc[i + 1], drawing_line_width)

def saveBestWeightsLR(precision, network):
    with open('Best_weights_learning_rate_mnist.txt', 'r') as f:
        file_lines = f.readlines()
    highest_percentage = float(file_lines[0])
    if precision > highest_percentage:
        f = open('Best_weights_learning_rate_mnist.txt', 'w')
        f.write(f"{precision}\n")
        f.close()
        f = open('Best_weights_learning_rate_mnist.txt', 'a')
        f.write(f"{network.learning_rate}\n")
        f.write(f"{network.W}")


class Network:
    def __init__(self, neuron_list, learning_rate, name):
        self.name = name
        self.neuron_list = neuron_list
        self.input_neurons = neuron_list[0]
        self.output_neurons = neuron_list[-1]
        self.learning_rate = learning_rate
        self.hidden_layer_arrays = []
        self.W = []
        for layer in range(len(neuron_list)-1):
            self.W.append(np.random.uniform(-0.5, 0.5, (neuron_list[layer+1], neuron_list[layer])))
        
    def sigmoid(self, z):
        return 1/(1+np.exp(-z))


    def feedforward(self, input_array):
        next_hidden_layer_array = input_array
        self.hidden_layer_arrays.append(next_hidden_layer_array)
        for hidden_layer in range(len(self.neuron_list)-1):
            next_hidden_layer_array = self.sigmoid(np.dot(self.W[hidden_layer], next_hidden_layer_array))
            self.hidden_layer_arrays.append(next_hidden_layer_array)
        return next_hidden_layer_array  # last hidden layer array = output array
    
    def getTargetArray(self, index):
        target_array = np.zeros(self.output_neurons,)
        target_array[index] = 1
        return target_array

    def Cost(self, E_out):
        Cost = 0
        for e in range(len(E_out)):
            Cost += np.power(E_out[e], 2)
        return 0.5*Cost

    def train(self, input_list):
        for line in range(len(input_list)):
            if line%200 == 0:
                print(f"Training {self.name}: {int(line/len(input_list) * 100)}%", end="\r")
            split_input_list = input_list[line].split(",")
            split_input_list = [float(i) for i in split_input_list]
            target_index = int(split_input_list[0])
            target_array = self.getTargetArray(target_index)
            input_array = np.array(split_input_list[1:len(split_input_list)])/255

            output_array = self.feedforward(input_array)
            self.hidden_layer_arrays.reverse()
            self.W.reverse()
            E_out = target_array - output_array
            W_new = []
            E_hidden = E_out
            for weights in range(len(self.W)):
                W_updated = self.W[weights] + self.learning_rate*np.dot(np.reshape((E_hidden*self.hidden_layer_arrays[weights]*(1-self.hidden_layer_arrays[weights])), (-1, 1)), np.reshape(self.hidden_layer_arrays[weights+1], (-1, 1)).transpose())
                W_new.append(W_updated)
                E_hidden = np.dot(self.W[weights].transpose(), E_hidden)       
            
            W_new.reverse()
            self.W = W_new
            self.hidden_layer_arrays = []
        print(f"Training {self.name}: 100%")
        
    def test(self, input_list):
        right_answers = 0
        for line in range(len(input_list)):
            if line%100 == 0:
                print(f"Test {self.name}: {int(line/len(input_list) * 100)}%", end="\r")
            split_input_list = input_list[line].split(",")
            split_input_list = [float(i) for i in split_input_list]
            target = int(split_input_list[0])
            input_array = np.array(split_input_list[1:len(split_input_list)])/255

            # get index of highest value in output list
            output_list = self.feedforward(input_array).tolist()
            highest_value = max(output_list)
            highest_value_index = output_list.index(highest_value)
            if highest_value_index == target:
                right_answers += 1

        print(f"Test {self.name}: 100%")
        return right_answers/len(input_list)*100

class ConsolMessage:
    def __init__(self, message, start_time):
        self.message = message
        self.st = start_time

class Button:
    def __init__(self, x, y, lenght, height, font, name, name_x, name_y, scene, active, type):
        self.x = x
        self.y = y
        self.len = lenght
        self.h = height
        self.name = name
        self.img = font.render(name, True, BLACK)
        self.pressed = False
        self.name_x = self.x + name_x
        self.name_y = self.y + name_y
        self.pressed = False
        self.scene = scene
        self.active = active
        self.type = type

        if name == 'Detect':
            self.message = "Detected"
        elif name == 'Clear':
            self.message = "Screen cleared"
        else: 
            self.message = ""

    def drawButton(self, surface):
        if self.pressed == True or self.active == False:
            color = GRAY
        else:
            color = WHITE
        pygame.draw.rect(surface, color,  (self.x, self.y, self.len, self.h))
        pygame.draw.rect(surface, BLACK,  (self.x, self.y, self.len, self.h), line_width)

        surface.blit(self.img, (self.name_x, self.name_y))
    
    def Pressed(self):
        (mx, my) = pygame.mouse.get_pos()
        if mx >= self.x and mx <= self.x+self.len and my >= self.y and my <= self.y+self.h:
            self.pressed = True
            return True
        return False


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
        #Scenes
        introducing_scene = True
        select_hidden_layers_scene = False
        select_neurons_per_hidden_layer_scene = False
        drawing_scene = False

        line_coordinates = []
        mouse_pressed = False
        detect_button_pressed = False
        clear_display_button_pressed = False
        font1 = pygame.font.SysFont('Arial.ttf', text_size1)
        font2 = pygame.font.SysFont('Arial.ttf', text_size2)
        consol_messages = []

        inputs_scene_2 = 0
        active_input_fiel = ""
        button_list = [Button(WIN_WIDTH - extra_space/2 - button_lenght/2, 20, button_lenght, button_height, font1, 'Detect', 7, 4, 4, True, "button"),
                      Button(WIN_WIDTH - extra_space/2 - button_lenght/2, 40+space_between_buttons, button_lenght, button_height, font1, 'Clear', 11, 4, 4, True, "button"),
                      Button(WIN_WIDTH/2 - button_lenght/2, WIN_HEIGHT - WIN_HEIGHT/3, button_lenght, button_height, font1, 'OK', 17, 4, 1, True, "button"),
                      Button(WIN_WIDTH/2 - input_fiel_lenght/2, WIN_HEIGHT/4, input_fiel_lenght, button_height, font1, '', 5, 4, 2, True, "input_str"),
                      Button(WIN_WIDTH/2 - input_fiel_lenght/2, WIN_HEIGHT/4 + 30, input_fiel_lenght, button_height, font1, '', 5, 4, 2, True, "input_float"),
                      Button(WIN_WIDTH/2 - input_fiel_lenght/2, WIN_HEIGHT/4 + 60, input_fiel_lenght, button_height, font1, '', 5, 4, 2, True, "input_float"),
                      Button(WIN_WIDTH/2 - button_lenght/2, WIN_HEIGHT/4 + 100, button_lenght, button_height, font1, 'OK', 17, 4, 2, False, "button")]
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
                        
                        for button in range(len(button_list)): 
                            if button_list[button].Pressed():
                                if button_list[button].name == 'Detect':
                                    pass
                                elif button_list[button].name == 'Clear':
                                    line_coordinates = []
                                elif button_list[button].name == 'OK':
                                    if button_list[button].scene == 1:
                                        introducing_scene = False
                                        select_hidden_layers_scene = True
                                    elif button_list[button].scene == 2:
                                        if button_list[button].active:
                                            select_hidden_layers_scene = False
                                            select_neurons_per_hidden_layer_scene = True

                                else:
                                    active_input_fiel = button_list[button]
                                if button_list[button].message != "":
                                    if len(consol_messages) >= consol_height/text_size2 - 1:
                                        consol_messages = []
                                    consol_messages.append(ConsolMessage(f"{button_list[button].message}", time.time()))

                if event.type == MOUSEBUTTONUP:
                    for b in range(len(button_list)):
                        button_list[b].pressed = False
                    mouse_pressed = False
                    if len(line_coordinates) > 0:
                        line_coordinates.append("break")

                    
                if event.type == KEYDOWN:

                    if event.key == pygame.K_BACKSPACE:
                        active_input_fiel.name = active_input_fiel.name[:-1]
                    elif len(active_input_fiel.name) <= 11:
                        if active_input_fiel.type == "input_float":
                            if event.key == pygame.K_0 or event.key == pygame.K_1 or event.key == pygame.K_2 or event.key == pygame.K_3 or event.key == pygame.K_4 or event.key == pygame.K_5 or event.key == pygame.K_6 or event.key == pygame.K_7 or event.key == pygame.K_8 or event.key == pygame.K_9 or event.key == pygame.K_PERIOD: 
                                active_input_fiel.name += event.unicode
                        else:
                            active_input_fiel.name += event.unicode
                    active_input_fiel.img = font1.render(active_input_fiel.name, True, BLACK)

                #update buttons
                for field in range(len(button_list)):
                    if button_list[field].scene == 2:
                        if button_list[field].name != '':
                            inputs_scene_2 += 1
                        if inputs_scene_2 > 3:
                            button_list[field].active = True
                        else:
                            if button_list[field].name == 'OK':
                                button_list[field].active = False
                inputs_scene_2 = 0
                
                        
                if drawing_scene:
                    if event.type == MOUSEMOTION:
                        if mouse_pressed:
                            (x, y) = pygame.mouse.get_pos()
                            if x < WIN_WIDTH - extra_space - drawing_line_width/2 and x > 0 and y > 0 and y < WIN_HEIGHT:
                                line_coordinates.append((x, y))
                            else:
                                line_coordinates.append("break")

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                self.exit()

            if drawing_scene:
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
            
            if introducing_scene:
                drawIntroducingScreen(self.screen, button_list, font2)

            elif select_hidden_layers_scene:
                drawHiddenLayerScreen(self.screen, button_list, font2)

            elif select_neurons_per_hidden_layer_scene:
                drawNeuronScreen(self.screen)

            elif drawing_scene:
                drawDrawingScreen(self.screen, font2,
                            button_list, consol_messages)
                drawFigure(self.screen, line_coordinates)

            

            # Update
            pygame.time.delay(TIME_DELAY)
            pygame.display.flip()
            pygame.display.update()
        pygame.quit()

mnist_network = Network([784, 50, 50, 10], 0.02, "MNIST network")

# get inputs and target from csv file
with open('data\mnist_train.csv', 'r') as ftr:
    input_list_mnist_train = ftr.readlines()

with open('data\mnist_test.csv', 'r') as fts:
    input_list_mnist_test = fts.readlines()

if __name__ == "__main__":
    Game().play()
