       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOWO2.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 HELLO-WORLD    PIC X(11).

       PROCEDURE DIVISION.
           
           MOVE 'hello world' TO HELLO-WORLD.

           DISPLAY HELLO-WORLD.

           STOP RUN.

