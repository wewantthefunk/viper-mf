       ID DIVISION.
       PROGRAM-ID.    CICS02.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 TEST-DATA PIC X(8).


       PROCEDURE DIVISION.

           MOVE 'CICS02' TO TEST-DATA
           EXEC CICS LINK      PROGRAM ('HELLOW64')
                               COMMAREA (TEST-DATA)
                               LENGTH (LENGTH OF TEST-DATA)
           END-EXEC

           STOP RUN.