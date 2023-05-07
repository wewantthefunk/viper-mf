       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW75.
       AUTHOR. CHRISTIAN STRAMA.

       ENVIRONMENT DIVISION. 

       INPUT-OUTPUT SECTION.

       FILE-CONTROL.  

      * set the environment variable TESTFILE=test-records-indexed.txt
      * prior to running the converted Python file
           SELECT INPUTFILE       ASSIGN TO TESTFILE
                                  FILE STATUS IS FILE-STATUS
                                  RECORD KEY IS SEARCH-KEY
                                  ACCESS RANDOM
                                  ORGANIZATION INDEXED.

       DATA DIVISION.

       FILE SECTION. 

       FD INPUTFILE 
           RECORD CONTAINS 14 CHARACTERS.

       01  TEST-REC.
           02 TEST-REC-KEY   PIC X(4).
           02 TEST-REC-DATA  PIC X(14).

       WORKING-STORAGE SECTION.

       01 SEARCH-KEY       PIC X(4).

       01 NO-MORE-RECORDS  PIC X(1) VALUE 'Y'.

       01 FILE-STATUS      PIC X(2).

       PROCEDURE DIVISION.

           DISPLAY 'expected value 0001test record 1'
           
           OPEN INPUT INPUTFILE.    

           IF FILE-STATUS = '00'
              MOVE 'N' TO NO-MORE-RECORDS
              PERFORM 0000-READ-FILE THRU 0000-READ-FILE-EXIT
           ELSE 
              DISPLAY 'error opening file - ' FILE-STATUS 
           END-IF.

           CLOSE INPUTFILE.       

           STOP RUN.

       0000-READ-FILE.
           MOVE '0001' TO SEARCH-KEY.

           READ INPUTFILE
              AT END MOVE 'Y' TO NO-MORE-RECORDS.

           DISPLAY '               ' TEST-REC.

       0000-READ-FILE-EXIT.
           EXIT.
