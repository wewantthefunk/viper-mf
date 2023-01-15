       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW42.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 JUNK-VAR.
          05 LEVEL-88-VAR PIC X(1).
             88 L-ONE     VALUE '1'.
             88 L-TWO     VALUE '2'.
          05 ANOTHER-VAR  PIC X(1).

       01 LEVEL-88-TEST PIC X(1).
           88 ONE       VALUE '1'.
           88 TWO       VALUE '2'.

       PROCEDURE DIVISION.
           SET TWO TO TRUE.
           SET L-TWO TO TRUE.

           DISPLAY 'expected value False'
           DISPLAY 'actual value   ' ONE.
           DISPLAY 'expected value 2'
           DISPLAY 'actual value   ' LEVEL-88-TEST.

           SET L-ONE TO TRUE.
           MOVE 9 TO ANOTHER-VAR.

           DISPLAY 'expected value 19'
           DISPLAY 'actual value   ' JUNK-VAR.

           SET L-TWO TO TRUE.
           MOVE 8 TO ANOTHER-VAR.

           DISPLAY 'expected value 28'
           DISPLAY 'actual value   ' JUNK-VAR.

           STOP RUN.

