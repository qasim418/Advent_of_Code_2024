from collections import deque

def parse_input(filename):
    coordinates = []
    with open(filename, 'r') as f:
        for line in f:
            x, y = map(int, line.strip().split(','))
            coordinates.append((x, y))
    return coordinates

def check_path_exists(corrupted, max_size=71):
    start = (0, 0)
    end = (max_size-1, max_size-1)
    queue = deque([start])
    visited = {start}
    
    while queue:
        x, y = queue.popleft()
        if (x, y) == end:
            return True
            
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < max_size and 
                0 <= ny < max_size and 
                (nx, ny) not in corrupted and 
                (nx, ny) not in visited):
                queue.append((nx, ny))
                visited.add((nx, ny))
    return False

def find_shortest_path(corrupted, max_size=71):
    start = (0, 0)
    end = (max_size-1, max_size-1)
    queue = deque([(start, 0)])
    visited = {start}
    
    while queue:
        pos, steps = queue.popleft()
        if pos == end:
            return steps
            
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            nx, ny = pos[0] + dx, pos[1] + dy
            new_pos = (nx, ny)
            if (0 <= nx < max_size and 
                0 <= ny < max_size and 
                new_pos not in corrupted and 
                new_pos not in visited):
                queue.append((new_pos, steps + 1))
                visited.add(new_pos)
    return None

def find_blocking_coordinate(coordinates):
    corrupted = set()
    for x, y in coordinates:
        corrupted.add((x, y))
        if not check_path_exists(corrupted):
            return x, y
    return None

def main():
    coordinates = parse_input('Day_18/day18_input.txt')
    
    # Part 1
    corrupted_1024 = set(coordinates[:1024])
    path_length = find_shortest_path(corrupted_1024)
    print(f"Part 1: {path_length}")
    
    # Part 2
    blocking_x, blocking_y = find_blocking_coordinate(coordinates)
    print(f"Part 2: {blocking_x},{blocking_y}")

if __name__ == '__main__':
    main()