import json
from datetime import datetime
import os


def add_to_json(new_data, filename='data.json'):
    root = os.path.dirname(__file__)
    with open(os.path.join(root, filename), 'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data[f"{datetime.timestamp(datetime.now())}"] = new_data
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=4)


def load_json(filename='data.json'):
    root = os.path.dirname(__file__)
    with open(os.path.join(root, filename), 'r') as file:
        return json.load(file)


def date(ts):
    return datetime.fromtimestamp(ts)
