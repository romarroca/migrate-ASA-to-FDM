migrate-objects-ASA-to-FDM

A utility script to migrate existing objects and object groups from Cisco ASA to Cisco Firepower Device Manager (FDM).
Background

While Cisco provides a migration tool, it's primarily suited for freshly installed FDM systems. In real-world scenarios, there might be cases where one needs to migrate bulk objects to an already running FDM. This script fills that gap.
Use Case

This tool is ideal for scenarios where:

    You have an existing FDM with some configurations and don't want to reset it.
    You wish to migrate objects in bulk from ASA to FDM without manual efforts.

Disclaimer

This is more of a utility script developed for specific needs. The code may not be polished or production-ready. Hence, it is essential to:

    Not use this directly in a production environment.
    Always take backups before performing any operations.
    Thoroughly test in a lab environment to understand its effects.

Use this script at your own risk.
Usage

    Clone the repository:

    bash

git clone https://github.com/your_username/migrate-objects-ASA-to-FDM.git

Navigate to the directory:

bash

cd migrate-objects-ASA-to-FDM

Run the script (and follow the prompts):

bash

python your_script_name.py
