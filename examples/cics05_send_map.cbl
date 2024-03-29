       ID DIVISION.
       PROGRAM-ID.    CICS05.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 TEST-DATA PIC X(10).

       01 TEST-AREA PIC X(200).

       01 FIRST-TIME  PIC X VALUE 'Y'.

       01 W-RESPONSE-CODE PIC S9(8) COMP.

       01 TERM-ID       PIC X(4).

       COPY RECVMAP.

       COPY HELLOMAP.

       PROCEDURE DIVISION.
           MOVE EIBTRMID TO TERM-ID.

           EXEC CICS READQ TS
              QUEUE   ('CICS05Q')
                     INTO    (TERM-ID)
                     LENGTH  (LENGTH OF TERM-ID)
                     ITEM    (1)
                     RESP    (W-RESPONSE-CODE)
                     END-EXEC.

           IF W-RESPONSE-CODE = ZERO 
              MOVE 'N' TO FIRST-TIME
           END-IF.

           IF FIRST-TIME = 'Y'
              EXEC CICS SEND MAP('RECVMAP')
                 RESP(W-RESPONSE-CODE)
              END-EXEC
              EXEC CICS WRITEQ TS 
                 QUEUE('CICS05Q')
                 FROM(TERM-ID)
              END-EXEC

              PERFORM RETURN-CONTROL
           ELSE
              MOVE 'N' TO FIRST-TIME
              EXEC CICS RECEIVE MAP('RECVMAP')
                 INTO (TEST-AREA)
                 RESP(W-RESPONSE-CODE)
              END-EXEC

              MOVE NAMEO TO HLBL2I

              EXEC CICS SEND MAP('HELLOMAP')
                 RESP(W-RESPONSE-CODE)
              END-EXEC

              PERFORM RETURN-TO-CICS
           END-IF.           

       RETURN-CONTROL.
           EXEC CICS
               RETURN
               TRANSID('CICS05')
           END-EXEC.

       RETURN-TO-CICS.

           EXEC CICS
             RETURN
           END-EXEC.

