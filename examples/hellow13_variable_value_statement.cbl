       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW13.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 HELLO-WORLD    PIC X(11) VALUE 'hello world'.

       PROCEDURE DIVISION.

           DISPLAY 'expected value hello world'
           DISPLAY 'actual value   ' HELLO-WORLD.

           STOP RUN.

