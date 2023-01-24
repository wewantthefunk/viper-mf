       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW56.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 COMP-3.
           05 TEST-FIELD.
              10 NUMBER-FIELD     PIC S9(2).
              10 NUMBER-FIELD-2   PIC S9(5).
              10 NUMBER-FIELD-3   PIC S9(5).

       PROCEDURE DIVISION.

           MOVE X'001D12345C54321D' TO TEST-FIELD.

           DISPLAY 'expected value is -001+12345-54321'
           DISPLAY 'actual value is   ' TEST-FIELD.           

           DISPLAY 'expected value is -001'
           DISPLAY 'actual value is   ' NUMBER-FIELD.

           ADD 1 TO NUMBER-FIELD.

           DISPLAY 'expected value is +000'
           DISPLAY 'actual value is   ' NUMBER-FIELD.

           MULTIPLY NUMBER-FIELD-2 BY 2 GIVING NUMBER-FIELD-2.

           DISPLAY 'expected value is +24690'
           DISPLAY 'actual value is   ' NUMBER-FIELD-2.

           STOP RUN.

