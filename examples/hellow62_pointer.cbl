       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW61.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 WS-POINTER USAGE IS POINTER.

       LINKAGE SECTION.

       01 TEST-DATA.

       PROCEDURE DIVISION.

           SET WS-POINTER TO ADDRESS OF TEST-DATA.

           STOP RUN.

