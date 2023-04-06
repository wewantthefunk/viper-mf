       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW81.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 TEST-VALUE PIC X(10).

       LINKAGE SECTION. 

       01 TEST-VALUE-ADDRESS POINTER.

       PROCEDURE DIVISION USING TEST-VALUE-ADDRESS.

           SET ADDRESS OF TEST-VALUE TO TEST-VALUE-ADDRESS.

           DISPLAY 'expected value: test'
           DISPLAY 'actual value:   ' TEST-VALUE.

           MOVE 'updated 10' TO TEST-VALUE.

           DISPLAY 'expected value: updated 10'
           DISPLAY 'actual value:   ' TEST-VALUE.

           STOP RUN.

