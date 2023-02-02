from cobol_variable import *
import importlib, inspect, os, sys
# PROGRAM-ID: HELLOW65
class HELLOW65Class:
    def __init__(self):
        self.call_result = None
        self.HELLOW65Memory = EMPTY_STRING
        self.EIBMemory = EMPTY_STRING
        self.variables_list = []
        self._INTERNALVars = []
        self.variables_list.append(self._INTERNALVars)
        self._INTERNALVars = Add_Variable('', self._INTERNALVars, 'MODULE-NAME', 0, 'X', 'MODULE-NAME', '', 0, 0, '', '01')[0]
        self._INTERNALVars[0].value = 'HELLOW65'
        self.error_func = None
        self.calling_module = None
        initialize()
# DATA DIVISION
# WORKING-STORAGE SECTION.
        self._WORKING_STORAGE_SECTIONVars = []
        self.variables_list.append(self._WORKING_STORAGE_SECTIONVars)
        result = Add_Variable(self.HELLOW65Memory,self._WORKING_STORAGE_SECTIONVars,'TEST-DATA', 0, 'X','TEST-DATA','',0,0,'','01','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.HELLOW65Memory = result[1]
        result = Add_Variable(self.HELLOW65Memory,self._WORKING_STORAGE_SECTIONVars,'MONTH-TABLE-AREA', 0, 'X','TEST-DATA','',0,0,'','05','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.HELLOW65Memory = result[1]
        result = Add_Variable(self.HELLOW65Memory,self._WORKING_STORAGE_SECTIONVars,'MONTH-TABLE-AREA-SUB-1', 24, 'X','MONTH-TABLE-AREA','',0,0,'','10','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.HELLOW65Memory = result[1]
        result = Add_Variable(self.HELLOW65Memory,self._WORKING_STORAGE_SECTIONVars,'MONTH-TABLE-AREA-SUB-2', 24, 'X','MONTH-TABLE-AREA','',0,0,'','10','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.HELLOW65Memory = result[1]
        result = Add_Variable(self.HELLOW65Memory,self._WORKING_STORAGE_SECTIONVars,'MONTH-TABLE-AREA-SUB-3', 24, 'X','MONTH-TABLE-AREA','',0,0,'','10','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.HELLOW65Memory = result[1]
        result = Add_Variable(self.HELLOW65Memory,self._WORKING_STORAGE_SECTIONVars,'MONTH-TABLE-AREA-SUB-4', 24, 'X','MONTH-TABLE-AREA','',0,0,'','10','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.HELLOW65Memory = result[1]
        result = Add_Variable(self.HELLOW65Memory,self._WORKING_STORAGE_SECTIONVars,'REDEFINEStmqj', 0, 'X','TEST-DATA','MONTH-TABLE-AREA',0,0,'','05','')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.HELLOW65Memory = result[1]
        result = Add_Variable(self.HELLOW65Memory,self._WORKING_STORAGE_SECTIONVars,'MONTH-INDEX', 10, '9','MONTH-TABLE','',0,0,'','10')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.HELLOW65Memory = result[1]
        result = Add_Variable(self.HELLOW65Memory,self._WORKING_STORAGE_SECTIONVars,'MONTH-TABLE', 0, 'X','REDEFINEStmqj','MONTH-TABLE-AREA',12,0,'','10','MONTH-INDEX')
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.HELLOW65Memory = result[1]
