       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW53.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 COMP-3-FIELD   PIC S9(5) COMP-3.

       PROCEDURE DIVISION.

           MOVE X'75110C' TO COMP-3-FIELD.

           DISPLAY 'expected value 75110C'
           DISPLAY 'actual value   ' COMP-3-FIELD.

           MOVE 12345 TO COMP-3-FIELD.

           DISPLAY 'expected value 12345C'
           DISPLAY 'actual value   ' COMP-3-FIELD.

           MOVE 1234 TO COMP-3-FIELD.

           DISPLAY 'expected value 01234C'
           DISPLAY 'actual value   ' COMP-3-FIELD.

           MOVE -11111 TO COMP-3-FIELD.

           DISPLAY 'expected value 11111D'
           DISPLAY 'actual value   ' COMP-3-FIELD.

           STOP RUN.
