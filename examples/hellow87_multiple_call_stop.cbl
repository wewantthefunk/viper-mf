       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW87.
       AUTHOR. CHRISTIAN STRAMA.

       PROCEDURE DIVISION.

           DISPLAY 'expected message:'
           DISPLAY 'Just Passing Through'
           DISPLAY 'actual message:'
           CALL 'HELLOW88'.

           DISPLAY 'we should not see this: returned'.

           STOP RUN.