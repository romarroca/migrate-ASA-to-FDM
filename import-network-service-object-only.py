import requests
import json
import warnings
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single InsecureRequestWarning from urllib3
warnings.simplefilter('ignore', InsecureRequestWarning)

# FDM API details
FDM_HOST = "https://192.168.8.69"
FDM_USERNAME = "admin"
FDM_PASSWORD = "P@ssw0rd"
AUTH_ENDPOINT = "/api/fdm/v6/fdm/token"
HEADERS = {
    'Content-Type': 'application/json'
}

# Authenticate and get access token
data = {
    'grant_type': 'password',
    'username': FDM_USERNAME,
    'password': FDM_PASSWORD
}

response = requests.post(FDM_HOST + AUTH_ENDPOINT, headers=HEADERS, data=json.dumps(data), verify=False)  # Note: verify=False ignores SSL errors
response_data = response.json()
access_token = response_data['access_token']

# Update headers for further requests
HEADERS['Authorization'] = 'Bearer ' + access_token

# Ask the user for the name of the JSON file to read
file_name = input("Enter the name of the JSON file with ASA objects: ")

# Parse the provided ASA objects JSON file
with open(file_name, "r") as file:
    asa_objects = json.load(file)

# Keep track of added objects for potential deletion
added_objects = []

# Push objects to FDM API
for obj in asa_objects:
    if obj["type"] == "networkobject":
        endpoint = "/api/fdm/v6/object/networks"
    elif obj["type"] == "tcpportobject":
        endpoint = "/api/fdm/v6/object/tcpports"
    elif obj["type"] == "udpportobject":
        endpoint = "/api/fdm/v6/object/udpports"
    elif obj["type"] == "networkobjectgroup":
        endpoint = "/api/fdm/v6/object/networkgroups"
    elif obj["type"] == "portobjectgroup":
        endpoint = "/api/fdm/v6/object/portgroups"
    else:
        print(f"Unknown object type {obj['type']} for {obj['name']}. Skipping...")
        continue

    # Send the object data to the determined endpoint
    response = requests.post(FDM_HOST + endpoint, headers=HEADERS, data=json.dumps(obj), verify=False)

    if response.status_code == 200 or response.status_code == 201:
        print(f"Object {obj['name']} added successfully!")
        added_objects.append({"id": response.json()["id"], "endpoint": endpoint})
    else:
        print(f"Failed to add object {obj['name']}. Status code: {response.status_code}. Response: {response.text}")

# Ask the user if they want to remove added objects
choice = input("\nDo you want to remove the added objects? (yes/no): ").lower()
if choice == "yes":
    for added_obj in added_objects:
        response = requests.delete(FDM_HOST + added_obj["endpoint"] + "/" + added_obj["id"], headers=HEADERS, verify=False)
        if response.status_code == 200:
            print(f"Object with ID {added_obj['id']} removed successfully!")
        else:
            print(f"Failed to remove object with ID {added_obj['id']}. Status code: {response.status_code}. Response: {response.text}")

print("Bbye! You can review the objects and deploy manually or use the deploy.py")
