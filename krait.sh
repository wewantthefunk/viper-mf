#!/bin/bash

# Change to the directory where the script is located
cd "$(dirname "$0")"

# Check if pyyaml is installed
if ! python3 -c "import yaml" >/dev/null 2>&1; then
  echo "Error: PyYAML is not installed. Please install it using 'pip install pyyaml'."
  exit 1
fi

# Specify the path to your YAML file
yaml_file="$1"

# Parse the YAML file using Python and set environment variables
python3 - <<EOF
import os
import yaml
import subprocess

if "$yaml_file" == "":
    subprocess.run(["python3", "converted/krait.py"])
else:
    with open("$yaml_file", "r") as file:
        data = yaml.safe_load(file)

    for key, value in data.items():
        if isinstance(value, dict):
            for nested_key, nested_value in value.items():
                os.environ[f"{nested_key.upper()}"] = nested_value
                print(nested_key.upper())
        else:
            os.environ[key.upper()] = value
            print(key.upper())

    subprocess.run(["python3", "converted/krait.py", os.environ["REGION"], os.environ["TRAN"]])
EOF