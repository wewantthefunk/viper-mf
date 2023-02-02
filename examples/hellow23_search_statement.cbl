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

           DISPLAY 'expected value is value found'
           SEARCH TEST-ARRAY 
              AT END DISPLAY 'actual value is   not found'
              WHEN VALUE-ONE(TS-INDEX) = 'gh'
                 DISPLAY 'actual value is   value found'
           END-SEARCH.

           MOVE 1 TO TS-INDEX.

           DISPLAY 'expected value is value found'
           SEARCH TEST-ARRAY 
              AT END DISPLAY 'actual value is   not found'
              WHEN 'gh' = VALUE-ONE(TS-INDEX)
                 DISPLAY 'actual value is   value found'
           END-SEARCH.

           MOVE 4 TO TS-INDEX.

           DISPLAY 'expected value is value not found'
           SEARCH TEST-ARRAY 
              AT END DISPLAY 'actual value is   value not found'
              WHEN VALUE-ONE(TS-INDEX) = 'ab'
                 DISPLAY 'actual value is   value found'
           END-SEARCH.

           STOP RUN.

