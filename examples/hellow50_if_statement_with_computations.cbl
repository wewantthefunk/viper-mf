       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW50.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 JULIAN-YY-X PIC 9(2) VALUE 11.
       01 JULIAN-YY   PIC 9(2) VALUE 40.
       01 JULIAN-CC   PIC 9(2) VALUE 40.

       PROCEDURE DIVISION.

           IF  (JULIAN-YY-X              >  ZERO
           AND JULIAN-YY                = (JULIAN-YY / +4) * +4)
           OR (JULIAN-YY-X              =  ZERO
           AND JULIAN-CC                = (JULIAN-CC / +4) * +4)
              DISPLAY 'OR if condition successful'
           END-IF.


           STOP RUN.

