@echo off
if "%~1"=="" goto BLANK

set folder=""

if "%~1"=="jes" set folder=JES2\OUTPUT

if %folder%=="" goto BLANK

cd /d %folder%
dir
del *.* /F /Q
dir

goto END

:BLANK

echo you need to specify the folder to clear out!

:END