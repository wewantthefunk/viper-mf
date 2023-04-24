       ID DIVISION.
       PROGRAM-ID.    CICS05.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 TEST-DATA PIC X(8).


       PROCEDURE DIVISION.
           MOVE 'KEYMAP' TO TEST-DATA.

           EXEC CICS RECEIVE MAP(TEST-DATA)
           END-EXEC.

           EXEC CICS SEND MAP('HELLOMAP')
           END-EXEC.

                      EXEC CICS
                          RETURN
                      END-EXEC.

