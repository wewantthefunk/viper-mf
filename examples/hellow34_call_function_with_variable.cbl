       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW34.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 SUB-PROGRAM   PIC X(8) VALUE 'HELLOW35'.

       PROCEDURE DIVISION.

           DISPLAY 'expected message:'
           DISPLAY 'Called module HELLOW35'
           DISPLAY 'actual message:'
           CALL SUB-PROGRAM.

           STOP RUN.

