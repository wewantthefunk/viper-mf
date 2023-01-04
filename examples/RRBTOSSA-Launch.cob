       ID DIVISION. 
       PROGRAM-ID. RRBTOSSA-LAUNCH.

       ENVIRONMENT DIVISION. 

       INPUT-OUTPUT SECTION.

       FILE-CONTROL.  

           SELECT INPUTFILE       ASSIGN TO RRBFILE
                                  FILE STATUS IS FILE-STATUS
                                  ORGANIZATION LINE SEQUENTIAL.

       DATA DIVISION.

       FILE SECTION. 

       FD INPUTFILE 
           RECORD CONTAINS 24 CHARACTERS.

       01  RRB-REC.
           02 RRB-NUMBER  PIC X(12).
           02 RRB-CONVERT-ASSERT PIC X(11).

       WORKING-STORAGE SECTION. 

       01 ERROR-COUNT PIC 9(3).

       01 FILE-STATUS PIC X(2).
       01 OUT-FILE-STATUS PIC X(2).

       01 NO-MORE-RECORDS PIC X(1) VALUE 'N'.

       01  RRBTOSSA-PARAMETERS.
           05  RP-RRB-HIC              PIC  X(12).
           05  RP-SSA-HIC              PIC  X(11).

       01 WS-CURRENT-DATE-DATA.
           05  WS-CURRENT-DATE.
               10  WS-CURRENT-YEAR         PIC 9(04).
               10  WS-CURRENT-MONTH        PIC 9(02).
               10  WS-CURRENT-DAY          PIC 9(02).
           05  WS-CURRENT-TIME.
               10  WS-CURRENT-HOURS        PIC 9(02).
               10  WS-CURRENT-MINUTE       PIC 9(02).
               10  WS-CURRENT-SECOND       PIC 9(02).
               10  WS-CURRENT-MILLISECONDS PIC 9(02).

       PROCEDURE DIVISION.

      * arrange
           MOVE FUNCTION CURRENT-DATE TO WS-CURRENT-DATE-DATA.
           MOVE 0 TO ERROR-COUNT.

           OPEN INPUT INPUTFILE.           

           PERFORM UNTIL NO-MORE-RECORDS = 'Y'

              READ INPUTFILE 
                 AT END MOVE 'Y' TO NO-MORE-RECORDS
              END-READ

              IF NO-MORE-RECORDS = 'N'
                    MOVE RRB-NUMBER TO RP-RRB-HIC
         
      * act
                    CALL 'RRBTOSSA' USING RRBTOSSA-PARAMETERS
         
      * assert

                    IF RP-SSA-HIC NOT = RRB-CONVERT-ASSERT
                       DISPLAY RP-RRB-HIC ' converted to ' RP-SSA-HIC

                       ADD 1 TO ERROR-COUNT
                    END-IF 
              END-IF

           END-PERFORM.
           
           DISPLAY 'RRBTOSSA,' WS-CURRENT-DATE-DATA ',' ERROR-COUNT.

           CLOSE INPUTFILE.

           STOP RUN.