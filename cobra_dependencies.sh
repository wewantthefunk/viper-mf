#!/bin/bash

# Change to the directory where the script is located
cd "$(dirname "$0")"

# Call the module
python3 src/cobra_dependencies_convert.py

cp src/krait.py converted/krait.py
cp src/krait_queue.py converted/krait_queue.py
cp src/krait_region.py converted/krait_region.py
cp src/krait_ui.py converted/krait_ui.py
cp src/krait_util.py converted/krait_util.py
cp maps/SYSMAP.txt converted/maps/SYSMAP.txt
