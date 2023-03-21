from cobol_variable import *
import importlib, inspect, os, sys
# PROGRAM-ID: RANDSTR
class RANDSTRClass:
    def __init__(self):
        self.call_result = None
        self.debug_line = '0'
        self.calling_module = None
        self.RANDSTRMemory = EMPTY_STRING
        self.EIBMemory = EMPTY_STRING
        self.variables_list = []
        self._INTERNALVars = []
        self._EIBListVars = []
        self.variables_list.append(self._INTERNALVars)
        self.variables_list.append(self._EIBListVars)
        self._INTERNALVars = Add_Variable('', self._INTERNALVars, 'MODULE-NAME', 0, 'X', 'MODULE-NAME', '', 0, 0, '', '01')[0]
        self._INTERNALVars[0].value = 'RANDSTR'
        self._INTERNALVars[0].address_module = AddressModule(self, 0)
        self._INTERNALVars = Add_Variable('', self._INTERNALVars, 'CALLING-MODULE-NAME', 0, 'X', 'CALLING-MODULE-NAME', '', 0, 0, '', '01')[0]
        self.error_func = None
        self.calling_module = None
        initialize()
# ENVIRONMENT DIVISION
# DATA DIVISION
# WORKING-STORAGE SECTION.
        self._WORKING_STORAGE_SECTIONVars = []
        self.variables_list.append(self._WORKING_STORAGE_SECTIONVars)
        result = Add_Variable(self.RANDSTRMemory,self._WORKING_STORAGE_SECTIONVars,'STRING-COUNTER', 2, '9','STRING-COUNTER','',0,0,'','01','',False)
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.RANDSTRMemory = result[1]
        result = Add_Variable(self.RANDSTRMemory,self._WORKING_STORAGE_SECTIONVars,'RANDOM-NUMBER', 9, '9','RANDOM-NUMBER','',0,0,'','01','',False)
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.RANDSTRMemory = result[1]
        result = Add_Variable(self.RANDSTRMemory,self._WORKING_STORAGE_SECTIONVars,'CHARACTER-CODE', 3, '9','CHARACTER-CODE','',0,0,'','01','',False)
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.RANDSTRMemory = result[1]
        result = Add_Variable(self.RANDSTRMemory,self._WORKING_STORAGE_SECTIONVars,'CURRENT-CHARACTER', 1, 'X','CURRENT-CHARACTER','',0,0,'','01','',False)
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.RANDSTRMemory = result[1]
        result = Add_Variable(self.RANDSTRMemory,self._WORKING_STORAGE_SECTIONVars,'SEED', 9, '9','SEED','',0,0,'','01','',False)
        self._WORKING_STORAGE_SECTIONVars = result[0]
        self.RANDSTRMemory = result[1]
# LINKAGE SECTION.
        self._LINKAGE_SECTIONVars = []
        self.variables_list.append(self._LINKAGE_SECTIONVars)
        result = Add_Variable(self.RANDSTRMemory,self._LINKAGE_SECTIONVars,'STRING-LENGTH', 2, '9','STRING-LENGTH','',0,0,'','01','',False)
        self._LINKAGE_SECTIONVars = result[0]
        self.RANDSTRMemory = result[1]
        result = Add_Variable(self.RANDSTRMemory,self._LINKAGE_SECTIONVars,'RANDOM-STRING', 50, 'X','RANDOM-STRING','',0,0,'','01','',False)
        self._LINKAGE_SECTIONVars = result[0]
        self.RANDSTRMemory = result[1]
        self.RANDSTRMemory = Set_Variable(self.RANDSTRMemory,self.variables_list,'STRING-COUNTER', 1,'STRING-COUNTER')[1]
# EIB Fields
        result = Add_Variable(self.EIBMemory,self._EIBListVars,'EIB-FIELDS', 0, 'X','EIB-FIELDS','',0,0,'','01','',False)
        self._LINKAGE_SECTIONVars = result[0]
        self.EIBMemory = result[1]
        result = Add_Variable(self.EIBMemory,self._EIBListVars,'EIBAID', 1, 'X','EIB-FIELDS','',0,0,'','05','',False)
        self._LINKAGE_SECTIONVars = result[0]
        self.EIBMemory = result[1]
        result = Add_Variable(self.EIBMemory,self._EIBListVars,'EIBCALEN', 4, 'S9','EIB-FIELDS','',0,0,'COMP','05','',False)
        self._LINKAGE_SECTIONVars = result[0]
        self.EIBMemory = result[1]
        result = Add_Variable(self.EIBMemory,self._EIBListVars,'EIBDATE', 7, 'S9','EIB-FIELDS','',0,0,'COMP-3','05','',False)
        self._LINKAGE_SECTIONVars = result[0]
        self.EIBMemory = result[1]
        result = Add_Variable(self.EIBMemory,self._EIBListVars,'IEBRCODE', 6, 'X','EIB-FIELDS','',0,0,'','05','',False)
        self._LINKAGE_SECTIONVars = result[0]
        self.EIBMemory = result[1]
        result = Add_Variable(self.EIBMemory,self._EIBListVars,'EIBTASKN', 7, 'S9','EIB-FIELDS','',0,0,'COMP-3','05','',False)
        self._LINKAGE_SECTIONVars = result[0]
        self.EIBMemory = result[1]
        result = Add_Variable(self.EIBMemory,self._EIBListVars,'EIBTIME', 7, 'S9','EIB-FIELDS','',0,0,'COMP-3','05','',False)
        self._LINKAGE_SECTIONVars = result[0]
        self.EIBMemory = result[1]
        result = Add_Variable(self.EIBMemory,self._EIBListVars,'EIBTRMID', 4, 'X','EIB-FIELDS','',0,0,'','05','',False)
        self._LINKAGE_SECTIONVars = result[0]
        self.EIBMemory = result[1]
        result = Add_Variable(self.EIBMemory,self._EIBListVars,'EIBTRNID', 4, 'X','EIB-FIELDS','',0,0,'','05','',False)
        self._LINKAGE_SECTIONVars = result[0]
        self.EIBMemory = result[1]


# PROCEDURE DIVISION
    def main(self,caller,_arg1,_arg2,*therest):
        try:
            self.EIBMemory=Retrieve_EIB_Area(self._INTERNALVars[0].value)
            self.calling_module = caller
            self._INTERNALVars[1].value = '&&*'
            self._INTERNALVars[1].address_module = AddressModule(caller, 0)
