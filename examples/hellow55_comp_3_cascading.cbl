       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW55.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 SYNC.
           05 COMP-3.
              10 NESTED-COMP3-FIELD  PIC S9(5).
           05 BACK-TO-REG.
              10 BTG-1 PIC X(2).
              
       01 COMP-3.
           05 TEST-FIELD.
              10 NUMBER-FIELD     PIC S9(2).
              10 NUMBER-FIELD-2   PIC S9(5).
              10 NUMBER-FIELD-3   PIC S9(5).

       01.
           05  DISPLAY-FIELD      PIC S9(2).
           05  DISPLAY-FIELD-2    PIC S9(5).
           05  DISPLAY-FIELD-3    PIC S9(5).

       PROCEDURE DIVISION.

           MOVE X'001D12345C54321D' TO TEST-FIELD.

           DISPLAY 'expected value is ↔↕☺*ã▬↔'
           DISPLAY 'actual value is   ' TEST-FIELD.

           MOVE NUMBER-FIELD TO DISPLAY-FIELD.

           MOVE NUMBER-FIELD-2 TO DISPLAY-FIELD-2.

           MOVE NUMBER-FIELD-3 TO DISPLAY-FIELD-3.

           DISPLAY DISPLAY-FIELD.

           DISPLAY DISPLAY-FIELD-2.

           DISPLAY DISPLAY-FIELD-3.

           STOP RUN.

