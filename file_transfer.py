import json
import csv

# Path to the JSON file
json_file_path = 'data.json'

# Path to the CSV file to be created
csv_file_path = 'data.csv'

field_names = set()

# Open the JSON file and load its contents
with open(json_file_path) as json_file:
    data = json.load(json_file)

    # Iterate over each JSON object
    for entry in data:
        # Collect the field names
        field_names.update(entry.keys())

# Open the JSON file and load its contents
with open(json_file_path) as json_file:
    data = json.load(json_file)

# Open the CSV file and write the data
with open(csv_file_path, 'w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=field_names)

    # Write the header row
    writer.writeheader()

    # Iterate over each JSON object and write as CSV rows
    for entry in data:
        writer.writerow(entry)
