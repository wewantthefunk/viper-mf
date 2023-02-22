       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW69.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 WS-LIMIT  PIC 9(3).
       01 TS-COUNT  PIC 9(3).

       01 TEST-ARRAY OCCURS 10 TO 100 TIMES 
              DEPENDING ON WS-LIMIT
              INDEXED BY TS-INDEX.
           05 VALUE-ONE    PIC X(2).
           05 VALUE-TWO    PIC X(2).

       PROCEDURE DIVISION.

           SET WS-LIMIT TO 5.

           DISPLAY 'expected value: 005'
           DISPLAY 'actual value:   ' WS-LIMIT

           PERFORM VARYING TS-INDEX FROM 1 BY 1 UNTIL
              TS-INDEX = WS-LIMIT
              DISPLAY TS-INDEX
           END-PERFORM.

           STOP RUN.

