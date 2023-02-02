from cobol_variable import *
import importlib, inspect, os, sys
# PROGRAM-ID: CMNDATCV
class CMNDATCVClass:
    def __init__(self):
        self.call_result = None
        self.CMNDATCVMemory = EMPTY_STRING
        self.EIBMemory = EMPTY_STRING
        self.variables_list = []
        self._INTERNALVars = []
        self.variables_list.append(self._INTERNALVars)
        self._INTERNALVars = Add_Variable('', self._INTERNALVars, 'MODULE-NAME', 0, 'X', 'MODULE-NAME', '', 0, 0, '', '01')[0]
        self._INTERNALVars[0].value = 'CMNDATCV'
        self.error_func = None
        self.calling_module = None
        initialize()
# ENVIRONMENT DIVISION
# DATA DIVISION
# WORKING-STORAGE SECTION.
        self._WORKING_STORAGE_SECTIONVars = []
        self.variables_list.append(self._WORKING_STORAGE_SECTIONVars)
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'SYNC', 0, 'X','SYNC','',0,0,'','01','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'SYNC-SUB-1', 32, 'X','SYNC','',0,0,'','05','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'CWF-PIVOT-YEAR', 2, 'X','SYNC','',0,0,'','05','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'COMP-3', 0, 'X','SYNC','',0,0,'','05','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'RELATIVE-DATE', 9, 'S9','COMP-3','',0,0,'','10','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'DAY-WORK', 9, 'S9','COMP-3','',0,0,'','10','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'DATE-SAVE', 9, 'S9','COMP-3','',0,0,'','10','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'WORK-DAYS', 9, 'S9','COMP-3','',0,0,'','10','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'WEEK-DAY', 3, '9','COMP-3','',0,0,'','10','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'DAYS-IN-YEAR', 3, 'S9','COMP-3','',0,0,'','10','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'ADJUST-YY', 3, 'S9','COMP-3','',0,0,'','10','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'ADJUST-MMM', 3, 'S9','COMP-3','',0,0,'','10','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'DAYS-INTEGER', 9, 'S9','COMP-3','',0,0,'','10','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'DAYS-USED', 11, 'S9','COMP-3','',0,2,'','10','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'REMAINING-DAYS', 11, 'S9','COMP-3','',0,2,'','10','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'WORK-FIELDS', 0, 'X','SYNC','',0,0,'','05','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'DISPLAY-WEEK-DAY', 2, '9','WORK-FIELDS','',0,0,'','10','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'SAVE-JULIAN-DATE', 0, 'X','WORK-FIELDS','',0,0,'','10','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'SAVE-JUL-YYYY-X', 4, 'X','SAVE-JULIAN-DATE','',0,0,'','15','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'SAVE-JUL-DDD', 3, '9','SAVE-JULIAN-DATE','',0,0,'','15','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'JULIAN-DATE', 0, 'X','WORK-FIELDS','',0,0,'','10','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'JULIAN-CC-X', 0, 'X','JULIAN-DATE','',0,0,'','15','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'JULIAN-CC', 2, '9','JULIAN-CC-X','',0,0,'','20','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'JULIAN-YY-X', 0, 'X','JULIAN-DATE','',0,0,'','15','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'JULIAN-YY', 2, '9','JULIAN-YY-X','',0,0,'','20','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'JULIAN-DDD-X', 0, 'X','JULIAN-DATE','',0,0,'','15','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'JULIAN-DDD', 3, '9','JULIAN-DDD-X','',0,0,'','20','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'REDEFINESmilh', 0, 'X','WORK-FIELDS','JULIAN-DATE',0,0,'','10','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'JULIAN-YYYY-X', 0, 'X','REDEFINESmilh','JULIAN-DATE',0,0,'','15','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'JULIAN-YYYY', 4, '9','JULIAN-YYYY-X','JULIAN-DATE',0,0,'','20','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'REDEFINESmilh-SUB-2', 3, 'X','REDEFINESmilh','JULIAN-DATE',0,0,'','15','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'REDEFINEShaxp', 0, 'X','WORK-FIELDS','JULIAN-DATE',0,0,'','10','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'JULIAN-YYYYDDD', 7, '9','REDEFINEShaxp','JULIAN-DATE',0,0,'','15','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'GREGORIAN-DATE', 0, 'X','WORK-FIELDS','',0,0,'','10','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'GREG-CC-X', 2, 'X','GREGORIAN-DATE','',0,0,'','15','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'GREG-YYMMDD', 0, 'X','GREGORIAN-DATE','',0,0,'','15','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'GREG-YY-X', 2, 'X','GREG-YYMMDD','',0,0,'','20','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'GREG-MM-X', 0, 'X','GREG-YYMMDD','',0,0,'','20','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'GREG-MM', 2, '9','GREG-MM-X','',0,0,'','25','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'GREG-DD-X', 0, 'X','GREG-YYMMDD','',0,0,'','20','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'GREG-DD', 2, '9','GREG-DD-X','',0,0,'','25','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'REDEFINESbihw', 0, 'X','WORK-FIELDS','GREGORIAN-DATE',0,0,'','10','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'GREG-YYYY-X', 0, 'X','REDEFINESbihw','GREGORIAN-DATE',0,0,'','15','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'GREG-YYYY', 4, '9','GREG-YYYY-X','GREGORIAN-DATE',0,0,'','20','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'GREG-MMDD-X', 4, 'X','REDEFINESbihw','GREGORIAN-DATE',0,0,'','15','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'REDEFINEShycf', 0, 'X','WORK-FIELDS','GREGORIAN-DATE',0,0,'','10','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'GREG-YYYYMMDD', 8, '9','REDEFINEShycf','GREGORIAN-DATE',0,0,'','15','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'SYNC-SUB-3', 9, 'S9','SYNC','',0,0,'COMP','05','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'SYNC-SUB-4', 1, 'X','SYNC','',0,0,'','05','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'FORMAT-AND-DATE', 12, 'X','SYNC','',0,0,'','05','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'REDEFINESyxff', 0, 'X','SYNC','FORMAT-AND-DATE',0,0,'','05','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'FORMAT', 2, 'X','REDEFINESyxff','FORMAT-AND-DATE',0,0,'','10','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'FORMAT-00-YYDDD', 0, 'X','FORMAT','FORMAT-AND-DATE',0,0,'','88','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'FORMAT-05-YYYYDDD', 0, 'X','FORMAT','FORMAT-AND-DATE',0,0,'','88','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'FORMAT-08-YYYYDDD-PACKED', 0, 'X','FORMAT','FORMAT-AND-DATE',0,0,'','88','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'FORMAT-10-MMDDYY', 0, 'X','FORMAT','FORMAT-AND-DATE',0,0,'','88','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'FORMAT-11-MMDDYY-SLASHES', 0, 'X','FORMAT','FORMAT-AND-DATE',0,0,'','88','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'FORMAT-12-MMDDYYYY', 0, 'X','FORMAT','FORMAT-AND-DATE',0,0,'','88','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'FORMAT-13-MMDDYYYY-SLASHES', 0, 'X','FORMAT','FORMAT-AND-DATE',0,0,'','88','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'FORMAT-14-0YYYYMMDD-PACKED', 0, 'X','FORMAT','FORMAT-AND-DATE',0,0,'','88','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'FORMAT-20-YYMMDD', 0, 'X','FORMAT','FORMAT-AND-DATE',0,0,'','88','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'FORMAT-21-YYYYMMDD', 0, 'X','FORMAT','FORMAT-AND-DATE',0,0,'','88','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'FORMAT-80-REL-MEDICARE', 0, 'X','FORMAT','FORMAT-AND-DATE',0,0,'','88','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'DATE-AREA', 0, 'X','REDEFINESyxff','FORMAT-AND-DATE',0,0,'','10','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'DA-08-14-PACKED', 9, 'S9','DATE-AREA','FORMAT-AND-DATE',0,0,'COMP-3','15','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'DATE-AREA-SUB-5', 5, 'X','DATE-AREA','FORMAT-AND-DATE',0,0,'','15','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'REDEFINESbwfw', 0, 'X','REDEFINESyxff','DATE-AREA',0,0,'','10','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'REDEFINESbwfw-SUB-6', 3, 'X','REDEFINESbwfw','DATE-AREA',0,0,'','15','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'DA-80-HALFWORD', 4, 'S9','REDEFINESbwfw','DATE-AREA',0,0,'COMP-5','15','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'REDEFINESbwfw-SUB-7', 5, 'X','REDEFINESbwfw','DATE-AREA',0,0,'','15','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'wxbmt', 0, 'X','SYNC','FORMAT-AND-DATE',0,0,'','05','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'DAY-OF-WEEK-X', 9, 'X','wxbmt','FORMAT-AND-DATE',0,0,'','10','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'MONTH-TABLE-AREA', 0, 'X','SYNC','',0,0,'','05','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'MONTH-TABLE-AREA-SUB-8', 24, 'X','MONTH-TABLE-AREA','',0,0,'','10','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'MONTH-TABLE-AREA-SUB-9', 24, 'X','MONTH-TABLE-AREA','',0,0,'','10','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'MONTH-TABLE-AREA-SUB-10', 24, 'X','MONTH-TABLE-AREA','',0,0,'','10','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'MONTH-TABLE-AREA-SUB-11', 24, 'X','MONTH-TABLE-AREA','',0,0,'','10','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'REDEFINESwgis', 0, 'X','SYNC','MONTH-TABLE-AREA',0,0,'','05','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'MONTH-INDEX', 10, '9','MONTH-TABLE','',0,0,'','10')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'MONTH-TABLE', 0, 'X','REDEFINESwgis','MONTH-TABLE-AREA',12,0,'','10','MONTH-INDEX')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'LEAP-INDEX', 10, '9','ozrbo','',0,0,'','15')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'ozrbo', 0, 'X','MONTH-TABLE','MONTH-TABLE-AREA',2,0,'','15','LEAP-INDEX')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'MT-DAYS-IN-MONTH', 2, 'X','ozrbo','MONTH-TABLE-AREA',0,0,'','20','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'MT-DAYS-BEFORE', 3, 'S9','ozrbo','MONTH-TABLE-AREA',0,0,'COMP-3','20','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._WORKING_STORAGE_SECTIONVars,'SYNC-SUB-12', 30, 'X','SYNC','',0,0,'','05','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
# LINKAGE SECTION.
        self._LINKAGE_SECTIONVars = []
        self.variables_list.append(self._LINKAGE_SECTIONVars)
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'W-DATE-AREA', 0, 'X','W-DATE-AREA','',0,0,'','01','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'W-FUNCTION-CODE', 1, 'X','W-DATE-AREA','',0,0,'','05','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'FUNC-CONV-THE-DATE', 0, 'X','W-FUNCTION-CODE','',0,0,'','88','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'FUNC-ADJUST-THE-DATE', 0, 'X','W-FUNCTION-CODE','',0,0,'','88','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'FUNC-CALC-DAYS-BETWEEN', 0, 'X','W-FUNCTION-CODE','',0,0,'','88','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'FUNC-CONV-TO-DAY-OF-WEEK', 0, 'X','W-FUNCTION-CODE','',0,0,'','88','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'FUNC-CONV-SYSTEM-DATE', 0, 'X','W-FUNCTION-CODE','',0,0,'','88','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'FUNC-ADJUST-YYMMM', 0, 'X','W-FUNCTION-CODE','',0,0,'','88','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'FUNC-VERIFY-THE-DATE', 0, 'X','W-FUNCTION-CODE','',0,0,'','88','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'W-FORMAT-AND-DATE-1', 0, 'X','W-DATE-AREA','',0,0,'','05','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'W-FORMAT-1', 2, 'X','W-FORMAT-AND-DATE-1','',0,0,'','10','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'FORMAT-1-YYDDD', 0, 'X','W-FORMAT-1','',0,0,'','88','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'FORMAT-1-YYYYDDD', 0, 'X','W-FORMAT-1','',0,0,'','88','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'FORMAT-1-YYYYDDD-PACKED', 0, 'X','W-FORMAT-1','',0,0,'','88','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'FORMAT-1-MMDDYY', 0, 'X','W-FORMAT-1','',0,0,'','88','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'FORMAT-1-MMDDYY-SLASHES', 0, 'X','W-FORMAT-1','',0,0,'','88','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'FORMAT-1-MMDDYYYY', 0, 'X','W-FORMAT-1','',0,0,'','88','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'FORMAT-1-MMDDYYYY-SLASHES', 0, 'X','W-FORMAT-1','',0,0,'','88','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'FORMAT-1-0YYYYMMDD-PACKED', 0, 'X','W-FORMAT-1','',0,0,'','88','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'FORMAT-1-YYMMDD', 0, 'X','W-FORMAT-1','',0,0,'','88','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'FORMAT-1-YYYYMMDD', 0, 'X','W-FORMAT-1','',0,0,'','88','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'FORMAT-1-REL-MEDICARE', 0, 'X','W-FORMAT-1','',0,0,'','88','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'W-DATE-1', 10, 'X','W-FORMAT-AND-DATE-1','',0,0,'','10','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'REDEFINESjnjp', 0, 'X','W-FORMAT-AND-DATE-1','W-DATE-1',0,0,'','10','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'W-DATE-1-5', 5, 'X','REDEFINESjnjp','W-DATE-1',0,0,'','15','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'W-DATE-1-5N', 5, '9','REDEFINESjnjp','W-DATE-1-5',0,0,'','15','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'REDEFINESjnjp-SUB-13', 5, 'X','REDEFINESjnjp','W-DATE-1',0,0,'','15','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'REDEFINESyetb', 0, 'X','W-FORMAT-AND-DATE-1','W-DATE-1',0,0,'','10','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'W-DATE-1-6', 6, 'X','REDEFINESyetb','W-DATE-1',0,0,'','15','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'W-DATE-1-6N', 6, '9','REDEFINESyetb','W-DATE-1-6',0,0,'','15','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'REDEFINESyetb-SUB-14', 4, 'X','REDEFINESyetb','W-DATE-1',0,0,'','15','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'W-DATE-1-7BYTES', 0, 'X','W-FORMAT-AND-DATE-1','W-DATE-1',0,0,'','10','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'W-DATE-1-7', 7, 'X','W-DATE-1-7BYTES','W-DATE-1',0,0,'','15','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'W-DATE-1-7BYTES-SUB-15', 3, 'X','W-DATE-1-7BYTES','W-DATE-1',0,0,'','15','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'W-DATE-1-8BYTES', 0, 'X','W-FORMAT-AND-DATE-1','W-DATE-1',0,0,'','10','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'W-DATE-1-8', 8, 'X','W-DATE-1-8BYTES','W-DATE-1',0,0,'','15','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'W-DATE-1-8N', 8, '9','W-DATE-1-8BYTES','W-DATE-1-8',0,0,'','15','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'W-DATE-1-8BYTES-SUB-16', 2, 'X','W-DATE-1-8BYTES','W-DATE-1',0,0,'','15','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'REDEFINESfxvz', 0, 'X','W-FORMAT-AND-DATE-1','W-DATE-1',0,0,'','10','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'W-DATE-1-10', 10, 'X','REDEFINESfxvz','W-DATE-1',0,0,'','15','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'REDEFINESauvg', 0, 'X','W-FORMAT-AND-DATE-1','W-DATE-1',0,0,'','10','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'W-DATE-1-PJ-FILL', 1, 'X','REDEFINESauvg','W-DATE-1',0,0,'','15','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'W-DATE-1-PJ-7', 7, 'S9','REDEFINESauvg','W-DATE-1',0,0,'COMP-3','15','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'REDEFINESauvg-SUB-17', 5, 'X','REDEFINESauvg','W-DATE-1',0,0,'','15','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'REDEFINESuncx', 0, 'X','W-FORMAT-AND-DATE-1','W-DATE-1',0,0,'','10','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'REDEFINESuncx-SUB-18', 1, 'X','REDEFINESuncx','W-DATE-1',0,0,'','15','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'W-DATE-1-FW', 9, 'S9','REDEFINESuncx','W-DATE-1',0,0,'COMP-5','15','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'REDEFINESuncx-SUB-19', 5, 'X','REDEFINESuncx','W-DATE-1',0,0,'','15','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'REDEFINESyfcm', 0, 'X','W-FORMAT-AND-DATE-1','W-DATE-1',0,0,'','10','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'W-DATE-1-5-PACKED', 9, 'S9','REDEFINESyfcm','W-DATE-1',0,0,'COMP-3','15','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'REDEFINESyfcm-SUB-20', 5, 'X','REDEFINESyfcm','W-DATE-1',0,0,'','15','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'W-FORMAT-AND-DATE-2', 0, 'X','W-DATE-AREA','',0,0,'','05','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'W-FORMAT-2', 2, 'X','W-FORMAT-AND-DATE-2','',0,0,'','10','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'FORMAT-2-YYYYDDD', 0, 'X','W-FORMAT-2','',0,0,'','88','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'FORMAT-2-YYYYDDD-PACKED', 0, 'X','W-FORMAT-2','',0,0,'','88','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'FORMAT-2-MMDDYY', 0, 'X','W-FORMAT-2','',0,0,'','88','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'FORMAT-2-MMDDYY-SLASHES', 0, 'X','W-FORMAT-2','',0,0,'','88','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'FORMAT-2-MMDDYYYY', 0, 'X','W-FORMAT-2','',0,0,'','88','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'FORMAT-2-MMDDYYYY-SLASHES', 0, 'X','W-FORMAT-2','',0,0,'','88','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'FORMAT-2-0YYYYMMDD-PACKED', 0, 'X','W-FORMAT-2','',0,0,'','88','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'FORMAT-2-YYMMDD', 0, 'X','W-FORMAT-2','',0,0,'','88','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'FORMAT-2-YYYYMMDD', 0, 'X','W-FORMAT-2','',0,0,'','88','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'FORMAT-2-REL-MEDICARE', 0, 'X','W-FORMAT-2','',0,0,'','88','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'W-DATE-2', 10, 'X','W-FORMAT-AND-DATE-2','',0,0,'','10','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'REDEFINESheac', 0, 'X','W-FORMAT-AND-DATE-2','W-DATE-2',0,0,'','10','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'W-DATE-2-6', 6, 'X','REDEFINESheac','W-DATE-2',0,0,'','15','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'W-DATE-2-6N', 6, '9','REDEFINESheac','W-DATE-2-6',0,0,'','15','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'REDEFINESheac-SUB-21', 4, 'X','REDEFINESheac','W-DATE-2',0,0,'','15','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'REDEFINESomfi', 0, 'X','W-FORMAT-AND-DATE-2','W-DATE-2',0,0,'','10','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'W-DATE-2-7', 7, 'X','REDEFINESomfi','W-DATE-2',0,0,'','15','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'W-DATE-2-7N', 7, '9','REDEFINESomfi','W-DATE-2-7',0,0,'','15','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'REDEFINESomfi-SUB-22', 3, 'X','REDEFINESomfi','W-DATE-2',0,0,'','15','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'W-DATE-2-8BYTES', 0, 'X','W-FORMAT-AND-DATE-2','W-DATE-2',0,0,'','10','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'W-DATE-2-8', 8, 'X','W-DATE-2-8BYTES','W-DATE-2',0,0,'','15','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'W-DATE-2-8N', 8, '9','W-DATE-2-8BYTES','W-DATE-2-8',0,0,'','15','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'W-DATE-2-8BYTES-SUB-23', 2, 'X','W-DATE-2-8BYTES','W-DATE-2',0,0,'','15','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'REDEFINESfifd', 0, 'X','W-FORMAT-AND-DATE-2','W-DATE-2',0,0,'','10','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'W-DATE-2-10', 10, 'X','REDEFINESfifd','W-DATE-2',0,0,'','15','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'W-DATE-2-PJULIAN-7', 0, 'X','W-FORMAT-AND-DATE-2','W-DATE-2',0,0,'','10','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'W-DATE-2-PJULIAN-7-SUB-24', 1, 'X','W-DATE-2-PJULIAN-7','W-DATE-2',0,0,'','15','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'W-DATE-2-PJ-7', 7, 'S9','W-DATE-2-PJULIAN-7','W-DATE-2',0,0,'COMP-3','15','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'W-DATE-2-PJULIAN-7-SUB-25', 5, 'X','W-DATE-2-PJULIAN-7','W-DATE-2',0,0,'','15','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'REDEFINESqyhx', 0, 'X','W-FORMAT-AND-DATE-2','W-DATE-2',0,0,'','10','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'REDEFINESqyhx-SUB-26', 3, 'X','REDEFINESqyhx','W-DATE-2',0,0,'','15','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'W-DATE-2-HALFWORD', 4, 'S9','REDEFINESqyhx','W-DATE-2',0,0,'COMP-5','15','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'REDEFINESqyhx-SUB-27', 5, 'X','REDEFINESqyhx','W-DATE-2',0,0,'','15','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'REDEFINESqzgo', 0, 'X','W-FORMAT-AND-DATE-2','W-DATE-2',0,0,'','10','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'REDEFINESqzgo-SUB-28', 1, 'X','REDEFINESqzgo','W-DATE-2',0,0,'','15','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'W-DATE-2-FULLWORD', 9, 'S9','REDEFINESqzgo','W-DATE-2',0,0,'COMP-5','15','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'REDEFINESqzgo-SUB-29', 5, 'X','REDEFINESqzgo','W-DATE-2',0,0,'','15','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'REDEFINESkffs', 0, 'X','W-FORMAT-AND-DATE-2','W-DATE-2',0,0,'','10','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'W-DATE-2-5-PACKED', 9, 'S9','REDEFINESkffs','W-DATE-2',0,0,'COMP-3','15','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'REDEFINESkffs-SUB-30', 5, 'X','REDEFINESkffs','W-DATE-2',0,0,'','15','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'W-NUMBER-FIELD', 5, 'S9','W-DATE-AREA','',0,0,'COMP-3','05','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'W-RETURN-CODE', 9, 'S9','W-DATE-AREA','',0,0,'COMP-5','05','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'CONVERT-RET-GOOD', 0, 'X','W-RETURN-CODE','',0,0,'','88','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'CONVERT-RET-BAD-DAY-OR-FMT', 0, 'X','W-RETURN-CODE','',0,0,'','88','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'CONVERT-RET-BAD-MTH-OR-FMT', 0, 'X','W-RETURN-CODE','',0,0,'','88','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'CONVERT-RET-BAD-FORMAT', 0, 'X','W-RETURN-CODE','',0,0,'','88','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'CONVERT-RET-BAD-FUNCTION', 0, 'X','W-RETURN-CODE','',0,0,'','88','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'CONVERT-RET-BAD-RANGE-INP', 0, 'X','W-RETURN-CODE','',0,0,'','88','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]
        result = Add_Variable(self.CMNDATCVMemory,self._LINKAGE_SECTIONVars,'CONVERT-RET-BAD-BINARY-LARGE', 0, 'X','W-RETURN-CODE','',0,0,'','88','')
        self._LINKAGE_SECTIONVars = result[0]
        self.CMNDATCVMemory = result[1]


        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'SYNC-SUB-1', 'CMNDATCV - BEGIN WORKING-STORAGE','SYNC-SUB-1')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'CWF-PIVOT-YEAR', '47','CWF-PIVOT-YEAR')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'RELATIVE-DATE', 0,'RELATIVE-DATE')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'DAY-WORK', 0,'DAY-WORK')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'DATE-SAVE', 0,'DATE-SAVE')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'WORK-DAYS', 0,'WORK-DAYS')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'WEEK-DAY', 0,'WEEK-DAY')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'DAYS-IN-YEAR', 0,'DAYS-IN-YEAR')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'ADJUST-YY', 0,'ADJUST-YY')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'ADJUST-MMM', 0,'ADJUST-MMM')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'DAYS-INTEGER', 0,'DAYS-INTEGER')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'DAYS-USED', 0,'DAYS-USED')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'REMAINING-DAYS', 0,'REMAINING-DAYS')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'WORK-FIELDS', 0,'WORK-FIELDS')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FORMAT-AND-DATE', '____spaces','FORMAT-AND-DATE')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FORMAT-00-YYDDD', 0,'FORMAT-00-YYDDD')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FORMAT-05-YYYYDDD', '05','FORMAT-05-YYYYDDD')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FORMAT-08-YYYYDDD-PACKED', '08','FORMAT-08-YYYYDDD-PACKED')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FORMAT-10-MMDDYY', '10','FORMAT-10-MMDDYY')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FORMAT-11-MMDDYY-SLASHES', '11','FORMAT-11-MMDDYY-SLASHES')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FORMAT-12-MMDDYYYY', '12','FORMAT-12-MMDDYYYY')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FORMAT-13-MMDDYYYY-SLASHES', '13','FORMAT-13-MMDDYYYY-SLASHES')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FORMAT-14-0YYYYMMDD-PACKED', '14','FORMAT-14-0YYYYMMDD-PACKED')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FORMAT-20-YYMMDD', '20','FORMAT-20-YYMMDD')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FORMAT-21-YYYYMMDD', '21','FORMAT-21-YYYYMMDD')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FORMAT-80-REL-MEDICARE', '80','FORMAT-80-REL-MEDICARE')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'wxbmt', 'SUNDAY   MONDAY   TUESDAY  WEDNESDAYTHURSDAY FRIDAY   SATURDAY ','wxbmt')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'MONTH-TABLE-AREA-SUB-8', '_hex_F3F1000CF3F1000CF2F8031CF2F9031CF3F1059CF3F1060C','MONTH-TABLE-AREA-SUB-8')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'MONTH-TABLE-AREA-SUB-9', '_hex_F3F0090CF3F0091CF3F1120CF3F1121CF3F0151CF3F0152C','MONTH-TABLE-AREA-SUB-9')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'MONTH-TABLE-AREA-SUB-10', '_hex_F3F1181CF3F1182CF3F1212CF3F1213CF3F0243CF3F0244C','MONTH-TABLE-AREA-SUB-10')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'MONTH-TABLE-AREA-SUB-11', '_hex_F3F1273CF3F1274CF3F0304CF3F0305CF3F1334CF3F1335C','MONTH-TABLE-AREA-SUB-11')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'SYNC-SUB-12', 'CMNDATCV - END WORKING-STORAGE','SYNC-SUB-12')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FUNC-CONV-THE-DATE', 0,'FUNC-CONV-THE-DATE')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FUNC-ADJUST-THE-DATE', '1','FUNC-ADJUST-THE-DATE')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FUNC-CALC-DAYS-BETWEEN', '2','FUNC-CALC-DAYS-BETWEEN')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FUNC-CONV-TO-DAY-OF-WEEK', '3','FUNC-CONV-TO-DAY-OF-WEEK')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FUNC-CONV-SYSTEM-DATE', '5','FUNC-CONV-SYSTEM-DATE')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FUNC-ADJUST-YYMMM', '6','FUNC-ADJUST-YYMMM')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FUNC-VERIFY-THE-DATE', '7','FUNC-VERIFY-THE-DATE')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FORMAT-1-YYDDD', 0,'FORMAT-1-YYDDD')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FORMAT-1-YYYYDDD', '05','FORMAT-1-YYYYDDD')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FORMAT-1-YYYYDDD-PACKED', '08','FORMAT-1-YYYYDDD-PACKED')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FORMAT-1-MMDDYY', '10','FORMAT-1-MMDDYY')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FORMAT-1-MMDDYY-SLASHES', '11','FORMAT-1-MMDDYY-SLASHES')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FORMAT-1-MMDDYYYY', '12','FORMAT-1-MMDDYYYY')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FORMAT-1-MMDDYYYY-SLASHES', '13','FORMAT-1-MMDDYYYY-SLASHES')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FORMAT-1-0YYYYMMDD-PACKED', '14','FORMAT-1-0YYYYMMDD-PACKED')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FORMAT-1-YYMMDD', '20','FORMAT-1-YYMMDD')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FORMAT-1-YYYYMMDD', '21','FORMAT-1-YYYYMMDD')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FORMAT-1-REL-MEDICARE', '80','FORMAT-1-REL-MEDICARE')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FORMAT-2-YYYYDDD', '05','FORMAT-2-YYYYDDD')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FORMAT-2-YYYYDDD-PACKED', '08','FORMAT-2-YYYYDDD-PACKED')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FORMAT-2-MMDDYY', '10','FORMAT-2-MMDDYY')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FORMAT-2-MMDDYY-SLASHES', '11','FORMAT-2-MMDDYY-SLASHES')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FORMAT-2-MMDDYYYY', '12','FORMAT-2-MMDDYYYY')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FORMAT-2-MMDDYYYY-SLASHES', '13','FORMAT-2-MMDDYYYY-SLASHES')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FORMAT-2-0YYYYMMDD-PACKED', '14','FORMAT-2-0YYYYMMDD-PACKED')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FORMAT-2-YYMMDD', '20','FORMAT-2-YYMMDD')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FORMAT-2-YYYYMMDD', '21','FORMAT-2-YYYYMMDD')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FORMAT-2-REL-MEDICARE', '80','FORMAT-2-REL-MEDICARE')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'CONVERT-RET-GOOD', 0,'CONVERT-RET-GOOD')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'CONVERT-RET-BAD-DAY-OR-FMT', 4,'CONVERT-RET-BAD-DAY-OR-FMT')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'CONVERT-RET-BAD-MTH-OR-FMT', 8,'CONVERT-RET-BAD-MTH-OR-FMT')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'CONVERT-RET-BAD-FORMAT', 12,'CONVERT-RET-BAD-FORMAT')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'CONVERT-RET-BAD-FUNCTION', 16,'CONVERT-RET-BAD-FUNCTION')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'CONVERT-RET-BAD-RANGE-INP', 28,'CONVERT-RET-BAD-RANGE-INP')[1]
        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'CONVERT-RET-BAD-BINARY-LARGE', 32,'CONVERT-RET-BAD-BINARY-LARGE')[1]
# EIB Fields
        result = Add_Variable(self.EIBMemory,self._LINKAGE_SECTIONVars,'EIB-FIELDS', 0, 'X','EIB-FIELDS','',0,0,'','01','')
        self._LINKAGE_SECTIONVars = result[0]
        self.EIBMemory = result[1]
        result = Add_Variable(self.EIBMemory,self._LINKAGE_SECTIONVars,'EIBAID', 1, 'X','EIB-FIELDS','',0,0,'','05','')
        self._LINKAGE_SECTIONVars = result[0]
        self.EIBMemory = result[1]
        result = Add_Variable(self.EIBMemory,self._LINKAGE_SECTIONVars,'EIBCALEN', 4, 'S9','EIB-FIELDS','',0,0,'COMP','05','')
        self._LINKAGE_SECTIONVars = result[0]
        self.EIBMemory = result[1]
        result = Add_Variable(self.EIBMemory,self._LINKAGE_SECTIONVars,'EIBDATE', 7, 'S9','EIB-FIELDS','',0,0,'COMP-3','05','')
        self._LINKAGE_SECTIONVars = result[0]
        self.EIBMemory = result[1]
        result = Add_Variable(self.EIBMemory,self._LINKAGE_SECTIONVars,'IEBRCODE', 6, 'X','EIB-FIELDS','',0,0,'','05','')
        self._LINKAGE_SECTIONVars = result[0]
        self.EIBMemory = result[1]
        result = Add_Variable(self.EIBMemory,self._LINKAGE_SECTIONVars,'EIBTASKN', 7, 'S9','EIB-FIELDS','',0,0,'COMP-3','05','')
        self._LINKAGE_SECTIONVars = result[0]
        self.EIBMemory = result[1]
        result = Add_Variable(self.EIBMemory,self._LINKAGE_SECTIONVars,'EIBTIME', 7, 'S9','EIB-FIELDS','',0,0,'COMP-3','05','')
        self._LINKAGE_SECTIONVars = result[0]
        self.EIBMemory = result[1]
        result = Add_Variable(self.EIBMemory,self._LINKAGE_SECTIONVars,'EIBTRMID', 4, 'X','EIB-FIELDS','',0,0,'','05','')
        self._LINKAGE_SECTIONVars = result[0]
        self.EIBMemory = result[1]
        result = Add_Variable(self.EIBMemory,self._LINKAGE_SECTIONVars,'EIBTRNID', 4, 'X','EIB-FIELDS','',0,0,'','05','')
        self._LINKAGE_SECTIONVars = result[0]
        self.EIBMemory = result[1]


# PROCEDURE DIVISION
    def main(self,_arg1):
        try:
            self.EIBMemory=Retrieve_EIB_Area(self._INTERNALVars[0].value)
            self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'W-DATE-AREA', _arg1,'W-DATE-AREA')[1]
            self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'CONVERT-RET-GOOD', True,'CONVERT-RET-GOOD')[1]
            self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'WORK-FIELDS', 0,'WORK-FIELDS')[1]
            if Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'FUNC-CONV-THE-DATE','FUNC-CONV-THE-DATE') == True :
                self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FORMAT-AND-DATE', Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'W-FORMAT-AND-DATE-1','W-FORMAT-AND-DATE-1'),'FORMAT-AND-DATE')[1]
                self._100_CONVERT_INPUT_DATE()
                self._100_EXIT()
                if Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'CONVERT-RET-GOOD','CONVERT-RET-GOOD') :
                    self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FORMAT', Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'W-FORMAT-2','W-FORMAT-2'),'FORMAT')[1]
                    self._110_CONVERT_OUTPUT_DATE()
                    self._110_EXIT()
            elif Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'FUNC-ADJUST-THE-DATE','FUNC-ADJUST-THE-DATE') == True :
                self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FORMAT-AND-DATE', Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'W-FORMAT-AND-DATE-1','W-FORMAT-AND-DATE-1'),'FORMAT-AND-DATE')[1]
                self._100_CONVERT_INPUT_DATE()
                self._100_EXIT()
                if Check_Value_Numeric(Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'W-NUMBER-FIELD','W-NUMBER-FIELD') ) != True :
                    self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'CONVERT-RET-BAD-RANGE-INP', True,'CONVERT-RET-BAD-RANGE-INP')[1]
                elif Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'CONVERT-RET-GOOD','CONVERT-RET-GOOD') == True :
                    self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'WORK-DAYS',str(eval('Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,"W-NUMBER-FIELD","W-NUMBER-FIELD")+Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,"JULIAN-DDD","JULIAN-DDD")')),'WORK-DAYS')[1]
                    self._300_LEAP_YEAR_CHECK()
                    self._300_EXIT()
                    while Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'WORK-DAYS','WORK-DAYS') >Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'DAYS-IN-YEAR','DAYS-IN-YEAR'):
                        self.CMNDATCVMemory = Update_Variable(self.CMNDATCVMemory,self.variables_list,Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'DAYS-IN-YEAR','DAYS-IN-YEAR'), 'WORK-DAYS', 'WORK-DAYS','-1','')[1]
                        self.CMNDATCVMemory = Update_Variable(self.CMNDATCVMemory,self.variables_list,'1', 'JULIAN-YYYY', 'JULIAN-YYYY','','')[1]
                        self._300_LEAP_YEAR_CHECK()
                        self._300_EXIT()
                    while Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'WORK-DAYS','WORK-DAYS') <=0:
                        self.CMNDATCVMemory = Update_Variable(self.CMNDATCVMemory,self.variables_list,'1', 'JULIAN-YYYY', 'JULIAN-YYYY','-1','')[1]
                        self._300_LEAP_YEAR_CHECK()
                        self._300_EXIT()
                        self.CMNDATCVMemory = Update_Variable(self.CMNDATCVMemory,self.variables_list,Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'DAYS-IN-YEAR','DAYS-IN-YEAR'), 'WORK-DAYS', 'WORK-DAYS','','')[1]
                    self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'JULIAN-DDD', Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'WORK-DAYS','WORK-DAYS'),'JULIAN-DDD')[1]
                    self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FORMAT', Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'W-FORMAT-2','W-FORMAT-2'),'FORMAT')[1]
                    self._110_CONVERT_OUTPUT_DATE()
                    self._110_EXIT()
            elif Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'FUNC-CALC-DAYS-BETWEEN','FUNC-CALC-DAYS-BETWEEN') == True :
                self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'W-NUMBER-FIELD', 0,'W-NUMBER-FIELD')[1]
                self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FORMAT-AND-DATE', Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'W-FORMAT-AND-DATE-1','W-FORMAT-AND-DATE-1'),'FORMAT-AND-DATE')[1]
                self._100_CONVERT_INPUT_DATE()
                self._100_EXIT()
                if Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'CONVERT-RET-GOOD','CONVERT-RET-GOOD') :
                    self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'SAVE-JULIAN-DATE', Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'JULIAN-DATE','JULIAN-DATE'),'SAVE-JULIAN-DATE')[1]
                    self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FORMAT-AND-DATE', Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'W-FORMAT-AND-DATE-2','W-FORMAT-AND-DATE-2'),'FORMAT-AND-DATE')[1]
                    self._100_CONVERT_INPUT_DATE()
                    self._100_EXIT()
                    if Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'CONVERT-RET-GOOD','CONVERT-RET-GOOD') :
                        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'GREGORIAN-DATE', 0,'GREGORIAN-DATE')[1]
                        if Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'JULIAN-YYYY-X','JULIAN-YYYY-X')  > Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'SAVE-JUL-YYYY-X','SAVE-JUL-YYYY-X') :
                            while Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'JULIAN-YYYY-X','JULIAN-YYYY-X') !=Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'SAVE-JUL-YYYY-X','SAVE-JUL-YYYY-X'):
                                self.CMNDATCVMemory = Update_Variable(self.CMNDATCVMemory,self.variables_list,'1', 'JULIAN-YYYY', 'JULIAN-YYYY','-1','')[1]
                                self._300_LEAP_YEAR_CHECK()
                                self._300_EXIT()
                                self.CMNDATCVMemory = Update_Variable(self.CMNDATCVMemory,self.variables_list,Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'DAYS-IN-YEAR','DAYS-IN-YEAR'), 'W-NUMBER-FIELD', 'W-NUMBER-FIELD','-1','')[1]
                        else:
                            while Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'JULIAN-YYYY-X','JULIAN-YYYY-X') !=Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'SAVE-JUL-YYYY-X','SAVE-JUL-YYYY-X'):
                                self._300_LEAP_YEAR_CHECK()
                                self._300_EXIT()
                                self.CMNDATCVMemory = Update_Variable(self.CMNDATCVMemory,self.variables_list,Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'DAYS-IN-YEAR','DAYS-IN-YEAR'), 'W-NUMBER-FIELD', 'W-NUMBER-FIELD','','')[1]
                                self.CMNDATCVMemory = Update_Variable(self.CMNDATCVMemory,self.variables_list,'1', 'JULIAN-YYYY', 'JULIAN-YYYY','','')[1]
                        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'W-NUMBER-FIELD',str(eval('Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,"W-NUMBER-FIELD","W-NUMBER-FIELD")+Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,"SAVE-JUL-DDD","SAVE-JUL-DDD")-Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,"JULIAN-DDD","JULIAN-DDD")')),'W-NUMBER-FIELD')[1]
            elif Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'FUNC-VERIFY-THE-DATE','FUNC-VERIFY-THE-DATE') == True :
                self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FORMAT-AND-DATE', Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'W-FORMAT-AND-DATE-1','W-FORMAT-AND-DATE-1'),'FORMAT-AND-DATE')[1]
                self._100_CONVERT_INPUT_DATE()
                self._100_EXIT()
            elif Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'FUNC-CONV-TO-DAY-OF-WEEK','FUNC-CONV-TO-DAY-OF-WEEK') == True :
                self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FORMAT-AND-DATE', Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'W-FORMAT-AND-DATE-1','W-FORMAT-AND-DATE-1'),'FORMAT-AND-DATE')[1]
                self._100_CONVERT_INPUT_DATE()
                self._100_EXIT()
                if Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'CONVERT-RET-GOOD','CONVERT-RET-GOOD') :
                    self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FORMAT-80-REL-MEDICARE', True,'FORMAT-80-REL-MEDICARE')[1]
                    self._110_CONVERT_OUTPUT_DATE()
                    self._110_EXIT()
                    self.CMNDATCVMemory = Update_Variable(self.CMNDATCVMemory,self.variables_list,Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'W-DATE-2-FULLWORD','W-DATE-2-FULLWORD'), 'GIVING', 'RELATIVE-DATE','','')[1]
                    self.CMNDATCVMemory = Update_Variable(self.CMNDATCVMemory,self.variables_list,Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'RELATIVE-DATE','RELATIVE-DATE'), '+7', 'RELATIVE-DATE','/','WEEK-DAY')[1]
                    self.CMNDATCVMemory = Update_Variable(self.CMNDATCVMemory,self.variables_list,'+1', 'WEEK-DAY', 'WEEK-DAY','','')[1]
                    self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'DISPLAY-WEEK-DAY', Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'WEEK-DAY','WEEK-DAY'),'DISPLAY-WEEK-DAY')[1]
                    self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'W-FORMAT-2', Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'DISPLAY-WEEK-DAY','DISPLAY-WEEK-DAY'),'W-FORMAT-2')[1]
                    self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'W-DATE-2', Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'DAY-OF-WEEK-X(WEEK-DAY)','DAY-OF-WEEK-X(WEEK-DAY)'),'W-DATE-2')[1]
            elif Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'FUNC-CONV-SYSTEM-DATE','FUNC-CONV-SYSTEM-DATE') == True :
                self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'JULIAN-YYYYDDD','__ACCEPT DAY YYYYDDD','JULIAN-YYYYDDD')[1]
                self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FORMAT', Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'W-FORMAT-2','W-FORMAT-2'),'FORMAT')[1]
                self._110_CONVERT_OUTPUT_DATE()
                self._110_EXIT()
            elif Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'FUNC-ADJUST-YYMMM','FUNC-ADJUST-YYMMM') == True :
                self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FORMAT-AND-DATE', Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'W-FORMAT-AND-DATE-1','W-FORMAT-AND-DATE-1'),'FORMAT-AND-DATE')[1]
                self._100_CONVERT_INPUT_DATE()
                self._100_EXIT()
                if Check_Value_Numeric(Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'W-NUMBER-FIELD','W-NUMBER-FIELD') ) != True  or Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'W-NUMBER-FIELD','W-NUMBER-FIELD') == True :
                    self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'CONVERT-RET-BAD-RANGE-INP', True,'CONVERT-RET-BAD-RANGE-INP')[1]
                elif Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'CONVERT-RET-GOOD','CONVERT-RET-GOOD') == True :
                    self.CMNDATCVMemory = Update_Variable(self.CMNDATCVMemory,self.variables_list,Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'W-NUMBER-FIELD','W-NUMBER-FIELD'), '+1000', 'ADJUST-YY','/','ADJUST-MMM')[1]
                    if int(Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'ADJUST-YY','ADJUST-YY'))  != 0 and int(Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'ADJUST-MMM','ADJUST-MMM'))  != 0:
                        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'CONVERT-RET-BAD-RANGE-INP', True,'CONVERT-RET-BAD-RANGE-INP')[1]
                    else:
                        if int(Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'ADJUST-YY','ADJUST-YY'))  == 0:
                            self.CMNDATCVMemory = Update_Variable(self.CMNDATCVMemory,self.variables_list,Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'W-NUMBER-FIELD','W-NUMBER-FIELD'), '+12', 'ADJUST-YY','/','ADJUST-MMM')[1]
                        self._220_JULIAN_TO_GREGORIAN()
                        self._220_EXIT()
                        self.CMNDATCVMemory = Update_Variable(self.CMNDATCVMemory,self.variables_list,Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'GREG-MM','GREG-MM'), 'ADJUST-MMM', 'ADJUST-MMM','','')[1]
                        if Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'ADJUST-MMM','ADJUST-MMM') > True :
                            self.CMNDATCVMemory = Update_Variable(self.CMNDATCVMemory,self.variables_list,'+12', 'ADJUST-MMM', 'ADJUST-MMM','-1','')[1]
                            self.CMNDATCVMemory = Update_Variable(self.CMNDATCVMemory,self.variables_list,'+1', 'ADJUST-YY', 'ADJUST-YY','','')[1]
                        elif Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'ADJUST-MMM','ADJUST-MMM') < True :
                            self.CMNDATCVMemory = Update_Variable(self.CMNDATCVMemory,self.variables_list,'+12', 'ADJUST-MMM', 'ADJUST-MMM','','')[1]
                            self.CMNDATCVMemory = Update_Variable(self.CMNDATCVMemory,self.variables_list,'+1', 'ADJUST-YY', 'ADJUST-YY','-1','')[1]
                        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'GREG-MM', Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'ADJUST-MMM','ADJUST-MMM'),'GREG-MM')[1]
                        self.CMNDATCVMemory = Update_Variable(self.CMNDATCVMemory,self.variables_list,Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'ADJUST-YY','ADJUST-YY'), 'GREG-YYYY', 'GREG-YYYY','','')[1]
                        self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'JULIAN-YYYY-X', Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'GREG-YYYY-X','GREG-YYYY-X'),'JULIAN-YYYY-X')[1]
                        self._300_LEAP_YEAR_CHECK()
                        self._300_EXIT()
                        if Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'MT-DAYS-IN-MONTH(GREG-MM,LEAP-INDEX)','MT-DAYS-IN-MONTH(GREG-MM,LEAP-INDEX)')  < Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'GREG-DD-X','GREG-DD-X') :
                            self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'GREG-DD-X', Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'MT-DAYS-IN-MONTH(GREG-MM,LEAP-INDEX)','MT-DAYS-IN-MONTH(GREG-MM,LEAP-INDEX)'),'GREG-DD-X')[1]
                        self._210_GREGORIAN_TO_JULIAN()
                        self._210_EXIT()
                        if Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'CONVERT-RET-GOOD','CONVERT-RET-GOOD') :
                            self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'FORMAT', Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'W-FORMAT-2','W-FORMAT-2'),'FORMAT')[1]
                            self._110_CONVERT_OUTPUT_DATE()
                            self._110_EXIT()
            else:
                self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'CONVERT-RET-BAD-FUNCTION', True,'CONVERT-RET-BAD-FUNCTION')[1]
            if Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'FORMAT-2-REL-MEDICARE','FORMAT-2-REL-MEDICARE')  and Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'CONVERT-RET-GOOD','CONVERT-RET-GOOD') :
                if Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'FORMAT-1-REL-MEDICARE','FORMAT-1-REL-MEDICARE') :
                    self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'W-DATE-2', Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'W-DATE-1','W-DATE-1'),'W-DATE-2')[1]
                else:
                    self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'W-DATE-2', Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'LOW-VALUES','LOW-VALUES'),'W-DATE-2')[1]
            return [Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'W-DATE-AREA','W-DATE-AREA')]
        except Exception as e:
            self._error_handler(e)
    def _100_CONVERT_INPUT_DATE(self):
        try:
            if Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'FORMAT-08-YYYYDDD-PACKED','FORMAT-08-YYYYDDD-PACKED') == True :
                self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'DATE-AREA(1:1)', Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'LOW-VALUES','LOW-VALUES'),'DATE-AREA(1:1)')[1]
                if Check_Value_Numeric(Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'DA-08-14-PACKED','DA-08-14-PACKED') ) :
                    self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'JULIAN-YYYYDDD', Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'DA-08-14-PACKED','DA-08-14-PACKED'),'JULIAN-YYYYDDD')[1]
                    self._200_VALIDATE_JULIAN_DATE()
                    self._200_EXIT()
                else:
                    self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'CONVERT-RET-BAD-RANGE-INP', True,'CONVERT-RET-BAD-RANGE-INP')[1]
            elif Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'FORMAT-05-YYYYDDD','FORMAT-05-YYYYDDD') == True :
                self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'JULIAN-DATE', Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'DATE-AREA','DATE-AREA')[1- 1:1 - 1 + 7],'JULIAN-DATE')[1]
                self._200_VALIDATE_JULIAN_DATE()
                self._200_EXIT()
            elif Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'FORMAT-12-MMDDYYYY','FORMAT-12-MMDDYYYY') == True :
                self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'GREG-YYYY-X', Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'DATE-AREA','DATE-AREA')[5- 1:5 - 1 + 4],'GREG-YYYY-X')[1]
                self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'GREG-MMDD-X', Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'DATE-AREA','DATE-AREA')[1- 1:1 - 1 + 4],'GREG-MMDD-X')[1]
                self._210_GREGORIAN_TO_JULIAN()
                self._210_EXIT()
            elif Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'FORMAT-13-MMDDYYYY-SLASHES','FORMAT-13-MMDDYYYY-SLASHES') == True :
                self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'GREG-YYYY-X', Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'DATE-AREA','DATE-AREA')[7- 1:7 - 1 + 4],'GREG-YYYY-X')[1]
                self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'GREG-MM-X', Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'DATE-AREA','DATE-AREA')[1- 1:1 - 1 + 2],'GREG-MM-X')[1]
                self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'GREG-DD-X', Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'DATE-AREA','DATE-AREA')[4- 1:4 - 1 + 2],'GREG-DD-X')[1]
                self._210_GREGORIAN_TO_JULIAN()
                self._210_EXIT()
            elif Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'FORMAT-14-0YYYYMMDD-PACKED','FORMAT-14-0YYYYMMDD-PACKED') == True :
                if Check_Value_Numeric(Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'DA-08-14-PACKED','DA-08-14-PACKED') ) :
                    self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'GREG-YYYYMMDD', Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'DA-08-14-PACKED','DA-08-14-PACKED'),'GREG-YYYYMMDD')[1]
                    self._210_GREGORIAN_TO_JULIAN()
                    self._210_EXIT()
                else:
                    self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'CONVERT-RET-BAD-RANGE-INP', True,'CONVERT-RET-BAD-RANGE-INP')[1]
            elif Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'FORMAT-21-YYYYMMDD','FORMAT-21-YYYYMMDD') == True :
                self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'GREGORIAN-DATE', Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'DATE-AREA','DATE-AREA')[1- 1:1 - 1 + 8],'GREGORIAN-DATE')[1]
                self._210_GREGORIAN_TO_JULIAN()
                self._210_EXIT()
            elif Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'FORMAT-80-REL-MEDICARE','FORMAT-80-REL-MEDICARE') == True :
                self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'RELATIVE-DATE', Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'DA-80-HALFWORD','DA-80-HALFWORD'),'RELATIVE-DATE')[1]
                self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'DATE-SAVE', Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'DA-80-HALFWORD','DA-80-HALFWORD'),'DATE-SAVE')[1]
                if Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'RELATIVE-DATE','RELATIVE-DATE')  < -21917 :
                    self.CMNDATCVMemory = Update_Variable(self.CMNDATCVMemory,self.variables_list,'+1', 'RELATIVE-DATE', 'RELATIVE-DATE','-1','')[1]
                self.CMNDATCVMemory = Update_Variable(self.CMNDATCVMemory,self.variables_list,Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'RELATIVE-DATE','RELATIVE-DATE'), '+365.25', 'RELATIVE-DATE','/','REMAINING-DAYS')[1]
                if int(Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'REMAINING-DAYS','REMAINING-DAYS'))  <= 0:
                    self.CMNDATCVMemory = Update_Variable(self.CMNDATCVMemory,self.variables_list,'+1', 'RELATIVE-DATE', 'RELATIVE-DATE','-1','')[1]
                self.CMNDATCVMemory = Update_Variable(self.CMNDATCVMemory,self.variables_list,'1961', 'GIVING', 'JULIAN-YYYY','','')[1]
                if int(Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'RELATIVE-DATE','RELATIVE-DATE'))  == 0:
                    self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'DAY-WORK', Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'DATE-SAVE','DATE-SAVE'),'DAY-WORK')[1]
                else:
                    self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'DAYS-USED',str(eval('Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,"RELATIVE-DATE","RELATIVE-DATE")*+365.25')),'DAYS-USED')[1]
                    self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'DAYS-INTEGER', Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'DAYS-USED','DAYS-USED'),'DAYS-INTEGER')[1]
                    if Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'DAYS-INTEGER','DAYS-INTEGER')  < 0 and Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'DAYS-USED','DAYS-USED')  != Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'DAYS-INTEGER','DAYS-INTEGER') :
                        self.CMNDATCVMemory = Update_Variable(self.CMNDATCVMemory,self.variables_list,'+1', 'DAYS-INTEGER', 'DAYS-INTEGER','-1','')[1]
                    if Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'DAYS-INTEGER','DAYS-INTEGER')  < -21917 :
                        self.CMNDATCVMemory = Update_Variable(self.CMNDATCVMemory,self.variables_list,'+1', 'DAYS-INTEGER', 'DAYS-INTEGER','','')[1]
                    self.CMNDATCVMemory = Update_Variable(self.CMNDATCVMemory,self.variables_list,Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'DAYS-INTEGER','DAYS-INTEGER'), 'DATE-SAVE', 'GIVING','-1','')[1]
                if int(Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'DAY-WORK','DAY-WORK'))  == 0:
                    self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'JULIAN-DDD-X', '001','JULIAN-DDD-X')[1]
                else:
                    self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'JULIAN-DDD', Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'DAY-WORK','DAY-WORK'),'JULIAN-DDD')[1]
            elif Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'FORMAT-00-YYDDD','FORMAT-00-YYDDD') == True :
                self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'JULIAN-DATE(3:5)', Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'DATE-AREA','DATE-AREA')[1- 1:1 - 1 + 5],'JULIAN-DATE(3:5)')[1]
                if Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'JULIAN-YY-X','JULIAN-YY-X')  < Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'CWF-PIVOT-YEAR','CWF-PIVOT-YEAR') :
                    self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'JULIAN-CC-X', '20','JULIAN-CC-X')[1]
                else:
                    self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'JULIAN-CC-X', '19','JULIAN-CC-X')[1]
                self._200_VALIDATE_JULIAN_DATE()
                self._200_EXIT()
            elif Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'FORMAT-20-YYMMDD','FORMAT-20-YYMMDD') == True :
                self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'GREG-YYMMDD', Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'DATE-AREA','DATE-AREA')[1- 1:1 - 1 + 6],'GREG-YYMMDD')[1]
                self._210_GREGORIAN_TO_JULIAN()
                self._210_EXIT()
            elif Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'FORMAT-10-MMDDYY','FORMAT-10-MMDDYY') == True :
                self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'GREG-YY-X', Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'DATE-AREA','DATE-AREA')[5- 1:5 - 1 + 2],'GREG-YY-X')[1]
                self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'GREG-MMDD-X', Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'DATE-AREA','DATE-AREA')[1- 1:1 - 1 + 4],'GREG-MMDD-X')[1]
                self._210_GREGORIAN_TO_JULIAN()
                self._210_EXIT()
            elif Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'FORMAT-11-MMDDYY-SLASHES','FORMAT-11-MMDDYY-SLASHES') == True :
                self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'GREG-YY-X', Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'DATE-AREA','DATE-AREA')[7- 1:7 - 1 + 2],'GREG-YY-X')[1]
                self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'GREG-MM-X', Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'DATE-AREA','DATE-AREA')[1- 1:1 - 1 + 2],'GREG-MM-X')[1]
                self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'GREG-DD-X', Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'DATE-AREA','DATE-AREA')[4- 1:4 - 1 + 2],'GREG-DD-X')[1]
                self._210_GREGORIAN_TO_JULIAN()
                self._210_EXIT()
            else:
                self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'CONVERT-RET-BAD-FORMAT', True,'CONVERT-RET-BAD-FORMAT')[1]

        except Exception as e:
            self._error_handler(e)
    def _100_EXIT(self):
        try:
            return
        except Exception as e:
            self._error_handler(e)
    def _110_CONVERT_OUTPUT_DATE(self):
        try:
            self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'DATE-AREA', '____spaces','DATE-AREA')[1]
            if Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'FORMAT-08-YYYYDDD-PACKED','FORMAT-08-YYYYDDD-PACKED') == True :
                self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'W-DATE-2-5-PACKED', Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'JULIAN-YYYYDDD','JULIAN-YYYYDDD'),'W-DATE-2-5-PACKED')[1]
            elif Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'FORMAT-05-YYYYDDD','FORMAT-05-YYYYDDD') == True :
                self.CMNDATCVMemory = Set_Variable(self.CMNDATCVMemory,self.variables_list,'W-DATE-2(1:7)', Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'JULIAN-DATE','JULIAN-DATE'),'W-DATE-2(1:7)')[1]
            elif Get_Variable_Value(self.CMNDATCVMemory,self.variables_list,'FORMAT-12-MMDDYYYY','FORMAT-12-MMDDYYYY') == True :
                self._220_JULIAN_TO_GREGORIAN()
                self._220_EXIT()
