       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW29.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 FILE-STATUS      PIC X(2).
       01 OTHER-STATUS     PIC X(2).

       PROCEDURE DIVISION.

           MOVE '00' TO FILE-STATUS.

           MOVE '01' TO OTHER-STATUS.

           IF FILE-STATUS = '00'
              DISPLAY 'if condition successful'
              IF OTHER-STATUS = '01'
                 DISPLAY 'nested if condition successful'
              ELSE
                 DISPLAY 'nested if condition error'
              END-IF
           ELSE
              DISPLAY 'if condition error'
           END-IF.       

           STOP RUN.

