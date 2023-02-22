       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW70.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 LEVEL-88-TEST PIC X(1).
           88 ONE-LIST  VALUE '1'
                              '2'.
           88 TWO-LIST  VALUE '3'
                         THRU '6'
                              'A'.

       PROCEDURE DIVISION.
           MOVE '1' TO LEVEL-88-TEST.

           DISPLAY 'expected value: True'
           EVALUATE TRUE
               WHEN ONE-LIST
                  DISPLAY 'actual value:   True'
               WHEN OTHER
                  DISPLAY 'actual value:   False'
           END-EVALUATE
           
           

           STOP RUN.

