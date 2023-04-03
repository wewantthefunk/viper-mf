#!/bin/bash

if [ $# -ne 2 ]; then
  echo "Error: This script requires two command line parameters."
  exit 1
fi

# Change to the directory where the script is located
cd "$(dirname "$0")"

# Call the cobra_main.py module with the two parameters
python3 src/cobra_main.py "$1" "$2"