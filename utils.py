import json
import os

def save_materials_to_json(materials, filepath):
    """
    Save a list of materials to a JSON file.

    Args:
        materials (list): A list of material dictionaries to save.
        filepath (str): The path to the JSON file where materials will be saved.

    Raises:
        ValueError: If materials is not a list or if it's empty.
        IOError: If there is an error writing to the file.
    """
    if not isinstance(materials, list):
        raise ValueError("Materials must be a list.")
    
    if not materials:
        raise ValueError("Materials list cannot be empty.")
    
    try:
        with open(filepath, 'w') as json_file:
            json.dump(materials, json_file, indent=4)
    except IOError as e:
        raise IOError(f"Failed to write to file {filepath}: {e}")

def load_materials_from_json(filepath):
    """
    Load materials from a JSON file.

    Args:
        filepath (str): The path to the JSON file from which materials will be loaded.

    Returns:
        list: A list of materials.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file is not valid JSON.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"The file {filepath} does not exist.")
    
    try:
        with open(filepath, 'r') as json_file:
            materials = json.load(json_file)
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Error decoding JSON from file {filepath}: {e.msg}", e.doc, e.pos)
    
    return materials

# TODO: Add functionality to validate material structures before saving
# TODO: Implement a function to merge materials from multiple JSON files
