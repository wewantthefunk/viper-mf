//HELLOW83   JOB  12345,'SORT TEST JOB'
//
//DELETESTEP EXEC PGM=IDCAMS
//SYSPRINT DD   SYSOUT=*
//SYSIN    DD   *
 DELETE TEST.OUTPUT.FILES.SORTED(HELLOW83)
/*
//
//STEP01    EXEC PGM=HELLOW83
//WORKFILE  DD DSNAME=DATA.INPUT.FILES(SORTTEST)
//OUTPUTFILE DD DSNAME=TEST.OUTPUT.FILES.SORTED(HELLOW83),DISP=(NEW,KEEP,DELETE)
//SYSOUT    DD SYSOUT=*
//SYSPRINT  DD SYSOUT=*
//