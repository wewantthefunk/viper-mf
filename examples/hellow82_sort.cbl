       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW82.
       AUTHOR. CHRISTIAN STRAMA.

       ENVIRONMENT DIVISION. 

       INPUT-OUTPUT SECTION. 
       FILE-CONTROL.

           SELECT SORT-WORK-1    ASSIGN NODDNAME.

       DATA DIVISION.

       FILE SECTION. 

       SD  SORT-WORK-1
           RECORD 22.

       01  SORT-RECORD-1. 
           05 SORT-KEY   PIC X(4).
           05 SORT-DATA  PIC X(11).
           05 FILLER     PIC X(1).
           05 SORT-DATA-CNT PIC X(2).
           05 SORT-SUB-KEY PIC X(4).

       WORKING-STORAGE SECTION.

       01  KEY-INFO.

           05 KEY-LEN  PIC 9(2).
           05 NEW-KEY  PIC X(4).

       01 COUNTER PIC 9(2).

       01 IS-END-OF-SORT  PIC X.
           88 NOT-END-OF-SORT  VALue 'N'.
           88 END-OF-SORT   VALUE 'Y'.

       PROCEDURE DIVISION.

           SORT SORT-WORK-1 ASCENDING SORT-KEY
                                      SORT-SUB-KEY 
              INPUT PROCEDURE IS 100-SORT-INPUT THRU 100-EXIT
              OUTPUT PROCEDURE IS 200-SORT-OUTPUT THRU 200-EXIT

           STOP RUN.

       100-SORT-INPUT.

           DISPLAY 'sort input'.

           MOVE 4 TO KEY-LEN.

      *  LOAD THE SORT ARRAY WITH RECORDS. THIS IS PROBABLY A LOOP

           PERFORM VARYING COUNTER FROM 1 BY 1 UNTIL COUNTER = 11

              CALL 'RANDSTR' USING KEY-LEN, NEW-KEY

              MOVE '1234' TO NEW-KEY
              MOVE NEW-KEY TO SORT-KEY

              CALL 'RANDSTR' USING KEY-LEN, NEW-KEY

              MOVE NEW-KEY TO SORT-SUB-KEY 

              MOVE 'test record' TO SORT-DATA

              MOVE COUNTER TO SORT-DATA-CNT 

              DISPLAY SORT-RECORD-1 

              RELEASE SORT-RECORD-1 

           END-PERFORM.

      *  PROCESS THOSE RECORDS PRE-SORT (COUNTING, CHECKING, ETC.)

      *  'RELEASE' THE RECORD TO THE SORT ARRAY
      *    RELEASE SORT-RECORD-1

      *  WRAP IT UP WITH DISPLAY MESSAGES OR FILE/DB UPDATES

       100-EXIT.

           EXIT.

       200-SORT-OUTPUT.

           DISPLAY 'sort output'.

           PERFORM UNTIL END-OF-SORT
              RETURN SORT-WORK-1 
                    AT END
                       SET END-OF-SORT TO TRUE 
                    NOT AT END
                       DISPLAY SORT-RECORD-1 
                       MOVE 1 TO COUNTER
              END-RETURN
           END-PERFORM.

      * AFTER THE DATA IS SORTED DO SOMETHING WITH IT

       200-EXIT.

           EXIT.