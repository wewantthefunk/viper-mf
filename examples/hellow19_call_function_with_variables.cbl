       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW19.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01  PASSED-VARIABLE  PIC X(8) VALUE 'default '.

       PROCEDURE DIVISION.

           DISPLAY 'expected message:'
           DISPLAY 'Called module HELLOW20 default *'

           DISPLAY 'actual message:'
           CALL 'HELLOW20' USING PASSED-VARIABLE.

           DISPLAY 'expecting returned value of HELLOW20'
           DISPLAY 'actual returned value is    ' PASSED-VARIABLE.

           STOP RUN.

