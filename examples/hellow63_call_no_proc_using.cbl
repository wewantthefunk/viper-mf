       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW63.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 TEST-DATA PIC X(8).

       01 SECOND-CALL PIC X(8).

       PROCEDURE DIVISION.

           DISPLAY 'exected message:'
           DISPLAY 'Called module HELLOW20 default *'.
           DISPLAY 'actual message:'.
           MOVE 'default' TO TEST-DATA.
           CALL 'HELLOW20' USING TEST-DATA.

           DISPLAY 'expected value commarea'
           MOVE 'commarea' TO TEST-DATA.
           MOVE 'HELLOW64' TO SECOND-CALL.
           CALL SECOND-CALL USING TEST-DATA.

           DISPLAY 'expected commarea response'
           DISPLAY 'updated commarea  ' TEST-DATA.

           STOP RUN.

