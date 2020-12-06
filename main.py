import numpy as np
import tree as tr

with open('test.csv', 'r', newline='') as csv:
    lines=csv.readlines()
    data = np.genfromtxt(lines, delimiter=',')
    root = tr.treeNode(data)
    tr.build_tree(root, data.shape[1])
