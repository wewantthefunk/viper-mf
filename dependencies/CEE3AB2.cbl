       IDENTIFICATION DIVISION. 
       PROGRAM-ID. CEE3AB2.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION. 

       LINKAGE SECTION. 

       01 PARAMETERS.
           05 ABEND-CODE    PIC S9(9) BINARY.
           05 REASON-CODE   PIC S9(9) BINARY.
           05 CLEANUP-CODE  PIC S9(9) BINARY.

       PROCEDURE DIVISION USING ABEND-CODE, REASON-CODE, CLEANUP-CODE.

           DISPLAY 'CEEAB2 ABEND!'.
           DISPLAY '  ABEND CODE: ' ABEND-CODE.
           DISPLAY ' REASON CODE: ' REASON-CODE.
           DISPLAY 'CLEANUP CODE: ' CLEANUP-CODE.

           STOP RUN.