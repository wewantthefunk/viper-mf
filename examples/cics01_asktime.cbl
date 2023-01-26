       ID DIVISION.
       PROGRAM-ID.    CICS01.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 WS-ABSTIME   PIC S9(15).


       PROCEDURE DIVISION.

           EXEC CICS        ASKTIME  ABSTIME(WS-ABSTIME)
           END-EXEC

           EXEC CICS        ASKTIME
           END-EXEC

           STOP RUN.