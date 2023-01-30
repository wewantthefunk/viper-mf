       ID DIVISION.
       PROGRAM-ID.    CICS06.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 TEST-DATA PIC X(8).


       PROCEDURE DIVISION.

           DISPLAY 'in the CICS program'
           
           PERFORM 999-EXIT.

       999-EXIT.
           EXEC CICS RETURN
           END-EXEC.

