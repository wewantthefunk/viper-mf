       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOWO4.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 HELLO-WORLD.
          02 HELLO-STRING.
             03 HS-ONE     PIC X(3).
             03 HS-TWO     PIC X(2).
          02 HELLO-SPACE   PIC X(1).
          02 WORLD-STRING.
             03 WS-ONE     PIC X(2).
             03 WS-TWO     PIC X(3).

       PROCEDURE DIVISION.

           PERFORM FIRST-PARA THRU FIRST-PARA-EXIT.

           STOP RUN.

       FIRST-PARA.

           MOVE 'hello world' TO HELLO-WORLD.

           DISPLAY 'expected value hello world'
           DISPLAY 'actual value   ' HELLO-WORLD.

       FIRST-PARA-EXIT.
           EXIT.

