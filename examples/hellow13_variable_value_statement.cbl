       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW13.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 HELLO-WORLD    PIC X(11) VALUE 'hello world'.
       
       01 HELLO-WORLD-2  PIC X(13) VALUE IS 'hello world 2'.

       PROCEDURE DIVISION.

           DISPLAY 'expected value hello world'
           DISPLAY 'actual value   ' HELLO-WORLD.

           DISPLAY 'expected value hello world 2'
           DISPLAY 'actual value   ' HELLO-WORLD-2.

           STOP RUN.

