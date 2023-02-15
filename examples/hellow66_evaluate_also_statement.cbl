       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW66.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 TEST-ARRAY OCCURS 100 TIMES INDEXED BY TS-INDEX.
           05 VALUE-ONE    PIC X(2).
           05 VALUE-TWO    PIC X(2).

       PROCEDURE DIVISION.

           MOVE 3 TO TS-INDEX.
           MOVE 'hi' TO VALUE-ONE(3).

           DISPLAY 'expected message:'
           DISPLAY 'true'
           DISPLAY 'actual message:'
           EVALUATE TS-INDEX = 3
              WHEN TRUE
                 DISPLAY 'true'
           END-EVALUATE.
              

           DISPLAY ''
           DISPLAY 'expected message:'
           DISPLAY 'evaluate true/true condition successful'
           PERFORM 100-PERFORM-EVALUATE THRU 100-EXIT.

           MOVE 4 TO TS-INDEX.
           MOVE 'hi' TO VALUE-ONE(3).

           DISPLAY ''
           DISPLAY 'expected message:'
           DISPLAY 'evaluate true/false condition successful'
           PERFORM 100-PERFORM-EVALUATE THRU 100-EXIT.

           MOVE 4 TO TS-INDEX.
           MOVE 'by' TO VALUE-ONE(3).

           DISPLAY ''
           DISPLAY 'expected message:'
           DISPLAY 'evaluate false/false condition successful'
           PERFORM 100-PERFORM-EVALUATE THRU 100-EXIT.

           MOVE 3 TO TS-INDEX.
           MOVE 'no' TO VALUE-ONE(3).

           DISPLAY ''
           DISPLAY 'expected message:'
           DISPLAY 'evaluate false/true condition successful'
           PERFORM 100-PERFORM-EVALUATE THRU 100-EXIT.

           STOP RUN.

       100-PERFORM-EVALUATE.

           DISPLAY 'actual message:'
           EVALUATE VALUE-ONE(3) = 'hi' ALSO TS-INDEX = 3
              WHEN  TRUE ALSO TRUE
                 DISPLAY 'evaluate true/true condition successful'

              WHEN TRUE ALSO FALSE
                 DISPLAY 'evaluate true/false condition successful'

              WHEN FALSE ALSO FALSE
                 DISPLAY 'evaluate false/false condition successful'

              WHEN FALSE ALSO TRUE
                 DISPLAY 'evaluate false/true condition successful'

           END-EVALUATE.

       100-EXIT.
           EXIT.

