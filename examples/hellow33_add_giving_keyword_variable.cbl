       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW33.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 FILE-STATUS      PIC 9(2).
       01 NEW-FILE-STATUS  PIC 9(2).
       01 ADDITION-VAL     PIC 9(1) VALUE 1.

       PROCEDURE DIVISION.

           MOVE 0 TO FILE-STATUS.

           DISPLAY 'expected value is 00'
           DISPLAY 'actual value is   ' FILE-STATUS.

           ADD ADDITION-VAL TO FILE-STATUS GIVING NEW-FILE-STATUS.

           DISPLAY 'expected value is 00'
           DISPLAY 'actual value is   ' FILE-STATUS. 

           DISPLAY 'expected value is 01'
           DISPLAY 'actual value is   ' NEW-FILE-STATUS.       

           STOP RUN.

