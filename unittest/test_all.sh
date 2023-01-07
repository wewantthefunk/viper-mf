cd ../src/

python3 main.py

cd ../converted/

echo HELLOWO1 - basic DISPLAY statement of literal value
python3 HELLOWO1.py

echo 
echo HELLOWO2 - basic setting and DISPLAY statement of top level variable
python3 HELLOWO2.py

echo
echo HELLOWO3 - basic setting and DISPLAY statement of hierarchical variable
python3 HELLOWO3.py

echo
echo HELLOWO4 - basic setting and DISPLAY statement of hierarchical variable, displayed from calling a PARAGRAPH
python3 HELLOWO4.py

echo
echo HELLOWO5 - basic setting and DISPLAY statement of hierarchical variable that is REDEFINE
python3 HELLOWO5.py

echo
echo HELLOWO6 - basic setting and DISPLAY statement of array values
python3 HELLOWO6.py

echo
echo HELLOWO7 - basic if condition
python3 HELLOWO7.py

echo
echo HELLOWO8 - basic if condition using array
python3 HELLOWO8.py

echo
echo HELLOWO9 - basic if condition with AND and OR boolean operator
python3 HELLOWO9.py

echo
echo HELLOW10 - basic evaluate statement
python3 HELLOW10.py

echo
echo HELLOW11 - nested evaluate statement
python3 HELLOW11.py

echo
echo HELLOW12 - sequential file access
export TESTFILE=test-records.txt
python3 HELLOW12.py

echo
echo HELLOW13 - create variable with a value statement
python3 HELLOW13.py

echo
echo HELLOW14 - squential file access, environment variable not set
python3 HELLOW14.py

echo
echo HELLOW15 - current date function
python3 HELLOW15.py

echo
echo HELLOW16 - inspect function
python3 HELLOW16.py

echo
echo HELLOW17 - call HELLOW18
python3 HELLOW17.py

echo
echo HELLOW18 - basic program that is called from HELLOW17
python3 HELLOW18.py

echo
echo HELLOW19 - call HELLOW20
python3 HELLOW19.py

echo
echo HELLOW20 - basic program that is called from HELLOW19 with parameters
python3 HELLOW20.py

echo
echo HELLOW21 - fall through evaluate statement
python3 HELLOW21.py

echo
echo HELLOW22 - set statement
python3 HELLOW22.py

echo
echo HELLOW23 - search statement
python3 HELLOW23.py

echo
echo HELLOW24 - search all statement
python3 HELLOW24.py

echo
echo HELLOW25 - perform varying loop
python3 HELLOW25.py

echo
echo HELLOW26 - space keyword
python3 HELLOW26.py

echo
echo HELLOW27 - zero keyword
python3 HELLOW27.py

echo
echo HELLOW28 - squential file access, environment variable set, file does not exist
export NOFILE=missing.txt
python3 HELLOW28.py