       ID DIVISION.
       PROGRAM-ID.    CICS04.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 TEST-DATA PIC X(8).


       PROCEDURE DIVISION.

           MOVE 'HELLOMAP' TO TEST-DATA.

           EXEC CICS SEND MAP(TEST-DATA)
           END-EXEC.

           EXEC CICS RETURN
           END-EXEC.

