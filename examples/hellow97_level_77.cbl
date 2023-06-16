       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW97.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 HELLO-WORLD    PIC X(11).

       77 LEVEL-77-TEST  PIC X(13).

       01 HAS-CHILDREN.
          03 CHILD-1     PIC X(7) VALUE 'CHILD 1'.
          03 FILLER      PIC X.
          03 CHILD-2     PIC X(7) VALUE 'CHILD 2'.

       PROCEDURE DIVISION.
           
           MOVE 'hello world' TO HELLO-WORLD.
           MOVE 'LEVEL 77 TEST' TO LEVEL-77-TEST.

           DISPLAY 'expected value hello world'
           DISPLAY 'actual value   ' HELLO-WORLD.

           DISPLAY LEVEL-77-TEST.

           DISPLAY HAS-CHILDREN.

           STOP RUN.

