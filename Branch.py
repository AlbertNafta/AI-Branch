from queue import PriorityQueue

# Class to represent an item in the knapsack problem
class Item:
    def __init__(self, weight, value, index):
        self.weight = weight
        self.value = value
        self.index = index
        self.bound = 0.0
    
    def __lt__(self, other):
        return self.bound > other.bound

# Function to solve the knapsack problem using the branch and bound algorithm
def knapsack_branch_and_bound(weights, values, capacity):
    items = []
    # Create Item objects for each item in the problem
    for i in range(len(weights)):
        item = Item(weights[i], values[i], i)
        items.append(item)
    
    # Sort items based on their value-to-weight ratio in descending order
    items.sort(key=lambda x: x.value/x.weight, reverse=True)
    
    # Initialize variables to track the maximum value and the items included in the solution
    max_value = 0
    max_items = []
    
    # Priority queue to store nodes (items) in the branch and bound tree
    priority_queue = PriorityQueue()
    root = Item(0, 0, -1)  # Create the root node
    root.bound = compute_bound(root, items, capacity)  # Compute the bound value for the root node, nhét item
    priority_queue.put(root)  # Add the root node to the priority queue
    
    # Main loop to explore nodes in the branch and bound tree
    while not priority_queue.empty():
        node = priority_queue.get()  # Get the node with the highest bound value from the priority queue
        
        # Check if the bound value of the node is greater than the current maximum value
        
        if node.bound > max_value:
            included = node.index != -1
            if included:
                max_items = [node.index]  # Add the index of the included item to the solution
                max_value = node.value  # Update the maximum value
            
            level = node.index + 1  # Level of the next node
            if level < len(items):
                new_weight = node.weight + items[level].weight  # Calculate the weight of including the next item
                new_value = node.value + items[level].value  # Calculate the value of including the next item
                
                # Check if the new weight does not exceed the capacity and the bound value is greater than the current maximum value
                if new_weight <= capacity and compute_bound(node, items, capacity) > max_value:
                    new_node = Item(new_weight, new_value, level)  # Create a new node for including the next item
                    new_node.bound = compute_bound(new_node, items, capacity)  # Compute the bound value for the new node
                    # print(new_node.bound)
                    priority_queue.put(new_node)  # Add the new node to the priority queue
                
                new_node = Item(node.weight, node.value, level)  # Create a new node for excluding the level item
                new_node.bound = compute_bound(new_node, items, capacity)  # Compute the bound value for the new node
                # print(new_node.bound)
                priority_queue.put(new_node)  # Add the new node to the priority queue
    
    return max_value, max_items

# Function to compute the bound value for a node
def compute_bound(node, items, capacity):
    if node.weight > capacity:  # If the weight of the node exceeds the capacity, the bound is 0
        return 0
    
    value_bound = node.value
    weight_bound = node.weight
    level = node.index + 1
    # Calculate the bound value by adding the values of the remaining items based on the remaining capacity
    while level < len(items) and weight_bound + items[level].weight <= capacity:
        value_bound += items[level].value
        weight_bound += items[level].weight
        level += 1
    
    # If there are still remaining items, calculate the potential value based on the value-to-weight ratio
    if level < len(items):
        value_bound += (capacity - weight_bound) * items[level].value / items[level].weight
    
    return value_bound

def check_positions(numbers, positions):
    max_position = max(positions) if positions else 0
    result = [0] * len(numbers)
    
    for pos in positions:
        if 0 <= pos < len(numbers):
            result[pos] = 1
    
    return result



def main():
    for q in range(10):
        input_file = f"input{q}.txt" 
        output_file = f"output{q}.txt" 

        with open(input_file, 'r') as f:
            # Read the input values from the file
            capacity = int(f.readline().strip())
            num_items = int(f.readline().strip())
            weights = list(map(float, f.readline().strip().split(',')))
            values = list(map(int, f.readline().strip().split(',')))
            labels = list(map(int, f.readline().strip().split(',')))

        # Solve the knapsack problem using the Branch and Bound algorithm
        max_value, max_items = knapsack_branch_and_bound(weights, values, capacity)
        result = check_positions(weights, max_items)
        with open(output_file, 'w') as f:
            # Write the result to the output file
            f.write("Max Value: " + str(max_value) + "\n")
            f.write("Items included: " + ', '.join(str(i) for i in result))


if __name__ == '__main__':
    main()
