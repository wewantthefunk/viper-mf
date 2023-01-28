       ID DIVISION.
       PROGRAM-ID.    CICS05.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 TEST-DATA PIC X(8).


       PROCEDURE DIVISION.
           MOVE 'COMPMAP1' TO TEST-DATA.

           EXEC CICS SEND MAP(TEST-DATA)
           END-EXEC.

           STOP RUN.

