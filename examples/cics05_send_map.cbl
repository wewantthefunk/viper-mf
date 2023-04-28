       ID DIVISION.
       PROGRAM-ID.    CICS05.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 TEST-DATA PIC X(8).

       01 FIRST-TIME  PIC X VALUE 'Y'.

       01 W-RESPONSE-CODE PIC S9(8) COMP.

       01 TERM-ID       PIC X(4).

       COPY RECVMAP.

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
              END-EXEC
              EXEC CICS WRITEQ TS 
                 QUEUE('CICS05Q')
                 FROM(TERM-ID)
              END-EXEC
           ELSE
              MOVE 'N' TO FIRST-TIME
              EXEC CICS RECEIVE MAP('HELLOMAP')
                 
              END-EXEC
           END-IF.           

           EXEC CICS
               RETURN
               TRANSID('CICS05')
           END-EXEC.

