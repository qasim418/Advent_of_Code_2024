def can_segment(design, patterns, memo):
    if design in memo:
        return memo[design]
    if not design:
        return True
    for pattern in patterns:
        if design.startswith(pattern):
            if can_segment(design[len(pattern):], patterns, memo):
                memo[design] = True
                return True
    memo[design] = False
    return False

def count_ways(design, patterns, memo):
    if design in memo:
        return memo[design]
    if not design:
        return 1
    total = 0
    for pattern in patterns:
        if design.startswith(pattern):
            total += count_ways(design[len(pattern):], patterns, memo)
    memo[design] = total
    return total

def main():
    try:
        with open('Day_19/day19_input.txt', 'r') as file:
            lines = [line.strip() for line in file]
    except FileNotFoundError:
        print("Possible Designs: 0")
        print("Total Ways: 0")
        return

    if not lines:
        print("Possible Designs: 0")
        print("Total Ways: 0")
        return

    # Split patterns
    patterns_line = lines[0]
    patterns = [p.strip() for p in patterns_line.split(',') if p.strip()]
    if not patterns:
        print("Possible Designs: 0")
        print("Total Ways: 0")
        return

    # Find index of first blank line
    try:
        blank_index = lines.index('')
    except ValueError:
        blank_index = 1

    # Remaining lines are designs
    designs = lines[blank_index+1:] if blank_index+1 < len(lines) else []
    if not designs:
        print("Possible Designs: 0")
        print("Total Ways: 0")
        return

    possible_designs = 0
    total_ways = 0
    for design in designs:
        if not design:
            continue
        ways = count_ways(design, patterns, {})
        if ways > 0:
            possible_designs +=1
            total_ways += ways

    print(f"Possible Designs: {possible_designs}")
    print(f"Total Ways: {total_ways}")

if __name__ == "__main__":
    main()
