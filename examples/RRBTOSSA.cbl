       ID DIVISION.
       PROGRAM-ID.      RRBTOSSA.

       DATA DIVISION.
       WORKING-STORAGE SECTION.

       01  SYNC.
           05                          PIC  X(32)  VALUE
                   'RRBTOSSA - BEGIN WORKING-STORAGE'.
      
           05  COMP.
               10  OFFSET              PIC S9(04)  VALUE ZERO.
               10  HIC-LENGTH          PIC S9(04)  VALUE ZERO.
      
           05  SSA-HIC                             VALUE SPACE.
               10  SSA-HIC-BYTE-1      PIC  X(01).
               10                      PIC  X(08).
               10  SSA-BIC             PIC  X(02).
      
       LINKAGE SECTION.
      
       01  RRBTOSSA-PARAMETERS.
           05  RP-RRB-HIC              PIC  X(12).
           05  RP-SSA-HIC              PIC  X(11).
       01  LS-TEST.
           05 LS-ONE PIC 9(2).
           05 LS-TWO PIC 9(2).
      
       PROCEDURE DIVISION           USING  RRBTOSSA-PARAMETERS.

      *    INSPECT...TALLYING GENERATES A CALL TO A SUBROUTINE,
      *    SO PERFORM...VARYING USES A FRACTION OF THE CPU-TIME.
      
           MOVE  SPACE                 TO  SSA-HIC
                                           RP-SSA-HIC
           PERFORM
             VARYING HIC-LENGTH      FROM  +12
                                       BY  -1
             UNTIL   HIC-LENGTH         <  +1
             OR      RP-RRB-HIC (HIC-LENGTH:1)
                                    NOT =  SPACE
           END-PERFORM
      
      *    7-BYTE RRB HIC   -  1 LETTER, 6 NUMBERS   -  X111222
      *    8-BYTE RRB HIC   -  2 LETTERS, 6 NUMBERS  -  XX111222
      *    9-BYTE RRB HIC   -  3 LETTERS, 6 NUMBERS  -  XXX111222
      
      *    10-BYTE RRB HIC  -  1 LETTER, 9 NUMBERS   -  X111222333
      *    11-BYTE RRB HIC  -  2 LETTERS, 9 NUMBERS  -  XX111222333
      *    12-BYTE RRB HIC  -  3 LETTERS, 9 NUMBERS  -  XXX111222333
      
      *    THE LETTERS ARE USED TO GENERATE THE 2-BYTE BIC IN POSITIONS
      *    10 AND 11 OF THE SSA HIC. IF THERE ARE 9 NUMBERS, THEY WILL
      *    BE PLACED IN POSITIONS 1-9, WITH THE ZONE OF THE HIGH-ORDER
      *    NUMBER CONVERTED FROM 'F' TO 'C' (X'F0' BECOMES X'C0', ETC.).
      *    IF THERE ARE 6 NUMBERS, THEY WILL BE PLACED IN POSITIONS 4-9
      *    WITH '{00' IN POSITIONS 1-3.
      
           EVALUATE  HIC-LENGTH
             WHEN  +7
             WHEN  +10
               MOVE  +2                TO  OFFSET
      
               EVALUATE  TRUE
                 WHEN  RP-RRB-HIC (1:1) =  'A'
                   MOVE  '10'          TO  SSA-BIC
      
                 WHEN  RP-RRB-HIC (1:1) =  'H'
                 AND   HIC-LENGTH       =  +7
                   MOVE  '80'          TO  SSA-BIC
               END-EVALUATE
      
             WHEN  +8
             WHEN  +11
               MOVE  +3                TO  OFFSET
      
               EVALUATE  TRUE
                 WHEN  RP-RRB-HIC (1:2) =  'MA'
                   MOVE  '14'          TO  SSA-BIC
      
                 WHEN  RP-RRB-HIC (1:2) =  'PA'
                   MOVE  '15'          TO  SSA-BIC
      
                 WHEN  RP-RRB-HIC (1:2) =  'WA'
                   MOVE  '16'          TO  SSA-BIC
      
                 WHEN  RP-RRB-HIC (1:2) =  'CA'
                   MOVE  '17'          TO  SSA-BIC
      
                 WHEN  RP-RRB-HIC (1:2) =  'PD'
                   MOVE  '45'          TO  SSA-BIC
      
                 WHEN  RP-RRB-HIC (1:2) =  'WD'
                   MOVE  '46'          TO  SSA-BIC
      
                 WHEN  HIC-LENGTH       =  +11
                   CONTINUE
      
                 WHEN  RP-RRB-HIC (1:2) =  'JA'
                   MOVE  '11'          TO  SSA-BIC
      
                 WHEN  RP-RRB-HIC (1:2) =  'MH'
                   MOVE  '84'          TO  SSA-BIC
      
                 WHEN  RP-RRB-HIC (1:2) =  'PH'
                   MOVE  '85'          TO  SSA-BIC
      
                 WHEN  RP-RRB-HIC (1:2) =  'WH'
                   MOVE  '86'          TO  SSA-BIC
               END-EVALUATE
      
             WHEN  +9
             WHEN  +12
               MOVE  +4                TO  OFFSET
      
               EVALUATE  TRUE
                 WHEN  RP-RRB-HIC (1:3) =  'WCA'
                   MOVE  '13'          TO  SSA-BIC
      
                 WHEN  RP-RRB-HIC (1:3) =  'WCD'
                   MOVE  '43'          TO  SSA-BIC
      
                 WHEN  RP-RRB-HIC (1:3) =  'WCH'
                 AND   HIC-LENGTH       =  +9
                   MOVE  '83'          TO  SSA-BIC
               END-EVALUATE
           END-EVALUATE
      
           EVALUATE  TRUE
             WHEN  SSA-BIC              =  SPACE
               CONTINUE
      
             WHEN  HIC-LENGTH          <=  +9
               MOVE  '{00'             TO  SSA-HIC (1:3)
               MOVE  RP-RRB-HIC (OFFSET:6)
                                       TO  SSA-HIC (4:6)
      
               IF  SSA-HIC (4:6)           NUMERIC
               AND SSA-HIC (4:6)    NOT =  ZERO
      
      *        FOR RRB HICS WITH SIX NUMERIC DIGITS, EXCLUDE INVALID
      *        COMBINATIONS OF BICS AND SIX-DIGIT NUMERIC RANGES.
      
               AND ((SSA-BIC (1:1)      =  '1'
               AND  (SSA-HIC (4:6)      <  '991274'
               OR                       >  '994999'))
      
               OR   (SSA-BIC (1:1)      =  '4'
               AND  (SSA-HIC (4:6)      <  '415936'
               OR                       >  '994999'))
      
               OR   (SSA-BIC (1:1)      =  '8'
               AND  (SSA-HIC (4:6)      <  '049160'
               OR                       >  '994999')))
                   MOVE  SSA-HIC       TO  RP-SSA-HIC
               END-IF
      
             WHEN  OTHER
               MOVE  RP-RRB-HIC (OFFSET:9)
                                       TO  SSA-HIC (1:9)
      
      *        'INSPECT' GENERATES A SINGLE ASSEMBLER 'TR' INSTRUCTION
      *        PROCESSING AN UNQUALIFIED FIELD, BUT GENERATES A LINK TO
      *        A SUBROUTINE IF REFERENCE MODIFICATION IS USED.
      
               IF  SSA-HIC (1:9)           NUMERIC
               AND SSA-HIC (1:9)    NOT =  ALL '9'
               AND SSA-HIC (1:3)    NOT =  ZERO
                   INSPECT SSA-HIC-BYTE-1
                               CONVERTING  '0123456789'
                                       TO  '{ABCDEFGHI'
                   MOVE  SSA-HIC       TO  RP-SSA-HIC
               END-IF
           END-EVALUATE
      
           GOBACK.
