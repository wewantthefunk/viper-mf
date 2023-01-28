       01  ERR020W.
           02  ERR020W-ERROR-MESSAGE.
               05  ERR020W-ERROR              PIC X(12).
               05  FILLER                     PIC X(06) VALUE 'ERROR('.
               05  ERR020W-RESPONSE-CODE      PIC 9(08).
               05  FILLER                     PIC X(07) VALUE ');PROG='.
               05  ERR020W-ERROR-PROGRAM      PIC X(09).
               05  FILLER                     PIC X(06) VALUE ';PARA='.
               05  ERR020W-ERROR-PARA         PIC X(06).
               05  ERR020W-ERROR-LITERAL      PIC X(08).
               05  FILLER                     PIC X(01) VALUE SPACES.
               05  ERR020W-ERROR-VALUE        PIC X(08).