       ID DIVISION.
       PROGRAM-ID.    CICS08.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 TEST-DATA PIC X(8).

       01 WRITE-DATA PIC X(8) VALUE '12345678'.

       01 FIRST-TIME  PIC X VALUE 'Y'.

       01 W-RESPONSE-CODE PIC S9(8) COMP.

       01 QUEUE-NAME PIC X(8) VALUE 'TESTQ'.

       PROCEDURE DIVISION.

           EXEC CICS WRITEQ TS
              QUEUE(QUEUE-NAME)
              FROM(WRITE-DATA)
              RESP(W-RESPONSE-CODE)
           END-EXEC.

           EXEC CICS READQ TS
              QUEUE   (QUEUE-NAME)
                     INTO    (TEST-DATA)
                     LENGTH  (LENGTH OF TEST-DATA)
                     ITEM    (1)
                     RESP    (W-RESPONSE-CODE)
                     END-EXEC.

           DISPLAY 'expected value: 00'
           DISPLAY 'actual value:   ' W-RESPONSE-CODE 

           DISPLAY 'expected value: 12345678'
           DISPLAY 'actual value:   ' TEST-DATA

           EXEC CICS RETURN END-EXEC.