#!/bin/bash

if [ $# -ne 2 ]; then
  echo "Error: This script requires two command line parameters."
  exit 1
fi

# Change to the directory where the script is located
cd "$(dirname "$0")"

# Call the parse_map_file.py module with the two parameters
python3 src/parse_map_file.py "$1" "$2"
cp "$1" converted/"$1"