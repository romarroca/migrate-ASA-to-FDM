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

Instructions
- I should probably create a video on how I used it
