       ID DIVISION.
       PROGRAM-ID.    CICS04.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 TEST-DATA PIC X(8).


       PROCEDURE DIVISION.

           EXEC CICS SEND MAP('TESTMAP')
           END-EXEC.

           MOVE 'TESTMAP' TO TEST-DATA.

           EXEC CICS SEND MAP(TEST-DATA)
           END-EXEC.

           STOP RUN.

