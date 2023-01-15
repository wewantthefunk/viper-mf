       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW49.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 W-DATE-2-FULLWORD PIC 9(5).

       PROCEDURE DIVISION.

           IF  W-DATE-2-FULLWORD    <  -32768
               OR                       >  +32767
              DISPLAY 'OR if condition successful'
           END-IF.


           STOP RUN.

