import hashlib
import Levenshtein

# Define a function to calculate hash
def calculate_hash(ingredient, quantity, unit):
    data = f"{ingredient}{quantity}{unit}"
    return hashlib.md5(data.encode()).hexdigest()

# Define two recipes with multiple ingredients, including duplicates
recipe1 = [
    ("Sugar", 100, "grams", calculate_hash("Sugar", 100, "grams")),
    ("Eggs", 2, "pieces", calculate_hash("Eggs", 2, "pieces")),
    ("Milk", 250, "ml", calculate_hash("Milk", 250, "ml")),
    ("Butter", 50, "grams", calculate_hash("Butter", 50, "grams")),
    ("Sugar", 100, "grams", calculate_hash("Sugar", 100, "grams")),
    ("Eggs", 2, "pieces", calculate_hash("Eggs", 2, "pieces"))
]

recipe2 = [
    ("Eggs", 3, "pieces", calculate_hash("Eggs", 3, "pieces")),
    ("Milk", 200, "ml", calculate_hash("Milk", 200, "ml")),
    ("Cocoa Powder", 50, "grams", calculate_hash("Cocoa Powder", 50, "grams")),
    ("Vanilla Extract", 1, "tsp", calculate_hash("Vanilla Extract", 1, "tsp")),
    ("Flour", 150, "grams", calculate_hash("Flour", 150, "grams"))
]

# Extract ingredient details (name, quantity, and unit) from recipes
recipe1_details = [f"{ingredient} {quantity} {unit}" for ingredient, quantity, unit, _ in recipe1]
recipe2_details = [f"{ingredient} {quantity} {unit}" for ingredient, quantity, unit, _ in recipe2]

# Custom implementation of Levenshtein distance with custom weights
def weighted_levenshtein(str1, str2, delete_weight=1, insert_weight=1, substitute_weight=1):
    len_str1 = len(str1)
    len_str2 = len(str2)

    # Create a distance matrix
    matrix = [[0] * (len_str2 + 1) for _ in range(len_str1 + 1)]

    # Initialize the base cases
    for i in range(len_str1 + 1):
        matrix[i][0] = i * delete_weight
    for j in range(len_str2 + 1):
        matrix[0][j] = j * insert_weight

    # Fill in the matrix
    for i in range(1, len_str1 + 1):
        for j in range(1, len_str2 + 1):
            cost = 0 if str1[i - 1] == str2[j - 1] else substitute_weight
            matrix[i][j] = min(
                matrix[i - 1][j] + delete_weight,  # Deletion
                matrix[i][j - 1] + insert_weight,  # Insertion
                matrix[i - 1][j - 1] + cost  # Substitution
            )

    return matrix[len_str1][len_str2]

# Function to calculate total weighted Levenshtein distance between two lists of ingredient details
def calculate_weighted_levenshtein_distance(list1, list2, delete_weight=1, insert_weight=1, substitute_weight=1):
    total_distance = 0
    for ingredient1 in list1:
        closest_match = min(list2, key=lambda x: weighted_levenshtein(ingredient1, x,
                                                                      delete_weight,
                                                                      insert_weight,
                                                                      substitute_weight))
        total_distance += weighted_levenshtein(ingredient1, closest_match,
                                               delete_weight,
                                               insert_weight,
                                               substitute_weight)
    return total_distance

# Calculate and print the Levenshtein distance based on ingredients, quantity, and unit with custom weights
delete_weight = 2  # Example weight for deletions
insert_weight = 1  # Example weight for insertions
substitute_weight = 3  # Example weight for substitutions

distance = calculate_weighted_levenshtein_distance(recipe1_details, recipe2_details,
                                                   delete_weight, insert_weight, substitute_weight)
print(f"Levenshtein distance between ingredients (name, quantity, and unit) from Recipe 1 and Recipe 2 with custom weights: {distance}")
