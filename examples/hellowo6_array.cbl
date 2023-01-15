       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOWO6.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 TEST-ARRAY OCCURS 100 TIMES INDEXED BY TS-INDEX.
           05 VALUE-ONE    PIC X(2).
           05 VALUE-TWO    PIC X(2).

       PROCEDURE DIVISION.

           MOVE 3 TO TS-INDEX.

      * display based on the broken line
           MOVE 'ab' TO 
              VALUE-ONE (1)
           DISPLAY 'expected value is ab'
           DISPLAY 'actual value is   ' 
                 VALUE-ONE
                    (1).

           MOVE 'hi' TO VALUE-ONE    (TS-INDEX).
           DISPLAY 'expected value hi'
           DISPLAY 'actual value   ' VALUE-ONE   (TS-INDEX).

      *  display a variable that hasn't been set
           DISPLAY 'next line should be blank'.
           DISPLAY VALUE-ONE(2).

      *  display a variable that isn't valid
           DISPLAY 'next line should be blank'.
           DISPLAY VALUE-ONE(101).


           STOP RUN.

