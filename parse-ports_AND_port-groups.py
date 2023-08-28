import re
import json

COMMON_PORTS = {
    "HTTPS": "443",
    "WWW": "80",
    "NTP": "123",
    "DOMAIN": "53",
    "RTSP": "554",
    "SIP": "5060"
}

def get_port_name_and_value(protocol, port):
    port = port.strip().upper()  # Remove any leading or trailing spaces and make uppercase
    port_value = COMMON_PORTS.get(port, port)
    port_name = f"{protocol.upper()}_{port_value}"
    return port_name, port_value



def parse_asa_config(filename):
    parsed_data = []
    
    service_pattern = re.compile(r'object-group service (\S+) (\S+)')
    port_object_pattern = re.compile(r'port-object (eq (\S+)|range (\S+) (\S+))')
    
    with open(filename, 'r') as file:
        lines = file.readlines()
        
        protocol_type = None
        for line in lines:
            line = line.strip()
            
            match = service_pattern.match(line)
            if match:
                protocol_type = match.group(2)
                continue
            
            match = port_object_pattern.match(line)
            if match and protocol_type:
                if "eq" in match.group(1):
                    port = match.group(2)
                    name, port_value = get_port_name_and_value(protocol_type, port)
                    parsed_data.append({
                        "name": name,
                        "description": name,
                        "type": f"{protocol_type}portobject",
                        "port": port_value
                    })

                else:
                    start_port, end_port = match.group(3), match.group(4)
                    name = f"PORT-RANGE_{start_port}-{end_port}"
                    parsed_data.append({
                        "name": name,
                        "description": name,
                        "type": f"{protocol_type}portobject",
                        "port": f"{start_port}-{end_port}"
                    })

    return parsed_data

def parse_asa_config_group(filename, objects_filename):
    groups = []

    service_pattern = re.compile(r'object-group service (\S+) (\S+)')
    port_object_pattern = re.compile(r'port-object (eq (\S+)|range (\S+) (\S+))')

    with open(objects_filename, 'r') as file:
        objects_data = json.load(file)

    with open(filename, 'r') as file:
        lines = file.readlines()
        group = None
        protocol_type = None

        for line in lines:
            line = line.strip()

            match = service_pattern.match(line)
            if match:
                if group:
                    groups.append(group)
                protocol_type = match.group(2)
                group = {
                    "name": match.group(1),
                    "description": match.group(1),
                    "type": "portobjectgroup",
                    "objects": []
                }
                continue

            match = port_object_pattern.match(line)
            if match and group:
                port = match.group(2) if "eq" in match.group(1) else f"{match.group(3)}-{match.group(4)}"
                port_obj = next((obj for obj in objects_data if obj["port"] == port and obj["type"].startswith(protocol_type)), None)
                if port_obj:
                    group["objects"].append({
                        "name": port_obj["name"],
                        "type": port_obj["type"]
                    })
                else:
                    port_name, _ = get_port_name_and_value(protocol_type, port)
                    group["objects"].append({
                        "name": port_name,
                        "type": f"{protocol_type}portobject"
                    })

        if group:
            groups.append(group)

    return groups

def main():
    input_file = input("Enter the filename of the ASA configuration text: ")

    objects = parse_asa_config(input_file)
    print("\nParsed Port Objects:")
    for obj in objects:
        print(f"Name: {obj['name']}, Port: {obj['port']}")
    proceed = input("\nDo you want to proceed with converting to JSON? (yes/no): ").lower()
    
    if proceed == "yes":
        with open("output_ports.json", 'w') as outfile:
            json.dump(objects, outfile, indent=4)

        group_data = parse_asa_config_group(input_file, 'output_ports.json')
        print("\nParsed Port Object Groups:")
        for group in group_data:
            print(f"Name: {group['name']}, Objects: {', '.join([obj['name'] for obj in group['objects']])}")
        proceed_group = input("\nDo you want to proceed with writing the port object groups to JSON? (yes/no): ").lower()
        
        if proceed_group == "yes":
            with open("output_group_ports.json", 'w') as outfile:
                json.dump(group_data, outfile, indent=4)
            print("\nSuccessfully created output_ports.json and output_group_ports.json!")
        else:
            print("\nOperation aborted for port object groups.")
    else:
        print("\nOperation aborted.")

if __name__ == "__main__":
    main()
