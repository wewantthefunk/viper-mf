       ID DIVISION.
       PROGRAM-ID.    CICS04.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 TEST-DATA PIC X(8).

       01 W-RESPONSE PIC 9(3).

       COPY HELLOMAP.


       PROCEDURE DIVISION.

           MOVE 'HELLOMAP' TO TEST-DATA.

           MOVE 'Developer' TO LBL2O. 

           EXEC CICS SEND MAP(TEST-DATA)
               RESP (W-RESPONSE)
           END-EXEC.

           EXEC CICS RETURN
           END-EXEC.

