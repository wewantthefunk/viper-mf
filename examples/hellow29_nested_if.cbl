       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW28.
       AUTHOR. CHRISTIAN STRAMA.

       ENVIRONMENT DIVISION. 

       INPUT-OUTPUT SECTION.

       FILE-CONTROL.  

           SELECT INPUTFILE       ASSIGN TO NOFILE
                                  FILE STATUS IS FILE-STATUS
                                  ORGANIZATION LINE SEQUENTIAL.

       DATA DIVISION.

       FILE SECTION. 

       FD INPUTFILE 
           RECORD CONTAINS 80 CHARACTERS.

       01  TEST-REC.
           02 TEST-NUMBER  PIC X(80).

       WORKING-STORAGE SECTION.

       01 FILE-STATUS      PIC X(2).

       PROCEDURE DIVISION.

           OPEN INPUT INPUTFILE.    

           DISPLAY 'file status should be 35'
           DISPLAY 'it is actually        '
              FILE-STATUS
       

           STOP RUN.

