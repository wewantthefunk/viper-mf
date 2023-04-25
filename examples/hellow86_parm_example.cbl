       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW86.
      
       DATA DIVISION.
       LINKAGE SECTION.
       01 LS-PARAMS.
         05 LS-PARAM-LENGTH  PIC S9(4) COMP.
         05 LS-PARAM-DATA    PIC X(100).
      
       PROCEDURE DIVISION USING LS-PARAMS.
           DISPLAY 'expected length : 13'
           DISPLAY 'expected data   : Hello, World!' 
           DISPLAY 'Parameter length: ' LS-PARAM-LENGTH.
           DISPLAY 'Parameter data  : ' LS-PARAM-DATA.
      
           GOBACK.