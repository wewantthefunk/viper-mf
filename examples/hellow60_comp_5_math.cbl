       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW60.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 COMP-5.
           05 TEST-FIELD.
              10 NUMBER-FIELD     PIC S9(2).
              10 NUMBER-FIELD-2   PIC S9(5).
              10 NUMBER-FIELD-3   PIC S9(5).

       PROCEDURE DIVISION.

           MOVE X'00100000FF3200001C00' TO TEST-FIELD.

           DISPLAY 'expected value is 001D12345C54321D'
           DISPLAY 'actual value is   ' TEST-FIELD.           

           DISPLAY 'expected value is 0010'
           DISPLAY 'actual value is   ' NUMBER-FIELD.

           ADD 1 TO NUMBER-FIELD.

           DISPLAY 'expected value is 0011'
           DISPLAY 'actual value is   ' NUMBER-FIELD.

           MULTIPLY NUMBER-FIELD-2 BY 2 GIVING NUMBER-FIELD-2.

           DISPLAY 'expected value is 0001FE64'
           DISPLAY 'actual value is   ' NUMBER-FIELD-2.

           STOP RUN.

