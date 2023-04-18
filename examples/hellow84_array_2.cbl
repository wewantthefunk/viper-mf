       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW84.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION. 

       01 VALUE 'TESTDATA'.
           10  TESTNAME  OCCURS 2 TIMES
                          INDEXED DD-INDEX
                          PIC  X(04).

       PROCEDURE DIVISION.

           DISPLAY TESTNAME(1).
           DISPLAY TESTNAME(2).

           STOP RUN.
