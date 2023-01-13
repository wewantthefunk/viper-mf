       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW45.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 FILE-STATUS      PIC 9(2) VALUE 8.
       01 DIVISOR          PIC 9(2) VALUE 4.
       01 REMAINDER-VAL    PIC 9(2).

       PROCEDURE DIVISION.

           MOVE 4 TO FILE-STATUS.
           DIVIDE FILE-STATUS BY 5 GIVING FILE-STATUS REMAINDER 
              REMAINDER-VAL.

           DISPLAY 'expected value is 00'
           DISPLAY 'actual value is   ' FILE-STATUS. 

           DISPLAY 'expected value is 04'
           DISPLAY 'actual value is   ' REMAINDER-VAL 

           MOVE 8 TO FILE-STATUS.
           DISPLAY '-------'
           DISPLAY 'expected value is 08'
           DISPLAY 'actual value is   ' FILE-STATUS.

           DIVIDE FILE-STATUS BY 2 GIVING FILE-STATUS.

           DISPLAY 'expected value is 04'
           DISPLAY 'actual value is   ' FILE-STATUS.    

           MOVE 16 TO FILE-STATUS.

           DIVIDE FILE-STATUS BY DIVISOR GIVING FILE-STATUS

           DISPLAY '-------'
           DISPLAY 'expected value is 04'
           DISPLAY 'actual value is   ' FILE-STATUS.   

           DIVIDE 16 BY 2 GIVING FILE-STATUS.

           DISPLAY '-------'
           DISPLAY 'expected value is 08'
           DISPLAY 'actual value is   ' FILE-STATUS.   

           MOVE 2 TO FILE-STATUS.
           DIVIDE 20 BY FILE-STATUS GIVING FILE-STATUS.

           DISPLAY '-------'
           DISPLAY 'expected value is 10'
           DISPLAY 'actual value is   ' FILE-STATUS. 

           STOP RUN.

