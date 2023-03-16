      
       01  :X:-CB-LINE-ITEM-TRLR.
           05  :X:-CB-TRLR-CODE        PIC  9(02).
           05  :X:-CB-HCPCS-REVENUE-CODES.
               10  :X:-CB-LINE-ITEM-COUNT
                                       PIC  9(03).
      
               10  :X:-CB-HCPCS-REV-CODES
                                       OCCURS 1 TO 50 TIMES
                                       DEPENDING :X:-CB-LINE-ITEM-COUNT
                                       INDEXED   :X:-CB-INDEX.
                   15  :X:-CB-LINE-ITEM-NUM
                                       PIC  9(03).
                   15  :X:-CB-REV-CODE PIC  X(04).
                   15  :X:-CB-HCPCS-CODE
                                       PIC  X(05).
                   15  :X:-CB-FROM-DATE
                                       PIC S9(07)   COMP-3.
                   15  :X:-CB-THRU-DATE
                                       PIC S9(07)   COMP-3.
