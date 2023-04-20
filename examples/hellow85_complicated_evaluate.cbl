       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW85.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION. 

       01 TEST-ONE  PIC X VALUE '1'.

       01 TEST-NUM  PIC X(11) VALUE '1123456790A'.

       PROCEDURE DIVISION.

           IF (TEST-NUM(1:1)
                    >= X'C0'
               AND  <= X'C9')
               AND TEST-NUM(1:10)
                       NUMERIC
              DISPLAY 'if statement'
           END-IF   .

           IF (TEST-NUM(1:1)
                    >= X'C0'
               AND  <= X'C9')
               AND TEST-NUM(1:10)
                       NUMERIC
               AND TEST-NUM(2:2)
                                        = ('L '
                     OR                    'M '
                     OR                    'N ')
              DISPLAY '2nd if statement'
           END-IF   .

           EVALUATE TRUE
               WHEN (TEST-NUM(1:1) 
                          >= X'C0'
                    AND   <= X'C9')
                    AND TEST-NUM(1:10) 
                                  NUMERIC
                  DISPLAY 'test'
           END-EVALUATE       

           STOP RUN.
