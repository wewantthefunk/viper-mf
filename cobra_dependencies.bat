@echo off
cd /D "%~dp0"
python3 src\cobra_dependencies_convert.py

echo copying krait CICS emulator
copy src\krait.py converted\krait.py
copy src\krait_queue.py converted\krait_queue.py
copy src\krait_region.py converted\krait_region.py
copy src\krait_ui.py converted\krait_ui.py
copy src\krait_util.py converted\krait_util.py

goto END

:END
