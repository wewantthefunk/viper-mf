       01  AMNMMNUI.
           02  FILLER PIC X(12).
           02  TERML    COMP  PIC  S9(4).
           02  TERMF    PICTURE X.
           02  FILLER REDEFINES TERMF.
             03 TERMA    PICTURE X.
           02  TERMI  PIC X(4).
           02  DATEL    COMP  PIC  S9(4).
           02  DATEF    PICTURE X.
           02  FILLER REDEFINES DATEF.
             03 DATEA    PICTURE X.
           02  DATEI  PIC X(10).
           02  TIMEL    COMP  PIC  S9(4).
           02  TIMEF    PICTURE X.
           02  FILLER REDEFINES TIMEF.
             03 TIMEA    PICTURE X.
           02  TIMEI  PIC X(8).
           02  SYSTEML    COMP  PIC  S9(4).
           02  SYSTEMF    PICTURE X.
           02  FILLER REDEFINES SYSTEMF.
             03 SYSTEMA    PICTURE X.
           02  SYSTEMI  PIC X(8).
           02  USERL    COMP  PIC  S9(4).
           02  USERF    PICTURE X.
           02  FILLER REDEFINES USERF.
             03 USERA    PICTURE X.
           02  USERI  PIC X(8).
           02  SELECTL    COMP  PIC  S9(4).
           02  SELECTF    PICTURE X.
           02  FILLER REDEFINES SELECTF.
             03 SELECTA    PICTURE X.
           02  SELECTI  PIC X.
           02  MESSAGEL    COMP  PIC  S9(4).
           02  MESSAGEF    PICTURE X.
           02  FILLER REDEFINES MESSAGEF.
             03 MESSAGEA    PICTURE X.
           02  MESSAGEI  PIC X(79).
       01  AMNMMNUO REDEFINES AMNMMNUI.
           02  FILLER PIC X(12).
           02  FILLER PICTURE X(3).
           02  TERMO  PIC X(4).
           02  FILLER PICTURE X(3).
           02  DATEO  PIC X(10).
           02  FILLER PICTURE X(3).
           02  TIMEO  PIC X(8).
           02  FILLER PICTURE X(3).
           02  SYSTEMO  PIC X(8).
           02  FILLER PICTURE X(3).
           02  USERO  PIC X(8).
           02  FILLER PICTURE X(3).
           02  SELECTO PIC X.
           02  FILLER PICTURE X(3).
           02  MESSAGEO  PIC X(79).
