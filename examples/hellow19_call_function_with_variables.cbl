       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW19.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01  PASSED-VARIABLE  PIC X(8).

       PROCEDURE DIVISION.

           CALL 'HELLOW20' USING PASSED-VARIABLE.

           DISPLAY 'expecting returned value of HELLOW20'
           DISPLAY 'actual returned value is    ' PASSED-VARIABLE.

           STOP RUN.

