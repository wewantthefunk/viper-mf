@echo off
cd /D "%~dp0"
python3 src\cobra_dependencies_convert.py

echo copying krait CICS emulator
copy src\krait.py converted\krait.py

goto END

:END
