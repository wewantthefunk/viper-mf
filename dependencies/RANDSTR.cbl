       IDENTIFICATION DIVISION.
       PROGRAM-ID. RANDSTR.
       
       ENVIRONMENT DIVISION.
       DATA DIVISION.
       
       WORKING-STORAGE SECTION.
       01 STRING-COUNTER          PIC 9(02) VALUE 1.
       01 RANDOM-NUMBER           PIC 9(09).
       01 CHARACTERS-LIST         PIC X(36)
           VALUE 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'.
       01 CHARACTER-TEMP          PIC X.

       LINKAGE SECTION. 

       01 STRING-LENGTH           PIC 9(02).
       01 RANDOM-STRING           PIC X(50).
       
       PROCEDURE DIVISION USING STRING-LENGTH, RANDOM-STRING.
           MOVE SPACES TO RANDOM-STRING 
         
           PERFORM STRING-GENERATION.
           
           GOBACK
           .
       
       STRING-GENERATION.
           PERFORM UNTIL STRING-COUNTER > STRING-LENGTH
              COMPUTE RANDOM-NUMBER = FUNCTION RANDOM(36)

              SET CHARACTER-TEMP TO CHARACTERS-LIST(RANDOM-NUMBER:1)
              MOVE CHARACTER-TEMP TO 
                 RANDOM-STRING(STRING-COUNTER:1)

              ADD 1 TO STRING-COUNTER 
           END-PERFORM
           .