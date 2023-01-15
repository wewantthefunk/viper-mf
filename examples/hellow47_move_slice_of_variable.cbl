       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW47.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 TEST-VAL PIC X(11) VALUE 'hello world'.

       01 TEST-VAL-2.
           03 TV-ONE   PIC X(5).
           03 TV-SPACE PIC X(1).
           03 TV-TWO   PIC X(5).

       PROCEDURE DIVISION.

           DISPLAY 'expected value is hello'
           MOVE TEST-VAL(1:5) TO TEST-VAL-2.

           DISPLAY 'actual value is   ' TEST-VAL-2.

           STOP RUN.

