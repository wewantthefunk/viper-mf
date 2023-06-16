       01 RECVMAPM.
          02 RECVMAPI.
            03 LBL1I PIC X(17) VALUE 'Enter your name: '.
            03 LBL1F PIC S9(4) COMP VALUE 17.
            03 LBL1L PIC S9(4) COMP.
            03 NAMEI PIC X(10) VALUE SPACES.
            03 NAMEF PIC S9(4) COMP VALUE 10.
            03 NAMEL PIC S9(4) COMP.
          02 RECVMAPO REDEFINES RECVMAPI.
            03 LBL1O PIC X(17).
            03 LBL1F-FILLER PIC X(2).
            03 LBL1L-FILLER PIC X(2).
            03 NAMEO PIC X(10).
            03 NAMEF-FILLER PIC X(2).
            03 NAMEL-FILLER PIC X(2).
