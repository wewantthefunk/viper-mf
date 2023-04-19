       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW84.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION. 

       01 VALUE 'TESTDATA'.
           10  TESTNAME  OCCURS 2 TIMES
                          INDEXED DD-INDEX
                          PIC  X(04).
       01 NEXT-VAR  PIC X(4) VALUE 'NEXT'.

       PROCEDURE DIVISION.

           DISPLAY TESTNAME(1).
           DISPLAY TESTNAME(2).

           STOP RUN.
