#!/bin/bash

# Change to the directory where the script is located
cd "$(dirname "$0")"

# Call the module
python3 src/cobra_dependencies_convert.py

cp src/krait.py converted/krait.py