       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW57.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 COMP-FIELD-4-BYTE   PIC 9(5) COMP.

       01 COMP-FIELD-2-BYTE   PIC 9(2) COMP.

       01 COMP-FIELD-4-BYTE-SIGNED   PIC S9(5) COMP.

       01 COMP-FIELD-2-BYTE-SIGNED   PIC S9(2) COMP.

       PROCEDURE DIVISION.

           MOVE 99 TO COMP-FIELD-2-BYTE.

           DISPLAY 'expected value 0063'
           DISPLAY 'actual value   ' COMP-FIELD-2-BYTE.

           MOVE 99999 TO COMP-FIELD-4-BYTE.

           DISPLAY 'expected value 0001869F'
           DISPLAY 'actual value   ' COMP-FIELD-4-BYTE.

           MOVE -12 TO COMP-FIELD-2-BYTE-SIGNED.

           DISPLAY 'expected value FFF4'
           DISPLAY 'actual value   ' COMP-FIELD-2-BYTE-SIGNED.

           MOVE -99999 TO COMP-FIELD-4-BYTE-SIGNED.

           DISPLAY 'expected value FFFE7961'
           DISPLAY 'actual value   ' COMP-FIELD-4-BYTE-SIGNED.

           STOP RUN.

