       01  W-DATE-AREA                             SYNC.
           05  W-FUNCTION-CODE         PIC  X(01).
               88  FUNC-CONV-THE-DATE              VALUE ZERO.
               88  FUNC-ADJUST-THE-DATE            VALUE '1'.
               88  FUNC-CALC-DAYS-BETWEEN          VALUE '2'.
               88  FUNC-CONV-TO-DAY-OF-WEEK        VALUE '3'.
               88  FUNC-CONV-SYSTEM-DATE           VALUE '5'.
               88  FUNC-ADJUST-YYMMM               VALUE '6'.
               88  FUNC-VERIFY-THE-DATE            VALUE '7'.
      
           05  W-FORMAT-AND-DATE-1.
               10  W-FORMAT-1          PIC  X(02).
                   88  FORMAT-1-YYDDD              VALUE ZERO.
                   88  FORMAT-1-YYYYDDD            VALUE '05'.
                   88  FORMAT-1-YYYYDDD-PACKED     VALUE '08'.
                   88  FORMAT-1-MMDDYY             VALUE '10'.
                   88  FORMAT-1-MMDDYY-SLASHES     VALUE '11'.
                   88  FORMAT-1-MMDDYYYY           VALUE '12'.
                   88  FORMAT-1-MMDDYYYY-SLASHES   VALUE '13'.
                   88  FORMAT-1-0YYYYMMDD-PACKED   VALUE '14'.
                   88  FORMAT-1-YYMMDD             VALUE '20'.
                   88  FORMAT-1-YYYYMMDD           VALUE '21'.
                   88  FORMAT-1-REL-MEDICARE       VALUE '80'.
      
               10  W-DATE-1            PIC  X(10).
               10  REDEFINES W-DATE-1.
                   15  W-DATE-1-5      PIC  X(05).
                   15  W-DATE-1-5N     REDEFINES W-DATE-1-5
                                       PIC  9(05).
                   15                  PIC  X(05).
      
               10  REDEFINES W-DATE-1.
                   15  W-DATE-1-6      PIC  X(06).
                   15  W-DATE-1-6N     REDEFINES W-DATE-1-6
                                       PIC  9(06).
                   15                  PIC  X(04).
      
               10  W-DATE-1-7BYTES     REDEFINES W-DATE-1.
                   15  W-DATE-1-7      PIC  X(07).
                   15                  PIC  X(03).
      
               10  W-DATE-1-8BYTES     REDEFINES W-DATE-1.
                   15  W-DATE-1-8      PIC  X(08).
                   15  W-DATE-1-8N     REDEFINES W-DATE-1-8
                                       PIC  9(08).
                   15                  PIC  X(02).
      
               10  REDEFINES W-DATE-1.
                   15  W-DATE-1-10     PIC  X(10).
      
               10  REDEFINES W-DATE-1.
                   15  W-DATE-1-PJ-FILL
                                       PIC  X(01).
                   15  W-DATE-1-PJ-7   PIC S9(07)  COMP-3.
                   15                  PIC  X(05).
      
               10  REDEFINES W-DATE-1.
                   15                  PIC  X(01).
                   15  W-DATE-1-FW     PIC S9(09)  COMP-5.
                   15                  PIC  X(05).
      
               10  REDEFINES W-DATE-1.
                   15  W-DATE-1-5-PACKED
                                       PIC S9(09)  COMP-3.
                   15                  PIC  X(05).
      
           05  W-FORMAT-AND-DATE-2.
               10  W-FORMAT-2          PIC  X(02).
                   88  FORMAT-2-YYYYDDD            VALUE '05'.
                   88  FORMAT-2-YYYYDDD-PACKED     VALUE '08'.
                   88  FORMAT-2-MMDDYY             VALUE '10'.
                   88  FORMAT-2-MMDDYY-SLASHES     VALUE '11'.
                   88  FORMAT-2-MMDDYYYY           VALUE '12'.
                   88  FORMAT-2-MMDDYYYY-SLASHES   VALUE '13'.
                   88  FORMAT-2-0YYYYMMDD-PACKED   VALUE '14'.
                   88  FORMAT-2-YYMMDD             VALUE '20'.
                   88  FORMAT-2-YYYYMMDD           VALUE '21'.
                   88  FORMAT-2-REL-MEDICARE       VALUE '80'.
      
               10  W-DATE-2            PIC  X(10).
               10  REDEFINES W-DATE-2.
                   15  W-DATE-2-6      PIC  X(06).
                   15  W-DATE-2-6N     REDEFINES W-DATE-2-6
                                       PIC  9(06).
                   15                  PIC  X(04).
      
               10  REDEFINES W-DATE-2.
                   15  W-DATE-2-7      PIC  X(07).
                   15  W-DATE-2-7N     REDEFINES W-DATE-2-7
                                       PIC  9(07).
                   15                  PIC  X(03).
      
               10  W-DATE-2-8BYTES     REDEFINES W-DATE-2.
                   15  W-DATE-2-8      PIC  X(08).
                   15  W-DATE-2-8N     REDEFINES W-DATE-2-8
                                       PIC  9(08).
                   15                  PIC  X(02).
      
               10  REDEFINES W-DATE-2.
                   15  W-DATE-2-10     PIC  X(10).
      
               10  W-DATE-2-PJULIAN-7  REDEFINES W-DATE-2.
                   15                  PIC  X(01).
                   15  W-DATE-2-PJ-7   PIC S9(07)  COMP-3.
                   15                  PIC  X(05).
      
               10  REDEFINES W-DATE-2.
                   15                  PIC  X(03).
                   15  W-DATE-2-HALFWORD
                                       PIC S9(04)  COMP-5.
                   15                  PIC  X(05).
      
               10  REDEFINES W-DATE-2.
                   15                  PIC  X(01).
                   15  W-DATE-2-FULLWORD
                                       PIC S9(09)  COMP-5.
                   15                  PIC  X(05).
      
               10  REDEFINES W-DATE-2.
                   15  W-DATE-2-5-PACKED
                                       PIC S9(09)  COMP-3.
                   15                  PIC  X(05).
      
           05  W-NUMBER-FIELD          PIC S9(05)  COMP-3.
      
           05  W-RETURN-CODE           PIC S9(09)  COMP-5.
               88  CONVERT-RET-GOOD                VALUE ZERO.
               88  CONVERT-RET-BAD-DAY-OR-FMT      VALUE +4.
               88  CONVERT-RET-BAD-MTH-OR-FMT      VALUE +8.
               88  CONVERT-RET-BAD-FORMAT          VALUE +12.
               88  CONVERT-RET-BAD-FUNCTION        VALUE +16.
               88  CONVERT-RET-BAD-RANGE-INP       VALUE +28.
               88  CONVERT-RET-BAD-BINARY-LARGE    VALUE +32.
