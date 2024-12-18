import sys
from collections import deque

def create_grid(size):
    return [['.' for _ in range(size)] for _ in range(size)]

def mark_corrupted(grid, byte_positions, max_bytes=None):
    for i, (x, y) in enumerate(byte_positions):
        if max_bytes and i >= max_bytes:
            break
        if 0 <= x < len(grid) and 0 <= y < len(grid):
            grid[y][x] = '#'

def bfs_shortest_path(grid, start, end):
    size = len(grid)
    queue = deque()
    queue.append((start, 0))  # (position, steps)
    visited = set()
    visited.add(start)

    while queue:
        current, steps = queue.popleft()
        if current == end:
            return steps

        x, y = current
        neighbors = [
            (x, y-1),  # Up
            (x, y+1),  # Down
            (x-1, y),  # Left
            (x+1, y)   # Right
        ]

        for nx, ny in neighbors:
            if 0 <= nx < size and 0 <= ny < size:
                if grid[ny][nx] == '.' and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append(((nx, ny), steps + 1))
    
    return -1

def read_byte_positions(filename):
    byte_positions = []
    try:
        with open(filename, 'r') as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue
                parts = line.split(',')
                if len(parts) != 2:
                    print(f"Invalid line format at line {line_number}: {line}. Expected 'X,Y'. Skipping.")
                    continue
                try:
                    x = int(parts[0])
                    y = int(parts[1])
                    byte_positions.append((x, y))
                except ValueError:
                    print(f"Invalid coordinates at line {line_number}: {line}. X and Y should be integers. Skipping.")
    except FileNotFoundError:
        print(f"File not found: {filename}")
        sys.exit(1)
    return byte_positions

def main():
    grid_size = 71  # Change to 7 for the example grid
    input_file = 'Day_18/day18_input.txt'
    byte_positions = read_byte_positions(input_file)
    
    if not byte_positions:
        print("No byte positions found in the input file.")
        sys.exit(1)
    
    grid = create_grid(grid_size)
    start = (0, 0)
    end = (70, 70)  # Change to (6, 6) for the example grid
    
    # Initial checks
    if byte_positions:
        first_x, first_y = byte_positions[0]
        if (first_x, first_y) == start:
            print("First byte corrupts the start position. No possible path.")
            print(f"Answer for Part Two: {first_x},{first_y}")
            sys.exit(0)
        if (first_x, first_y) == end:
            print("First byte corrupts the exit position. No possible path.")
            print(f"Answer for Part Two: {first_x},{first_y}")
            sys.exit(0)
    
    path_found = False
    min_steps = -1
    critical_byte = None
    
    # Process bytes one by one, without a predefined limit
    for i, (x, y) in enumerate(byte_positions, start=1):
        if 0 <= x < grid_size and 0 <= y < grid_size:
            grid[y][x] = '#'
        else:
            print(f"Byte {i}: Invalid coordinates ({x},{y}). Skipping corruption.")
            continue
        
        steps = bfs_shortest_path(grid, start, end)
        
        if steps == -1:
            critical_byte = (x, y)
            print(f"Answer for Part Two: {x},{y}")
            break
        
        # For Part One, capture the first successful path's steps
        if not path_found:
            min_steps = steps
            path_found = True
    
    # Part One Output
    if path_found:
        print(f"Answer for Part One: {min_steps}")
    else:
        print("No path exists even before any bytes are inserted.")
    
    # Part Two Output
    if not critical_byte and len(byte_positions) >= 1024:
        print("No critical byte found within the first 1024 bytes.")
    elif not critical_byte:
        print("No critical byte found within the provided byte positions.")

if __name__ == "__main__":
    main()
