import json
import os
from student import Student

DEFAULT_DATA_FILE = os.path.join("data", "students.json")


def ensure_data_dir(filepath=DEFAULT_DATA_FILE):
    """Ensures the directory for the storage file exists."""
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)


def load_students(filepath=DEFAULT_DATA_FILE):
    """Loads student records from a JSON file. Handles missing or empty files gracefully."""
    ensure_data_dir(filepath)
    if not os.path.exists(filepath):
        save_students([], filepath)
        return []

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            raw_data = json.load(file)
            return [Student.from_dict(item) for item in raw_data]
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        print(f"[Warning] Could not parse '{filepath}' ({e}). Starting with an empty record list.")
        return []
    except OSError as e:
        print(f"[Error] File access error while loading data: {e}")
        return []


def save_students(students, filepath=DEFAULT_DATA_FILE):
    """Saves a list of Student objects to a JSON file."""
    ensure_data_dir(filepath)
    try:
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump([s.to_dict() for s in students], file, indent=4)
        return True
    except OSError as e:
        print(f"[Error] Failed to save student records: {e}")
        return False
