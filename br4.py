import numpy as np
import time

class Item:
    def __init__(self, weight, value, class_label):
        self.weight = weight
        self.value = value
        self.class_label = class_label

def bound(i, weight, value, taken, W, items, item_matrix, max_value):
    if weight > W:
        return -float('inf')
    if i == len(items):
        return value
    #print("1")

    class_taken = np.logical_or.reduce(item_matrix[:, i])
    if np.any(np.logical_and(taken, class_taken)):
        value += np.sum(np.fromiter((items[j].value for j in range(i, len(items)) if not taken[j]), dtype=int))
        max_value = np.sum(np.fromiter((items[j].value for j in range(i, len(items)) if not taken[j]), dtype=int))
        return value


    lower_bound = value
    j = i
    while j < len(items) and weight + items[j].weight <= W:
        lower_bound += items[j].value
        weight += items[j].weight
        j += 1
    #print("2")
    if j < len(items):
        lower_bound += (W - weight) * items[j].value / items[j].weight
    value = max_value
    return lower_bound

def check_label(arr, N):
    
    missing_numbers = []
    num_set = set(arr)
    for i in range(1, N+1):
        if i not in num_set:
            missing_numbers.append(i)
    
    print(missing_numbers)
    return missing_numbers

def b_b_r(i, weight, value, taken, W, items, item_matrix, max_value, max_taken):
    current_value = max_value
    if weight > W or i == len(items):
        if weight <= W and value > max_value:
            max_value = value
            max_taken = taken.copy()
            current_value = max_value
        return max_value, max_taken

    if bound(i, weight, value, taken, W, items, item_matrix, max_value) <= max_value:
        return max_value, max_taken
    if bound(i, weight, value, taken, W, items, item_matrix, current_value) <= max_value:
        return max_value, max_taken
    
    class_taken = np.logical_or.reduce(item_matrix[:, i])
    #print("1")
    if not np.any(class_taken) and np.sum(taken) == 0:
        taken[i] = 1
        max_value, max_taken = b_b_r(i + 1, weight + items[i].weight, value + items[i].value, taken, W, items, item_matrix, max_value, max_taken)
        taken[i] = 0
        return max_value, max_taken
    # max_value, max_taken = b_b_r(i , weight, value, taken, W, items, item_matrix, max_value, max_taken)
    taken[i] = 1
    max_value, max_taken = b_b_r(i + 1, weight + items[i].weight, value + items[i].value, taken, W, items, item_matrix, max_value, max_taken)
    taken[i] = 0
    current_value +=bound(i, weight, value, taken, W, items, item_matrix, current_value)
    max_value, max_taken = b_b_r(i + 1, weight, value, taken, W, items, item_matrix, max_value, max_taken)
    current_value+= value
    return max_value, max_taken

def branchNb(W, items):
    n = len(items)
    m = max(item.class_label for item in items)
    item_matrix = np.zeros((m, n))
    for i in range(n):
        item_matrix[items[i].class_label - 1, i] = 1
    #max_value = 0
    max_value = -float('inf')
    max_taken = None

    taken = np.zeros(n, dtype=int)
    max_value, max_taken = b_b_r(0, 0, 0, taken, W, items, item_matrix, max_value, max_taken)

    return max_value, max_taken

def read_input_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    W = int(lines[0].strip())
    m = int(lines[1].strip())
    weights = list(map(float, lines[2].strip().split(', ')))
    #print ("weight")
    values = list(map(int, lines[3].strip().split(', ')))
    class_labels = list(map(int, lines[4].strip().split(', ')))
    # print(class_label)
    items = []
    classes = []
    for weight, value, class_label in zip(weights, values, class_labels):
        item = Item(weight, value, class_label)
        items.append(item)
        classes.append(class_label)
    miss = check_label(classes,m)
    return W, items, miss

def write_output_file(filename, max_value, max_taken, miss):
    
    with open(filename, 'w') as file:
        if len(miss) ==0:
            file.write(str(max_value) + '\n')
            file.write(', '.join(str(taken) for taken in max_taken))
        else:
            file.write(str("0") + '\n')
            output_string = ', '.join(str(element) for element in miss)
            file.write("No item class: ")
            file.write(output_string)

def main():
    for q in range(10):
        if q in [2, 6, 7, 8]:
            continue

        input_filename = f"input{q}.txt"
        output_filename = f"output{q}.txt"
        miss = []
        W, items,miss = read_input_file(input_filename)
        print(q)
        start_time = time.time()
        max_value, max_taken = branchNb(W, items)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print("Elapsed time: {:.2f} seconds".format(elapsed_time))
        write_output_file(output_filename, max_value, max_taken, miss)

if __name__ == '__main__':
    main()
