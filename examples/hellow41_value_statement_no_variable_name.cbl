       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW41.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 VALUE 'hello world'.
          02 HW-1.
           05 HELLO    PIC X(5).
           05 SPC      PIC X(1).
           05 WORLD    PIC x(5).
          02 REDEFINES HW-1.
           05 HW-2-R   PIC X(11).

       PROCEDURE DIVISION.
           DISPLAY 'expected value hello world'
           DISPLAY 'actual value   ' HELLO SPC WORLD.

           STOP RUN.

