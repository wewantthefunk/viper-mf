       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW46.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 TEST-VAL PIC X(4) VALUE X'F381'.

       01 TEST-VAL-2.
           03 TV-ONE   PIC X(2).
           03 TV-TWO   PIC X(2).

       PROCEDURE DIVISION.
           DISPLAY 'expected value is F381'
           DISPLAY 'actual value is   ' TEST-VAL.

           MOVE X'827C' TO TEST-VAL-2.

           DISPLAY 'expected value is 827C'
           DISPLAY 'actual value is   ' TEST-VAL-2.

           STOP RUN.

