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

       01  TEST-VAR-2 PIC X(2).

       PROCEDURE DIVISION.
       
           DISPLAY LETTER-A.
           DISPLAY LETTER-B.  

           DISPLAY TEST-VAR.

           MOVE '00' TO TEST-VAR-2.

           DISPLAY TEST-VAR-2.                                     

           STOP RUN.

