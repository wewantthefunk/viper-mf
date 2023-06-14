       ID DIVISION.
       PROGRAM-ID.    CICS04.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 TEST-DATA PIC X(8).

       COPY HELLOMAP.


       PROCEDURE DIVISION.

           MOVE 'HELLOMAP' TO TEST-DATA.

           MOVE 'Developer' TO LBL2O. 

           EXEC CICS SEND MAP(TEST-DATA)
           END-EXEC.

           EXEC CICS RETURN
           END-EXEC.

