import numpy as np
from numpy.core.defchararray import rindex


def sigmoid(z_vektor):
    for z in range(len(z_vektor)):
        z_vektor[z] = 1/(1+(1/np.power(np.e, z_vektor[z])))
    return z_vektor


def getStrongestOutputNeuron(sol, ol):
    sol.sort()
    highest_number = sol[-1]
    for a in range(len(ol)):
        if ol[a] == highest_number:
            return a


WA = np.array([[-0.3, -0.7, -0.9, -0.9],
               [-1, -0.6, -0.6, -0.6],
               [0.8, 0.5, 0.7, 0.8]])

WB = np.array([[2.6, 2.1, -1.2],
               [-2.3, -2.3, 1.1]])

W = []
neuron_list = [4, 3, 2]  # define number of layers, with numbers of neurones

for n in range(len(neuron_list)-1):  # create random weighting for all neurons
    W.append(np.random.rand(neuron_list[n+1], neuron_list[n]))

W[0] = WA
W[1] = WB

with open('data\data_dark_bright_test_4000.csv', 'r') as f:
    input_list = f.readlines()

right_answers = 0
for i in range(len(input_list)):
    # get input arguments
    split_input_list = input_list[i].split(",")

    for h in range(len(split_input_list)):
        if h == 0:
            target = int(split_input_list[0])
        else:
            split_input_list[h] = float(split_input_list[h])/255

    input_vektor = np.array(
        [split_input_list[1], split_input_list[2], split_input_list[3], split_input_list[4]])
    # calculate
    next_hidden_layer_vektor = input_vektor
    for c in range(len(neuron_list)-1):
        next_hidden_layer_vektor = sigmoid(
            np.dot(W[c], next_hidden_layer_vektor))

    sortable_output_list = next_hidden_layer_vektor.tolist()
    output_list = next_hidden_layer_vektor.tolist()
    decision = getStrongestOutputNeuron(sortable_output_list, output_list)
    if decision == target:
        right_answers += 1
precision = right_answers/len(input_list)*100

print(f"Ihr neuronales Netz hat eine Präzision von: {precision}%")
