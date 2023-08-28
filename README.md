# migrate-objects-ASA-to-FDM

A not perfect script to migrate cisco ASA objects to FDM. Cisco does support migration from ASA to FDM using CDO. However, it will wipe the current configuration of the FDM. If you encounter migrating like really big lines of object groups, this tool might help.

## This tool is ideal for scenarios where:
- You have an existing FDM with some configurations and don't want to reset it.
- You wish to migrate objects in bulk from ASA to FDM without manual efforts.

## Disclaimer
This is more of a utility script developed for my specific needs. The code may not be polished or production-ready. I am not a coder or some python wizard and chatgpt help me create this tool for my needs. Hence, it is essential to:

- Not use this directly in a production environment.
- Always take backups before performing any operations.
- Thoroughly test in a lab environment to understand its effects.

Use this script at your own risk.

## Instructions
I should probably create a video on how I used it

- To not messed up your python, use python env
- ![image](https://github.com/romarroca/migrate-ASA-to-FDM/assets/87074019/f8b210ec-b73f-4f5c-afa7-31a349e2c720)

- supply the objects.txt or whatever the filename of the txt file containing objects that you want to process and this script will parse and convert all the network and ports objects.
- ![image](https://github.com/romarroca/migrate-ASA-to-FDM/assets/87074019/19014460-825a-46c6-9537-2e16b27d9d01)
- You can review the output files first.

- to upload it to FDM, makesure to change the following to your setup
- ![image](https://github.com/romarroca/migrate-ASA-to-FDM/assets/87074019/d29b5e85-72b1-486f-ba41-b2706d062cd1)
- In importing, you need to import in following sequence
    1. import 1st output_objects_network.json and deploy manually or using deploy.py
    2. import 2nd output_ports.json and deploy manually or using deploy.py
    3. import 3rd output_group_ports.json and deploy manually or using deploy.py
    4. import 4th output_objects_network_groups.json and deploy manually or using deploy.py

## TO DO
- Add function to migrate also Cisco ASA ACL to FDM


