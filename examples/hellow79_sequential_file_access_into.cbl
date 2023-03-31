       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW79.
       AUTHOR. CHRISTIAN STRAMA.

       ENVIRONMENT DIVISION. 

       INPUT-OUTPUT SECTION.

       FILE-CONTROL.  

      * set the environment variable TESTFILE=test-records.txt
      * prior to running the converted Python file
           SELECT INPUTFILE       ASSIGN TO TESTFILE
                                  FILE STATUS IS FILE-STATUS
                                  ORGANIZATION LINE SEQUENTIAL.

       DATA DIVISION.

       FILE SECTION. 

       FD INPUTFILE 
           RECORD CONTAINS 14 CHARACTERS.

       01  TEST-REC.
           02 FILLER      PIC X(10).
           02 RRB-NUMBER  PIC X(14).

       WORKING-STORAGE SECTION.

       01 NO-MORE-RECORDS  PIC X(1) VALUE 'Y'.

       01 FILE-STATUS      PIC X(2).

       PROCEDURE DIVISION.

           DISPLAY 'expected value test record 1'
           DISPLAY '               test record 2'
           DISPLAY '               test record 3'
           
           OPEN INPUT INPUTFILE.    

           IF FILE-STATUS = '00'
              MOVE 'N' TO NO-MORE-RECORDS
           ELSE 
              DISPLAY 'error opening file - ' FILE-STATUS 
           END-IF.

           PERFORM UNTIL NO-MORE-RECORDS = 'Y'
              READ INPUTFILE INTO RRB-NUMBER
                 AT END MOVE 'Y' TO NO-MORE-RECORDS

              IF NO-MORE-RECORDS = 'N'
                 DISPLAY RRB-NUMBER
              END-IF
           END-PERFORM.

           CLOSE INPUTFILE.       

           STOP RUN.

