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

           DISPLAY 'expected value is ►ÿ▬∟'
           DISPLAY 'actual value is   ' TEST-FIELD.           

           DISPLAY 'expected value is 16'
           DISPLAY 'actual value is   ' NUMBER-FIELD.

           ADD 1 TO NUMBER-FIELD.

           DISPLAY 'expected value is 17'
           DISPLAY 'actual value is   ' NUMBER-FIELD.

           MULTIPLY NUMBER-FIELD-2 BY 2 GIVING NUMBER-FIELD-2.

           DISPLAY 'expected value is 130660'
           DISPLAY 'actual value is   ' NUMBER-FIELD-2.

           STOP RUN.

