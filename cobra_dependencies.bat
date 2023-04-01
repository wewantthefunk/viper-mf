@echo off
cd /D "%~dp0"
python3 src\cobra_dependencies_convert.py

copy src\kix.py converted\kix.py

:END
