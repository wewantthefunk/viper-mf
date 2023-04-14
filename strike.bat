@echo off
if "%~1"=="" goto BLANK

cd /D "%~dp0"
python3 converted\%1.py

goto END

:BLANK

echo you need to specify the module or jcl to execute!

:END