       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW48.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 TEST-VAL   PIC 9(4) VALUE ZERO.
       01 TEST-VAL-2 PIC 9(4) VALUE ZERO.

       01 OPERAND1 PIC 9(2) VALUE 1.

       01 OPERAND2 PIC 9(2) VALUE 2.

       PROCEDURE DIVISION.

           COMPUTE TEST-VAL = OPERAND1 + OPERAND2.

           DISPLAY 'expected value is 0003'
           DISPLAY 'actual value is   ' TEST-VAL.

           DISPLAY 'expected value is 0012'
           COMPUTE TEST-VAL = (3 + 2) * 2 + 2.

           DISPLAY 'actual value is   ' TEST-VAL.

           DISPLAY 'expected value is 0008'
           COMPUTE TEST-VAL = (OPERAND1 + 2) * 2 + 2.

           DISPLAY 'actual value is   ' TEST-VAL.

           DISPLAY 'expected value is 0007'
           COMPUTE TEST-VAL 
                   TEST-VAL-2 = (OPERAND1 + 2) * 2 + 1.

           DISPLAY 'actual value is   ' TEST-VAL.
           DISPLAY 'actual value is   ' TEST-VAL-2.

           STOP RUN.

