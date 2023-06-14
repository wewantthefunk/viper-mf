       ID DIVISION.
       PROGRAM-ID.    COMPL001.
       ENVIRONMENT DIVISION.
       CONFIGURATION SECTION.
       SPECIAL-NAMES.
      
           CLASS SPACE-A-C-F-Q-2-THRU-9    ' '
                                           'A'
                                           'C'
                                           'FQ23456789'
           CLASS CONVERTED-VALUES           'BDEGHJKLMNPRSTUVWXYZ'

           CLASS TEST-CLASS                LOW-VALUES
                                           HIGH-VALUES
                                           SPACE
                                           ZERO.
      
       DATA DIVISION.
       WORKING-STORAGE SECTION.
      
       01.
           05  STATUS-TABLE-AREA.
               10                      PIC  X(55)  VALUE
              'A A  B B  BAE  BDF  BGI  BHJ  BJK  BKE  BLF  BND  BPE  '.
               10                      PIC  X(55)  VALUE
              'BQF  BRG  BTH  BWH  BYG  B1G  B2B  B3C  B4H  B5C  B6B  '.
               10                      PIC  X(55)  VALUE
              'B7D  B8D  B9C  CACA CBCB CCCC CDCD CECE CFCF CGCG CHCH '.
               10                      PIC  X(55)  VALUE
              'CICI CJCJ CKCK CLCL CMCM CNCN COCO CPCP CQCQ CRCR CSCS '.
               10                      PIC  X(55)  VALUE
              'CTCT CUCU CVCV CWCW CXCX CYCY CZCZ C1C1 C2C2 C3C3 C4C4 '.
               10                      PIC  X(55)  VALUE
              'C5C5 C6C6 C7C7 C8C8 C9C9 D B  DAD  DCG  DDE  DGF  DHI  '.
               10                      PIC  X(55)  VALUE
              'DJJ  DKK  DLE  DMH  DNF  DPH  DQI  DRJ  DSI  DTK  DVD  '.
               10                      PIC  X(55)  VALUE
              'DWE  DXJ  DYF  DZK  D1G  D2C  D3H  D4B  D5G  D6B  D7C  '.
               10                      PIC  X(55)  VALUE
              'D8D  D9C  E B  EAF  EBD  ECE  EDF  EFI  EGJ  EHK  EJI  '.
               10                      PIC  X(55)  VALUE
              'EKJ  EMK  E1B  E2C  E3C  E4G  E5G  E6H  E7D  E8E  E9H  '.
               10                      PIC  X(55)  VALUE
              'F1F1 F2F2 F3F3 F4F4 F5F5 F6F6 F7F7 F8F8 J1A  J2A  J3A  '.
               10                      PIC  X(55)  VALUE
              'J4A  KAD  KBD  KCD  KDE  KEE  KFE  KGE  KHF  KJF  KLF  '.
               10                      PIC  X(55)  VALUE
              'KMF  K1B  K2B  K3B  K4B  K5C  K6C  K7C  K8C  K9D  M A  '.
               10                      PIC  X(55)  VALUE
              'M1A  T A  TAA  TCC1 TFTF TQTQ T2C2 T3C3 T4C4 T5C5 T6C6 '.
               10                      PIC  X(55)  VALUE
              'T7C7 T8C8 T9C9 W B  WBJ  WCE  WFF  WGK  WJF  WRG  WTH  '.
               10                      PIC  X(55)  VALUE
              'W1G  W2C  W3H  W4D  W5I  W6B  W7C  W8D  W9E  1010 1111 '.
               10                      PIC  X(55)  VALUE
              '13N  14L  1515 16L  17N  4343 4545 4646 8080 8383 84M  '.
               10                      PIC  X(10)  VALUE   '8585 86M  '.
           05  REDEFINES STATUS-TABLE-AREA.
               10  STATUS-TABLE           OCCURS 189 TIMES
                                       ASCENDING ST-VALUE-ONE
                                       INDEXED   ST-INDEX.
                   15  ST-VALUE-ONE          PIC  X(02).
                   15  ST-CATEGORY     PIC  X(02).
                   15                  PIC  X(01).
      
       LINKAGE SECTION.
      
       01  STATUS-AREA.
           05  STATUS-IN.
               10  STATUS-IN-1            PIC  X(01).
               10  STATUS-IN-2            PIC  X(01).
      
           05  STATUS-SEX                 PIC  X(01).
      
           05  STATUS-CAT.
               10  STATUS-CAT-1           PIC  X(01).
               10                      PIC  X(01).
      
           05  STATUS-RET-CD              PIC  X(01).
      /
       PROCEDURE DIVISION           USING  STATUS-AREA.
      
           IF STATUS-IN-1               =  'H'
               MOVE STATUS-IN-2         TO STATUS-IN-1
               MOVE SPACE            TO STATUS-IN-2
           END-IF
      
           MOVE  SPACE               TO  STATUS-CAT
           MOVE  'R'                 TO  STATUS-RET-CD
      
           EVALUATE  TRUE
             WHEN  STATUS-IN-1         NOT =  'T'
             WHEN  STATUS-IN-2                SPACE-A-C-F-Q-2-THRU-9
               SEARCH  ALL STATUS-TABLE
                 WHEN  ST-VALUE-ONE (ST-INDEX)
                                        =  STATUS-IN
                   MOVE  ST-CATEGORY (ST-INDEX)
                                       TO  STATUS-CAT
                   MOVE  'A'           TO  STATUS-RET-CD
               END-SEARCH
      
             WHEN  STATUS-IN-2                CONVERTED-VALUES
               EVALUATE  STATUS-SEX
                 WHEN  '1'
                 WHEN  'M'
                   MOVE  'A'           TO  STATUS-RET-CD
                   MOVE  STATUS-IN-2      TO  STATUS-CAT-1
      
                   INSPECT STATUS-CAT-1
                               CONVERTING  'BDEGHLMNPRSTUVWXYZ'
                                       TO  'GGGHIHIJKHIJKKGHIJ'
                 WHEN  '2'
                 WHEN  'F'
                   MOVE  'A'           TO  STATUS-RET-CD
                   MOVE  STATUS-IN-2      TO  STATUS-CAT-1
      
                   INSPECT STATUS-CAT-1
                               CONVERTING  'DEGHJKLMNPRSTUVWXYZ'
                                       TO  'BBCDEFCDEFCDEFFBCDE'
               END-EVALUATE
           END-EVALUATE
      
           GOBACK.
