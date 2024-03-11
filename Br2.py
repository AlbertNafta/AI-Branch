from queue import PriorityQueue

# Class to represent an item in the knapsack problem
class Item:
    def __init__(self, weight, value, class_label):
        self.weight = weight
        self.value = value
        self.class_label = class_label
        self.bound = 0.0
    
    def __lt__(self, other):
        return self.bound > other.bound

# Function to solve the knapsack problem using the branch and bound algorithm
def knapsack_branch_and_bound(items, capacity):
    # Sort items based on their value-to-weight ratio in descending order
    items.sort(key=lambda x: x.value/x.weight, reverse=True)
    
    # Initialize variables to track the maximum value and the items included in the solution
    max_value = 0
    max_items = []
    
    # Priority queue to store nodes (items) in the branch and bound tree
    priority_queue = PriorityQueue()
    root = Item(0, 0, None)  # Create the root node
    root.bound = compute_bound(root, items, capacity)
    priority_queue.put(root)
    
    # Track the classes and their inclusion status
    class_inclusion = {}
    
    # Main loop to explore nodes in the branch and bound tree
    while not priority_queue.empty():
        node = priority_queue.get()
        
        # Check if the bound value of the node is greater than the current maximum value
        if node.bound > max_value:
            included = node.class_label is not None
            if included:
                max_items.append(node)
                max_value += node.value
                
                # Update class inclusion status
                if node.class_label in class_inclusion:
                    class_inclusion[node.class_label] = True
            
            level = node.class_label + 1 if node.class_label is not None else 0
            if level < len(items):
                new_weight = node.weight + items[level].weight
                new_value = node.value + items[level].value
                new_class_label = items[level].class_label
                
                if new_weight <= capacity and compute_bound(node, items, capacity) > max_value:
                    new_node = Item(new_weight, new_value, new_class_label)
                    new_node.bound = compute_bound(new_node, items, capacity)
                    priority_queue.put(new_node)
                
                new_node = Item(node.weight, node.value, new_class_label)
                new_node.bound = compute_bound(new_node, items, capacity)
                priority_queue.put(new_node)
    
    return max_value, max_items

# Function to compute the bound value for a node
def compute_bound(node, items, capacity):
    if node.weight > capacity:
        return 0
    
    value_bound = node.value
    weight_bound = node.weight
    level = node.class_label + 1 if node.class_label is not None else 0
    
    while level < len(items) and weight_bound + items[level].weight <= capacity:
        value_bound += items[level].value
        weight_bound += items[level].weight
        level += 1
    
    return value_bound

def main():
    for q in range(10):
        input_file = f"input{q}.txt" 
        output_file = f"output{q}.txt" 

        with open(input_file, 'r') as f:
            # Read the input values from the file
            capacity = int(f.readline().strip())
            num_classes = int(f.readline().strip())
            items = []
            
            for _ in range(num_classes):
                weights = []
                values = []
                class_labels = []
                
                # Read the weights, values, and class labels for each item in the class
                while True:
                    line = f.readline().strip()
                    if line == "":
                        break
                    
                    weights_values_labels = list(map(int, line.split(',')))
                    
                    if len(weights_values_labels) != 3:
                        continue  # Skip lines with incorrect format
                    
                    weight, value, class_label = weights_values_labels
                    weights.append(weight)
                    values.append(value)
                    class_labels.append(class_label)
                
                # Create items for each item in the class and add them to the list
                for weight, value, class_label in zip(weights, values, class_labels):
                    item = Item(weight, value, class_label)
                    items.append(item)

        # Solve the knapsack problem using the Branch and Bound algorithm
        max_value, max_items = knapsack_branch_and_bound(items, capacity)
        
        with open(output_file, 'w') as f:
            # Write the result to the output file
            f.write("Max Value: " + str(max_value) + "\n")
            f.write("Items included:\n")
            
            class_inclusion = set()
            for item in max_items:
                class_inclusion.add(item.class_label)
                f.write(f"Item {item.class_label}: Weight={item.weight}, Value={item.value}\n")
            
            # Check if any class is missing and include at least one item from each class
            for class_label in range(1, num_classes + 1):
                if class_label not in class_inclusion:
                    f.write(f"No item included from Class {class_label}\n")

if __name__ == '__main__':
    main()
