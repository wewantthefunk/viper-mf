       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW23.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 TEST-ARRAY OCCURS 4 TIMES INDEXED BY TS-INDEX.
           05 VALUE-ONE    PIC X(2).

       PROCEDURE DIVISION.

           MOVE 1 TO TS-INDEX.
           MOVE 'ab' TO VALUE-ONE(TS-INDEX).
           MOVE 2 TO TS-INDEX.
           MOVE 'cd' TO VALUE-ONE(TS-INDEX).
           MOVE 3 TO TS-INDEX.
           MOVE 'ef' TO VALUE-ONE(TS-INDEX).
           MOVE 4 TO TS-INDEX.
           MOVE 'gh' TO VALUE-ONE(TS-INDEX).

           MOVE 1 TO TS-INDEX.

           SEARCH TEST-ARRAY 
              AT END DISPLAY 'value not found'
              WHEN VALUE-ONE(TS-INDEX) = 'gh'
                 DISPLAY 'value found'
           END-SEARCH.

           MOVE 4 TO TS-INDEX.

           SEARCH TEST-ARRAY 
              AT END DISPLAY 'value not found'
              WHEN VALUE-ONE(TS-INDEX) = 'ab'
                 DISPLAY 'value found'
           END-SEARCH.

           STOP RUN.

