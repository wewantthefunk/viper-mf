       ID DIVISION.
       PROGRAM-ID.    CICS05.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 TEST-DATA PIC X(8).

       01 FIRST-TIME  PIC X VALUE 'Y'.

       01 W-RESPONSE-CODE PIC S9(8) COMP.


       PROCEDURE DIVISION.
           MOVE 'KEYMAP' TO TEST-DATA.

           EXEC CICS READQ TS
              QUEUE   (WS-HITF-Q-NAME)
                     INTO    (TS-HITF-SESSION)
                     LENGTH  (LENGTH OF TS-HITF-SESSION)
                     ITEM    (1)
                     RESP    (W-RESPONSE-CODE)
                     END-EXEC.

           IF W-RESPONSE-CODE = ZERO 
              MOVE 'N' TO FIRST-TIME
           END-IF.

           IF FIRST-TIME = 'Y'
              EXEC CICS SEND MAP('HELLOMAP')
              END-EXEC
           ELSE
              MOVE 'N' TO FIRST-TIME
              EXEC CICS RECEIVE MAP(TEST-DATA)
              END-EXEC
           END-IF.           

           EXEC CICS
               RETURN
               TRANSID('CICS05')
           END-EXEC.

