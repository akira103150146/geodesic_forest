import numpy as np
import tree as tr


def choose_n_points(mat, number: int):
    indexes = np.random.randint(0, mat.shape[0], size=number)

    return indexes - 1, mat[indexes]


def create_point_array(choosePoints):
    points = []

    for p in choosePoints:
        points.append(tr.point(p[1:4], p[0]))

    return np.array(points)


def create_n_trees(data: np.array, number: int):
    trees = []

    for i in range(number):
        indexes, choosePoints = choose_n_points(data, 200)
        root = tr.treeNode(create_point_array(choosePoints), indexes=indexes)
        tr.build_tree(root, 3)
        trees.append(root)

    return trees

def get_point_appear_in_trees_count(trees, index):
    count = 0

    for tree in trees:
        if index in tree.indexes:
            count += 1

    return count

def get_all_points_groups(trees):
    groups = []
    for tree in trees:
        tree.getPointsGroup(groups)

    return groups

def get_similarity_matrix(trees, indexes):
    mat = np.zeros((1000, 1000))
    groups = get_all_points_groups(trees)

    for x in indexes:
        for y in indexes:
            if x == y:
                mat[int(x), int(y)] = 1

    uniqueElements = []

    for group in groups:
        for element in group:
            if not element in uniqueElements:
                uniqueElements.append(element)

    for element in uniqueElements:
        t = get_point_appear_in_trees_count(trees, element)
        needToAdds = {}

        for group in groups:
            if element in group:
                for index in group:
                    if index != element:
                        if needToAdds.get((element, index)) is None:
                            needToAdds[(element, index)] = 1
                        else:
                            needToAdds[(element, index)] += 1

        for key in needToAdds:
            # print(key)
            mat[key] = needToAdds[key] / t

    np.savetxt('similarity_matrix.txt', mat, fmt='%.2f')

with open('helix.csv', 'r', newline='') as csv:
    np.set_printoptions(suppress=True)
    lines = csv.readlines()
    data = np.genfromtxt(lines, delimiter=',')
    trees = create_n_trees(data, 5)
    # [print(t.printTree()) for t in trees]
    get_similarity_matrix(trees, data[1:,0])
