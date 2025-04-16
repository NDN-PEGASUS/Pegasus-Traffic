import itertools

def parse_product_combinations(file_path):
    product_combinations = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines[2:]:  # Skip header lines
            combination, count = line.strip().split()
            product_combinations.append((list(map(int, combination.split('/'))), int(count)))
    return product_combinations

def generate_box_combinations(max_cost=206, start=4, end=22):
    box_combinations = []
    for num_boxes in range(1, 8):  # Up to 7 boxes
        for capacities in itertools.product(range(start, end), repeat=num_boxes):
            cost = 3 * sum(capacities) + len(capacities)
            if cost <= max_cost:
                box_combinations.append(capacities)
    state = max_cost
    return box_combinations, state, start, end

def can_pack(box, product):
    return all(box[i] >= product[i] for i in range(len(product)))

def find_optimal_combination(results):
    optimal_combination = max(results, key=lambda x: x[1])
    return optimal_combination

def write_results(results, index, state, start, end):
    optimal_combination = find_optimal_combination(results)
    print(optimal_combination)
    file_name = "./optimal_formats/" + f"results_state_{state}_range_{start}_{end}_{index}.txt"
    with open(file_name, "w") as f:
        f.write(f"optimal: {optimal_combination}\n")
        for box, count in results:
            f.write(f"{box}\t{count}\n")

def evaluate_combinations(box_combinations, product_combinations, state, start, end):
    results = []
    index = 0
    box_num = len(box_combinations)
    print("box_combinations:" + str(box_num))
    for box in box_combinations:
        # count = sum(1 for product, _ in product_combinations if can_pack(box, product))
        cur_count = 0
        for product, count in product_combinations:
            if len(box) >= len(product):
                if can_pack(box, product):
                    cur_count += count
        results.append((box, cur_count))
        index += 1
        # print(f"Processed box {index}/{box_num}")

        if index % 500000 == 0:
            write_results(results, index, state, start, end)
            results = []

    if results:
        write_results(results, index, state, start, end)

# Main function
file_path = 'format_counts.txt'
product_combinations = parse_product_combinations(file_path)
box_combinations, state, start, end  = generate_box_combinations()
evaluate_combinations(box_combinations, product_combinations, state, start, end)