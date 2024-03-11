import time

def powerset(items):
    """
    Returns a list of all possible subsets of the given items.
    """
    res = [[]]
    for item in items:
        newset = [r+[item] for r in res]
        res.extend(newset)
    return res

def knapsack_brute_force(weights, values, max_weight, max_items=0):
    items = list(zip(weights, values))
    knapsack = []
    best_weight = 0
    best_value = 0
    for item_set in powerset(items):
        set_weight = sum(item[0] for item in item_set)
        set_value = sum(item[1] for item in item_set)
        if set_value > best_value and set_weight <= max_weight and (not max_items or len(item_set) <= max_items):
            best_weight = set_weight
            best_value = set_value
            knapsack = item_set
    return knapsack, best_weight, best_value

def run_test_case(test_case_num):
    input_file = 'input{}.txt'.format(test_case_num)
    output_file = 'output{}.txt'.format(test_case_num)

    with open(input_file, 'r') as f:
        max_weight = int(f.readline().strip())
        weights = [int(w) for w in f.readline().strip().split(', ')]
        values = [int(v) for v in f.readline().strip().split(', ')]
        max_items = [int(x) for x in f.readline().strip().split(',')]

    if max_items:
        max_items = max_items[0] # The input file provides a list of integers, so we need to extract the first element

    start_time = time.time()
    knapsack, knapsack_weight, knapsack_value = knapsack_brute_force(weights, values, max_weight, max_items)
    end_time = time.time()

    with open(output_file, 'w') as f:
        f.write("Maximum value: {}\n".format(knapsack_value))
        f.write("Total weight: {}\n".format(knapsack_weight))
        f.write("Items included in the knapsack:\n")
        for item in knapsack:
            f.write("  weight={}, value={}\n".format(item[0], item[1]))

    print("Test case {} completed in {:.4f} milliseconds".format(test_case_num, (end_time - start_time) * 1000))

def main():
    for i in range(0, 10):
        run_test_case(i)

if __name__ == '__main__':
    main()