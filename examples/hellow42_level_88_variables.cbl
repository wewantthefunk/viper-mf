       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW42.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 LEVEL-88-TEST PIC X(1).
           88 ONE       VALUE '1'.
           88 TWO       VALUE '2'.

       PROCEDURE DIVISION.
           SET TWO TO TRUE.

           DISPLAY 'expected value 2'
           DISPLAY 'actual value   ' LEVEL-88-TEST.

           STOP RUN.

