       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW27.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 TEST-VAR  PIC 9(3).

       PROCEDURE DIVISION.

           MOVE '111' TO TEST-VAR.

           MOVE ZERO TO TEST-VAR.

           DISPLAY 'expected value is *000*'
           DISPLAY 'actual value is   *' TEST-VAR '*'

           IF TEST-VAR = ZERO
               DISPLAY 'actual value is correct'
           ELSE
               DISPLAY 'actual value is incorrect'
           END-IF.
           

           STOP RUN.

