import numpy as np
import time

class Item:
    def __init__(self, weight, value, class_label):
        self.weight = weight
        self.value = value
        self.class_label = class_label

def knapsack_branch_and_bound(W, items):
    n = len(items)
    m = max(item.class_label for item in items)
    item_matrix = np.zeros((m, n))
    for i in range(n):
        item_matrix[items[i].class_label - 1, i] = 1

    max_value = -float('inf')
    max_taken = None

    def bound(i, weight, value, taken):
        if weight > W:
            return -float('inf')
        if i == n:
            return value

        # Check if taking the whole class is feasible
        class_taken = np.logical_or.reduce(item_matrix[:, i])
        if np.any(np.logical_and(taken, class_taken)):
            value += np.sum(np.fromiter((items[j].value for j in range(i, n) if not taken[j]), dtype=int))
            return value

        # Compute lower bound
        lower_bound = value
        j = i
        while j < n and weight + items[j].weight <= W:
            lower_bound += items[j].value
            weight += items[j].weight
            j += 1

        if j < n:
            lower_bound += (W - weight) * items[j].value / items[j].weight

        return lower_bound

    def branch_and_bound_recursive(i, weight, value, taken):
        nonlocal max_value, max_taken

        if weight > W or i == n:
            if weight <= W and value > max_value:
                max_value = value
                max_taken = taken.copy()
            return

        if bound(i, weight, value, taken) <= max_value:
            return

        # Ensure at least one item is selected from each class
        class_taken = np.logical_or.reduce(item_matrix[:, i])
        if not np.any(class_taken) and np.sum(taken) == 0:
            taken[i] = 1
            branch_and_bound_recursive(i + 1, weight + items[i].weight, value + items[i].value, taken)
            taken[i] = 0
            return

        # Explore taking the item
        taken[i] = 1
        branch_and_bound_recursive(i + 1, weight + items[i].weight, value + items[i].value, taken)
        taken[i] = 0

        # Explore not taking the item
        branch_and_bound_recursive(i + 1, weight, value, taken)

    taken = np.zeros(n, dtype=int)
    branch_and_bound_recursive(0, 0, 0, taken)

    return max_value, max_taken


def read_input_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    W = int(lines[0].strip())
    m = int(lines[1].strip())
    weights = list(map(float, lines[2].strip().split(', ')))
    values = list(map(int, lines[3].strip().split(', ')))
    class_labels = list(map(int, lines[4].strip().split(', ')))

    items = []
    classes = []
    for weight, value, class_label in zip(weights, values, class_labels):
        item = Item(weight, value, class_label)
        
    return W, items


def write_output_file(filename, max_value, max_taken):
    with open(filename, 'w') as file:
        file.write(str(max_value) + '\n')
        file.write(', '.join(str(taken) for taken in max_taken))

def main():
    for q in range(10):
        if q in [2, 6, 7, 8]:
            continue

        input_filename = f"input{q}.txt"
        output_filename = f"output{q}.txt"

        W, items = read_input_file(input_filename)
        print(q)
        start_time = time.time()
        max_value, max_taken = knapsack_branch_and_bound(W, items)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print("Elapsed time: {:.2f} seconds".format(elapsed_time))
        write_output_file(output_filename, max_value, max_taken)

if __name__ == '__main__':
    main()
