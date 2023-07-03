import json

with open('schoollinks.json') as file:
    data = json.load(file)

# Convert the list to a set to remove duplicates
unique_values = list(set(data))

with open('uni_schoollinks.json', 'w') as file:
    json.dump(unique_values, file,indent=3)