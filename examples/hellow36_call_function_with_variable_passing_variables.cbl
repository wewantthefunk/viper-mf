       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW36.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 SUB-PROGRAM   PIC X(8) VALUE 'HELLOW37'.
       01 PASSED-VARIABLE  PIC X(8).

       PROCEDURE DIVISION.

           MOVE 'default' TO PASSED-VARIABLE.
           DISPLAY 'expected message:'
           DISPLAY 'Called module HELLOW37 default *'
           DISPLAY 'actual message:'
           CALL SUB-PROGRAM USING PASSED-VARIABLE.

           DISPLAY 'expected value HELLOW37'
           DISPLAY 'actual value   ' PASSED-VARIABLE

           STOP RUN.

