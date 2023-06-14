       IDENTIFICATION DIVISION. 
       PROGRAM-ID. CEE3ABD.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION. 

       LINKAGE SECTION. 

       01 PARAMETERS.
           05 ABEND-CODE    PIC S9(9) BINARY.
           05 CLEANUP-CODE   PIC S9(9) BINARY.

       PROCEDURE DIVISION USING ABEND-CODE, CLEANUP-CODE.

           DISPLAY 'CEE3ABD ABEND!'.
           DISPLAY '  ABEND CODE: ' ABEND-CODE.
           DISPLAY 'CLEANUP CODE: ' CLEANUP-CODE.

           STOP RUN.