       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW80.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 TEST-VALUE         PIC X(10).

       01 TEST-VALUE-ADDRESS POINTER.

       01 TEST-VALUE-2       PIC X(10).

       PROCEDURE DIVISION.

           MOVE 'test' TO TEST-VALUE.

           SET TEST-VALUE-ADDRESS TO ADDRESS OF TEST-VALUE.

           CALL 'HELLOW81' USING TEST-VALUE-ADDRESS.

           DISPLAY 'expected value: updated 10'
           DISPLAY 'actual value:   ' TEST-VALUE.

           STOP RUN.

