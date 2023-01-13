       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW44.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 FILE-STATUS      PIC 9(2) VALUE 2.
       01 MULTIPLIER       PIC 9(2) VALUE 4.

       PROCEDURE DIVISION.

           DISPLAY 'expected value is 02'
           DISPLAY 'actual value is   ' FILE-STATUS.

           MULTIPLY FILE-STATUS BY 2 GIVING FILE-STATUS.

           DISPLAY 'expected value is 04'
           DISPLAY 'actual value is   ' FILE-STATUS.    

           MULTIPLY 2 BY 3 GIVING FILE-STATUS.

           DISPLAY 'expected value is 06'
           DISPLAY 'actual value is   ' FILE-STATUS.   

           MULTIPLY FILE-STATUS BY MULTIPLIER GIVING FILE-STATUS.

           DISPLAY 'expected value is 24'
           DISPLAY 'actual value is   ' FILE-STATUS.   

           MOVE 2 TO FILE-STATUS.
           MULTIPLY MULTIPLIER BY FILE-STATUS GIVING FILE-STATUS.

           DISPLAY 'expected value is 08'
           DISPLAY 'actual value is   ' FILE-STATUS. 

           STOP RUN.

