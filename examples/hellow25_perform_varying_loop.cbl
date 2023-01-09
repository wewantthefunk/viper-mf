       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW25.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 TEST-COUNT  PIC 9(3).

       PROCEDURE DIVISION.

           DISPLAY 'expecting numbers 1-10 printed from loop'
           
           PERFORM VARYING TEST-COUNT FROM 1
                BY 1 UNTIL TEST-COUNT > 10
                DISPLAY TEST-COUNT
           END-PERFORM.

           DISPLAY 'expecting numbers 10 - 1 printed from loop'
           PERFORM VARYING TEST-COUNT FROM 10
                BY -1 UNTIL TEST-COUNT = 0
                DISPLAY TEST-COUNT
           END-PERFORM.

           STOP RUN.

