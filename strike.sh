#!/bin/bash

if [ $# -ne 1 ]; then
  echo "Error: This script requires one command line parameters."
  exit 1
fi

# Change to the directory where the script is located
cd "$(dirname "$0")"

# Call the module
python3 converted/"$1"