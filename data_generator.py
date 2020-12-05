import random
import numpy as np

def linear(number):
    with open('linear.csv', 'w', newline='') as csvfile:
        for i in range(number):
            t = random.uniform(0, 1)
            x = 4 * t
            y = 6 * t
            z = 9 * t
            csvfile.write(str(x) + "," + str(y) + "," + str(z) + "\n")

def sphere(number):
    with open('sphere.csv', 'w', newline='') as csvfile:
        r = 9
        for i in range(number):
            u = random.uniform(0, np.pi * 2)
            v = random.uniform(0, np.pi)
            x = r * np.cos(u) * np.sin(v)
            y = r * np.sin(u) * np.sin(v)
            z = r * np.cos(v)
            csvfile.write(str(x) + "," + str(y) + "," + str(z) + "\n")

