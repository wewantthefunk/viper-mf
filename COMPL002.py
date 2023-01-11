from COMPL001 import *
from COMPL001 import *
from cobol_variable import *
import importlib
call_result = None
# PROGRAM-ID: COMPL002
variables_list = []
# DATA DIVISION
# WORKING-STORAGE SECTION.
_WORKING_STORAGE_SECTIONVars = []
variables_list.append(_WORKING_STORAGE_SECTIONVars)
_WORKING_STORAGE_SECTIONVars = Add_Variable(_WORKING_STORAGE_SECTIONVars,'PASSED-VARIABLE', 6, 'X','PASSED-VARIABLE','',0)
# PROCEDURE DIVISION
def main_COMPL002():
    global call_result, variables_list
    Set_Variable(variables_list,'PASSED-VARIABLE', 'TT8C8 ','PASSED-VARIABLE')
    call_result = None
    call_result = main_COMPL001(Get_Variable_Value(variables_list,'PASSED-VARIABLE','PASSED-VARIABLE'))
    if call_result != None:
        for cr in call_result:
            x = 0
            Set_Variable(variables_list,'PASSED-VARIABLE', cr ,'PASSED-VARIABLE')
    Display_Variable(variables_list,'expecting returned value of 00','literal',False,False)
    Display_Variable(variables_list,'','literal',True,True)
    Display_Variable(variables_list,'actual returned value is    ','literal',False,False)
    Display_Variable(variables_list,'PASSED-VARIABLE','PASSED-VARIABLE',False,False)
    Display_Variable(variables_list,'','literal',True,True)
    Set_Variable(variables_list,'PASSED-VARIABLE', 'J4A   ','PASSED-VARIABLE')
    call_result = None
    call_result = main_COMPL001(Get_Variable_Value(variables_list,'PASSED-VARIABLE','PASSED-VARIABLE'))
    if call_result != None:
        for cr in call_result:
            x = 0
            Set_Variable(variables_list,'PASSED-VARIABLE', cr ,'PASSED-VARIABLE')
    Display_Variable(variables_list,'expecting returned value of 00','literal',False,False)
    Display_Variable(variables_list,'','literal',True,True)
    Display_Variable(variables_list,'actual returned value is    ','literal',False,False)
    Display_Variable(variables_list,'PASSED-VARIABLE','PASSED-VARIABLE',False,False)
    Display_Variable(variables_list,'','literal',True,True)
    return []
if __name__ == '__main__':
    main_COMPL002()
