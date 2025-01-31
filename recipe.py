import hashlib
from collections import defaultdict
import Levenshtein


# Define a function to calculate hash
def calculate_hash(ingredient, quantity, unit):
    data = f"{ingredient}{quantity}{unit}"
    return hashlib.md5(data.encode()).hexdigest()

# Define two recipes with multiple ingredients, including duplicates
recipe1 = [
    ("Flour", 150, "grams", calculate_hash("Flour", 150, "grams")),
    ("Sugar", 100, "grams", calculate_hash("Sugar", 100, "grams")),
    ("Sugar", 100, "grams", calculate_hash("Sugar", 100, "grams")),
    ("Eggs", 2, "pieces", calculate_hash("Eggs", 2, "pieces")),
    ("Milk", 250, "ml", calculate_hash("Milk", 250, "ml")),
    ("Butter", 50, "grams", calculate_hash("Butter", 50, "grams")),
    ("Sugar", 100, "grams", calculate_hash("Sugar", 100, "grams")),
    ("Eggs", 2, "pieces", calculate_hash("Eggs", 2, "pieces"))
]

recipe2 = [
    ("Flour", 150, "grams", calculate_hash("Flour", 150, "grams")),
    ("Sugar", 100, "grams", calculate_hash("Sugar", 100, "grams")),
    ("Eggs", 3, "pieces", calculate_hash("Eggs", 3, "pieces")),
    ("Milk", 200, "ml", calculate_hash("Milk", 200, "ml")),
    ("Cocoa Powder", 50, "grams", calculate_hash("Cocoa Powder", 50, "grams")),
    ("Vanilla Extract", 1, "tsp", calculate_hash("Vanilla Extract", 1, "tsp")),
    ("Flour", 150, "grams", calculate_hash("Flour", 150, "grams"))
]

# Function to print recipes
def print_recipe(recipe, recipe_name):
    print(f"{recipe_name}:")
    for ingredient, quantity, unit, hash_value in recipe:
        print(f"- {ingredient}: {quantity} {unit} (Hash: {hash_value})")
    print()

# Function to remove duplicate pairs based on matching hashes
def remove_duplicate_pairs(recipe1, recipe2):
    # Create defaultdicts to track occurrences of each hash in both recipes
    recipe1_hashes = defaultdict(list)
    recipe2_hashes = defaultdict(list)

    # Fill the hash maps with the indices of matching ingredients
    for i, item in enumerate(recipe1):
        recipe1_hashes[item[3]].append(i)

    for i, item in enumerate(recipe2):
        recipe2_hashes[item[3]].append(i)

    # Process recipe1 and remove pairs found in recipe2
    to_remove_recipe1 = set()
    to_remove_recipe2 = set()

    # Remove matching ingredients from recipe1 and recipe2
    for hash_value in list(recipe1_hashes):
        if hash_value in recipe2_hashes:
            # Remove one occurrence from both recipes
            if recipe1_hashes[hash_value] and recipe2_hashes[hash_value]:
                to_remove_recipe1.add(recipe1_hashes[hash_value].pop(0))  # Remove one from recipe1
                to_remove_recipe2.add(recipe2_hashes[hash_value].pop(0))  # Remove one from recipe2

    # Remove the marked items from both recipes
    recipe1 = [item for i, item in enumerate(recipe1) if i not in to_remove_recipe1]
    recipe2 = [item for i, item in enumerate(recipe2) if i not in to_remove_recipe2]

    return recipe1, recipe2


# Remove duplicate pairs based on matching hashes
recipe1, recipe2 = remove_duplicate_pairs(recipe1, recipe2)

# Print the cleaned recipes
print("After removing duplicate pairs across recipes:")
print_recipe(recipe1, "Recipe 1")
print_recipe(recipe2, "Recipe 2")

# Extract ingredient details (name, quantity, and unit) from recipes
recipe1_details = [(ingredient, quantity, unit) for ingredient, quantity, unit, _ in recipe1]
recipe2_details = [(ingredient, quantity, unit) for ingredient, quantity, unit, _ in recipe2]


# Function to calculate weighted Levenshtein distance between ingredient, quantity, and unit
def weighted_levenshtein(ingredient1, ingredient2, quantity1, quantity2, unit1, unit2, ingredient_weight=1, quantity_weight=0.5, unit_weight=0.2):
    # Levenshtein distance for ingredient name
    ingredient_distance = Levenshtein.distance(ingredient1, ingredient2) * ingredient_weight
    # Levenshtein distance for quantity (as string comparison)
    quantity_distance = Levenshtein.distance(str(quantity1), str(quantity2)) * quantity_weight
    # Levenshtein distance for unit
    unit_distance = Levenshtein.distance(unit1, unit2) * unit_weight

    # Total weighted distance
    return ingredient_distance + quantity_distance + unit_distance

# Calculate weighted Levenshtein distance between recipe1 and recipe2
def calculate_weighted_levenshtein_distance(list1, list2, ingredient_weight=1, quantity_weight=0.5, unit_weight=0.2):
    total_distance = 0
    for ingredient1, quantity1, unit1 in list1:
        # Find closest match for ingredient in recipe2
        closest_match = min(list2, key=lambda x: weighted_levenshtein(ingredient1, x[0], quantity1, x[1], unit1, x[2], ingredient_weight, quantity_weight, unit_weight))
        ingredient2, quantity2, unit2 = closest_match
        # Calculate the distance for the matched pair
        total_distance += weighted_levenshtein(ingredient1, ingredient2, quantity1, quantity2, unit1, unit2, ingredient_weight, quantity_weight, unit_weight)

    return total_distance

# Calculate and print the weighted Levenshtein distance
ingredient_weight = 1  # Weight for ingredient name
quantity_weight = 0.5  # Weight for quantity
unit_weight = 0.2      # Weight for unit

distance = calculate_weighted_levenshtein_distance(recipe1_details, recipe2_details, ingredient_weight, quantity_weight, unit_weight)
print(f"Weighted Levenshtein distance between ingredients (name, quantity, and unit) from Recipe 1 and Recipe 2: {distance}")