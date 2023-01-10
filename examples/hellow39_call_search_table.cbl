       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW39.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01  PASSED-VARIABLE  PIC X(2) VALUE '00'.

       PROCEDURE DIVISION.

           DISPLAY 'expected message:'
           DISPLAY 'FILE STATUS 00 IS SUCCESSFUL COMPLETION'

           DISPLAY 'actual message:'
           CALL 'HELLOW38' USING PASSED-VARIABLE.

           DISPLAY 'expecting returned value of 00'
           DISPLAY 'actual returned value is    ' PASSED-VARIABLE.

           MOVE '97' TO PASSED-VARIABLE
           DISPLAY 'expected message:'
           DISPLAY 'FILE STATUS 97 IS FILE VERIFIED AT OPEN'

           DISPLAY 'actual message:'
           CALL 'HELLOW38' USING PASSED-VARIABLE.

           DISPLAY 'expecting returned value of 97'
           DISPLAY 'actual returned value is    ' PASSED-VARIABLE.

           MOVE '41' TO PASSED-VARIABLE
           DISPLAY 'expected message:'
           DISPLAY 'FILE STATUS 41 IS FILE ALREADY OPEN'

           DISPLAY 'actual message:'
           CALL 'HELLOW38' USING PASSED-VARIABLE.

           DISPLAY 'expecting returned value of 41'
           DISPLAY 'actual returned value is    ' PASSED-VARIABLE.

           MOVE '99' TO PASSED-VARIABLE
           DISPLAY 'expected message:'
           DISPLAY 'FILE STATUS 99 IS UNKNOWN'

           DISPLAY 'actual message:'
           CALL 'HELLOW38' USING PASSED-VARIABLE.

           DISPLAY 'expecting returned value of 99'
           DISPLAY 'actual returned value is    ' PASSED-VARIABLE.

           STOP RUN.