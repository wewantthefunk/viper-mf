       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW73.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 TEST-VAR PIC X(2) VALUE LOW-VALUES.

       PROCEDURE DIVISION.
           DISPLAY 'expected value: true'
           IF TEST-VAR = LOW-VALUES
              DISPLAY 'actual value:   true'
           ELSE
              DISPLAY 'actual value:   false'
           END-IF.

           MOVE HIGH-VALUES TO TEST-VAR.

           DISPLAY 'expected value: true'
           IF TEST-VAR = HIGH-VALUES
              DISPLAY 'actual value:   true'
           ELSE
              DISPLAY 'actual value:   false'
           END-IF.

           STOP RUN.

