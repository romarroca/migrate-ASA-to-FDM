import json
import ipaddress

def format_name(name):
    """Format the name by replacing special characters with underscores."""
    return name.replace(":", "_")

# Prompt the user for the name of the text file to read
file_name = input("Enter the name of the ASA configuration text file: ")

# Read ASA configuration objects from the specified text file
with open(file_name, "r") as file:
    lines = file.readlines()

# Initialize variables
asa_objects = []
current_object = None

# Process each line in the file
for line in lines:
    line = line.strip()

    if line.startswith("object network"):
        name = format_name(line.split()[2])
        if current_object:
            asa_objects.append(current_object)
        current_object = {
            "name": name,
            "type": "networkobject",
            "description": name  # default description
        }
    elif line.startswith("object service"):
        name = format_name(line.split()[2])
        if current_object:
            asa_objects.append(current_object)
        current_object = {
            "name": name,
            "description": name  # default description
        }
    elif line.startswith("service tcp"):
        _, _, _, _, port = line.split()
        current_object["type"] = "tcpportobject"
        current_object["port"] = port
    elif line.startswith("service udp"):
        _, _, _, _, port = line.split()
        current_object["type"] = "udpportobject"
        current_object["port"] = port
    elif line.startswith("subnet"):
        _, subnet_ip, subnet_mask = line.split()
        subnet_prefix = ipaddress.IPv4Network(f"{subnet_ip}/{subnet_mask}", strict=False).prefixlen
        current_object["subType"] = "NETWORK"
        current_object["value"] = f"{subnet_ip}/{subnet_prefix}"
    elif line.startswith("host"):
        _, host_ip = line.split()
        current_object["subType"] = "HOST"
        current_object["value"] = host_ip
    elif line.startswith("fqdn"):
        _, _, fqdn_value = line.split()
        current_object["subType"] = "FQDN"
        current_object["value"] = fqdn_value
    elif line.startswith("range"):
        _, start_ip, end_ip = line.split()
        current_object["subType"] = "RANGE"
        current_object["value"] = f"{start_ip}-{end_ip}"
    elif line.startswith("description"):
        description = line[len("description "):]
        current_object["description"] = description if description else current_object["name"]

# Add the last object
if current_object:
    asa_objects.append(current_object)

# Print the objects read from the file
print("\nObjects read from the file:")
for obj in asa_objects:
    if obj.get('type') == "networkobject":
        print(f"SubType: {obj.get('subType')}, Name: {obj['name']}, Description: {obj.get('description', 'none')}")
    else:  # tcpportobject or udpportobject
        print(f"Type: {obj.get('type')}, Name: {obj['name']}, Port: {obj.get('port')}, Description: {obj.get('description', 'none')}")

# Ask the user to convert to JSON or exit
while True:
    choice = input("\nDo you want to convert the objects to JSON? (yes/no): ").lower()
    if choice == "yes":
        # Write ASA objects in JSON format to a file
        with open("output_objects_network.json", "w") as json_file:
            json.dump(asa_objects, json_file, indent=4)
        
        print("ASA objects converted to JSON and stored in output_objects_network.json")
        break
    elif choice == "no":
        print("Exiting the script.")
        break
    else:
        print("Invalid choice. Please enter 'yes' or 'no'.")
