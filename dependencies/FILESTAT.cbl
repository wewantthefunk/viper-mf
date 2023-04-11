C24398 ID DIVISION.
       PROGRAM-ID.    FILESTAT.
       AUTHOR.        CHRISTIAN STRAMA.

       DATA DIVISION.
       WORKING-STORAGE SECTION.

       01.
           05                          PIC  X(32)  VALUE
                   'FILESTAT - BEGIN WORKING-STORAGE'.

           05  STATUS-TABLE-AREA.
               10                      PIC  X(50)  VALUE
                   '  UNKNOWN                                         '.
               10                      PIC  X(50)  VALUE
                   '00SUCCESSFUL COMPLETION                           '.
               10                      PIC  X(50)  VALUE
                   '02SUCCESSFUL COMPLETION - DUPLICATE KEY           '.
               10                      PIC  X(50)  VALUE
                   '04SUCCESSFUL COMPLETION - WRONG LENGTH RECORD     '.
               10                      PIC  X(50)  VALUE
                   '05OPTIONAL FILE NOT PRESENT AT OPEN               '.
               10                      PIC  X(50)  VALUE
                   '07CLOSE UNABLE TO REWIND/UNLOAD FILE              '.
               10                      PIC  X(50)  VALUE
                   '10END OF FILE                                     '.
               10                      PIC  X(50)  VALUE
                   '14READ PAST END OF RELATIVE FILE                  '.
               10                      PIC  X(50)  VALUE
                   '21SEQUENCE ERROR                                  '.
               10                      PIC  X(50)  VALUE
                   '22DUPLICATE KEY                                   '.
               10                      PIC  X(50)  VALUE
                   '23NO RECORD FOUND                                 '.
               10                      PIC  X(50)  VALUE
                   '24FILE IS OUT OF SPACE                            '.
               10                      PIC  X(50)  VALUE
                   '30NO FURTHER INFORMATION                          '.
               10                      PIC  X(50)  VALUE
                   '34BOUNDARY VIOLATION                              '.
               10                      PIC  X(50)  VALUE
                   '35FILE NOT PRESENT AT OPEN                        '.
               10                      PIC  X(50)  VALUE
                   '37INVALID FILE MODE AT OPEN                       '.
               10                      PIC  X(50)  VALUE
                   '38ATTEMPT TO OPEN LOCKED FILE                     '.
               10                      PIC  X(50)  VALUE
                   '39FILE ATTRIBUTE CONFLICT AT OPEN                 '.
               10                      PIC  X(50)  VALUE
                   '41FILE ALREADY OPEN                               '.
               10                      PIC  X(50)  VALUE
                   '42FILE NOT OPEN                                   '.
               10                      PIC  X(50)  VALUE
                   '43NO READ BEFORE REWRITE/DELETE                   '.
               10                      PIC  X(50)  VALUE
                   '44RECORD LENGTH LESS/GREATER THAN DEFINED LIMITS  '.
               10                      PIC  X(50)  VALUE
                   '46FILE NOT POSITIONED FOR READ                    '.
               10                      PIC  X(50)  VALUE
                   '47FILE NOT OPEN FOR INPUT                         '.
               10                      PIC  X(50)  VALUE
                   '48FILE NOT OPEN FOR OUTPUT                        '.
               10                      PIC  X(50)  VALUE
                   '49FILE NOT OPEN FOR UPDATE                        '.
               10                      PIC  X(50)  VALUE
                   '90NO FURTHER INFORMATION                          '.
               10                      PIC  X(50)  VALUE
                   '91PASSWORD FAILURE/INSUFFICENT RACF ACCESS        '.
               10                      PIC  X(50)  VALUE
                   '92LOGIC ERROR                                     '.
               10                      PIC  X(50)  VALUE
                   '93RESOURCE NOT AVAILABLE                          '.
               10                      PIC  X(50)  VALUE
                   '94NO FILE POSITION INDICATOR                      '.
               10                      PIC  X(50)  VALUE
                   '95INCOMPLETE FILE INFORMATION                     '.
               10                      PIC  X(50)  VALUE
                   '96MISSING DD STATEMENT                            '.
               10                      PIC  X(50)  VALUE
                   '97FILE VERIFIED AT OPEN                           '.

           05  REDEFINES STATUS-TABLE-AREA.
               10  STATUS-TABLE        OCCURS 34 TIMES
                                       INDEXED ST-INDEX.
                   15  ST-STATUS-CODE  PIC  X(02).
                   15  ST-MESSAGE      PIC  X(48).

           05                          PIC  X(30)  VALUE
                   'FILESTAT - END WORKING-STORAGE'.

       LINKAGE SECTION.

       01  FILE-STATUS                 PIC  X(02).
      
       PROCEDURE DIVISION           USING  FILE-STATUS.

           SET   ST-INDEX              TO  +2

           SEARCH  STATUS-TABLE
             END
               SET   ST-INDEX          TO  +1

             WHEN  FILE-STATUS          =  ST-STATUS-CODE (ST-INDEX)
               CONTINUE
           END-SEARCH

           DISPLAY 'FILESTAT  FILE STATUS '
                   FILE-STATUS
                   ' IS '
                   ST-MESSAGE (ST-INDEX)
           GOBACK.
