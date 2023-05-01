       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW90.
       AUTHOR. CHRISTIAN STRAMA.

       ENVIRONMENT DIVISION. 

       INPUT-OUTPUT SECTION.

       FILE-CONTROL.  

           SELECT INPUTFILE       ASSIGN TO TESTFILE
                                  FILE STATUS IS FILE-STATUS
                                  ORGANIZATION LINE SEQUENTIAL.

           SELECT INPUTFLE2       ASSIGN TO TESTFLE2
                                  FILE STATUS IS FILE-STATUS-2
                                  ORGANIZATION LINE SEQUENTIAL.

           SELECT OUTPUTFILE      ASSIGN TO TESTFL3
                                  FILE STATUS IS FILE-STATUS
                                  ORGANIZATION LINE SEQUENTIAL.

       DATA DIVISION.

       FILE SECTION. 

       FD INPUTFILE 
           RECORD CONTAINS 14 CHARACTERS.

       01  TEST-REC.
           02 FILLER      PIC X(10).
           02 RRB-NUMBER  PIC X(14).
       
       FD INPUTFLE2 
           RECORD CONTAINS 14 CHARACTERS.

       01  TEST-REC-2.
           02 FILLER        PIC X(10).
           02 RRB-NUMBER-2  PIC X(14).

       FD OUTPUTFILE 
           RECORD CONTAINS 14 CHARACTERS.

       01  TEST-REC-3.
           02 FILLER        PIC X(10).
           02 RRB-NUMBER-3  PIC X(14).

       WORKING-STORAGE SECTION. 

       01  FILE-STATUS   PIC X(2).

       01  FILE-STATUS-2 PIC X(2).

       PROCEDURE DIVISION.

           OPEN INPUT  INPUTFILE
                       INPUTFLE2
                OUTPUT OUTPUTFILE

           CLOSE INPUTFILE 
                 INPUTFLE2 
                 OUTPUTFILE 

           STOP RUN.