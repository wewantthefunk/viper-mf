       01 EIB-FIELDS.

      *  https://www.tutorialspoint.com/cics/cics_interface_block.htm

      *    Aid key pressed
           05 EIBAID     PIC X(1).

      *    Length of DFHCOMMAREA
           05 EIBCALEN   PIC S9(4) COMP.

      *    Current System Date
           05 EIBDATE    PIC S9(7) COMP-3.

      *    Return code of the last transaction
           05 IEBRCODE  PIC X(6).

      *    Task Number
           05 EIBTASKN PIC S9(7) COMP-3.

      *    Current System Time
           05 EIBTIME PIC S9(7) COMP-3.

      *    Terminal Identifier
           05 EIBTRMID PIC X(4).

      *    Transaction Identifier
           05 EIBTRNID PIC X(4).