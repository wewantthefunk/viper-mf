       01 RECVMAPI.
          02 LBL1I PIC X(17) VALUE 'Enter your name: '.
          02 LBL1F PIC S9(4) COMP VALUE 17.
          02 NAMEI PIC X(10) VALUE SPACES.
          02 NAMEF PIC S9(4) COMP VALUE 10.
       01 RECVMAPO REDEFINES RECVMAPI.
          02 LBL1O PIC X(17).
          02 FILLER PIC X(2).
          02 NAMEO PIC X(10).
          02 FILLER PIC X(2).
