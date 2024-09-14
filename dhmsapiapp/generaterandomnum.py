import random

def generate_unique_number():
    # Generate a random 8-digit number
    number = random.randint(10000000, 99999999)
    return number

# # Example usage
# unique_number = generate_unique_number()
# print(f"Unique 8-digit number: {unique_number}")
