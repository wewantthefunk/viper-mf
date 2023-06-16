# Viper Mainframe Emulator

## Author: Christian Strama

## Purpose
The purpose of this utility is to transform COBOL code into Python code and emulate mainframe execution. The problem statement is as follows:

* Executing COBOL code on a mainframe is slow, disjointed, and expensive. Using JCL jobs requires the execute and feedback be accessed from different areas, while the jobs are queued and executed serially. By using Python, we can execute the code and get immediate feedback within our same terminal window. This will speed up testing and development efforts.

* COBOL is a language and technology that has a shrinking developer base. It is expensive to run, it does not promote good programming practice, and it is difficult to break into readable, maintainable modules. By converting to Python, the first steps of converting legacy code can be taken.

* JCL is a type of scripting language. It is no more powerful than Bash or DOS batch commands. It can be leveraged to setup dependencies for the code to be executed and keep the results of the execution in a file structure.

* This project has a single, "North Star" goal: SEAMLESSLY EXECUTE MAINFRAME CODE ON A PC.

## Hypothesis

If we can make COBOL programs easier and faster to test, we will promote good programming habits and create a foundation for converting legacy code to modern tech stacks that have more tools, resources, and developers to support it. Good programming habits, in this case, are:

* Small modules that have a single responsibility. These modules call, and are called by, other modules for logic and data collaboration.
* Code organized into PARAGRAPHs to reduce cognitive load.
* Code organized to promote small, repeatable unit tests for automation.

## Solution

The Viper MF emulator is a set of tools designed to improve the quality of life of the developer by providing faster feedback and easier debugging.

* Cobra COBOL Source Code Converter
* Boa JCL Code Converter
* Krait CICS Emulator

## Cobra Converter

This converter will brute force translate a COBOL module line-by-line into an equivalent Python statement. Several "helper" functions have been created to accomodate for COBOL's hierarchichal variable structure. These helper functions are located in the cobol_variable.py module. This module must be carried with the converted .py modules as a dependency. The helper functions were created to handle the hierarchical structure of COBOL variables.

The main goal is to not burden the mainframe developer with having to write code one way for this converter to function, and then make changes for the final mainframe source code. Therefore, mainframe behavior emulation is required, along with adherence to IBM standards for COBOL.

### Things to know

* The converted Python file name is the PROGRAM-ID of the COBOL with a .py extension (not the name of the source file).

* File access is accomplished by assigning environment variables. The environment variable name is the ASSIGN value, which is the DD statement in a JCL script. If the environment variable is not assigned, a file status of 35 is assigned to the file status field designated. If the environment variable is set, but the file does not exist, a file status of 35 is assigned to the file status field designated.

* CALL statements call out to other converted Python modules, and any variables in USING clause are treated as byref. The return value from these variables are assigned upon return from the called module. A psuedo memory management passing feature is used to simulate the DFHCOMMAREA.

* Paragraphs are converted to functions.

* CICS statements are converted.

### Limitations and Understanding

This tool is intended, for now, to be a mechanism for automated unit testing. It is a "brute force", line-by-line conversion of COBOL code. There is no manipulation to use objected oriented practices or patterns, except with the cobol_variable.py module. Bad COBOL code will be bad Python code. This is not intended for production use.

This tool DOES NOT check for proper COBOL syntax. It is NOT a compiler. It will do it's best, but if there is bad COBOL syntax, it will create bad Python syntax that probably won't execute.

#### Comments in the COBOL program

The comments in the COBOL are not copied to the Python program. The Python program is not intended to be used for debugging, it is used for test validation. Comments are added to the Python to give an indication of the corresponding COBOL Division and Section, so basic understanding of where the logic is in the Python is gained.

#### The first 6 characters of a line in a COBOL program

The first six characters of COBOL source code lines are ignored. The seventh character is reserved for the comment indicator of asterisk (*). 

#### Whitespace in the COBOL program

The whitespace in the COBOL is not copied to the Python program. The Python program is not intended to be used for debugging, it is used for test validation. 

## COBOL Syntax Requirements for the Converter

### IF Blocks

IF blocks need to end with and END-IF statement. Sure, I could look for the period, but nested IF blocks make it that much harder. Just implement a decent coding practice and use an END-IF statement. Spare me the "COBOL doesn't require it" nonsense. When there isn't an END-IF statement it's bad code, and you know it.

### EVALUATE Blocks

See above, IF Blocks

### PERFORM Blocks

See above, IF Blocks

### Fall through paragraphs

Don't use fall through paragraphs. Even though COBOL has no concept of encapsulation, that doesn't mean you shouldn't try to write clean code.

Having said that, there is a lot of legacy that falls through. Don't do it going forward, but fall through "logic" works.

### Commas in multi-dimensional array element reference

When referencing a multi dimensional array element, a comma is required between the first and second indexes. While this is "legal" in COBOL,

         TABLE-NAME(INDEX-1 INDEX-2)

it is ugly and difficult to parse. Just put a comma in and make it easy for everyone.

         TABLE-NAME(INDEX-1,INDEX-2)

This is a line I was trying to parse from legacy source code

         TABLE-NAME                 
              (INDEX-1 + +1 INDEX-2)

Not only am I contending with the line break and whitespace between the command tokens, but the math on INDEX-1 made it almost impossible (read: not worth the parsing logic effort) to determine index 1 and index 2. Putting a comma in made it manageable. 

         TABLE-NAME                 
              (INDEX-1 + +1, INDEX-2)

In addition, the lack of a comma between indexes increases the cognitive load for developers. Again, this is clean code we're striving for. While it may be seen as a limitation of the converter (which it is), it's actually enforcing coding standards that should be there, anyway.

## Boa JCL Converter

It became clear over time that some sort of JCL functionality would be needed. The setup of files for input and output is an integral part of mainframe processing. So, the Boa JCL converter was created. This will interpret DD statements to set environment variables to the appropriate path/filename for use in the converted COBOL program.

A JES2-like system for tracking the results of programs was included. The output of the execution of a JCL "job" is stored in a simple text file in the JES2/OUTPUT path from where the JCL job is executed.

As with all things in this project, as functionality is discovered through the conversion of real world legacy code, the product will evolve and become more robust.

Basic utility functions from IDCAMS and IEBGENER are being added over time. So far:

* IDCAMS
  * DELETE

* IEBGENER
  * none

## Krait CICS Emulator

CICS is not voodoo or magic. After spending a short amount of time reading the specifications and trying some things out, the nature of CICS became clear. Although the Model-View-Controller concept became solidified in the early 00's, CICS is an early predecessor to MVC (much like quite a few mainframe concepts and features). CICS itself is a memory and task manager. CICS statements are transformed into standard COBOL statements in a preprocessing step in the compilation process. Putting all of this together made it a not difficult feat to create a task and memory manager to emulate the behavior of CICS.

As with all things in this project, as functionality is discovered through the conversion of real world legacy code, the product will evolve and become more robust.

## How to use

### Python dependencies

Make sure the following Python dependencies are installed:

* datetime
* decimal
* glob
* importlib
* inspect
* io
* math
* os
* pathlib
* random
* request
* shutil
* string
* sys
* tkinter

In the src folder, modify the input_dir variable in the main.py module to point to your COBOL source code folder relative to the src folder.

Navigate to the src folder in a terminal.

Execute python3 main.py from the terminal.

Converted Python files are put in the converted/ folder. The cobol_variable.py file is copied from the dependencies/ folder to the converted/ folder.

For unit tests of all examples in this repository, navigate to the unittest folder and execute the test_all.sh script. This will delete ALL python files from the converted folder and convert all of the .cbl files in the examples folder and execute each of the converted files.

## Challenges

* Hierarchical variable structure of COBOL. Some variables aren't real variables, they are concatenations of other (sub) variables. This presented a challenge.
* REDEFINES variables in COBOL. See above, then add on more complexity.
* Arrays in COBOL. See above and add even more complexity.
* Level 88 variables, the dollar store enum.
* COMP(-X) fields. 
* Error handling. COBOL doesn't have error handling, such as try/catch. So there is no error handling added by the converter. There is an error handling command in CICS. (CICS commands will eventually be converted)
* Quotes for literals MUST be single quotes (') in the COBOL program. Double quotes are not processed as literals.
* PERIODs (.) are semi-optional. Not having a rigid statement delimiter, such as the semi-colon (;) in C based languages, makes for a challenge.
* EVALUATE TRUE statements.
* Nested IF and EVALUATE statements.

## Inspiration

The inspiration for this project came from the Otterkit COBOL Compiler https://github.com/otterkit/otterkit

That compiler converts to C#, I decided to convert to Python.

Thanks for giving me the inspiration!

## What's Next?

Only a small set of COBOL verbs, functions, and keywords are converted, at this time. As more modules are used in testing, more verbs and keywords will be added. Conversions for CICS statements are also planned.

COMP-1, COMP-2, and COMP-4 datatypes are not handled.

## Bug Reporting

If this code is erroneous in some way, you can submit a bug or submit a pull request with the fix. Please note, a bug is NOT a missing feature or keyword processing or anything like that. For the verbs and keywords that are processed, they should be handled correctly.

Thank you!

### Current Known Bugs

* None known, but they exist

## Things to Think About

***The use of COBOL cripples the mind; its teaching should, therefore, be regarded as a criminal offense.*** - Edsger Wybe Dijkstra (Dutch computer scientist)

***A computer without COBOL and Fortran is like a piece of chocolate cake without ketchup and mustard.*** - Anonymous

***COBOL programs are an exercise in Artificial Inelegance.*** - Anonymous

***COBOL means Completely Obsolete Business Orientated Language.*** - Anonymous

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

## Standard Acknowledgement

Any organization interested in reproducing the COBOL standard and specifications in whole or in part,
using ideas from this document as the basis for an instruction manual or for any other purpose, is free
to do so. However, all such organizations are requested to reproduce the following acknowledgment
paragraphs in their entirety as part of the preface to any such publication (any organization using a
short passage from this document, such as in a book review, is requested to mention "COBOL" in
acknowledgment of the source, but need not quote the acknowledgment):

COBOL is an industry language and is not the property of any company or group of companies, or of any
organization or group of organizations.

No warranty, expressed or implied, is made by any contributor or by the CODASYL COBOL Committee
as to the accuracy and functioning of the programming system and language. Moreover, no
responsibility is assumed by any contributor, or by the committee, in connection therewith.

The authors and copyright holders of the copyrighted materials used herein:

- FLOW-MATIC® (trademark of Sperry Rand Corporation), Programming for the 'UNIVAC® I and
  II, Data Automation Systems copyrighted 1958,1959, by Sperry Rand Corporation;
- IBM Commercial Translator Form No F 28-8013, copyrighted 1959 by IBM;
- FACT, DSI 27A5260-2760, copyrighted 1960 by Minneapolis-Honeywell

Have specifically authorized the use of this material in whole or in part, in the COBOL specifications.
Such authorization extends to the reproduction and use of COBOL specifications in programming
manuals or similar publications.
