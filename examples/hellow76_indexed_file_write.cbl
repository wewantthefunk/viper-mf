       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW76.
       AUTHOR. CHRISTIAN STRAMA.

       ENVIRONMENT DIVISION. 

       INPUT-OUTPUT SECTION.

       FILE-CONTROL.  

      * set the environment variable TESTFILE=test-records.txt
      * prior to running the converted Python file
           SELECT INPUTFILE       ASSIGN TO TESTFILE
                                  FILE STATUS IS FILE-STATUS
                                  RECORD KEY IS SEARCH-KEY
                                  ACCESS RANDOM
                                  ORGANIZATION INDEXED.

       DATA DIVISION.

       FILE SECTION. 

       FD INPUTFILE 
           RECORD CONTAINS 18 CHARACTERS.

       01  TEST-REC.
           02 TEST-REC-KEY    PIC X(4).
           02 TEST-REC-DATA.
              05 TEST-REC-D-1 PIC X(12).
              05 TEST-REC-D-2 PIC X(2).

       WORKING-STORAGE SECTION.

       01 SEARCH-KEY       PIC X(4).

       01 NO-MORE-RECORDS  PIC X(1) VALUE 'Y'.

       01 FILE-STATUS      PIC X(2).

       01 NEW-KEY          PIC X(4).

       01 KEY-LEN          PIC 9(2) VALUE 4.

       PROCEDURE DIVISION.
           
           OPEN I-O INPUTFILE.    

           IF FILE-STATUS = '00'
              MOVE 'N' TO NO-MORE-RECORDS
              PERFORM 1000-WRITE-FILE THRU 1000-WRITE-FILE-EXIT
              PERFORM 0000-READ-FILE THRU 0000-READ-FILE-EXIT
           ELSE 
              DISPLAY 'error opening file - ' FILE-STATUS 
           END-IF.

           CLOSE INPUTFILE.       

           STOP RUN.

       0000-READ-FILE.
           DISPLAY 'expected value ' SEARCH-KEY 'test record ' 
              TEST-REC-D-2
           READ INPUTFILE
              AT END MOVE 'Y' TO NO-MORE-RECORDS.

           DISPLAY '               ' TEST-REC.

       0000-READ-FILE-EXIT.
           EXIT.

       1000-WRITE-FILE.
           CALL 'RANDSTR' USING KEY-LEN, NEW-KEY.
           MOVE NEW-KEY TO SEARCH-KEY.
           MOVE NEW-KEY TO TEST-REC-KEY.
           MOVE 2 TO KEY-LEN.
           CALL 'RANDSTR' USING KEY-LEN, TEST-REC-D-2.
           MOVE 'test record' TO TEST-REC-D-1.

           WRITE TEST-REC.

       1000-WRITE-FILE-EXIT.
           EXIT.
