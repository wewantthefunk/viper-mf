       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW68.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 TEST-VALUE         PIC X(10).

       01 TEST-VALUE-ADDRESS POINTER.

       01 TEST-VALUE-2       PIC X(10).

       PROCEDURE DIVISION.

           MOVE 'test' TO TEST-VALUE.

           SET TEST-VALUE-ADDRESS TO ADDRESS OF TEST-VALUE.

           SET ADDRESS OF TEST-VALUE-2 TO TEST-VALUE-ADDRESS.

           DISPLAY TEST-VALUE-2.

           STOP RUN.

