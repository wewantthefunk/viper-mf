       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW11.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 TEST-ARRAY OCCURS 100 TIMES INDEXED BY TS-INDEX.
           05 VALUE-ONE    PIC X(2).
           05 VALUE-TWO    PIC X(2).

       PROCEDURE DIVISION.

           MOVE 3 TO TS-INDEX.
           MOVE 'hi' TO VALUE-ONE(TS-INDEX).

           EVALUATE TRUE
              WHEN VALUE-ONE(TS-INDEX) = 'hi' 
              WHEN TS-INDEX = 3
              DISPLAY 'evaluate condition successful'
                 EVALUATE TRUE 
                    WHEN TS-INDEX = 3
                    DISPLAY 'evaluate condition successful'
                 END-EVALUATE
           END-EVALUATE.


           STOP RUN.

