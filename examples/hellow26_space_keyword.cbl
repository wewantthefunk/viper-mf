       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW26.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 TEST-VAR  PIC X(3).

       PROCEDURE DIVISION.

           MOVE 'xxx' TO TEST-VAR.

           MOVE SPACE TO TEST-VAR.

           DISPLAY 'expected value is *   *'
           DISPLAY 'actual value is   *' TEST-VAR '*'

           IF TEST-VAR = SPACE
               DISPLAY 'actual value is correct'
           ELSE
               DISPLAY 'actual value is incorrect'
           END-IF.

           IF TEST-VAR = SPACES
               DISPLAY 'actual value is correct'
           ELSE
               DISPLAY 'actual value is incorrect'
           END-IF.
           

           STOP RUN.

