       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW83.
       AUTHOR. CHRISTIAN STRAMA.

       ENVIRONMENT DIVISION. 

       INPUT-OUTPUT SECTION. 
       FILE-CONTROL.

           SELECT WORK-FILE      ASSIGN WORKFILE
                                 FILE STATUS IS WORK-FILE-STATUS.

           SELECT SORT-WORK-1    ASSIGN NODDNAME.

           SELECT OUTPUT-FILE    ASSIGN OUTPUTFILE
                                 FILE STATUS IS OUT-FILE-STATUS.

       DATA DIVISION.

       FILE SECTION. 

       FD  WORK-FILE.

       01  WORK-RECORD-1 PIC X(18).

       SD  SORT-WORK-1
           RECORD 18.

       01  SORT-RECORD-1. 
           05 SORT-KEY   PIC X(4).
           05 SORT-DATA  PIC X(11).
           05 FILLER     PIC X(1).
           05 SORT-DATA-CNT PIC X(2).

       FD  OUTPUT-FILE.

       01  OUTPUT-RECORD-1 PIC X(18). 

       WORKING-STORAGE SECTION. 

       01 WORK-FILE-STATUS  PIC X(1).

       01 OUT-FILE-STATUS   PIC X(1). 

       PROCEDURE DIVISION.

           SORT  SORT-WORK-1    ASCENDING  SORT-KEY
                                    USING  WORK-FILE
                                   GIVING  OUTPUT-FILE

           STOP RUN.
