       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW54.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 TOP-LEVEL.
           05 TEST-FIELD     PIC X(5).
           05 REDEFINES TEST-FIELD.
              10 NUMBER-FIELD   PIC 9(2).
              10 COMP-3-FIELD   PIC S9(5) COMP-3.
           05 REDEFINES TEST-FIELD.
              10 NUM-FIELD-2    PIC 9(2).
              10 COMP-3-FIELD-2 PIC 9(5) COMP-3.

       PROCEDURE DIVISION.

           MOVE X'F3F0012345' TO TEST-FIELD.

           DISPLAY TEST-FIELD.

           DISPLAY COMP-3-FIELD.

           DISPLAY COMP-3-FIELD-2.

           STOP RUN.

