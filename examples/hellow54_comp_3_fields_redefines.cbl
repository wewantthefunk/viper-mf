       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW54.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 TOP-LEVEL.
           05 TEST-FIELD     PIC X(5).
           05 TEST-FIELD-2 REDEFINES TEST-FIELD.
              10 NUMBER-FIELD   PIC 9(2).
              10 COMP-3-FIELD   PIC S9(5) COMP-3.
           05 REDEFINES TEST-FIELD.
              10 NUM-FIELD-2    PIC 9(2).
              10 COMP-3-FIELD-2 PIC 9(5) COMP-3.

       PROCEDURE DIVISION.

           MOVE X'F3F0123450' TO TEST-FIELD.

           DISPLAY 'expected value is 30↕☺&'
           DISPLAY '(note: linux may not show some characters)'
           DISPLAY 'actual value is   ' TEST-FIELD.

           DISPLAY 'expected value is +12345'
           DISPLAY 'actual value is   ' COMP-3-FIELD.

           DISPLAY 'expected value is 12345'
           DISPLAY 'actual value is   ' COMP-3-FIELD-2.

           MOVE X'F4F254321D' TO TEST-FIELD.

           DISPLAY 'expected value is 42ã▬↔'
           DISPLAY '(note: linux may not show some characters)'
           DISPLAY 'actual value is   ' TEST-FIELD.

           DISPLAY 'expected value is -54321'
           DISPLAY 'actual value is   ' COMP-3-FIELD.

           DISPLAY 'expected value is 54321'
           DISPLAY 'actual value is   ' COMP-3-FIELD-2.

           DISPLAY 'expected value is 42ã▬↔'
           DISPLAY 'actual value is   ' TEST-FIELD-2.

           STOP RUN.

