import json
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Load the JSON data
with open("locations.json", "r") as file:
    data = json.load(file)

# Extract canonical names
canonical_names = [location["canonical_name"] for location in data]


# Function to find closest match
def find_closest_match(user_input):
    return process.extractOne(user_input, canonical_names)[0]
