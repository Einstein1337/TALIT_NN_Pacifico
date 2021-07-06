import numpy as np


class Network:
    def __init__(self, neuron_list):
        self.neuron_list = neuron_list
        self.W = []
        for n in range(len(neuron_list)-1):
            self.W.append(
                np.random.uniform(-0.5, 0.5, (neuron_list[n+1], neuron_list[n])))

    def sigmoid(self, z):
        return 1/(1+np.exp(-z))

    def feedforward(self, input_array):
        next_hidden_layer_array = input_array
        for c in range(len(self.neuron_list)-1):
            next_hidden_layer_array = self.sigmoid(
                np.dot(self.W[c], next_hidden_layer_array))
        return next_hidden_layer_array  # last hidden layer array = output array

    def test(self, input_list):
        right_answers = 0
        for i in range(len(input_list)):
            split_input_list = input_list[i].split(",")
            for h in range(len(split_input_list)):
                if h == 0:
                    target = int(split_input_list[0])
                else:
                    split_input_list[h] = float(split_input_list[h])/255

            input_array = np.zeros(len(split_input_list)-1)
            for a in range(len(split_input_list)-1):
                input_array[a] = split_input_list[a+1]

            output_list = self.feedforward(input_array).tolist()

            highest_value = max(output_list)
            highest_value_index = output_list.index(highest_value)
            if highest_value_index == target:
                right_answers += 1

        return right_answers/len(input_list)*100


toy_problem_network = Network([4, 3, 2])
MNIST_network = Network(
    [784, 100, 100, 10])

# get inputs and target from csv file
with open('data\data_dark_bright_test_4000.csv', 'r') as f1:
    input_list_toy_problem = f1.readlines()

with open('data\mnist_test.csv', 'r') as f2:
    input_list_MNIST = f2.readlines()

precision_toy_problem = toy_problem_network.test(input_list_toy_problem)
precision_MNIST = MNIST_network.test(input_list_MNIST)

print(f"Toy problem network precision: {precision_toy_problem}%")
print(f"MNIST network precision:       {precision_MNIST}%")
