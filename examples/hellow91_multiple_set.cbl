       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW91.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION. 

       01  TEST-1   PIC X(2).

       01  TEST-2   PIC X(2).

       01  TEST-3   PIC X(2).

       PROCEDURE DIVISION.

           SET TEST-1 
               TEST-2 
               TEST-3 TO 'XX'.

           DISPLAY 'expected value: XX XX XX'

           DISPLAY 'actual value:   ' TEST-1 ' ' TEST-2 ' ' TEST-3

           STOP RUN.