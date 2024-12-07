def evaluate_expression(numbers, operators):
    """Evaluate expression left to right with given numbers and operators"""
    result = numbers[0]
    for i, op in enumerate(operators):
        if op == '+':
            result += numbers[i + 1]
        elif op == '*':
            result *= numbers[i + 1]
        else:  # op == '||'
            result = int(str(result) + str(numbers[i + 1]))
    return result

def generate_operator_combinations(n, include_concat=False):
    """Generate all possible combinations of operators for n positions"""
    operators = ['+', '*'] if not include_concat else ['+', '*', '||']
    from itertools import product
    return product(operators, repeat=n)  # More efficient than recursion

def can_equation_be_true(test_value, numbers, include_concat=False):
    """Check if equation can be made true with any operator combination"""
    num_operators = len(numbers) - 1
    for operators in generate_operator_combinations(num_operators, include_concat):
        try:
            result = evaluate_expression(numbers, operators)
            if result == test_value:
                return True
        except:
            continue
    return False

# Read and parse input
equations = []
with open('Day_7/day7_input.txt', 'r') as f:
    for line in f:
        test_value, numbers = line.strip().split(': ')
        test_value = int(test_value)
        numbers = [int(x) for x in numbers.split()]
        equations.append((test_value, numbers))

# Process each equation for both parts
total_part1 = 0
total_part2 = 0

# Add progress tracking
total_equations = len(equations)
for idx, (test_value, numbers) in enumerate(equations, 1):
    print(f"Processing equation {idx}/{total_equations}: {test_value}: {numbers}")
    
    # Part 1: Only + and *
    if can_equation_be_true(test_value, numbers, False):
        total_part1 += test_value
        print(f"Valid for Part 1: {test_value}")
    
    # Part 2: Include concatenation
    if can_equation_be_true(test_value, numbers, True):
        total_part2 += test_value
        print(f"Valid for Part 2: {test_value}")

print(f"\nPart 1 - Total calibration result (+ and * only): {total_part1}")
print(f"Part 2 - Total calibration result (with concatenation): {total_part2}")