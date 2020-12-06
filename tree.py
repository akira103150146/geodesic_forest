import numpy as np
import fast_bic as fb

class treeNode:  
    def __init__(self, value: np.array, depth = 1):
        self.value = value
        self.depth = depth
        self.left = None
        self.right = None

    # def __str__(self):
    #     if self.value is None:
    #         return "Node: \n"
        
    #     result = ''
    #     for e in self.value:
    #         result = result + str(e)
    #     return result + "\n" + "\tL:" + self.left.__str__() + "\n" + "\tR:" + self.right.__str__() + "\n"
    
    def getColumnByDim(self, dim: int):
        column = self.value[:,dim]
        column.sort()

        return column

    def count(self):
        return len(self.value)
    
    def split(self, dim: int, splitPoint: float):
        sortedMatrix = self.value[np.argsort(self.value[:, dim])]
        self.left = treeNode(sortedMatrix[sortedMatrix[:, dim] <= splitPoint], self.depth + 1)
        self.right = treeNode(sortedMatrix[sortedMatrix[:, dim] > splitPoint], self.depth + 1)
        print("split" + " depth: " + str(self.depth) + " dim: " + str(dim) + "  splitPoint: " + str(splitPoint))
        print("left: ", self.left.value)
        print("right: ", self.right.value)
        print("------------")

def should_split_continue(tree: treeNode):
    return tree.count() >= 5 

def build_tree(tree: treeNode, d: int):
    if not should_split_continue(tree):
        return
    else:
        bestDim, splitPoint = find_best_dim_and_split_point(tree, d)
        tree.split(bestDim, splitPoint)
        build_tree(tree.right, d)
        build_tree(tree.left, d)
        
def find_best_dim_and_split_point(tree: treeNode, d: int):
    tempBestDim = None
    tempSplitPoint = None
    tempMinBIC = np.Inf

    for i in range(d):
        splitPoint, minBIC = fb.fast_bic(tree.getColumnByDim(i))
        if minBIC < tempMinBIC:
            tempBestDim = i
            tempSplitPoint = splitPoint
    
    return tempBestDim, tempSplitPoint







       
    