       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW16.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01  TEST-DATA   PIC X(14) VALUE 'THIS IS A TEST'.

       PROCEDURE DIVISION.

           DISPLAY TEST-DATA.

           INSPECT TEST-DATA  
              CONVERTING  'ABCDEFGHIJ'
                                       TO  '0123456789'

           DISPLAY 'Expected output is T78S 8S 0 T4ST'
           DISPLAY 'Actual output is   '
            TEST-DATA

           STOP RUN.

