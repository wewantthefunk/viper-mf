@echo off
if "%~1"=="" goto BLANK
if "%~2"=="" goto BLANK

cd /D "%~dp0"
python3 src\parse_map_file.py %1 %2

goto END

:BLANK

echo you need to specify the input file and the output folder!

:END