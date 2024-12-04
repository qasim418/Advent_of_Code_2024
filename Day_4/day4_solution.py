# Read the grid from the input file
with open('Day_4/day4_input.txt') as f:
    grid = [list(line.strip()) for line in f]

rows = len(grid)
cols = len(grid[0])
word = "XMAS"
word_len = len(word)
count_part1 = 0

# Directions: N, NE, E, SE, S, SW, W, NW
directions = [(-1, 0),  (-1, 1), (0, 1),  (1, 1),
              (1, 0),   (1, -1), (0, -1), (-1, -1)]

# Part One: Find all occurrences of "XMAS"
for i in range(rows):
    for j in range(cols):
        for dx, dy in directions:
            x, y = i, j
            match = True
            for k in range(word_len):
                if 0 <= x < rows and 0 <= y < cols and grid[x][y] == word[k]:
                    x += dx
                    y += dy
                else:
                    match = False
                    break
            if match:
                count_part1 += 1

print("Part One - Total occurrences of XMAS:", count_part1)

# Part Two: Find all occurrences of X-shaped patterns made by two "MAS"
def check_x_mas(i, j):
    # Possible variations of "MAS" and "SAM"
    mas_variations = ["MAS", "SAM"]
    count = 0
    # Check all combinations of diagonals
    for diag1 in mas_variations:
        for diag2 in mas_variations:
            match = True
            # First diagonal (\)
            for k in range(3):
                x = i - 1 + k
                y = j - 1 + k
                if not (0 <= x < rows and 0 <= y < cols and grid[x][y] == diag1[k]):
                    match = False
                    break
            if not match:
                continue
            # Second diagonal (/)
            for k in range(3):
                x = i - 1 + k
                y = j + 1 - k
                if not (0 <= x < rows and 0 <= y < cols and grid[x][y] == diag2[k]):
                    match = False
                    break
            if match:
                count += 1
    return count

count_part2 = 0

# Since the 'X' is 3x3, we need to avoid edges
for i in range(1, rows - 1):
    for j in range(1, cols - 1):
        count_part2 += check_x_mas(i, j)

print("Part Two - Total occurrences of X-MAS:", count_part2)