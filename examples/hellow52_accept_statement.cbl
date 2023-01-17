       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOW52.
       AUTHOR. CHRISTIAN STRAMA.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 ACCEPT-VALUE-DAY   PIC 9(5).
       01 ACCEPT-VALUE-DAY-LONG  PIC 9(7).

       01 ACCEPT-VALUE-DATE   PIC 9(6).
       01 ACCEPT-VALUE-DATE-LONG  PIC 9(8).

       01 ACCEPT-SYSIN  PIC X(10).

       PROCEDURE DIVISION.

           ACCEPT ACCEPT-VALUE-DAY FROM DAY.

           DISPLAY 'expected value YYDDD'
           DISPLAY 'actual value   ' ACCEPT-VALUE-DAY.

           ACCEPT ACCEPT-VALUE-DAY-LONG FROM DAY YYYYDDD.

           DISPLAY 'expected value YYYYDDD'
           DISPLAY 'actual value   ' ACCEPT-VALUE-DAY-LONG.

           ACCEPT ACCEPT-VALUE-DATE FROM DATE.

           DISPLAY 'expected value YYMMDD'
           DISPLAY 'actual value   ' ACCEPT-VALUE-DATE.

           ACCEPT ACCEPT-VALUE-DATE-LONG FROM DATE YYYYMMDD.

           DISPLAY 'expected value YYYYMMDD'
           DISPLAY 'actual value   ' ACCEPT-VALUE-DATE-LONG.

           ACCEPT ACCEPT-SYSIN.

           DISPLAY 'expected value sysin_val'
           DISPLAY 'actual value   ' ACCEPT-SYSIN.

           STOP RUN.

