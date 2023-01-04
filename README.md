# COBOL to Python Converter

## Author: Christian Strama

## Purpose:
The purpose of this utility is to transform COBOL code into Python code. The problem statement is as follows:

* Executing COBOL code on a mainframe is slow and disjointed. Using JCL jobs requires the execute and feedback be accessed from different areas. By using Python, we can execute the code and get immediate feedback within our same terminal window. This will speed up testing and development efforts.

* COBOL is a language and technology that has a shrinking developer base. By converting to Python, the first steps of converting legacy code can be taken.

## Solution

This converter will brute force translate a COBOL module line-by-line into an equivalent Python statement. Several "helper" functions have been created to accomodate for COBOL's hierarchichal variable structure. These helper functions are located in the cobol_variable.py module. This module must be carried with the converted .py modules as a dependency.

File access is accomplished by assigning environment variables. The environment variable name is the ASSIGN value, which is the DD statement in a JCL script. If the environment variable is not assigned, a file is created that is named the ASSIGN value.

CALL statements call out to other convered Python modules, and any variables in USING clause are treated as byref. The return value from these variables are assigned upon return from the called module.

### Limitations and Understanding

This tool is intended, for now, to be a mechanism for automated unit testing. It is "brute force", line-by-line conversion of COBOL code. There is no manipulation to use objected oriented practices or patterns, except with the cobol_variable.py module. Bad COBOL code will be bad Python code. This is not intended for production use.

## What's Next?

Only a small set of COBOL verbs and keywords are converted, at this time. As more modules are used in testing, more verbs and keywords will be added. Conversions for CICS statements are also planned and intended.

File access is limited to sequential reads starting with the first line. Indexed record lookups are planned and intended. This will help with VSAM file development.

Level 77 and 88 variables are not processed or handled properly in logic statements.

Arrays are not processed or handled properly in logic statements.

## Bug Reporting

If this code is erroneous in some way, you can submit a bug or submit a pull request with the fix. Please note, a bug is NOT a missing feature or keyword processing or anything like that. For the verbs and keywords that are processed, they should be handled correctly.

Thank you!

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