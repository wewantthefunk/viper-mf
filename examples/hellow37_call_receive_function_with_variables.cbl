       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW37.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       LINKAGE SECTION. 

       01  PASSED-VARIABLE PIC X(8).

       PROCEDURE DIVISION USING PASSED-VARIABLE.

           DISPLAY 'Called module HELLOW37 ' PASSED-VARIABLE '*'.

           MOVE 'HELLOW37' TO PASSED-VARIABLE.

           STOP RUN.

