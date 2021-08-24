from sys import float_repr_style
import sys
import numpy as np
from numpy.core.fromnumeric import transpose
from numpy.core.function_base import add_newdoc
from numpy.core.numeric import outer
import os
from numpy.lib.function_base import delete
from numpy.lib.type_check import imag
import pygame
import time
from pygame import Surface, draw
from pygame import surface
from pygame import font
from pygame.constants import KEYDOWN, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION
import ast

## VARIABLES ##
line_width = 2
image_res = 28  # image is square
image_res_factor = 20
drawing_surface_size = image_res*image_res_factor  # square width = height
extra_space = 15 * image_res_factor
WIN_WIDTH = drawing_surface_size + extra_space + line_width 
WIN_HEIGHT = drawing_surface_size 

space_between_buttons = WIN_HEIGHT/28
button_lenght = WIN_WIDTH/7.8545
button_height = WIN_HEIGHT/14
input_fiel_lenght = WIN_WIDTH/4.32
button_space_and_height = space_between_buttons + button_height

consol_height = WIN_HEIGHT/2
console_message_max_time = 5
drawing_line_width = int(image_res_factor*2.25)
FPS = 60
TIME_DELAY = int(1000/FPS)


text_size1 = int(WIN_HEIGHT/14)
text_size2 = int(WIN_HEIGHT/18.666666)

loading_bar_max_len = WIN_WIDTH/2
loading_bar_h = WIN_HEIGHT/10
loading_bar_x = WIN_WIDTH/4
loading_bar_y = WIN_HEIGHT/2 - loading_bar_h/2

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
BG_COLOR = WHITE

## FUNCTIONS ##
def drawIntroducingScene(surface, bl, font):
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

def drawHiddenLayerScene(surface, bl, font):
    img_list = [font.render('Name:', True, BLACK),
                font.render('Learning rate:', True, BLACK),
                font.render('Hidden layers (max. 5):', True, BLACK),]
    for img in range(len(img_list)):
        surface.blit(img_list[img], (WIN_WIDTH/10, WIN_HEIGHT/4+button_space_and_height*img + (button_height/2-text_size2/4)))

    for button in range(len(bl)):
        if bl[button].scene == 2:
            bl[button].drawButton(surface)

    with open(os.path.join(sys.path[0], "Best_precision_number_weights_z_ultimate.txt"), 'r') as f:
        file_line = f.readlines()


    txt = font.render(f'Best weights precision: {int(float(file_line[0]))}%', True, BLACK)
    surface.blit(txt, (WIN_WIDTH/3+image_res_factor/2, WIN_HEIGHT/4+button_space_and_height*5 + (button_height/2-text_size2/4)))


def drawNeuronScene(surface, bl, font):
    buttons_in_scene = 0
    for button in range(len(bl)):
        if bl[button].scene == 3:
            buttons_in_scene += 1
            bl[button].drawButton(surface)

    img_list = []
    for new_image in range(buttons_in_scene-1):
        img_list.append(font.render(f'Neurons hidden layer {new_image+1}:', True, BLACK))

    for img in range(len(img_list)):
        surface.blit(img_list[img], (WIN_WIDTH/10, WIN_HEIGHT/5+button_space_and_height*img + (button_height/2-text_size2/4)))

def drawSuccessRateScene(surface, bl, font, precision, name):
    success_string = f'{name} has a success rate of {float(precision)}%'
    img = font.render(success_string, True, BLACK)
    surface.blit(img, (WIN_WIDTH/2  - button_lenght/2*1.5 - button_lenght*1.5 - space_between_buttons, WIN_HEIGHT/4))

    for btn in range(len(bl)):
        if bl[btn].scene == 4:
            bl[btn].drawButton(surface)

def drawLoadingBar(surface, font, percentage, mode):
    surface.fill(BG_COLOR)
    pygame.draw.rect(surface, BLACK,  (loading_bar_x, loading_bar_y, loading_bar_max_len, loading_bar_h), line_width)
    pygame.draw.rect(surface, BLACK,  (loading_bar_x, loading_bar_y, loading_bar_max_len*percentage, loading_bar_h))
    img = font.render(f'{mode}: {int(percentage*100)}%', True, BLACK)
    surface.blit(img, (WIN_WIDTH/2.5, WIN_HEIGHT-WIN_HEIGHT/2.5))
    pygame.display.flip()
    pygame.display.update()

# cbp = convert button pressed, cdbp = clear display button pressed
def drawDrawingScene(surface, f, button_list, consol_m):
    pygame.draw.line(
        surface, BLACK, (drawing_surface_size, 0), (drawing_surface_size, WIN_HEIGHT), line_width)

    for btn in range(len(button_list)):
        if button_list[btn].scene == 5:
            button_list[btn].drawButton(surface)

    #text in consol
    for k in range(len(consol_m)):
        msg = f.render(consol_m[k].message, True, BLACK)
        surface.blit(msg, (WIN_WIDTH - extra_space +
                           WIN_WIDTH/56, WIN_HEIGHT - consol_height + k*text_size2))


def drawFigure(surface, lc):
    if len(lc) > 0:
        for i in range(len(lc) - 1):
            if lc[i] != "break" and lc[i + 1] != "break":
                pygame.draw.circle(surface, BLACK, lc[i], drawing_line_width/2)
                if len(lc[i]) > 1:
                    pygame.draw.line(
                        surface, BLACK, lc[i], lc[i + 1], drawing_line_width)
    
                
def getLayerList(neuron_list):
    layer_list = [784]
    for l in range(len(neuron_list)):
        layer_list.append(neuron_list[l])
    layer_list.append(10)
    return layer_list

def saveBestWeights(precision, network):
    with open(os.path.join(sys.path[0], "Best_precision_number_weights_z_ultimate.txt"), 'r') as f:
        file_line = f.readlines()
    highest_precision = float(file_line[0])
    if precision > highest_precision:
        with open(os.path.join(sys.path[0], "Best_precision_number_weights_z_ultimate.txt"), 'w') as f:
            f.write(f"{precision}\n")
        with open(os.path.join(sys.path[0], "Best_precision_number_weights_z_ultimate.txt"), 'a') as f:
            f.write(f"{network.neuron_list}\n")
            f.write(f"{network.learning_rate}\n")
            f.write(network.name)
            f.write(f"\n{len(network.W)}")
        with open(os.path.join(sys.path[0], "Best_weights_z_ultimate.npy"), 'wb') as f:
            for weights in range(len(network.W)):
                np.save(f, network.W[weights])

def CreateBestNetwork():
    with open(os.path.join(sys.path[0], "Best_precision_number_weights_z_ultimate.txt"), 'r') as nd:
        network_data = nd.readlines()
    neuron_list = ast.literal_eval(network_data[1])
    learning_rate = float(network_data[2])
    mnist_network = Network(neuron_list, learning_rate, network_data[3]) 
    mnist_network.W = []

    with open(os.path.join(sys.path[0], "Best_weights_z_ultimate.npy"), 'rb') as f:
        for weights in range(int(network_data[4])):
                mnist_network.W.append(np.load(f))

    return mnist_network

def detectNumber(surface, network):
    with open(os.path.join(sys.path[0], "data\mnist_test.csv"), 'r') as fts:
        input_list_mnist_test = fts.readlines()

    # split_input_list = input_list_mnist_test[389].split(",")
    # split_input_list = [float(i) for i in split_input_list]
    # v_list = split_input_list[1:len(split_input_list)]
    
    # color = 0
    # for y in range(28):
    #     for x in range(28):
    #         pygame.draw.rect(surface, (255 - v_list[color], 255 - v_list[color], 255 - v_list[color]),  (image_res_factor*x, image_res_factor*y, image_res_factor, image_res_factor))
    #         color += 1
    #         pygame.time.delay(1)
    #         pygame.display.flip()
    #         pygame.display.update()

    input_list = []
    for y in range(image_res):
        for x in range(image_res):
            middle_pixel_brightness = 0
            for pixel_y in range(image_res_factor):
                for pixel_x in range(image_res_factor):
                    middle_pixel_brightness += surface.get_at((x*image_res_factor + pixel_x,y*image_res_factor+pixel_y))[0]
            input_list.append(255 - middle_pixel_brightness/np.power(image_res_factor, 2))
            color = 255 - middle_pixel_brightness/np.power(image_res_factor, 2)
            pygame.draw.rect(surface, (color, color, color),  (x*image_res_factor, y*image_res_factor, image_res_factor, image_res_factor))
            pygame.display.flip()
            pygame.display.update()
            pygame.time.delay(1) 

    # image = pygame.Surface((image_res*image_res_factor, image_res*image_res_factor)) # Create image surface
    # # Blit portion of the display to the image
    # image.blit(surface, (0, 0), ((0,0), (image_res*image_res_factor,image_res*image_res_factor)))
    # pygame.image.save(image, "image.jpg")  # Save the image to the dis
    return network.detect(np.array(input_list)/255)

def TrainTestNetwork(network, surface, font):
    # get inputs and target from csv file
    with open(os.path.join(sys.path[0], "data\mnist_train.csv"), 'r') as ftr:
        input_list_mnist_train = ftr.readlines()

    with open(os.path.join(sys.path[0], "data\mnist_test.csv"), 'r') as fts:
        input_list_mnist_test = fts.readlines()
    
    network.train(input_list_mnist_train, surface, font)
    precision = network.test(input_list_mnist_test, surface, font)
    saveBestWeights(precision, network)
    return [True, precision]

class Network:
    def __init__(self, neuron_list, learning_rate, name):
        self.name = name
        self.neuron_list = neuron_list
        self.input_neurons = neuron_list[0]
        self.output_neurons = neuron_list[-1]
        self.learning_rate = learning_rate
        self.hidden_layer_arrays = []
        self.training_percentage = 0
        self.test_percentage = 0
        self.W = []
        for layer in range(len(neuron_list)-1):
            self.W.append(np.random.uniform(-0.5, 0.5, (neuron_list[layer+1], neuron_list[layer])))
        
    def sigmoid(self, z):
        return 1/(1+np.exp(-z))

    def detect(self, input_array):
        next_hidden_layer_array = input_array
        for hidden_layer in range(len(self.neuron_list)-1):
            next_hidden_layer_array = self.sigmoid(np.dot(self.W[hidden_layer], next_hidden_layer_array))
        output_list = next_hidden_layer_array.tolist()
        highest_output = max(output_list)
        return output_list.index(highest_output)

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

    def train(self, input_list, surface, font):
        for line in range(len(input_list)):
            if line%200 == 0:
                drawLoadingBar(surface, font, line/len(input_list), "Training")
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
        drawLoadingBar(surface, font, 1, "Training")
        
    def test(self, input_list, surface, font):
        right_answers = 0
        for line in range(len(input_list)):
            if line%100 == 0:
                drawLoadingBar(surface, font, line/len(input_list), " Testing")
            split_input_list = input_list[line].split(",")
            split_input_list = [float(i) for i in split_input_list]
            target = int(split_input_list[0])
            for number in range(len(split_input_list)-1):
                if split_input_list[number+1] > 0:
                    split_input_list[number+1] = 1
            input_array = np.array(split_input_list[1:len(split_input_list)])
            # get index of highest value in output list
            output_list = self.feedforward(input_array).tolist()
            highest_value = max(output_list)
            highest_value_index = output_list.index(highest_value)
            if highest_value_index == target:
                right_answers += 1

        drawLoadingBar(surface, font, 1, " Testing")
        return right_answers/len(input_list)*100

class ConsolMessage:
    def __init__(self, message, start_time):
        self.message = message
        self.st = start_time

class Button:
    def __init__(self, x, y, lenght, height, font, name, name_x, name_y, scene, active, type, tag):
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
        self.tag = tag

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
        success_rate_scene = False
        drawing_scene = False

        able_to_draw = False
        line_coordinates = []
        mouse_pressed = False
        detect_button_pressed = False
        clear_display_button_pressed = False
        font1 = pygame.font.SysFont('Arial.ttf', text_size1)
        font2 = pygame.font.SysFont('Arial.ttf', text_size2)
        consol_messages = []

        active_input_field = ""
        button_list = [Button(WIN_WIDTH - extra_space/2 - button_lenght/2, 20, button_lenght, button_height, font1, 'Detect', WIN_WIDTH/61.7143, button_height/5, 5, True, "button", ""),
                      Button(WIN_WIDTH - extra_space/2 - button_lenght/2, 20 + button_space_and_height, button_lenght, button_height, font1, 'Clear', WIN_WIDTH/39.2727, button_height/5, 5, True, "button", ""),
                      Button(WIN_WIDTH/2 - button_lenght/2, WIN_HEIGHT - WIN_HEIGHT/3, button_lenght, button_height, font1, 'OK', WIN_WIDTH/25.41176, button_height/5, 1, True, "button", ""),
                      Button(WIN_WIDTH/2 - input_fiel_lenght/2, WIN_HEIGHT/4, input_fiel_lenght, button_height, font1, '', WIN_WIDTH/86.4, button_height/5, 2, True, "input_str", "name"),
                      Button(WIN_WIDTH/2 - input_fiel_lenght/2, WIN_HEIGHT/4 + button_space_and_height, input_fiel_lenght, button_height, font1, '', WIN_WIDTH/86.4, button_height/5, 2, True, "input_float", "learning_rate"),
                      Button(WIN_WIDTH/2 - input_fiel_lenght/2, WIN_HEIGHT/4 + button_space_and_height*2, input_fiel_lenght, button_height, font1, '', WIN_WIDTH/86.4, button_height/5, 2, True, "input_hidden_layer", "hidden_layers"),
                      Button(WIN_WIDTH/2 - button_lenght/2, WIN_HEIGHT/4 + button_space_and_height*3+space_between_buttons, button_lenght, button_height, font1, 'OK', WIN_WIDTH/25.41176, button_height/5, 2, False, "button", ""),
                      Button(WIN_WIDTH/2 - button_lenght - 10, WIN_HEIGHT/4 + button_space_and_height*4+space_between_buttons, button_lenght*2 + 20, button_height, font1, 'Use best weights', 5, button_height/5, 2, False, "button", ""),
                      Button(WIN_WIDTH/2  - button_lenght/2*1.5 - button_lenght*1.5 - space_between_buttons, WIN_HEIGHT/4 + button_space_and_height + space_between_buttons, button_lenght*1.5, button_height, font1, 'Recreate', WIN_WIDTH/39.2727, button_height/5, 4, True, "button", ""),
                      Button(WIN_WIDTH/2 - button_lenght/2*1.5, WIN_HEIGHT/4 + button_space_and_height + space_between_buttons, button_lenght*1.5, button_height, font1, 'Train again', WIN_WIDTH/107.75, button_height/5, 4, True, "button", ""),
                      Button(WIN_WIDTH/2 + button_lenght/2*1.5 + space_between_buttons, WIN_HEIGHT/4 + button_space_and_height + space_between_buttons, button_lenght*1.5, button_height, font1, 'Go on', WIN_WIDTH/21.55, button_height/5, 4, True, "button", "")]
        
        network_name = ""
        learning_rate = 0
        hidden_layers = 0
        neuron_list  = []
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
                            if button_list[button].active:
                                if button_list[button].Pressed():
                                    if drawing_scene:
                                        if button_list[button].name == 'Detect':  
                                            button_list[button].message = f"{mnist_network.name} detected {detectNumber(self.screen, mnist_network)}"
                                        elif button_list[button].name == 'Clear':
                                            line_coordinates = []
                                    elif button_list[button].name == 'OK' or button_list[button].name == 'Create / Train':
                                        if button_list[button].scene == 1:
                                            if introducing_scene:
                                                introducing_scene = False
                                                select_hidden_layers_scene = True
                                        elif button_list[button].scene == 2:
                                            if select_hidden_layers_scene:
                                                if learning_rate == 0:
                                                    learning_rate = 0.00000000001
                                                for layer in range(hidden_layers):
                                                    button_list.append(Button(WIN_WIDTH/2 - input_fiel_lenght/2, WIN_HEIGHT/5 + button_space_and_height*layer, input_fiel_lenght, button_height, font1, '', WIN_WIDTH/86.4, button_height/5, 3, True, "input_neurons", "neurons"),)
                                                button_list.append(Button(WIN_WIDTH/2 - button_lenght, WIN_HEIGHT/5 + button_space_and_height*(hidden_layers)+space_between_buttons, button_lenght*2, button_height, font1, 'Create / Train', WIN_WIDTH/50.70588, button_height/5, 3, False, "button", ""))
                                                select_hidden_layers_scene = False
                                                select_neurons_per_hidden_layer_scene = True
                                        elif button_list[button].scene == 3:
                                            if select_neurons_per_hidden_layer_scene:
                                                mnist_network = Network(getLayerList(neuron_list), learning_rate, network_name)
                                                success_rate_list = TrainTestNetwork(mnist_network, self.screen, font1)
                                                success_rate_scene = success_rate_list[0]
                                                select_neurons_per_hidden_layer_scene = False

                                    elif button_list[button].name == 'Use best weights':
                                        mnist_network = CreateBestNetwork()
                                        select_hidden_layers_scene = False
                                        drawing_scene = True
                                    elif button_list[button].name == 'Recreate':
                                        if success_rate_scene:
                                            deleted_buttons = 0
                                            for i in range(len(button_list)):
                                                if button_list[i - deleted_buttons].scene == 3:
                                                    del button_list[i - deleted_buttons]
                                                    deleted_buttons += 1
                                            success_rate_scene = False
                                            select_hidden_layers_scene = True
                                            break
                                    elif button_list[button].name == 'Train again':
                                        if success_rate_scene:
                                            success_rate_scene = False
                                            success_rate_list = TrainTestNetwork(mnist_network, self.screen, font1)
                                            success_rate_scene = success_rate_list[0]
                                    elif button_list[button].name == 'Go on':
                                        if success_rate_scene:
                                            success_rate_scene = False
                                            drawing_scene = True
                                    else:
                                        active_input_field = button_list[button]
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
                    if active_input_field != "":
                        if active_input_field.type != 'button':
                            if event.key == pygame.K_BACKSPACE:
                                active_input_field.name = active_input_field.name[:-1]
                            
                            elif active_input_field.tag == "hidden_layers" and active_input_field.name == '':
                                if event.key == pygame.K_1 or event.key == pygame.K_2 or event.key == pygame.K_3 or event.key == pygame.K_4 or event.key == pygame.K_5: 
                                    active_input_field.name += event.unicode
                            
                            elif active_input_field.type != "input_hidden_layer" and active_input_field.type != "input_neurons" and len(active_input_field.name) <= 11:
                                if active_input_field.type == "input_float":
                                    if event.key == pygame.K_0 or event.key == pygame.K_1 or event.key == pygame.K_2 or event.key == pygame.K_3 or event.key == pygame.K_4 or event.key == pygame.K_5 or event.key == pygame.K_6 or event.key == pygame.K_7 or event.key == pygame.K_8 or event.key == pygame.K_9 or event.key == pygame.K_PERIOD: 
                                        active_input_field.name += event.unicode
                                else:
                                    active_input_field.name += event.unicode

                            elif active_input_field.type == "input_neurons"  and len(active_input_field.name) < 3:
                                if active_input_field.name == '':
                                    if event.key == pygame.K_1 or event.key == pygame.K_2 or event.key == pygame.K_3 or event.key == pygame.K_4 or event.key == pygame.K_5 or event.key == pygame.K_6 or event.key == pygame.K_7 or event.key == pygame.K_8 or event.key == pygame.K_9:
                                        active_input_field.name += event.unicode
                                else:
                                    if event.key == pygame.K_0 or event.key == pygame.K_1 or event.key == pygame.K_2 or event.key == pygame.K_3 or event.key == pygame.K_4 or event.key == pygame.K_5 or event.key == pygame.K_6 or event.key == pygame.K_7 or event.key == pygame.K_8 or event.key == pygame.K_9:
                                        active_input_field.name += event.unicode
                            if active_input_field.name != '':
                                if active_input_field.tag == "name":
                                    network_name = active_input_field.name
                                elif active_input_field.tag == "learning_rate":
                                    learning_rate = float(active_input_field.name)
                                elif active_input_field.tag == "hidden_layers":
                                    hidden_layers = int(active_input_field.name)

                            active_input_field.img = font1.render(active_input_field.name, True, BLACK)

                #update buttons
                inputs_scene_2 = 0
                inputs_scene_3 = 0
                neuron_list = []
                for field in range(len(button_list)):
                    if button_list[field].scene == 2:
                        if button_list[field].name != '':
                            inputs_scene_2 += 1
                        if inputs_scene_2 > 3:
                            button_list[field].active = True
                        elif button_list[field].name == 'OK':
                            button_list[field].active = False

                    if button_list[field].scene == 3:
                        if button_list[field].name != '':
                            inputs_scene_3 += 1
                        if inputs_scene_3 > hidden_layers:
                            button_list[field].active = True
                        elif button_list[field].name == 'OK':
                            button_list[field].active = False
                
                    if button_list[field].tag == "neurons":
                        if button_list[field].name != '':
                            neuron_list.append(int(button_list[field].name))
                        
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
                drawIntroducingScene(self.screen, button_list, font2)

            elif select_hidden_layers_scene:
                for btn in range(len(button_list)):
                    if button_list[btn].name == "Use best weights":
                        button_list[btn].active = True
                drawHiddenLayerScene(self.screen, button_list, font2)

            elif select_neurons_per_hidden_layer_scene:
                drawNeuronScene(self.screen, button_list, font2)
            
            elif success_rate_scene:
                drawSuccessRateScene(self.screen, button_list, font1, success_rate_list[1], mnist_network.name)

            elif drawing_scene:
                drawDrawingScene(self.screen, font2,
                            button_list, consol_messages)
                if able_to_draw:
                    drawFigure(self.screen, line_coordinates)
                able_to_draw = True

            

            # Update
            pygame.time.delay(TIME_DELAY)
            pygame.display.flip()
            pygame.display.update()
        pygame.quit()


if __name__ == "__main__":
    Game().play()