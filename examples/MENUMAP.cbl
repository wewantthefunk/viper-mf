       ID DIVISION.
       PROGRAM-ID.    MENUMAP.
       ENVIRONMENT DIVISION.
             
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  BEGIN-WS                    PIC X(40) VALUE
           '**MENUMAP WORKING STORAGE BEGINS HERE** ' .

      ****************************************************************
      *    MISCELLANEOUS SWITCHES                                    *
      ****************************************************************
       01  MISC-SWITCHES.
           05  CICS-ERROR-SW           PIC XXX VALUE 'NO'.
               88  CICS-ERROR                  VALUE 'YES'.
           05  CICS-ABEND-ERROR-SW     PIC XXX VALUE 'NO'.
               88  CICS-ABEND-ERROR            VALUE 'YES'.
           05  ERROR-SW                PIC XXX VALUE 'YES'.
               88  EDIT-OKAY                   VALUE 'YES'.
               88  EDIT-NOT-OKAY               VALUE 'NO '.
                 
      ****************************************************************
      *    COPYLIB MNUCPY - DSECT (MAP) FOR MNUCPY                   *
      ****************************************************************
           COPY MENUCPY.
                 
      ****************************************************************
      *    WORKING STORAGE FOR COM AREA                              *
      ****************************************************************
       01  WS-COM-AREA.
           05  WS-CA-MAP-NO            PIC X(01).
               88  FIRST-TIME          VALUE ' '.
           05  WS-CA-SITE-NO           PIC 9(02).

       01  COMM-AREA-LENGTH            PIC S9(04)  COMP VALUE +0003.

      ****************************************************************
      *    MISCELLANEOUS WORK AREAS                                  *
      ****************************************************************
       01  MISC-WORK-AREA.
           05  WS-RETURN-CODE          PIC S9(08) COMP VALUE ZEROS.
           05  WS-END-LOAD             PIC S9(03) COMP-3 VALUE +19.
           05  WS-SYSTEM-ERROR         PIC  X(80) VALUE SPACES.
           05  PREV-SITE-NUM           PIC  9(02) VALUE ZERO.
           05  WS-CONTR-NAME           PIC  X(40) VALUE SPACES.
           05  FILLER REDEFINES WS-CONTR-NAME.
               10  WS-PF-KEY           PIC  X(06).
               10  WS-DISPLAY-NAME     PIC  X(34).
           05  WS-SITE-NO-A            PIC  X(02) VALUE ZEROS.
           05  WS-SITE-NO REDEFINES
               WS-SITE-NO-A            PIC  9(02).
           05  WS-MNU001OC-RESCOUNT    PIC  S9(08) COMP VALUE +0000.
           05  WS-CURSOR-POS           PIC  S9(04) COMP VALUE -0001.
           05  WS-START-TIME           PIC  S9(07) COMP VALUE ZERO.
           05  WS-COMPL-TIME           PIC  S9(07) COMP VALUE ZERO.
           05  WS-SUB-TIME             PIC  S9(07) COMP VALUE ZERO.
           05  WS-CONV-START-DATE-1900 PIC  S9(07) COMP VALUE ZERO.
           05  WS-CONV-COMPL-DATE-1900 PIC  S9(07) COMP VALUE ZERO.
           05  WS-CONV-RESUB-DATE-1900 PIC  S9(07) COMP VALUE ZERO.
                 
      ****************************************************************
      * WORK AREA FOR REFORMATTING SYSTEM TIME & DATE BEFORE DISPLAY *
      ****************************************************************
       01  WS-WORK-DATES-TIMES.
           05  WS-TASK-ASKTIME.
               10  WS-TSK-ASKTIME-SEC  PIC X(6).
               10  WS-TSK-ASKTIME-HUND PIC S9(3) COMP-3.
           05  WS-TASK-DATE.
               10  WS-TASK-DATE-MM     PIC 9(2).
               10  FILLER              PIC X          VALUE '/'.
               10  WS-TASK-DATE-DD     PIC 9(2).
               10  FILLER              PIC X          VALUE '/'.
               10  WS-TASK-DATE-YYYY   PIC 9(4).
           05  WS-GREG-DATE            PIC 9(6)       VALUE ZEROS.
           05  WS-WORK-DATE            PIC 9(7)       VALUE ZEROS.
           05  WS-WORK-DATE-NO REDEFINES
               WS-WORK-DATE.
               10  FILLER              PIC X.
               10  WS-WORK-DATE-CENT   PIC 9.
               10  WS-WORK-DATE-YEAR   PIC 9(2).
               10  WS-WORK-DATE-DAYS   PIC 9(3).
           05  WS-WORK-TIME            PIC 9(7)       VALUE ZEROS.
           05  WS-WORK-TIME-NO REDEFINES
               WS-WORK-TIME.
               10  FILLER              PIC X.
               10  WS-WORK-TIME-NO-HR  PIC 9(2).
               10  WS-WORK-TIME-NO-MIN PIC 9(2).
               10  WS-WORK-TIME-NO-SEC PIC 9(2).
           05  WS-TASK-TIME-NO.
               10  WS-TASK-TIME-NO-HR  PIC 9(2).
               10  WS-TASK-TIME-NO-MIN PIC 9(2).
               10  WS-TASK-TIME-NO-SEC PIC 9(2).
           05  WS-TASK-TIME-NO-NUM REDEFINES
               WS-TASK-TIME-NO         PIC 9(6).
           05  WS-TASK-TIME            PIC X(8)       VALUE '00:00:00'.
           05  WS-TASK-TIME-NUM  REDEFINES
               WS-TASK-TIME.
               10  WS-TASK-TIME-HR     PIC 9(2).
               10  FILLER              PIC X.
               10  WS-TASK-TIME-MIN    PIC 9(2).
               10  FILLER              PIC X.
               10  WS-TASK-TIME-SEC    PIC 9(2).
                 
      ****************************************************************
      *    CONSTANTS WORK AREA                                       *
      ****************************************************************
       01  WS-CONSTANTS.
           05  WS-INTERVAL         PIC S9(7) COMP-3   VALUE +0000000.
           05  WS-THIS-TRANS       PIC X(4)           VALUE 'MENU'.
           05  WS-START-TRANS1     PIC X(4)           VALUE 'MEN1'.
           05  WS-START-TRANS2     PIC X(4)           VALUE 'MEN2'.
           05  WS-START-TRANS3     PIC X(4)           VALUE 'MEN3'.
           05  WS-START-TRANS4     PIC X(4)           VALUE 'MEN4'.
           05  WS-START-TRANS5     PIC X(4)           VALUE 'MEN5'.
           05  WS-TRAN-RUN         PIC X(4)           VALUE 'MRUN'.
           05  WS-MNUCCNTL         PIC X(8)           VALUE 'MENCCNTL'.
           05  WS-PROGRAM-ID       PIC X(8)           VALUE 'MENCMENU'.
           05  WS-REQID            PIC X(8)           VALUE 'MENCCNTL'.
           05  C-CMNDATCV          PIC X(8)           VALUE 'CMNDATCV'.

           05  WS-18TH-CENT        PIC 9(2)           VALUE 18.
           05  WS-19TH-CENT        PIC 9(2)           VALUE 19.
           05  WS-20TH-CENT        PIC 9(2)           VALUE 20.
      ****************************************************************
      *    MNU ERROR ROUTINE - COPYBOOK
      ****************************************************************
       COPY ERR020W.

      ****************************************************************
      *    DATE CONVERSION   - COPYBOOK
      ****************************************************************
       COPY DATEAREA.

      ****************************************************************
      *    CICS DFHAID - FOR PF KEY USAGE                            *
      ****************************************************************
       COPY DFHAID.
                 
      *
                 
       01  END-WS                           PIC X(23) VALUE
               '**END WORKING STORAGE**'.
             
      ****************************************************************
      *    BEGINNING OF THE LINKAGE SECTION                          *
      ****************************************************************
       LINKAGE SECTION.
       01  DFHCOMMAREA                      PIC X(03).
       01  POINTERS.
           05  BLL-CELL-POINTER         PIC S9(08) COMP.
           05  CW020M1-POINTER          PIC S9(08) COMP.
       01  CW020M1-DSECT.
           05  CW020M1-RESPONSE    PIC X(11) OCCURS 91 TIMES.
                 
       PROCEDURE DIVISION.
      ****************************************************************
      *    BEGINNING OF THE PROCEDURE DIVISION -- MAIN LINE PROCESS  *
      ****************************************************************

       0000-MAIN-LINE.

           PERFORM 1000-INITIAL-PROCESS-CHECK
              THRU 1000-EXIT.

           PERFORM 2000-MAIN-PROCESS
              THRU 2000-EXIT.

           GO TO 6000-TERMINATION-ROUTINE.

      *****************************************************************
      *  CHECK FOR ERRORS AND PF KEY EXITS.                           *
      *****************************************************************
       1000-INITIAL-PROCESS-CHECK.

           IF EIBCALEN > 0
               MOVE DFHCOMMAREA TO WS-COM-AREA
           ELSE
               MOVE SPACES TO WS-COM-AREA.

           MOVE LOW-VALUES  TO  MNUMMNUO.
           MOVE EIBTRMID    TO TERMO.

           MOVE EIBTIME TO WS-WORK-TIME.
           COMPUTE WS-WORK-DATE = EIBDATE + 1900000.

           MOVE WS-WORK-TIME-NO-HR
            TO  WS-TASK-TIME-NO-HR
                WS-TASK-TIME-HR.

           MOVE WS-WORK-TIME-NO-MIN
            TO  WS-TASK-TIME-NO-MIN
                WS-TASK-TIME-MIN.

           MOVE WS-WORK-TIME-NO-SEC
            TO  WS-TASK-TIME-NO-SEC
                WS-TASK-TIME-SEC.

           SET FORMAT-1-YYYYDDD
               FORMAT-2-MMDDYYYY
               FUNC-CONV-THE-DATE   TO TRUE.
           MOVE WS-WORK-DATE        TO W-DATE-1-7
      
           CALL C-CMNDATCV  USING  W-DATE-AREA                          
      
           IF CONVERT-RET-GOOD
              MOVE W-DATE-2-8 (1:2)
                TO WS-TASK-DATE-MM
              MOVE W-DATE-2-8 (3:2)
                TO WS-TASK-DATE-DD
              MOVE W-DATE-2-8 (5:4)
                TO WS-TASK-DATE-YYYY
           ELSE
              MOVE 'INVALID DATE CONVERSION '
                TO  MESSAGEO
              PERFORM 4100-DISPLAY-REFRSH-MAP
                 THRU 4100-EXIT
              GO TO 6000-TERMINATION-ROUTINE.

            EXEC CICS
               ASSIGN APPLID(SYSTEMO)
                      USERID(USERO)
            END-EXEC.


       00100-EXIT.
           EXIT.
       1000-EXIT.
           EXIT.
                 
      *****************************************************************
      *  PROCESS A REQUEST.                                          *
      *****************************************************************
       2000-MAIN-PROCESS.

           IF EIBCALEN GREATER THAN ZERO
              IF EIBAID EQUAL DFHPF3
              OR EIBAID EQUAL DFHCLEAR
                   GO TO 9900-EXIT-SYSTEM
              ELSE
                   GO TO 3000-EDIT-INPUT
           ELSE
               PERFORM 2100-FIRST-TIME
                   THRU 2100-EXIT.
       2000-EXIT.
           EXIT.
                 
       2100-FIRST-TIME.

           MOVE WS-TASK-DATE TO DATEO.
           MOVE WS-TASK-TIME TO TIMEO.

           PERFORM 4000-DISPLAY-MAP
              THRU 4000-EXIT.

           MOVE '1' TO WS-CA-MAP-NO.

       2100-EXIT.
           EXIT.
       3000-EDIT-INPUT.

           PERFORM 5000-RECEIVE-MAP
              THRU 5000-EXIT.

           MOVE WS-TASK-DATE TO DATEO.
           MOVE WS-TASK-TIME TO TIMEO.

           IF SELECTL > 0
              IF SELECTI NUMERIC
                 IF SELECTI = 1
                    GO TO 3100-START-TRANS1
                 ELSE
                 IF SELECTI = 2
                    GO TO 3200-START-TRANS2
                 ELSE
                 IF SELECTI = 3
                    GO TO 3300-START-TRANS3
                 ELSE
                 IF SELECTI = 4
                    GO TO 3400-START-TRANS4
                 ELSE
                 IF SELECTI = 5
                    GO TO 3500-START-TRANS5
                 ELSE
                    MOVE 'ENTER A VALID SELECTION ' TO MESSAGEO
                    PERFORM 4100-DISPLAY-REFRSH-MAP
                       THRU 4100-EXIT
                    GO TO 6000-TERMINATION-ROUTINE
                 END-IF
                 END-IF
                 END-IF
                 END-IF
              ELSE
                IF SELECTI EQUAL 'X'
                  GO TO 9900-EXIT-SYSTEM
                ELSE
                  MOVE 'ENTER A VALID SELECTION ' TO MESSAGEO
                  PERFORM 4100-DISPLAY-REFRSH-MAP
                     THRU 4100-EXIT
                  GO TO 6000-TERMINATION-ROUTINE
                END-IF
              END-IF
           ELSE
              MOVE 'PLEASE ENTER SELECTION ' TO MESSAGEO
              PERFORM 4100-DISPLAY-REFRSH-MAP
                 THRU 4100-EXIT
              GO TO 6000-TERMINATION-ROUTINE
           END-IF.

       3100-START-TRANS1.

           EXEC CICS
               START INTERVAL(WS-INTERVAL)
               TRANSID(WS-START-TRANS1)
               TERMID(EIBTRMID)
               REQID(WS-REQID)
               NOHANDLE
               RESP(WS-RETURN-CODE)
           END-EXEC.

           IF WS-RETURN-CODE = DFHRESP(NORMAL)
               GO TO 9900-EXIT-SYSTEM
           ELSE
               MOVE ' UNABLE TO START STATUS PROGRAM'
                 TO  MESSAGEO.
              MOVE '03100'
                TO  MNU020W-ERROR-PARA
              MOVE 'STR TRAN'
                TO  MNU020W-ERROR-LITERAL
              MOVE WS-START-TRANS1
                TO  MNU020W-ERROR-VALUE
              PERFORM 9000-ERROR
                 THRU 9000-EXIT
              PERFORM 4100-DISPLAY-REFRSH-MAP
                 THRU 4100-EXIT
              GO TO 6000-TERMINATION-ROUTINE.

       3200-START-TRANS2.

           EXEC CICS
               INQUIRE PROGRAM(WS-MNUCCNTL)
               RESCOUNT(WS-MNU001OC-RESCOUNT)
               NOHANDLE
               RESP(WS-RETURN-CODE)
           END-EXEC.

           IF WS-MNU001OC-RESCOUNT = 0
               EXEC CICS
                   CANCEL
                   TRANSID(WS-TRAN-RUN)
                   REQID(WS-REQID)
                   NOHANDLE
                   RESP (WS-RETURN-CODE)
               END-EXEC
               IF WS-RETURN-CODE = DFHRESP(NORMAL)
                  GO TO 3200-START-TRANS2
               ELSE
               IF WS-RETURN-CODE = DFHRESP(NOTFND)
                  NEXT SENTENCE
               ELSE
                  MOVE '03200'
                    TO  MNU020W-ERROR-PARA
                  MOVE 'CAN TRAN'
                    TO  MNU020W-ERROR-LITERAL
                  MOVE WS-TRAN-RUN
                    TO  MNU020W-ERROR-VALUE
                  PERFORM 9000-ERROR
                     THRU 9000-EXIT
                 PERFORM 4100-DISPLAY-REFRSH-MAP
                    THRU 4100-EXIT
                  GO TO 6000-TERMINATION-ROUTINE
           ELSE
               MOVE ' MNUCCNTL RUNNING TRY AGAIN IN A FEW SECONDS '
                 TO  MESSAGEO
               PERFORM 4100-DISPLAY-REFRSH-MAP
                  THRU 4100-EXIT
              GO TO 6000-TERMINATION-ROUTINE.

           EXEC CICS
               START INTERVAL(WS-INTERVAL)
               TRANSID(WS-START-TRANS2)
               TERMID(EIBTRMID)
               REQID(WS-REQID)
               NOHANDLE
               RESP(WS-RETURN-CODE)
           END-EXEC.

           IF WS-RETURN-CODE = DFHRESP(NORMAL)
              GO TO 9900-EXIT-SYSTEM
           ELSE
              MOVE '03200'
                TO  MNU020W-ERROR-PARA
              MOVE 'STR TRAN'
                TO  MNU020W-ERROR-LITERAL
              MOVE WS-START-TRANS2
                TO  MNU020W-ERROR-VALUE
              PERFORM 9000-ERROR
                 THRU 9000-EXIT
             PERFORM 4100-DISPLAY-REFRSH-MAP
                THRU 4100-EXIT
             GO TO 6000-TERMINATION-ROUTINE.

       3300-START-TRANS3.

           EXEC CICS
               INQUIRE PROGRAM(WS-MNUCCNTL)
               RESCOUNT(WS-MNU001OC-RESCOUNT)
               NOHANDLE
               RESP(WS-RETURN-CODE)
           END-EXEC.

           IF WS-MNU001OC-RESCOUNT = 0
              EXEC CICS
                  START INTERVAL(WS-INTERVAL)
                  TRANSID(WS-START-TRANS3)
                  TERMID(EIBTRMID)
                  REQID(WS-REQID)
                  NOHANDLE
                  RESP(WS-RETURN-CODE)
              END-EXEC
              IF WS-RETURN-CODE = DFHRESP(NORMAL)
                 GO TO 9900-EXIT-SYSTEM
              ELSE
                 MOVE '03200'
                   TO  MNU020W-ERROR-PARA
                 MOVE 'STR TRAN'
                   TO  MNU020W-ERROR-LITERAL
                 MOVE WS-START-TRANS2
                   TO  MNU020W-ERROR-VALUE
                 PERFORM 9000-ERROR
                    THRU 9000-EXIT
                PERFORM 4100-DISPLAY-REFRSH-MAP
                   THRU 4100-EXIT
                GO TO 6000-TERMINATION-ROUTINE
           ELSE
              MOVE ' MNUCCNTL RUNNING TRY AGAIN IN A FEW SECONDS '
                TO  MESSAGEO
              PERFORM 4100-DISPLAY-REFRSH-MAP
                 THRU 4100-EXIT
              GO TO 6000-TERMINATION-ROUTINE.

       3400-START-TRANS4.

           EXEC CICS
               START INTERVAL(WS-INTERVAL)
               TRANSID(WS-START-TRANS4)
               TERMID(EIBTRMID)
               REQID(WS-REQID)
               NOHANDLE
               RESP(WS-RETURN-CODE)
           END-EXEC.

           IF WS-RETURN-CODE = DFHRESP(NORMAL)
               GO TO 9900-EXIT-SYSTEM
           ELSE
              MOVE '03400'
                TO  MNU020W-ERROR-PARA
              MOVE 'STR TRAN'
                TO  MNU020W-ERROR-LITERAL
              MOVE WS-START-TRANS4
                TO  MNU020W-ERROR-VALUE
              PERFORM 9000-ERROR
                 THRU 9000-EXIT
              PERFORM 4100-DISPLAY-REFRSH-MAP
                 THRU 4100-EXIT
              GO TO 6000-TERMINATION-ROUTINE.

       3500-START-TRANS5.
      
           EXEC CICS
               START INTERVAL(WS-INTERVAL)
               TRANSID(WS-START-TRANS5)
               TERMID(EIBTRMID)
               REQID(WS-REQID)
               NOHANDLE
               RESP(WS-RETURN-CODE)
           END-EXEC.
      
           IF WS-RETURN-CODE = DFHRESP(NORMAL)
               GO TO 9900-EXIT-SYSTEM
           ELSE
               MOVE ' UNABLE TO START FPS PROGRAM'
                 TO  MESSAGEO.
              MOVE '03500'
                TO  MNU020W-ERROR-PARA
              MOVE 'FPS TRAN'
                TO  MNU020W-ERROR-LITERAL
              MOVE WS-START-TRANS5
                TO  MNU020W-ERROR-VALUE
              PERFORM 9000-ERROR
                 THRU 9000-EXIT
              PERFORM 4100-DISPLAY-REFRSH-MAP
                 THRU 4100-EXIT
              GO TO 6000-TERMINATION-ROUTINE.

       4000-DISPLAY-MAP.

           MOVE WS-CURSOR-POS TO SELECTL.

           EXEC CICS SEND MAP ('MNUMMNU')
               FROM     (MNUMMNUI)
               ERASE
               CURSOR
               FREEKB
               NOHANDLE
               RESP     (WS-RETURN-CODE)
           END-EXEC.

           IF WS-RETURN-CODE = DFHRESP(NORMAL)
              NEXT SENTENCE
           ELSE
              MOVE '04000'
                TO  MNU020W-ERROR-PARA
              MOVE 'SND MAP'
                TO  MNU020W-ERROR-LITERAL
              MOVE 'MNUMMNU'
                TO  MNU020W-ERROR-VALUE
              PERFORM 9000-ERROR
                 THRU 9000-EXIT
              PERFORM 4700-SEND-SYSTEM-ERROR
                 THRU 4700-EXIT
              GO TO 6000-TERMINATION-ROUTINE.

       4000-EXIT.
           EXIT.
                 

       4100-DISPLAY-REFRSH-MAP.

           MOVE WS-CURSOR-POS TO SELECTL.

           EXEC CICS SEND MAP ('MNUMMNU')
               FROM     (MNUMMNUI)
               DATAONLY
               FREEKB
               CURSOR
               NOHANDLE
               RESP     (WS-RETURN-CODE)
           END-EXEC.

           IF WS-RETURN-CODE = DFHRESP(NORMAL)
              NEXT SENTENCE
           ELSE
              MOVE '04100'
                TO  MNU020W-ERROR-PARA
              MOVE 'SND MAP'
                TO  MNU020W-ERROR-LITERAL
              MOVE 'MNUMMNU'
                TO  MNU020W-ERROR-VALUE
              PERFORM 9000-ERROR
                 THRU 9000-EXIT
              PERFORM 4700-SEND-SYSTEM-ERROR
                 THRU 4700-EXIT
              GO TO 6000-TERMINATION-ROUTINE.

       4100-EXIT.
           EXIT.

       4700-SEND-SYSTEM-ERROR.

           EXEC CICS SEND TEXT
               FROM     (MESSAGEO)
               LENGTH   (80)
               FREEKB
               ERASE
               NOHANDLE
               RESP     (WS-RETURN-CODE)
           END-EXEC.

           IF WS-RETURN-CODE = DFHRESP(NORMAL)
              NEXT SENTENCE
           ELSE
              MOVE '04700'
                TO  MNU020W-ERROR-PARA
              MOVE 'SND TXT'
                TO  MNU020W-ERROR-LITERAL
              MOVE 'MNUMMNU'
                TO  MNU020W-ERROR-VALUE
              PERFORM 9000-ERROR
                 THRU 9000-EXIT
              GO TO 9900-EXIT-SYSTEM.

       4700-EXIT.
           EXIT.
                 
       5000-RECEIVE-MAP.

           EXEC CICS RECEIVE MAP ('MNUMMNU')
               INTO (MNUMMNUI)
               NOHANDLE
               RESP (WS-RETURN-CODE)
           END-EXEC.

           IF WS-RETURN-CODE = DFHRESP(NORMAL)
              NEXT SENTENCE
           ELSE
              MOVE '05000'
                TO  MNU020W-ERROR-PARA
              MOVE 'REC MAP'
                TO  MNU020W-ERROR-LITERAL
              MOVE 'MNUMMNU'
                TO  MNU020W-ERROR-VALUE
              PERFORM 9000-ERROR
                 THRU 9000-EXIT
              PERFORM 4100-DISPLAY-REFRSH-MAP
                 THRU 4100-EXIT
              GO TO 6000-TERMINATION-ROUTINE.

       5000-EXIT.
           EXIT.
                 
       6000-TERMINATION-ROUTINE.

           EXEC CICS RETURN
               TRANSID(WS-THIS-TRANS)
               COMMAREA(WS-COM-AREA)
               LENGTH(COMM-AREA-LENGTH)
           END-EXEC.              
                 
       9000-ERROR.
           EXEC CICS LOAD
              PROGRAM('MNUCKXRS')
              SET(ADDRESS OF CW020M1-DSECT)
           END-EXEC.

           COMPUTE MNU020W-RESPONSE-CODE EQUAL WS-RETURN-CODE.
           MOVE WS-PROGRAM-ID TO MNU020W-ERROR-PROGRAM.
           MOVE CW020M1-RESPONSE(MNU020W-RESPONSE-CODE)
             TO MNU020W-ERROR.

            MOVE MNU020W-ERROR-MESSAGE
              TO   MESSAGEO.

       9000-EXIT.
           EXIT.

      *****************************************************************
      *  PROCESS ERROR CONDITIONS.                                    *
      *****************************************************************

       9900-EXIT-SYSTEM.
           MOVE SPACES TO WS-SYSTEM-ERROR.
           EXEC CICS SEND TEXT
               FROM     (MESSAGEO)
               LENGTH   (80)
               FREEKB
               ERASE
               NOHANDLE
               RESP     (WS-RETURN-CODE)
           END-EXEC.
      
           IF WS-RETURN-CODE = DFHRESP(NORMAL)
              NEXT SENTENCE
           ELSE
      *       **********************************************
      *       * THESE VALUES ARE ONLY USED FOR INTERACTIVE *
      *       * DEBUGGING IF THE ABOVE SEND TEXT FAILS     *
      *       **********************************************
              MOVE '09900'
                TO  MNU020W-ERROR-PARA
              MOVE 'SND TXT'
                TO  MNU020W-ERROR-LITERAL
              MOVE 'MNUMMNU'
                TO  MNU020W-ERROR-VALUE
           END-IF.

           EXEC CICS RETURN
               END-EXEC.

