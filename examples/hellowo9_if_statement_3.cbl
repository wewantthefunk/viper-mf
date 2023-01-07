       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOWO9.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 TEST-ARRAY OCCURS 100 TIMES INDEXED BY TS-INDEX.
           05 VALUE-ONE    PIC X(2).
           05 VALUE-TWO    PIC X(2).

       PROCEDURE DIVISION.

           MOVE 3 TO TS-INDEX.
           MOVE 'hi' TO VALUE-ONE(TS-INDEX).
      * multi condition if statement
           IF VALUE-ONE(TS-INDEX) = 'hi' AND TS-INDEX = 3
              DISPLAY 'AND if condition successful'
           END-IF.

           IF VALUE-ONE(TS-INDEX) = 'hello' OR TS-INDEX = 3
               DISPLAY 'OR if condition successful'
           END-IF.


           STOP RUN.

