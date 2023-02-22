       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW71.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 TEST-VAL PIC X(1) VALUE '1'.

       PROCEDURE DIVISION.

           IF TEST-VAL = ('1' OR '2')
              OR TEST-VAL = '3'
              DISPLAY 'true'
           END-IF.

           STOP RUN.

