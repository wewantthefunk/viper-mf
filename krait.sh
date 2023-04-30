#!/bin/bash

# Change to the directory where the script is located
cd "$(dirname "$0")"

# Call the module
python3 converted/krait.py $1
