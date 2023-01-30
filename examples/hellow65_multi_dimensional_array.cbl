       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW65.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 TEST-DATA.
           05  MONTH-TABLE-AREA.
               10                PIC  X(24)  VALUE
                   X'F3F1000CF3F1000CF2F8031CF2F9031CF3F1059CF3F1060C'.
      *               -- JANUARY ---  -- FEBRUARY --  --- MARCH ----
      
               10                PIC  X(24)  VALUE
                   X'F3F0090CF3F0091CF3F1120CF3F1121CF3F0151CF3F0152C'.
      *               --- APRIL ----  ---- MAY -----  ---- JUNE ----
      
               10                PIC  X(24)  VALUE
                   X'F3F1181CF3F1182CF3F1212CF3F1213CF3F0243CF3F0244C'.
      *               ---- JULY ----  --- AUGUST ---  - SEPTEMBER --
      
               10                PIC  X(24)  VALUE
                   X'F3F1273CF3F1274CF3F0304CF3F0305CF3F1334CF3F1335C'.
      *               -- OCTOBER ---  -- NOVEMBER --  -- DECEMBER --
      
           05  REDEFINES MONTH-TABLE-AREA.
               10  MONTH-TABLE         OCCURS 12 TIMES
                                       INDEXED MONTH-INDEX.
                   15                  OCCURS 2 TIMES
                                       INDEXED LEAP-INDEX.
                       20  MT-DAYS-IN-MONTH
                                       PIC  X(02).
                       20  MT-DAYS-BEFORE
                                       PIC S9(03)  COMP-3.

       01 DAY-WORK            PIC S9(09)  VALUE ZERO. 

       PROCEDURE DIVISION.

           MOVE 1 TO LEAP-INDEX.
           MOVE 1 TO MONTH-INDEX.
           MOVE 251 TO DAY-WORK.

           SEARCH  MONTH-TABLE
             WHEN  MONTH-INDEX          =  +12
             OR    MT-DAYS-BEFORE (MONTH-INDEX + +1, LEAP-INDEX)
                                       >=  DAY-WORK

               DISPLAY 'found'

           END-SEARCH.

           GOBACK.

