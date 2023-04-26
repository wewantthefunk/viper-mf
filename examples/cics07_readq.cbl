       ID DIVISION.
       PROGRAM-ID.    CICS07.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 TEST-DATA PIC X(8).

       01 FIRST-TIME  PIC X VALUE 'Y'.

       01 W-RESPONSE-CODE PIC S9(8) COMP.

       01 QUEUE-NAME PIC X(8) VALUE 'TESTQ'.

       PROCEDURE DIVISION.

           EXEC CICS READQ TS
              QUEUE   (QUEUE-NAME)
                     INTO    (TEST-DATA)
                     LENGTH  (LENGTH OF TEST-DATA)
                     ITEM    (1)
                     RESP    (W-RESPONSE-CODE)
                     END-EXEC.

           EXEC CICS RETURN END-EXEC.