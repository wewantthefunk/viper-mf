       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW78.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 SUB-PROGRAM   PIC X(8) VALUE 'HELLOW37'.

       PROCEDURE DIVISION.

           DISPLAY 'expected message:'
           DISPLAY 'Called module HELLOW37 content *'
           DISPLAY 'actual message:'
           CALL SUB-PROGRAM USING CONTENT 'content'.

           STOP RUN.

