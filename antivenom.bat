@echo off
if "%~1"=="" goto BLANK

set folder=""

if "%~1"=="jes" set folder=JES2\OUTPUT\
if "%~1"=="converted" set folder=converted\

if %folder%=="" goto BLANK

echo Clearing files in %folder%

if "%~1"=="jes" (
    del %folder%*.* /F /Q 
)

if "%~1"=="converted" (
    del %folder%*.py /F /Q
)

goto END

:BLANK

echo you need to specify the folder to clear out!
echo valid values are:
echo                        jes == JES2\OUTPUT\
echo                  converted == converted\

:END