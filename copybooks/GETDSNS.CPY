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