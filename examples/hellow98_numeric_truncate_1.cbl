       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW98.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 N3    PIC 9(3).
       01 SN3   PIC S9(3).

       PROCEDURE DIVISION.
           
           MOVE 1234 TO N3.

           DISPLAY 'N3=' N3.

           MOVE -1 TO N3.

           DISPLAY 'N3=' N3.
           IF N3 < 0
              DISPLAY 'N3<0'
           ELSE
              DISPLAY 'N3>=0'
           END-IF.

           MOVE -12 TO N3.

           DISPLAY 'N3=' N3.
           IF N3 < 0
              DISPLAY 'N3<0'
           ELSE
              DISPLAY 'N3>=0'
           END-IF.

           MOVE -1 TO SN3.

           DISPLAY 'SN3=' SN3.
           IF SN3 < 0
              DISPLAY 'SN3<0'
           ELSE
              DISPLAY 'SN3>=0'
           END-IF.

           MOVE -1234 TO SN3.

           DISPLAY 'SN3=' SN3.
           IF SN3 < 0
              DISPLAY 'SN3<0'
           ELSE
              DISPLAY 'SN3>=0'
           END-IF.

           STOP RUN.

