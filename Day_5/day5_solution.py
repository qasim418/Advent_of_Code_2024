# Read the input from the file
with open('Day_5/day5_input.txt', 'r') as f:
    lines = [line.strip() for line in f]

# Separate the rules and the updates
rules = []
updates = []
section = 0  # 0 for rules, 1 for updates

for line in lines:
    if line == '':
        section = 1
        continue
    if section == 0:
        rules.append(line)
    else:
        updates.append(line)

# Build the ordering rules as a list of tuples
ordering_rules = []
for rule in rules:
    x, y = rule.split('|')
    ordering_rules.append((int(x), int(y)))

# Part One: Identify correctly ordered updates
total_part_one = 0

for update_str in updates:
    pages = [int(x) for x in update_str.split(',')]
    page_positions = {page: idx for idx, page in enumerate(pages)}
    correct = True
    for x, y in ordering_rules:
        if x in page_positions and y in page_positions:
            if page_positions[x] >= page_positions[y]:
                correct = False
                break
    if correct:
        # Get the middle page number
        middle_index = len(pages) // 2
        middle_page = pages[middle_index]
        total_part_one += middle_page

print("Part One - Total sum of middle pages:", total_part_one)

# Part Two: Correct the incorrectly ordered updates
from collections import defaultdict, deque

# Build a graph from the ordering rules
graph = defaultdict(list)
in_degree = defaultdict(int)

for x, y in ordering_rules:
    graph[x].append(y)
    in_degree[y] += 1
    if x not in in_degree:
        in_degree[x] = in_degree.get(x, 0)

total_part_two = 0

for update_str in updates:
    pages = [int(x) for x in update_str.split(',')]
    page_set = set(pages)
    # Filter the graph and in-degrees to only include pages in the update
    graph_filtered = defaultdict(list)
    in_degree_filtered = {page: 0 for page in page_set}
    for x in page_set:
        for y in graph[x]:
            if y in page_set:
                graph_filtered[x].append(y)
                in_degree_filtered[y] += 1
    # Topological sort
    queue = deque([node for node in pages if in_degree_filtered[node] == 0])
    sorted_pages = []
    in_degree_temp = in_degree_filtered.copy()
    while queue:
        node = queue.popleft()
        sorted_pages.append(node)
        for neighbor in graph_filtered[node]:
            in_degree_temp[neighbor] -= 1
            if in_degree_temp[neighbor] == 0:
                queue.append(neighbor)
    if len(sorted_pages) != len(pages):
        print("Cycle detected in update:", update_str)
        continue
    # Only consider incorrectly ordered updates
    original_positions = {page: idx for idx, page in enumerate(pages)}
    new_positions = {page: idx for idx, page in enumerate(sorted_pages)}
    incorrectly_ordered = False
    for x, y in ordering_rules:
        if x in page_set and y in page_set:
            if original_positions[x] >= original_positions[y]:
                incorrectly_ordered = True
                break
    if incorrectly_ordered:
        # Get the middle page number after sorting
        middle_index = len(sorted_pages) // 2
        middle_page = sorted_pages[middle_index]
        total_part_two += middle_page

print("Part Two - Total sum of middle pages after reordering:", total_part_two)