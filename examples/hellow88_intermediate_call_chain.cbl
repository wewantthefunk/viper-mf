       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW88.
       AUTHOR. CHRISTIAN STRAMA.

       PROCEDURE DIVISION.

           DISPLAY 'Just Passing Through'

           DISPLAY 'Expected message: End of Call Chain'
           DISPLAY 'Actual message  : '
           CALL 'HELLOW89'.

           DISPLAY 'we should not see this: returned'.

           GOBACK.