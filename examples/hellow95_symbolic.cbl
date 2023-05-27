       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW95.
       AUTHOR. CHRISTIAN STRAMA.

       ENVIRONMENT DIVISION. 
       CONFIGURATION SECTION.
       SPECIAL-NAMES.

           SYMBOLIC LETTER-A IS 194
                    LETTER-B 195

           CLASS CLASS-TEST '12345'.

       DATA DIVISION. 

       WORKING-STORAGE SECTION. 

       01  TEST-VAR PIC X(12) VALUE 'hello, world'.

       01  TEST-VAR-2 PIC X(1).

       PROCEDURE DIVISION.
       
           DISPLAY LETTER-A.
           DISPLAY LETTER-B.  

           DISPLAY TEST-VAR.

           MOVE 'A' TO TEST-VAR-2.

           IF TEST-VAR-2 = LETTER-A 
              DISPLAY 'they are the same'
           END-IF.
           
           DISPLAY TEST-VAR-2.                                     

           STOP RUN.

