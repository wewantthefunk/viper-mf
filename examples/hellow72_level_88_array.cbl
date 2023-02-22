       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW72.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 TEST-ARRAY.
          05 TEST-VAL OCCURS 5 TIMES
              INDEXED BY TA-INDEX.
             10 TV PIC X(1).
                88 ONE   VALUE '1'.
                88 TWO   VALUE '2'.

       PROCEDURE DIVISION.

           SET TWO(1) TO TRUE.

           IF TWO(1)
              DISPLAY 'true'
           END-IF.

           STOP RUN.

