import numpy as np
from numpy.core.numeric import outer
import os

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

class Network:
    def __init__(self, neuron_list, learning_rate):
        self.neuron_list = neuron_list
        self.input_neurons = neuron_list[0]
        self.output_neurons = neuron_list[-1]
        self.learning_rate = learning_rate
        self.hidden_layer_arrays = []
        self.W = []
        for layer in range(len(neuron_list)-1):
            self.W.append(np.random.uniform(-0.5, 0.5, (neuron_list[layer+1], neuron_list[layer])))

        # self.W[0] = np.array([[0.36, 0.13, 0.3, -0.37], 
        #                       [-0.46, 0.25, 0.27, 0.2], 
        #                       [0.25, -0.19, -0.2, -0.17]])

        # self.W[1] = np.array([[0.19, -0.43, 0.28], 
        #                       [-0.21, 0.03, -0.26]])

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

    def train(self, input_list):
        for line in range(1):
            split_input_list = input_list[line].split(",")
            split_input_list = [float(i) for i in split_input_list]
            target_index = 1#int(split_input_list[0])
            target_array = self.getTargetArray(target_index)
            input_array = np.array([1, 0.98, 0.76, 0.58])#np.array(split_input_list[1:len(split_input_list)])/255

            output_array = self.feedforward(input_array)
            self.hidden_layer_arrays.reverse()
            self.W.reverse()
            E_out = target_array - output_array
            W_new = []
            E_hidden = E_out
            for weights in range(len(self.W)):
                transposed_array = np.reshape(self.hidden_layer_arrays[weights+1], (1, -1))
                W_updated = self.W[weights] + self.learning_rate*np.dot(np.reshape((E_hidden*self.hidden_layer_arrays[weights]*(1-self.hidden_layer_arrays[weights])), (-1, 1)), transposed_array)
                W_new.append(W_updated)
                print(self.W)
                print(self.W.T)
                E_hidden = np.dot(self.W[weights].T, E_hidden)
                

            W_new.reverse()
            self.W = W_new
            self.hidden_layer_arrays = []
            


    def test(self, input_list):
        right_answers = 0
        for line in range(len(input_list)):
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

        return right_answers/len(input_list)*100




toy_problem_network = Network([4, 3, 2], 0.01)
#MNIST_network = Network([784, 100, 100, 10], 1)

# get inputs and target from csv file
with open('data\data_dark_bright_training_20000.csv', 'r') as f1tr:
    input_list_toy_problem_train = f1tr.readlines()

with open('data\data_dark_bright_test_4000.csv', 'r') as f1ts:
    input_list_toy_problem_test = f1ts.readlines()

for k in range(10):
    toy_problem_network.train(input_list_toy_problem_train)
# with open('data\mnist_test.csv', 'r') as f2:
#     input_list_MNIST = f2.readlines()

precision_toy_problem = toy_problem_network.test(input_list_toy_problem_test)
#precision_MNIST = MNIST_network.test(input_list_MNIST)

print(f"Toy problem network precision: {precision_toy_problem}%")
#print(f"MNIST network precision:       {precision_MNIST}%")