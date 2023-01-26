       ID DIVISION.
       PROGRAM-ID.    CICS03.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 TEST-DATA PIC X(8).

       01 TEST-DATA-NUM PIC 9(3) VALUE ZERO.


       PROCEDURE DIVISION.

           EXEC CICS HANDLE ABEND   LABEL (9990-ABEND-INTERCEPT)
                                 NOHANDLE
                                 END-EXEC

           DISPLAY 'expected message:'
           DISPLAY 'ABEND Handled by CICS Command'
           DISPLAY 'actual message'

           ADD TEST-DATA TO TEST-DATA-NUM.

           STOP RUN.


       9990-ABEND-INTERCEPT.

           DISPLAY 'ABEND Handled by CICS Command'.

