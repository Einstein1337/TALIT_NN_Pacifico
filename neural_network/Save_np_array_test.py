import numpy as np
import os
import sys

my_list = [np.array([[2, 2], [3, 4]]), np.array([[1, 2], [3, 4]])]

print(my_list)
print("")

with open(os.path.join(sys.path[0], "Save_array_test.txt"), 'wb') as f:
    for weights in range(len(my_list)):
        np.save(f, my_list[weights])

new_list = []

with open(os.path.join(sys.path[0], "Save_array_test.txt"), 'rb') as f:
    for weights in range(2):
            new_list.append(np.load(f))

print(new_list)