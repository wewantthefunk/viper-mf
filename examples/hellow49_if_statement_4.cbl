       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW49.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 W-DATE-2-FULLWORD PIC S9(5).

       PROCEDURE DIVISION.

           MOVE -32769 TO W-DATE-2-FULLWORD.

           DISPLAY 'expected return is OR if condition successful'.

           IF  W-DATE-2-FULLWORD    <  -32768
               OR                       >  +32767
              DISPLAY 'OR if condition successful'
           END-IF.


           STOP RUN.

