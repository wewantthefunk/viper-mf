       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW10.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 TEST-ARRAY OCCURS 100 TIMES INDEXED BY TS-INDEX.
           05 VALUE-ONE    PIC X(2).
           05 VALUE-TWO    PIC X(2).

       PROCEDURE DIVISION.

           DISPLAY 'exepcted value evaluate condition successful'
           DISPLAY '               evaluate condition successful'
           MOVE 3 TO TS-INDEX.
           MOVE 'hi' TO VALUE-ONE(TS-INDEX).

           EVALUATE TRUE
              WHEN VALUE-ONE(TS-INDEX) = 'hi' 
              WHEN TS-INDEX = 3
              DISPLAY 'evaluate condition successful'
           END-EVALUATE.

           EVALUATE TRUE 
              WHEN TS-INDEX = 3
              DISPLAY 'evaluate condition successful'
           END-EVALUATE.


           STOP RUN.

