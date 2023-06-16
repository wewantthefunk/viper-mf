       01 HELLOMAPM.
          02 HELLOMAPI.
            03 HLBL1I PIC X(07) VALUE 'hello, '.
            03 HLBL1F PIC S9(4) COMP VALUE 07.
            03 HLBL1L PIC S9(4) COMP.
            03 HLBL2I PIC X(10) VALUE SPACES.
            03 HLBL2F PIC S9(4) COMP VALUE 10.
            03 HLBL2L PIC S9(4) COMP.
          02 HELLOMAPO REDEFINES HELLOMAPI.
            03 HLBL1O PIC X(07).
            03 HLBL1F-FILLER PIC X(2).
            03 HLBL1L-FILLER PIC X(2).
            03 HLBL2O PIC X(10).
            03 HLBL2F-FILLER PIC X(2).
            03 HLBL2L-FILLER PIC X(2).
