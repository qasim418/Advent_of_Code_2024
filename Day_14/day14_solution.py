import re
from collections import defaultdict

# Define grid dimensions
GRID_WIDTH = 101
GRID_HEIGHT = 103

# Function to parse input
def parse_input(input_file):
    robots = []
    with open(input_file, 'r') as file:
        lines = [line.strip() for line in file if line.strip()]
        for line in lines:
            # Parse positions and velocities
            parts = line.strip().split()
            p_part = parts[0].split('=')[1]
            v_part = parts[1].split('=')[1]
            px, py = map(int, p_part.split(','))
            vx, vy = map(int, v_part.split(','))
            robots.append({
                'position': (px, py),
                'velocity': (vx, vy)
            })
    return robots

# Simulate robots for Part 1
def simulate_robots(robots, seconds):
    positions = defaultdict(int)
    for robot in robots:
        px, py = robot['position']
        vx, vy = robot['velocity']
        # Calculate new position after 'seconds' time steps with wrapping
        nx = (px + vx * seconds) % GRID_WIDTH
        ny = (py + vy * seconds) % GRID_HEIGHT
        positions[(nx, ny)] += 1
    return positions

# Calculate safety factor for Part 1
def calculate_safety_factor(positions):
    # Initialize quadrants
    quadrant_counts = [0, 0, 0, 0]
    for (x, y), count in positions.items():
        if x == GRID_WIDTH // 2 or y == GRID_HEIGHT // 2:
            continue  # Exclude robots in the middle
        if x < GRID_WIDTH // 2 and y < GRID_HEIGHT // 2:
            quadrant_counts[0] += count  # Top-left quadrant
        elif x >= GRID_WIDTH // 2 and y < GRID_HEIGHT // 2:
            quadrant_counts[1] += count  # Top-right quadrant
        elif x < GRID_WIDTH // 2 and y >= GRID_HEIGHT // 2:
            quadrant_counts[2] += count  # Bottom-left quadrant
        elif x >= GRID_WIDTH // 2 and y >= GRID_HEIGHT // 2:
            quadrant_counts[3] += count  # Bottom-right quadrant
    # Calculate the product of robot counts in all quadrants
    safety_factor = 1
    for count in quadrant_counts:
        safety_factor *= count
    return safety_factor

# Find time until all positions are distinct for Part 2
def find_time_until_positions_unique(robots):
    positions = [robot['position'] for robot in robots]
    velocities = [robot['velocity'] for robot in robots]
    x_max = GRID_WIDTH
    y_max = GRID_HEIGHT
    T = 0
    while True:
        distinct_positions = set(positions)
        if len(distinct_positions) == len(positions):
            break  # All positions are unique
        # Update positions
        for i in range(len(positions)):
            px, py = positions[i]
            vx, vy = velocities[i]
            positions[i] = ((px + vx) % x_max, (py + vy) % y_max)
        T += 1
    return T

if __name__ == "__main__":
    input_file = "Day_14/day14_input.txt"

    # Parse input
    robots = parse_input(input_file)

    # Part 1: Simulate for 100 seconds
    positions_after_100 = simulate_robots(robots, 100)
    safety_factor = calculate_safety_factor(positions_after_100)
    print(f"Safety Factor after 100 seconds: {safety_factor}")

    # Part 2: Find time until all positions are distinct
    time_to_unique = find_time_until_positions_unique(robots)
    print(f"Time until all positions are distinct: {time_to_unique}")