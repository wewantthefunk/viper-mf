       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW64.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 TEST-DATA PIC X(8).

       01 SECOND-CALL PIC X(8).

       LINKAGE SECTION.

       01 DFHCOMMAREA PIC X(8).

       PROCEDURE DIVISION.

           MOVE DFHCOMMAREA TO TEST-DATA.

           DISPLAY 'actual value   ' TEST-DATA.

           MOVE 'response' TO DFHCOMMAREA.

           GOBACK.

