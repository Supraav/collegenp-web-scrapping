import json

# Load the JSON file
with open('final_collegenp.json') as file:
    data = json.load(file)

# Count the total number of entries
total_entries = len(data)

# Print the result
print("Total number of entries:", total_entries)
