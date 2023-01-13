       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW43.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 FILE-STATUS      PIC 9(2).

       PROCEDURE DIVISION.

           MOVE 1 TO FILE-STATUS.

           DISPLAY 'expected value is 01'
           DISPLAY 'actual value is   ' FILE-STATUS.

           SUBTRACT 1 FROM FILE-STATUS.

           DISPLAY 'expected value is 00'
           DISPLAY 'actual value is   ' FILE-STATUS.       

           STOP RUN.

