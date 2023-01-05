       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOWOR.
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

          02 WORLD-STRING-2 REDEFINES WORLD-STRING.
             03 WS-2-ONE   PIC X(3).
             03 WS-2-TWO   PIC X(2).


       PROCEDURE DIVISION.

           MOVE 'hello world' TO HELLO-WORLD.

           DISPLAY HELLO-WORLD.

           DISPLAY WS-2-TWO 

           PERFORM FIRST-PARA THRU FIRST-PARA-EXIT.

           STOP RUN.

       FIRST-PARA.

           DISPLAY 'in FIRST-PARA'.

       FIRST-PARA-EXIT.
           EXIT.

