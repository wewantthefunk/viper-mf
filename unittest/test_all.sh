cd ../converted/

rm *.py &

wait

cd ../src/

python3 main.py &

wait

cd ../converted/

echo HELLOWO1 - basic DISPLAY statement of literal value
python3 HELLOWO1.py &
wait

echo 
echo HELLOWO2 - basic setting and DISPLAY statement of top level variable
python3 HELLOWO2.py &
wait

echo
echo HELLOWO3 - basic setting and DISPLAY statement of hierarchical variable
python3 HELLOWO3.py &
wait

echo
echo HELLOWO4 - basic setting and DISPLAY statement of hierarchical variable, displayed from calling a PARAGRAPH
python3 HELLOWO4.py &
wait

echo
echo HELLOWO5 - basic setting and DISPLAY statement of hierarchical variable that is REDEFINE
python3 HELLOWO5.py &
wait

echo
echo HELLOWO6 - basic setting and DISPLAY statement of array values
python3 HELLOWO6.py &
wait

echo
echo HELLOWO7 - basic if condition
python3 HELLOWO7.py &
wait

echo
echo HELLOWO8 - basic if condition using array
python3 HELLOWO8.py &
wait

echo
echo HELLOWO9 - basic if condition with AND and OR boolean operator
python3 HELLOWO9.py &
wait

echo
echo HELLOW10 - basic evaluate statement
python3 HELLOW10.py &
wait

echo
echo HELLOW11 - nested evaluate statement
python3 HELLOW11.py &
wait

echo
echo HELLOW12 - sequential file access
export TESTFILE=test-records.txt
python3 HELLOW12.py &
wait

echo
echo HELLOW13 - create variable with a value statement
python3 HELLOW13.py &
wait

echo
echo HELLOW14 - squential file access, environment variable not set
python3 HELLOW14.py &
wait

echo
echo HELLOW15 - current date function
python3 HELLOW15.py &
wait

echo
echo HELLOW16 - inspect function
python3 HELLOW16.py &
wait

echo
echo HELLOW17 - call HELLOW18
python3 HELLOW17.py &
wait

echo
echo HELLOW18 - basic program that is called from HELLOW17
python3 HELLOW18.py &
wait

echo
echo HELLOW19 - call HELLOW20
python3 HELLOW19.py &
wait

echo
echo HELLOW20 - basic program that is called from HELLOW19 with parameters
python3 HELLOW20.py &
wait

echo
echo HELLOW21 - fall through evaluate statement
python3 HELLOW21.py &
wait

echo
echo HELLOW22 - set statement
python3 HELLOW22.py &
wait

echo
echo HELLOW23 - search statement
python3 HELLOW23.py &
wait

echo
echo HELLOW24 - search all statement
python3 HELLOW24.py &
wait

echo
echo HELLOW25 - perform varying loop
python3 HELLOW25.py &
wait

echo
echo HELLOW26 - space keyword
python3 HELLOW26.py &
wait

echo
echo HELLOW27 - zero keyword
python3 HELLOW27.py &
wait

echo
echo HELLOW28 - squential file access, environment variable set, file does not exist
export NOFILE=missing.txt
python3 HELLOW28.py &
wait

echo
echo HELLOW29 - nested if statement
python3 HELLOW29.py &
wait

echo
echo HELLOW30 - add/addition verb
python3 HELLOW30.py &
wait

echo
echo HELLOW31 - add/addition with giving verb
python3 HELLOW31.py &
wait

echo
echo HELLOW32 - add/addition verb using a variable
python3 HELLOW32.py &
wait

echo
echo HELLOW33 - add/addition with giving verb using a variable
python3 HELLOW33.py &
wait

echo
echo HELLOW34 - call function using a variable
python3 HELLOW34.py &
wait

echo
echo HELLOW35 - call receive function
python3 HELLOW35.py &
wait

echo
echo HELLOW36 - call function using a variable passing variables
python3 HELLOW36.py &
wait

echo
echo HELLOW37 - call receive function with variable arguments
python3 HELLOW37.py &
wait

echo
echo HELLOW38 - search table redefined literals
python3 HELLOW38.py &
wait

echo
echo HELLOW39 - call search table redefined literals
python3 HELLOW39.py &
wait

echo
echo COMPL001 - search table redefined literals
python3 COMPL001.py &
wait

echo
echo COMPL002 - call out to search table redefined literals
python3 COMPL002.py &
wait

echo
echo HELLOW40 - DISPLAY keyword with UPON CONSOLE ignored
python3 HELLOW40.py &
wait

echo
echo HELLOW41 - Declare variable with no name and a VALUE statement
python3 HELLOW41.py &
wait

echo
echo HELLOW42 - LEVEL 88 variables
python3 HELLOW42.py &
wait

echo
echo HELLOW43 - subtract keyword
python3 HELLOW43.py &
wait

echo
echo HELLOW44 - multiply keyword
python3 HELLOW44.py &
wait

echo
echo HELLOW45 - divide keyword
python3 HELLOW45.py &
wait

echo
echo HELLOW46 - value statement hex value
python3 HELLOW46.py &
wait

echo
echo HELLOW47 - move slice of variable to another variable
python3 HELLOW47.py &
wait

echo
echo HELLOW48 - compute statement
python3 HELLOW48.py &
wait

echo
echo HELLOW49 - complex if statement
python3 HELLOW49.py &
wait

echo
echo HELLOW50 - another complex if statement
python3 HELLOW50.py &
wait

echo
echo HELLOW51 - another complex if statement
python3 HELLOW51.py &
wait

echo
echo HELLOW52 - accept statement
export SYSIN=sysin_val
python3 HELLOW52.py &
wait

echo
echo HELLOW53 - comp-3 fields
python3 HELLOW53.py &
wait

echo
echo HELLOW54 - comp-3 fields redefines
python3 HELLOW54.py &
wait

echo
echo HELLOW55 - comp-3 fields cascading
python3 HELLOW55.py &
wait

echo
echo HELLOW56 - comp-3 fields math
python3 HELLOW56.py &
wait

#echo
#echo HELLOW57 - comp fields
#python3 HELLOW57.py &
#wait

#echo
#echo HELLOW58 - comp fields math
#python3 HELLOW58.py &
#wait

echo
echo HELLOW59 - comp-5 fields
python3 HELLOW59.py &
wait

echo
echo HELLOW60 - comp-5 fields math
python3 HELLOW60.py &
wait

#echo
#echo HELLOW61 - decimal fields
#python3 HELLOW61.py &
#wait

echo
echo HELLOW63 - called program that sends DFHCOMMAREA
python3 HELLOW63.py &
wait

#echo
#echo HELLOW64 - called program that receives DFHCOMMAREA
#python3 HELLOW64.py &
#wait

#echo
#echo CICS01 - cics asktime
#python3 CICS01.py &
#wait

#echo
#echo CICS02 - cics link
#python3 CICS02.py &
#wait