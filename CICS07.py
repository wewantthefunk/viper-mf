from cobol_variable import *
import importlib, inspect, os, sys
# PROGRAM-ID: CICS07
class CICS07Class:
    def __init__(self):
        self.call_result = None
        self.terminate = False
        self.debug_line = '0'
        self.calling_module = None
        self.CICS07Memory = EMPTY_STRING
        self.EIBMemory = EMPTY_STRING
        self.SPECIALREGISTERSMemory = EMPTY_STRING
        self.variables_list = []
        self._INTERNALVars = []
        self.variables_list.append(self._INTERNALVars)
        self._INTERNALVars = Add_Variable('', self._INTERNALVars, 'MODULE-NAME', 0, 'X', 'MODULE-NAME', '', 0, 0, '', '01')[0]
        self._INTERNALVars[0].value = 'CICS07'
        self._INTERNALVars[0].address_module = AddressModule(self, 0)
        self._INTERNALVars = Add_Variable('', self._INTERNALVars, 'CALLING-MODULE-NAME', 0, 'X', 'CALLING-MODULE-NAME', '', 0, 0, '', '01')[0]
        self._INTERNALVars = Add_Variable(self.SPECIALREGISTERSMemory, self._INTERNALVars, 'SORT-RETURN', 4, '9', 'SORT-RETURN', '', 0, 0, '', '01')[0]
        self._INTERNALVars = Add_Variable(self.SPECIALREGISTERSMemory, self._INTERNALVars, 'RETURN-CODE', 4, '9', 'RETURN-CODE', '', 0, 0, '', '01')[0]
        result = Allocate_Memory(self._INTERNALVars,self.SPECIALREGISTERSMemory)
        self._INTERNALVars = result[0]
        self.SPECIALREGISTERSMemory = result[1]
        self.SPECIALREGISTERSMemory = Set_Variable(self.SPECIALREGISTERSMemory,self.variables_list,'SORT-RETURN', 0,'SORT-RETURN')[1]
        self.SPECIALREGISTERSMemory = Set_Variable(self.SPECIALREGISTERSMemory,self.variables_list,'RETURN-CODE', 0,'RETURN-CODE')[1]
        self.error_func = None
        self.calling_module = None
        self.job_name = EMPTY_STRING
        self.job_step = EMPTY_STRING
        self.dd_name_list = []
        self._DataDivisionVars = []
        self.variables_list.append(self._DataDivisionVars)
        self.EIBList = []
        self.variables_list.append(self.EIBList)
        self._FILE_CONTROLVars = []
        initialize()
# DATA DIVISION
# WORKING-STORAGE SECTION.
        self._DataDivisionVars = Add_Variable(self.CICS07Memory,self._DataDivisionVars,'TEST-DATA', 8, 'X','TEST-DATA','',0,0,'','01','',False,'')[0]
        self._DataDivisionVars = Add_Variable(self.CICS07Memory,self._DataDivisionVars,'FIRST-TIME', 1, 'X','FIRST-TIME','',0,0,'','01','',False,'')[0]
        self._DataDivisionVars = Add_Variable(self.CICS07Memory,self._DataDivisionVars,'W-RESPONSE-CODE', 8, 'S9','W-RESPONSE-CODE','',0,0,'COMP','01','',False,'')[0]
        self._DataDivisionVars = Add_Variable(self.CICS07Memory,self._DataDivisionVars,'QUEUE-NAME', 8, 'X','QUEUE-NAME','',0,0,'','01','',False,'')[0]
        result = Allocate_Memory(self._DataDivisionVars,self.CICS07Memory)
        self._DataDivisionVars = result[0]
        self.CICS07Memory = result[1]
        self.CICS07Memory = Set_Variable(self.CICS07Memory,self.variables_list,'FIRST-TIME', 'Y','FIRST-TIME')[1]
        self.CICS07Memory = Set_Variable(self.CICS07Memory,self.variables_list,'QUEUE-NAME', 'TESTQ','QUEUE-NAME')[1]
# EIB Fields
# Inserted Copybook: copybooks/EIB.CPY
        self.EIBList = Add_Variable(self.EIBMemory,self.EIBList,'EIB-FIELDS', 0, 'X','EIB-FIELDS','',0,0,'','01','',False,'')[0]
        self.EIBList = Add_Variable(self.EIBMemory,self.EIBList,'EIBAID', 1, 'X','EIB-FIELDS','',0,0,'','05','',False,'')[0]
        self.EIBList = Add_Variable(self.EIBMemory,self.EIBList,'EIBCALEN', 4, 'S9','EIB-FIELDS','',0,0,'COMP','05','',False,'')[0]
        self.EIBList = Add_Variable(self.EIBMemory,self.EIBList,'EIBDATE', 7, 'S9','EIB-FIELDS','',0,0,'COMP-3','05','',False,'')[0]
        self.EIBList = Add_Variable(self.EIBMemory,self.EIBList,'IEBRCODE', 6, 'X','EIB-FIELDS','',0,0,'','05','',False,'')[0]
        self.EIBList = Add_Variable(self.EIBMemory,self.EIBList,'EIBTASKN', 7, 'S9','EIB-FIELDS','',0,0,'COMP-3','05','',False,'')[0]
        self.EIBList = Add_Variable(self.EIBMemory,self.EIBList,'EIBTIME', 7, 'S9','EIB-FIELDS','',0,0,'COMP-3','05','',False,'')[0]
        self.EIBList = Add_Variable(self.EIBMemory,self.EIBList,'EIBTRMID', 4, 'X','EIB-FIELDS','',0,0,'','05','',False,'')[0]
        self.EIBList = Add_Variable(self.EIBMemory,self.EIBList,'EIBTRNID', 4, 'X','EIB-FIELDS','',0,0,'','05','',False,'')[0]
        self.EIBList = Add_Variable(self.EIBMemory,self.EIBList,'EIBRESP', 8, 'S9','EIB-FIELDS','',0,0,'COMP','05','',False,'')[0]
        self.EIBList = Add_Variable(self.EIBMemory,self.EIBList,'EIBRESP2', 8, 'S9','EIB-FIELDS','',0,0,'COMP','05','',False,'')[0]


        result = Allocate_Memory(self.EIBList,self.EIBMemory)
        self.EIBList = result[0]
        self.EIBMemory = result[1]
# PROCEDURE DIVISION
    def main(self,caller,*therest):
        try:
            self.EIBMemory=Retrieve_EIB_Area(self._INTERNALVars[0].value)
            self.calling_module = caller
            self._INTERNALVars[1].value = '&&*'
            self._INTERNALVars[1].address_module = AddressModule(caller, 0)
            self.debug_line = '18'
