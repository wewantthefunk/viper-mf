       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOWO7.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 TEST-ARRAY OCCURS 100 TIMES INDEXED BY TS-INDEX.
           05 VALUE-ONE    PIC X(2).
           05 VALUE-TWO    PIC X(2).

       PROCEDURE DIVISION.

           DISPLAY 'expected value if condition successful'
           MOVE 3 TO TS-INDEX.
           MOVE 'hi' TO VALUE-ONE(TS-INDEX).

      *  check array position using literal
           IF VALUE-ONE(3) = 'hi'
              DISPLAY 'if condition successful'
           END-IF.


           STOP RUN.

