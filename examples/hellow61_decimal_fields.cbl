       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW61.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01.
           05 NUMBER-FIELD     PIC S9(2)V99.
           05 NUMBER-FIELD-2   PIC S9(5)V99.
           05 NUMBER-FIELD-3   PIC S9(5)V999.

           05 NUMBER-FIELD-4   PIC S9(5)V999 COMP-3.

           05 NUMBER-FIELD-5   PIC S9(5).

       PROCEDURE DIVISION.

           MOVE 12.34 TO NUMBER-FIELD.

           DISPLAY 'expected value is 12.34'
           DISPLAY 'actual value is   ' NUMBER-FIELD.

           MOVE 55 TO NUMBER-FIELD-2

           DISPLAY 'expected value is 00055.00'
           DISPLAY 'actual value is   ' NUMBER-FIELD-2.

           MOVE 888.11 TO NUMBER-FIELD-3

           DISPLAY 'expected value is 00888.110'
           DISPLAY 'actual value is   ' NUMBER-FIELD-3.

           MOVE 999.99 TO NUMBER-FIELD-4

           DISPLAY 'expected value is 000999990C'
           DISPLAY 'actual value is   ' NUMBER-FIELD-4.

           MOVE -123 TO NUMBER-FIELD-5

           DISPLAY 'expected value is -00123'
           DISPLAY 'actual value is   ' NUMBER-FIELD-5.

           STOP RUN.

