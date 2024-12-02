from collections import Counter

def calculate_total_distance(left_list, right_list):
    # Sort both lists
    left_sorted = sorted(left_list)
    right_sorted = sorted(right_list)
    
    # Calculate the total distance
    total_distance = sum(abs(l - r) for l, r in zip(left_sorted, right_sorted))
    return total_distance

def calculate_similarity_score(left_list, right_list):
    # Count the occurrences of each number in the right list
    right_count = Counter(right_list)
    
    # Calculate the similarity score
    similarity_score = sum(num * right_count[num] for num in left_list)
    return similarity_score

# Read the input lists from the file
with open("Day_1/day1_input.txt") as f:
    lines = [[int(i) for i in l.split()] for l in f]

# Split the input into two lists
left_list, right_list = zip(*lines)

# Part 1: Calculate the total distance
total_distance = calculate_total_distance(left_list, right_list)
print("Total Distance:", total_distance)

# Part 2: Calculate the similarity score
similarity_score = calculate_similarity_score(left_list, right_list)
print("Similarity Score:", similarity_score)