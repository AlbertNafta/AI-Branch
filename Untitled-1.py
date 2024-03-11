def read_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]


def get_items(lines):
    W = float(lines[0])
    m = int(lines[1])
    weights = list(map(float, lines[2].split(', ')))
    values = list(map(int, lines[3].split(', ')))
    classes = list(map(int, lines[4].split(', ')))
    return W, m, weights, values, classes


def branch_and_bound(W, m, weights, values, classes):
    # create a node for the root of the tree
    node = Node(0, [], [])

    # create a priority queue to store the nodes in the tree
    pq = PriorityQueue()
    pq.put(node)

    # while the priority queue is not empty
    while not pq.empty():
        # get the node with the highest priority from the priority queue
        node = pq.get()

        # if the node is a leaf node
        if len(node.items) == m:
            # check if the total weight of the items in the node is less than or equal to the knapsack capacity
            if sum(node.weights) <= W:
                # return the total value of the items in the node
                return sum(node.values)

        # for each item that is not in the node
        for i in range(len(weights)):
            # if the item is not in the node and it is not from a class that is already represented in the node
            if i not in node.items and classes[i] not in node.classes:
                # create a new node by adding the item to the node
                new_node = Node(node.level + 1, node.items + [i], node.classes + [classes[i]])

                # if the total weight of the items in the new node is less than or equal to the knapsack capacity
                if sum(new_node.weights) <= W:
                    # update the priority of the new node
                    new_node.priority = sum(new_node.values)

                    # add the new node to the priority queue
                    pq.put(new_node)

    # if the priority queue is empty, then there is no solution
    return -1


class Node:
    def __init__(self, level, items, classes):
        self.level = level
        self.items = items
        self.classes = classes
        self.weights = [weights[i] for i in items]
        self.values = [values[i] for i in items]
        self.priority = sum(self.values)


class PriorityQueue:
    def __init__(self):
        self.queue = []

    def put(self, node):
        self.queue.append(node)
        self.queue.sort(key=lambda node: node.priority)

    def get(self):
        return self.queue.pop(0)


if __name__ == '__main__':
    # read the input file
    lines = read_file('input2.txt')

    # get the knapsack capacity, number of classes, weights, values, and classes of the items
    W, m, weights, values, classes = get_items(lines)

    # solve the knapsack problem using the branch and bound algorithm
    solution = branch_and_bound(W, m, weights, values, classes)

    # print the solution
    print(solution)