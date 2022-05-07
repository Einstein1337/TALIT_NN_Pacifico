import numpy as np
from numpy.core.fromnumeric import transpose
from numpy.core.numeric import outer
import os
import sys


def saveBestWeightsLR(precision, network):
    with open(os.path.join(sys.path[0], 'Best_weights_learning_rate_mnist.txt'), 'r') as f:
        file_lines = f.readlines()
    highest_percentage = float(file_lines[0])
    if precision > highest_percentage:
        f = open(os.path.join(sys.path[0], 'Best_weights_learning_rate_mnist.txt'), 'w')
        f.write(f"{precision}\n")
        f.close()
        f = open(os.path.join(sys.path[0], 'Best_weights_learning_rate_mnist.txt'), 'a')
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


    def feedForward(self, input_array):
        next_hidden_layer_array = input_array
        self.hidden_layer_arrays.append(next_hidden_layer_array)
        for hidden_layer in range(len(self.neuron_list)-1):
            next_hidden_layer_array = self.sigmoid(np.dot(self.W[hidden_layer], next_hidden_layer_array))
            self.hidden_layer_arrays.append(next_hidden_layer_array)
        return next_hidden_layer_array  # last hidden layer array = output array
       
    def feedBackwards(self, input_vector):
        pass
    
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

            output_array = self.feedForward(input_array)
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
            output_list = self.feedForward(input_array).tolist()
            highest_value = max(output_list)
            highest_value_index = output_list.index(highest_value)
            if highest_value_index == target:
                right_answers += 1

        print(f"Test {self.name}: 100%")
        return right_answers/len(input_list)*100


learning_rate = 0.02
mnist_network = Network([784, 50, 50, 10], 0.01, "MNIST network")

# get inputs and target from csv file
with open(os.path.join(sys.path[0], 'data\mnist_train.csv'), 'r') as f2tr:
    input_list_mnist_train = f2tr.readlines()

with open(os.path.join(sys.path[0], 'data\mnist_test.csv'), 'r') as f2ts:
    input_list_mnist_test = f2ts.readlines()


for i in range(1):  
    mnist_network.__init__([784, 50, 50, 10], 0.0121, "MNIST network")
    mnist_network.train(input_list_mnist_train)

    precision_mnist = mnist_network.test(input_list_mnist_test)


    saveBestWeightsLR(precision_mnist, mnist_network)

    print(f"MNIST network precision: {precision_mnist}%")
print("Done")
