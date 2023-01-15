       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW51.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 VALUE-ONE PIC X(5).

       01 ARRAY  OCCURS 5 TIMES INDEXED BY I.
           05 ARRAY-ONE  PIC X(5).

       PROCEDURE DIVISION.

           MOVE 'hello' TO VALUE-ONE.
           MOVE 1 TO I.
           MOVE 'hello' TO ARRAY(1).

           DISPLAY 'expected return is OR if condition successful'.

           IF  VALUE-ONE            =  ARRAY
                                                   (I)
              DISPLAY 'OR if condition successful'
           END-IF.


           STOP RUN.

