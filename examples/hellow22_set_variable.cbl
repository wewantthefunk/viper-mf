       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW22.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 HELLO-WORLD    PIC 9(3).

       01 VALUE-TWO      PIC 9(3).

       PROCEDURE DIVISION.
           
           DISPLAY 'expecting value of 001'.
           SET HELLO-WORLD TO 1.

           DISPLAY 'actual value is    ' HELLO-WORLD.

           SET VALUE-TWO TO HELLO-WORLD.

           DISPLAY 'actual value is    ' VALUE-TWO.

           STOP RUN.

