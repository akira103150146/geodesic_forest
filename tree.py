import numpy as np
import fast_bic as fb
import math


class point:
    def __init__(self, value: np.array, index: int):
        self.value = value
        self.index = index

    def getValue(self):
        return self.value

class treeNode:
    def __init__(self, value: np.array, depth=1, indexes=None):
        self.value = value
        self.depth = depth
        self.left = None
        self.right = None
        self.indexes = indexes

    def getColumnByDim(self, dim: int):
        column = [p.value[dim] for p in self.value]
        column.sort()

        return column

    def count(self):
        return len(self.value)

    def split(self, dim: int, splitPoint: float):
        sortedPoints = sorted(self.value, key=lambda p: p.value[dim].any())
        left = [x for x in sortedPoints if x.value[dim] <= splitPoint]
        right = [x for x in sortedPoints if x.value[dim] > splitPoint]
        self.value = None
        self.left = treeNode(left, depth=self.depth + 1)
        self.right = treeNode(right, depth=self.depth + 1)


    def printTree(self):
        if self.value != None:
            [print("index: ", p.index, " value: ", p.value) for p in self.value]
            print("\n----")

        if self.left != None:
            self.left.printTree()

        if self.right != None:
            self.right.printTree()

    def getPointsGroup(self, result):
        if self.value != None:
            result.append([int(v.index) for v in self.value])

        if self.left != None:
            self.left.getPointsGroup(result)

        if self.right != None:
            self.right.getPointsGroup(result)


def should_split_continue(tree: treeNode):
    return tree.count() >= 50


def build_tree(tree: treeNode, d: int):
    if not should_split_continue(tree):
        return
    else:
        bestDim, splitPoint = find_best_dim_and_split_point(tree, d)
        tree.split(bestDim, splitPoint)
        build_tree(tree.right, d)
        build_tree(tree.left, d)


def find_best_dim_and_split_point(node: treeNode, d: int):
    tempBestDim = None
    tempSplitPoint = None
    tempMinBIC = np.Inf

    for i in range(d):
        # splitPoint, minBIC = fb.fast_bic(node.getColumnByDim(i))
        splitPoint, minBIC = fb.Two_means(node.getColumnByDim(i))
        if math.isnan(minBIC):
            minBIC = 100000
        
        if minBIC < tempMinBIC:
            tempBestDim = i
            tempSplitPoint = splitPoint
            tempMinBIC = minBIC

    return tempBestDim, tempSplitPoint
