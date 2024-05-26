import json
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Load the JSON data
with open("locations.json", "r") as file:
    data = json.load(file)

# Extract canonical names
canonical_names = [location["canonical_name"] for location in data]


# Function to find closest match
def find_closest_match(user_input: str) -> str:
    """
    Find the closest match to the user input from the list of canonical names using fuzzy matching.

    Args:
        user_input (str): The user entered location name.

    Returns:
        str: The closest match to the user input supported by SerpApi.
    """
    return process.extractOne(user_input, canonical_names)[0]
