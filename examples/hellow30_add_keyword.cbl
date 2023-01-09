       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW30.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 FILE-STATUS      PIC 9(2).

       PROCEDURE DIVISION.

           MOVE 0 TO FILE-STATUS.

           DISPLAY 'expected value is 00'
           DISPLAY 'actual value is   ' FILE-STATUS.

           ADD 1 TO FILE-STATUS.

           DISPLAY 'expected value is 01'
           DISPLAY 'actual value is   ' FILE-STATUS.       

           STOP RUN.

