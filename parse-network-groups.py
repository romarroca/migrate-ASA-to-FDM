import json

def summarize_object_groups(groups):
    print("\nSummarized Network Object Groups:")
    print("================================")
    print(f"Total Object Groups: {len(groups)}")
    for group in groups:
        print(f"Object Group Name: {group['name']}")
        print(f"  - Number of Objects: {len(group['objects'])}")
    print("================================\n")

# Prompt the user for the name of the text file to read
file_name = input("Enter the name of the ASA configuration text file: ")

# Read ASA configuration objects from the specified text file
with open(file_name, "r") as file:
    lines = file.readlines()

# Initialize variables
asa_object_groups = []
current_group = None

# Process each line in the file
for line in lines:
    line = line.strip()

    if line.startswith("object-group network"):
        # If we encounter a new object-group, we finish the current one and start a new one
        if current_group:
            asa_object_groups.append(current_group)
        current_group = {
            "name": line.split()[2],
            "description": None,
            "isSystemDefined": False,
            "objects": [],
            "type": "networkobjectgroup"
        }
    elif line.startswith("network-object object"):
        if current_group:  # Assuming we're inside a network object group
            member_name = line.split()[2]
            member_object = {
                "name": member_name,
                "type": "networkobject"
            }
            current_group["objects"].append(member_object)

# Add the last object group if it exists
if current_group:
    asa_object_groups.append(current_group)

# Show summary before saving
summarize_object_groups(asa_object_groups)

# Ask the user if they want to save
choice = input("Do you want to save the parsed object groups to JSON? (yes/no): ").lower()
if choice == "yes":
    json_filename = "output_objects_network_groups.json"
    with open(json_filename, "w") as json_file:
        json.dump(asa_object_groups, json_file, indent=4)
    print(f"\nASA object groups converted to JSON and stored in {json_filename}")
else:
    print("\nNo JSON file was created.")
