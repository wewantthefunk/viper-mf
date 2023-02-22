       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW71.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 TEST-VAL PIC X(1) VALUE '1'.

       PROCEDURE DIVISION.

           DISPLAY 'expected value: true'
           
           IF TEST-VAL = ('1' OR '2' OR '4' OR '5')
              OR TEST-VAL = '3'
              DISPLAY 'actual value:   true'
           ELSE
              DISPLAY 'actual value:   false'
           END-IF.

           STOP RUN.

