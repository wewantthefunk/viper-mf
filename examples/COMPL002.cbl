       IDENTIFICATION DIVISION.
       PROGRAM-ID. COMPL002.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01  PASSED-VARIABLE  PIC X(6).

       PROCEDURE DIVISION.

           MOVE 'TT8C8 ' TO PASSED-VARIABLE.
           CALL 'COMPL001' USING PASSED-VARIABLE.

           DISPLAY 'expecting returned value of TT8  R'
           DISPLAY 'actual returned value is    ' PASSED-VARIABLE.

           MOVE 'J4A   ' TO PASSED-VARIABLE
           CALL 'COMPL001' USING PASSED-VARIABLE.

           DISPLAY 'expecting returned value of J4A  A'
           DISPLAY 'actual returned value is    ' PASSED-VARIABLE.

           STOP RUN.