       IDENTIFICATION DIVISION.
       PROGRAM-ID. FIZZBUZZ.
       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       DATA DIVISION.
       WORKING-STORAGE SECTION.

       01  BINARY.    
           05  THE-REMAINDER      PIC S9(4).
           05  THE-QUOTIENT       PIC S9(4).
           05  THE-DIVISOR        PIC S9(4).

       01  FILLER.
           05  CURRENT-NUMBER     PIC 9(4).
           05  CURRENT-RESULT     PIC X(12).
           05  FIZZ-OUT           PIC X(4) VALUE SPACES.
           05  BUZZ-OUT           PIC X(4) VALUE SPACES.

       LINKAGE SECTION. 

       01  ARGUMENTS.
           05  ARG-LENGTH         PIC S9(4) COMP.
           05  STARTING-NUMBER    PIC 9(4).
           05  ENDING-NUMBER      PIC 9(4).

       PROCEDURE DIVISION USING ARGUMENTS.

       0000-MAIN.

           PERFORM
               VARYING CURRENT-NUMBER 
               FROM STARTING-NUMBER BY 1
               UNTIL CURRENT-NUMBER > ENDING-NUMBER

               PERFORM 1000-PROCESS-NUMBER
               DISPLAY 'Result for ' CURRENT-NUMBER
                       ' is ' CURRENT-RESULT
           END-PERFORM    
           GOBACK
           .

       1000-PROCESS-NUMBER.
           MOVE SPACES TO CURRENT-RESULT FIZZ-OUT BUZZ-OUT
           MOVE 15 TO THE-DIVISOR
           PERFORM 2000-DIVIDE
           IF THE-REMAINDER = 0
               MOVE "FIZZBUZZ" TO CURRENT-RESULT
           END-IF        
           IF  CURRENT-RESULT = SPACES
               MOVE 3 TO THE-DIVISOR
               PERFORM 2000-DIVIDE
               IF THE-REMAINDER = 0
                   MOVE "FIZZ" TO CURRENT-RESULT
               END-IF
           END-IF
           IF  CURRENT-RESULT = SPACES        
               MOVE 5 TO THE-DIVISOR
               PERFORM 2000-DIVIDE
               IF THE-REMAINDER = 0
                   MOVE "BUZZ" TO CURRENT-RESULT
               END-IF
           END-IF       
           IF  CURRENT-RESULT = SPACES        
               MOVE 7 TO THE-DIVISOR
               PERFORM 2000-DIVIDE
               IF THE-REMAINDER = 0
                   MOVE "BAZ" TO CURRENT-RESULT
               END-IF
           END-IF             
           IF  CURRENT-RESULT = SPACES 
               MOVE CURRENT-NUMBER TO CURRENT-RESULT
           END-IF    
           .

       2000-DIVIDE.
           DIVIDE THE-DIVISOR INTO CURRENT-NUMBER 
               GIVING THE-QUOTIENT 
               REMAINDER THE-REMAINDER 
           END-DIVIDE
           .