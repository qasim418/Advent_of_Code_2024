from functools import cache
from typing import List, Tuple

# Define the numeric keypad layout
NUMERIC_KEYPAD = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    [None, "0", "A"],
]

# Define the directional keypad layout
DIRECTIONAL_KEYPAD = [
    [None, "^", "A"],
    ["<", "v", ">"]
]

def read_input(file_path: str) -> List[str]:
    """
    Reads input from a file and returns a list of codes.
    Each code is expected to be on a separate line.
    """
    try:
        with open(file_path, "r") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []

def get_pos(arr: List[List[str]], code: str) -> Tuple[int, int]:
    """
    Returns the (row, column) position of the given code on the keypad.
    """
    for i, row in enumerate(arr):
        if code in row:
            return (i, row.index(code))
    raise ValueError(f"Code '{code}' not found on the keypad.")

@cache
def shortest(start: Tuple[int, int], end: Tuple[int, int], layers: int) -> int:
    """
    Recursively calculates the shortest sequence of button presses
    from start to end across the specified number of layers.
    """
    if layers == 0:
        return 1  # Only 'A' press needed at the numeric keypad layer

    # Determine movement directions
    vert = None
    hori = None
    if end[0] < start[0]:
        vert = "^"
    elif end[0] > start[0]:
        vert = "v"
    if end[1] < start[1]:
        hori = "<"
    elif end[1] > start[1]:
        hori = ">"

    # No movement needed, just press 'A'
    if not hori and not vert:
        return shortest(get_pos(DIRECTIONAL_KEYPAD, "A"), get_pos(DIRECTIONAL_KEYPAD, "A"), layers - 1)

    sequences = []

    if hori:
        # Move horizontally first
        sequences.append(
            shortest(get_pos(DIRECTIONAL_KEYPAD, "A"), get_pos(DIRECTIONAL_KEYPAD, hori), layers - 1) +
            (abs(end[1] - start[1]) - 1) * shortest(get_pos(DIRECTIONAL_KEYPAD, hori), get_pos(DIRECTIONAL_KEYPAD, hori), layers - 1) +
            shortest(get_pos(DIRECTIONAL_KEYPAD, hori), get_pos(DIRECTIONAL_KEYPAD, "A"), layers - 1)
        )

    if vert:
        # Move vertically first
        sequences.append(
            shortest(get_pos(DIRECTIONAL_KEYPAD, "A"), get_pos(DIRECTIONAL_KEYPAD, vert), layers - 1) +
            (abs(end[0] - start[0]) - 1) * shortest(get_pos(DIRECTIONAL_KEYPAD, vert), get_pos(DIRECTIONAL_KEYPAD, vert), layers - 1) +
            shortest(get_pos(DIRECTIONAL_KEYPAD, vert), get_pos(DIRECTIONAL_KEYPAD, "A"), layers - 1)
        )

    return min(sequences) if sequences else float('inf')

def compute_sequence_length(code: str, layers: int) -> int:
    """
    Computes the total sequence length to type the given code
    across the specified number of layers.
    """
    total_presses = 0
    current_button = "A"  # Start at 'A' on the topmost directional keypad

    for char in code:
        if char not in [button for row in NUMERIC_KEYPAD for button in row if button]:
            print(f"Warning: Invalid character '{char}' in code '{code}'. Skipping.")
            continue

        # Get positions on the numeric keypad
        start_pos = get_pos(NUMERIC_KEYPAD, current_button)
        end_pos = get_pos(NUMERIC_KEYPAD, char)

        # Calculate the number of button presses to move from current to end
        presses = shortest(start_pos, end_pos, layers)
        total_presses += presses
        current_button = char  # Move to the next button

    return total_presses

def compute_total_complexity(codes: List[str], layers: int) -> int:
    """
    Computes the total complexity for a list of codes based on the number of layers.
    """
    total_complexity = 0
    for code in codes:
        # Extract numeric part (ignore leading zeros and 'A')
        numeric_part_str = ''.join(filter(str.isdigit, code))
        numeric_part = int(numeric_part_str.lstrip('0') or '0')

        # Compute the sequence length
        sequence_length = compute_sequence_length(code, layers)

        # Compute complexity
        complexity = sequence_length * numeric_part

        print(f"Code: {code}, Sequence Length: {sequence_length}, Numeric Part: {numeric_part}, Complexity: {complexity}")
        total_complexity += complexity

    return total_complexity

def main():
    # Replace this with the path to your input file
    file_path = "Day_21/day21_input.txt"

    # Read input codes from the file
    input_codes = read_input(file_path)

    if not input_codes:
        # If input file is not found or empty, use the example input
        print("Using example input:")
        input_codes = [
            "029A",
            "980A",
            "179A",
            "456A",
            "379A"
        ]
        for code in input_codes:
            print(code)
        print()

    # Part One: 3 layers
    print("----- Part One: 3 Layers -----")
    layers_part_one = 3
    total_complexity_part_one = compute_total_complexity(input_codes, layers_part_one)
    print(f"Total Complexity (Part One, Layers={layers_part_one}): {total_complexity_part_one}\n")

    # Part Two: 27 layers (1 user + 25 robots + 1 numeric keypad)
    print("----- Part Two: 27 Layers -----")
    layers_part_two = 27
    total_complexity_part_two = compute_total_complexity(input_codes, layers_part_two)
    print(f"Total Complexity (Part Two, Layers={layers_part_two}): {total_complexity_part_two}")

if __name__ == "__main__":
    main()
