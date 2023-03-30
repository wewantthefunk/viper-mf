       IDENTIFICATION DIVISION. 
       PROGRAM-ID. GETDSNS.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION. 

       LINKAGE SECTION. 

       05  GETDSNS-PARAMETERS.
           10  COMP-5.
               15  GP-RETURN-CODE  PIC S9(04)  VALUE ZERO.
               15  GP-MAXIMUM-DATA-SETS
                                 PIC S9(04)  VALUE +10.
               15  GP-CURRENT-DATA-SETS
                                 PIC S9(04)  VALUE ZERO.
           10  VALUE SPACE.
               15  GP-DDNAME       PIC  X(08).

               15                  OCCURS 10 TIMES
                                 INDEXED GP-INDEX.
                 20  GP-DATA-SET-NAME
                                 PIC  X(44).
                 20  GP-GENERATION
                                 PIC  X(08).

       PROCEDURE DIVISION USING GETDSNS-PARAMETERS.

           IF GP-DDNAME = 'INPUT   '
              MOVE 'DSN1' TO GP-DATA-SET-NAME(1)
              MOVE 'DSN2' TO GP-DATA-SET-NAME(2)
              MOVE 2 TO GP-CURRENT-DATA-SETS 
           END-IF.

           IF GP-DDNAME = 'OUTPUT  '
              MOVE 'O-DSN1' TO GP-DATA-SET-NAME(1)
              MOVE 'O-DSN2' TO GP-DATA-SET-NAME(2)
              MOVE 2 TO GP-CURRENT-DATA-SETS
           END-IF.

           GOBACK.