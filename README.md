# COBOL to Python Converter

## Author: Christian Strama

## Purpose:
The purpose of this utility is to transform COBOL code into Python code. The problem statement is as follows:

* Executing COBOL code on a mainframe is slow, disjointed, and expensive. Using JCL jobs requires the execute and feedback be accessed from different areas. By using Python, we can execute the code and get immediate feedback within our same terminal window. This will speed up testing and development efforts.

* COBOL is a language and technology that has a shrinking developer base. It is expensive to run, it does not promote good programming practice, and it is difficult to break into readable, maintainable modules. By converting to Python, the first steps of converting legacy code can be taken.

## Hypothesis

If we can make COBOL programs easier and faster to test, we will promote good programming habits and create a foundation for converting legacy code to a modern language that has more tools, resources, and developers to support it. Good programming habits, in this case, are:

* Small modules that have a single responsibility. These modules call, and are called by, other modules for logic and data collaboration.
* Code organized into PARAGRAPHs to reduce cognitive load.
* Code organized to promote small, repeatable unit tests for automation.

## Solution

This converter will brute force translate a COBOL module line-by-line into an equivalent Python statement. Several "helper" functions have been created to accomodate for COBOL's hierarchichal variable structure. These helper functions are located in the cobol_variable.py module. This module must be carried with the converted .py modules as a dependency. The helper functions were created to handle the hierarchical structure of COBOL variables.

### Things to know

* The converted Python file name is the PROGRAM-ID of the COBOL with a .py extension.

* File access is accomplished by assigning environment variables. The environment variable name is the ASSIGN value, which is the DD statement in a JCL script. If the environment variable is not assigned, a file status of 35 is assigned to the field designated. If the environment variable is set, but the file does not exist, a file status of 35 is assigned to the field designated.

* CALL statements call out to other converted Python modules, and any variables in USING clause are treated as byref. The return value from these variables are assigned upon return from the called module.

* Paragraphs are converted to functions

### Limitations and Understanding

This tool is intended, for now, to be a mechanism for automated unit testing. It is a "brute force", line-by-line conversion of COBOL code. There is no manipulation to use objected oriented practices or patterns, except with the cobol_variable.py module. Bad COBOL code will be bad Python code. This is not intended for production use.

#### Comments in the COBOL program

The comments in the COBOL are not copied to the Python program. The Python program is not intended to be used for debugging, it is used for test validation. Comments are added to the Python to give an indication of the corresponding COBOL Division and Section, so basic understanding of where the logic is in the Python is gained.

#### The first 6 characters of a line in a COBOL program

The first six characters are ignored. The seventh character is reserved for the comment indicator of asterisk (*). 

#### Whitespace in the COBOL program

The whitespace in the COBOL is not copied to the Python program. The Python program is not intended to be used for debugging, it is used for test validation. 

## How to use

### Python dependencies

Make sure the following Python dependencies are installed:

* datetime
* glob
* importlib
* os
* random
* request
* shutil
* string

In the src folder, modify the input_dir variable in the main.py module to point to your COBOL source code folder relative to the src folder.

Navigate to the src folder in a terminal.

Execute python3 main.py from the terminal.

Converted Python files are put in the converted/ folder. The cobol_variable.py file is copied from the dependencies/ folder to the converted/ folder.

For unit tests of all examples in this repository, navigate to the unittest folder and execute the test_all.sh script. This will delete ALL python files from the converted folder and convert all of the .cbl files in the examples folder and execute each of the converted files.

## Challenges

* Hierarchical variable structure of COBOL. Some variables aren't real variables, they are concatenations of other (sub) variables. This presented a challenge.
* REDEFINES variables in COBOL. See above, then add on more complexity.
* Arrays in COBOL. See above and add even more complexity.
* Error handling. COBOL doesn't have error handling, such as try/catch. So there is no error handling added by the converter. There is an error handling command in CICS. (CICS commands will eventually be converted)
* Quotes for literals MUST be single quotes (') in the COBOL program. Double quotes are not processed as literals.
* PERIODs (.) are semi-optional. Not having a rigid statement delimiter, such as the semi-colon (;) in C based languages, makes for a challenge

## What's Next?

Only a small set of COBOL verbs, functions, and keywords are converted, at this time. As more modules are used in testing, more verbs and keywords will be added. Conversions for CICS statements are also planned.

File access is limited to sequential reads starting with the first line. Indexed record lookups are planned and intended. This will help with VSAM file development.

Level 77 variables are not processed or handled properly in logic statements.

## Bug Reporting

If this code is erroneous in some way, you can submit a bug or submit a pull request with the fix. Please note, a bug is NOT a missing feature or keyword processing or anything like that. For the verbs and keywords that are processed, they should be handled correctly.

Thank you!

### Current Known Bugs

* None found, but they exist

## Things to Think About

***The use of COBOL cripples the mind; its teaching should, therefore, be regarded as a criminal offense. *** - Edsger Wybe Dijkstra (Dutch computer scientist)

***A computer without COBOL and Fortran is like a piece of chocolate cake without ketchup and mustard. *** - Anonymous

***COBOL programs are an exercise in Artificial Inelegance. *** - Anonymous

***COBOL means Completely Obsolete Business Orientated Language. *** - Anonymous

## LICENSE

Copyright 2023 Christian Strama

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.