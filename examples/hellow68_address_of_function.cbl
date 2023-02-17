       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW68.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 TEST-VALUE   PIC X(10).

       01 TEST-COMP-3  PIC S9(5) COMP-3.

       01 LENGTH-VAL   PIC 9(3).

       PROCEDURE DIVISION.

           DISPLAY 'expected value: 10'
           DISPLAY 'actual value:   ' LENGTH OF TEST-VALUE.

           DISPLAY 'expected value: 3'
           DISPLAY 'actual value:   ' LENGTH OF TEST-COMP-3.

           MOVE LENGTH OF TEST-VALUE TO LENGTH-VAL.

           DISPLAY 'expected value: 010'
           DISPLAY 'actual value:   ' LENGTH-VAL.


           COMPUTE LENGTH-VAL = LENGTH OF TEST-VALUE + 5.

           STOP RUN.

