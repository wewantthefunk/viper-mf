from datetime import datetime
import os, math, string, time
from pathlib import Path
from os.path import exists
from random import *

ACCEPT_VALUE_FLAG = "__ACCEPT "
ADD_COMMAND = "add"
ADDRESS_INDICATOR = "&&*"
ALPHANUMERIC_DATA_TYPE = "X"
BIG_BYTE_ORDER = "big"
BINARY_INDICATOR = "BINARY"
CLOSE_PARENS = ")"
COBOL_FILE_VARIABLE_TYPE = "COBOLFileVariable"
COLON = ":"
COMMA = ","
COMM_AREA_EXT = "comm.txt"
COMP_INDICATOR = "COMP"
COMP_3_INDICATOR = "COMP-3"
COMP_5_INDICATOR = "COMP-5"
DASH = "-"
DATA_FILE_EXT = ".dat"
DFHCOMMAREA_NAME = "DFHCOMMAREA"
DISP_COMMAND = "display"
DIVISION_OPERATOR = "/"
DOUBLE_EQUALS = "=="
EIB_EXT = "eib.txt"
EMPTY_STRING = ""
END_OF_FILE_STATUS = "10"
GET_COMMAND = "get"
GREATER_THAN = ">"
GREATER_THAN_EQUAL = ">="
HEX_DISPLAY_PREFIX = "0x"
HEX_PREFIX = "_hex_"
HIGH_VALUES_NAME = 'HIGH-VALUES'
INDEX_FILE_EXT = ".idx"
INDEX_FILE_FIELD_DELIMITER = "^^^"
LENGTH_FUNC_PREFIX = "len_"
LESS_THAN = "<"
LESS_THAN_EQUAL = "<="
LEVEL_88 = "88"
LITERAL = "literal"
LOW_VALUES_NAME = 'LOW-VALUES'
MULTIPLICATION_OPERATOR = "*"
NEGATIVE_SIGN = "-"
NEGATIVE_SIGNED_HEX_FLAG = "D"
NEWLINE = "\n"
NOT_EQUALS = "!="
NUMERIC_DATA_TYPE = "9"
NUMERIC_SIGNED_DATA_TYPE = "S9"
ONE = 1
OPEN_PARENS = "("
PERIOD = "."
PLUS_SIGN = "+"
POINTER_DATATYPE = "P"
POSITIVE_SIGN = "+"
POSITIVE_SIGNED_HEX_FLAG = "C"
SET_COMMAND = "set"
SORT_IDENTIFIER = "___sd"
SPACE = " "
SPACES_INITIALIZER = "____spaces"
SYSIN_ENV_VARIABLE = "SYSIN"
UNSIGNED_HEX_FLAG = "F"
UPD_COMMAND = "update"
ZERO = 0
ZERO_MASK = "0"
ZERO_STRING = "0"

BINARY_COMP_LIST = [
    COMP_5_INDICATOR
    , COMP_INDICATOR
    , BINARY_INDICATOR
]

COMP_DATA_TYPES = [
    COMP_INDICATOR
    , COMP_3_INDICATOR
    , COMP_5_INDICATOR
    , BINARY_INDICATOR
]

EBCDIC_ASCII_CHART = [

]

NUMERIC_DATA_TYPES = [
    NUMERIC_DATA_TYPE
    , NUMERIC_SIGNED_DATA_TYPE
]

NUMERIC_SIGNS = [
    POSITIVE_SIGN
    , NEGATIVE_SIGN
]

class EBCDICASCII:
    def __init__(self, hex_val: str, ebcdic_val: str, ascii_val: str, ascii_hex = '') -> None:
        self.hex_value = hex_val
        self.EBCDIC_value = ebcdic_val
        self.ASCII_value = ascii_val
        self.decimal_value = int(hex_val, 16)
        self.COMP3_value = ascii_val
        if ascii_hex == EMPTY_STRING:
            self.ASCII_hex = hex(ord(ascii_val))
        else:
            self.ASCII_hex = ascii_hex

class COBOLVariable:
    def __init__(self, name: str, length: int, data_type: str, parent: str, redefines: str, occurs_length: int, decimal_length: int, level: str, comp_indicator: str, pos: int, unpacked_length: int, index: str, array_pos: int, is_top_redefines: bool, display_mask = EMPTY_STRING):
        self.name = name
        self.length = length
        self.data_type = data_type
        self.parent = parent
        if parent != name:
            self.parent = parent
        else:
            self.parent = EMPTY_STRING
        self.value = EMPTY_STRING
        self.level88value = []
        self.occurs_values = []
        self.occurs_indexes = []
        self.redefines = redefines
        self.occurs_length = occurs_length
        self.level = level
        self.decimal_length = decimal_length
        self.is_hex = False
        self.comp_indicator = comp_indicator
        self.main_memory_position = pos
        self.redefine_length = 0
        self.child_length = 0
        self.child_length_divisor = 1
        self.sign = EMPTY_STRING
        self.unpacked_length = unpacked_length
        self.index_variable = index
        self.array_pos = array_pos
        self.is_top_redefines = is_top_redefines
        self.display_mask = display_mask
        self.children = []

class AddressModule:
    def __init__(self, module, pos) -> None:
        self.module = module
        self.position = pos

class COBOLFileVariable:
    def __init__(self, name: str, assign: str, organization: str, access: str, record_key: str, file_status: str):
        if organization.strip() == EMPTY_STRING:
            organization = "SEQUENTIAL"
        self.name = name
        self.assign = assign
        self.organization = organization
        self.access = access
        self.record_key = record_key
        self.file_status = file_status
        self.file_pointer = None
        self.record = EMPTY_STRING
        self.parent = EMPTY_STRING
        self.redefines = EMPTY_STRING
        self.filename = EMPTY_STRING
        self.method = EMPTY_STRING
        self.in_memory_array = []
        self.is_in_memory = False

    def open_file(self, main_variable_memory, variables_list, method: str):
        filename = os.getenv(self.assign)

        if self.organization == "INDEXED":
            filename = filename + INDEX_FILE_EXT

        if filename == None:
            result = Set_Variable(main_variable_memory, variables_list, self.file_status, '35', self.file_status)
            return result[1]
        elif exists(filename) == False and self.method == "INPUT":
            result = Set_Variable(main_variable_memory, variables_list, self.file_status, '35', self.file_status)
            return result[1]

        self.file_pointer = open(filename, method)

        result = Set_Variable(main_variable_memory, variables_list, self.file_status, '00', self.file_status)

        self.filename = filename
        self.method = method

        return result[1]

    def close_file(self):
        if self.file_pointer != None:
            self.file_pointer.close()
            self.file_pointer = None

        return

    def append_data(self, data: str):
        if self.is_in_memory:
            self.in_memory_array.append(data)
        else:
            self._write_sequential(data)

        return 
    
    def _read_sequential(self):
        line = self.file_pointer.readline().decode('latin-1').replace(NEWLINE, EMPTY_STRING).replace("\r", EMPTY_STRING)

        at_end = False

        if not line:
            at_end = True
            line = EMPTY_STRING

        return [line, at_end]
    
    def _read_indexed(self, main_variable_memory, variables_list):
        key_data = Get_Variable_Value(main_variable_memory, variables_list, self.record_key, [self.record_key], True)
        self.file_pointer.seek(0)
        line = self.file_pointer.readline().decode('latin-1').replace(NEWLINE, EMPTY_STRING).replace("\r", EMPTY_STRING)
        rec_line = -1
        while line:
            s = line.split(INDEX_FILE_FIELD_DELIMITER)
            if s[0] == key_data:
                rec_line = int(s[1])
                break
            line = self.file_pointer.readline().decode('latin-1').replace(NEWLINE, EMPTY_STRING).replace("\r", EMPTY_STRING)
        
        if rec_line == -1:
            return [EMPTY_STRING, True]

        data_filename = self.filename[0:len(self.filename) - len(INDEX_FILE_EXT)] + DATA_FILE_EXT
        data_file = open(data_filename, "rb")
        data_line = data_file.readline().decode('latin-1').replace(NEWLINE, EMPTY_STRING).replace("\r", EMPTY_STRING)
        count = 0
        at_end = False
        while data_line and count < rec_line:
            data_line = data_file.readline().decode('latin-1').replace(NEWLINE, EMPTY_STRING).replace("\r", EMPTY_STRING)
            count = count + 1

        if count != rec_line:
            at_end = True
            
        data_file.close()

        return [data_line, at_end]
    
    def _write_sequential(self, data: str):
        if self.file_pointer != None:
            if not data.endswith(NEWLINE):
                data = data + NEWLINE
            self.file_pointer.write(bytes(data, 'utf-8'))
    
        return

    def _write_indexed(self, data: str, key_value: str):
        if self.file_pointer == None:
            return
        
        data_filename = self.filename[0:len(self.filename) - len(INDEX_FILE_EXT)] + DATA_FILE_EXT

        data_file = open(data_filename, "ab+")
        data_file.write(bytes(NEWLINE + data, 'utf-8'))
        count = -1
        data_file.seek(0)
        line = data_file.readline()
        while line:
            line = data_file.readline().decode('latin-1').replace(NEWLINE, EMPTY_STRING).replace("\r", EMPTY_STRING)
            count = count + 1
        data_file.close()

        self.file_pointer.write(bytes(NEWLINE + key_value + INDEX_FILE_FIELD_DELIMITER + str(count),"utf-8"))

        self.file_pointer.flush()

        return
    
    def read(self, main_variable_memory, variables_list):
        if self.organization == "LINE SEQUENTIAL" or self.organization == "SEQUENTIAL":
            return self._read_sequential()
        elif self.organization == "INDEXED":
            return self._read_indexed(main_variable_memory, variables_list)
        return [EMPTY_STRING, True]

    def write(self, data: str, key_data: str):
        if self.organization == "LINE SEQUENTIAL" or self.organization == "SEQUENTIAL":
            self._write_sequential(data)
        if self.organization == "INDEXED":
            self._write_indexed(data, key_data)

        return

def Add_Variable(main_variable_memory, list, name: str, length: int, data_type: str, parent: str, redefines = EMPTY_STRING, occurs_length = 0, decimal_len = 0, comp_indicator = EMPTY_STRING, level = "01", index = EMPTY_STRING, is_top_redefines = False, display_mask = EMPTY_STRING):
    for l in list:
        if l.name == name:
            return [list, main_variable_memory]

    unpacked_length = length

    if comp_indicator == COMP_3_INDICATOR and data_type in NUMERIC_DATA_TYPES:
        length = math.ceil((length + 1) / 2)
        # fix the math to account for the sign nibble
        if length == 2:
            unpacked_length = 4
        elif length == 1:
            unpacked_length = 2
    elif (comp_indicator in BINARY_COMP_LIST) and data_type in NUMERIC_DATA_TYPES:
        if length < 5:
            length = 2
        elif length < 10:
            length = 4
        else:
            length = 8

    if redefines != EMPTY_STRING:
        orig_redefines = redefines
        next_redefines = redefines
        while next_redefines != EMPTY_STRING:
            rv = _find_variable(list, redefines)
            if rv != None:
                if rv.level == level:
                    rv.redefine_length = ZERO
                next_redefines = rv.redefines
                redefines = next_redefines
                if level == LEVEL_88:
                    next_pos = rv.main_memory_position
                else:
                    next_pos = rv.main_memory_position + rv.redefine_length
                rv.redefine_length = rv.redefine_length + length
            else:
                next_redefines = EMPTY_STRING
                next_pos = -1

        redefines = orig_redefines
    else:
        next_pos = len(main_variable_memory)

    if level == LEVEL_88:
        redefines = EMPTY_STRING

    list.append(COBOLVariable(name, length, data_type, parent, redefines, occurs_length, decimal_len, level, comp_indicator, next_pos, unpacked_length, index, len(list), is_top_redefines, display_mask))

    return [list, main_variable_memory]

def _find_all_variables(var_list, name: str):
    result = []

    for var in var_list:
        if var.name == name:
            result.append(var)

    return result

def _find_all_sibling_variables(var_list, name: str):
    result = []

    for var in var_list:
        if var.parent == name:
            result.append(var)

    return result

def Allocate_Memory(var_list, memory: str):
    memory_temp = EMPTY_STRING

    for var in reversed(var_list):
        children = _find_all_children(var_list, var.name)

        for child in children:
            var.children.append(child)

        if var.occurs_length > 0:
            pv = _find_variable(var_list, var.parent)
            pv.child_length_divisor = var.occurs_length

    for var in reversed(var_list):
        if len(var.children) > 0 and var.child_length == 0:
            length = _get_length_of_children(var)
            if var.occurs_length > 0:
                length = length * var.occurs_length
                var.child_length_divisor = var.occurs_length
            var.child_length = length

    array_length = []
    array_vars = []
    redefine_length = []
    redefine_vars = []
    position = len(memory)
    highest_level = 0
    for var in var_list:
        if var.redefines != EMPTY_STRING:
            continue
        var.main_memory_position = position   
        length = var.length
        if var.occurs_length > 0:
            length = var.length * var.occurs_length

        if int(var.level) < highest_level:
            position = var.main_memory_position + length
            highest_level = int(var.level)
        else:
            position = position + length
            highest_level = int(var.level)
        
    last_known_redefine = EMPTY_STRING
    for var in var_list:
        if var.redefines == EMPTY_STRING:
            continue
        
        if var.redefines != last_known_redefine:
            last_known_redefine = var.redefines
            rv = _find_variable(var_list, last_known_redefine)
            position = rv.main_memory_position

        var.main_memory_position = position        
        if int(var.level) < highest_level:
            position = var.main_memory_position + var.length
            highest_level = int(var.level)
        else:
            position = position + var.length
            highest_level = int(var.level)

    memory_temp = memory + pad(var_list[len(var_list) - 1].main_memory_position + var_list[len(var_list) - 1].length)

    return [var_list, memory_temp]

def _get_length_of_children(var: COBOLVariable):
    result = ZERO

    for child in var.children:
        if child.length == 0:
            result = result + child.child_length
        else:
            occurs = 1
            if child.occurs_length > 0:
                occurs = child.occurs_length
            result = result + (child.length * occurs)
            result = result + _get_length_of_children(child)

    return result

def Display_Memory(mem_len, list):
    main_variable_memory = EMPTY_STRING
    count = 0
    for x in range(0,mem_len):
        main_variable_memory = main_variable_memory + str(count)
        count = count + 1
        if count > 9:
            count = 0
    for var in list:
        length = var.length
        if length == 0:
            length = var.child_length
        print(var.name + "," + str(var.main_memory_position) + "," + str(length) + "," + main_variable_memory[var.main_memory_position:var.main_memory_position + length])

    return

def _update_parent_child_length(main_variable_memory, list, name: str, length: int, sub_occurs_length: int):
    skip_add = False
    if name == EMPTY_STRING:
        return [skip_add, main_variable_memory]

    for l in list:
        if l.name == name:
            l.child_length = l.child_length + length
            if l.occurs_length > 0:
                pc = SPACE
                if l.data_type in NUMERIC_DATA_TYPES:
                    pc = ZERO_STRING
                main_variable_memory = main_variable_memory + pad_char(l.occurs_length * length, pc)
                skip_add = True
            if sub_occurs_length > 0:
                pc = SPACE
                if l.data_type in NUMERIC_DATA_TYPES:
                    pc = ZERO_STRING
                main_variable_memory = main_variable_memory + pad_char(sub_occurs_length * length, pc)
                l.length = l.length + length * sub_occurs_length
                skip_add = True
            if l.parent != EMPTY_STRING and not l.is_top_redefines:
                result = _update_parent_child_length(main_variable_memory, list, l.parent, length, ZERO)
                skip_add = result[0]
                main_variable_memory = result[1]
            break

    return [skip_add, main_variable_memory]

def _find_variable(list, name: str):
    result = None

    for var in list:
        if var.name == name:
            result = var
            break

    return result

def _find_all_children(list, name: str):
    result = []

    for var in list:
        if var.parent == name:
            result.append(var)

    return result

def Open_File(main_variable_memory, variables_list, var_list, name: str, method: str):
    success = main_variable_memory
    for var in var_list:
        if var.name == name:
            success = var.open_file(main_variable_memory, variables_list, convert_open_method(method))            
            break

    return success

def Close_File(var_list, name: str):
    success = False
    for var in var_list:
        if var.name == name:
            var.close_file()
            success = True
            break

    return success

def Get_Sort_Array(var_list, name: str):
    for var in var_list:
        if var.name == name:
            return var.in_memory_array
        
    return []

def Get_Sort_Record_Name(var_list, name: str):
    for var in var_list:
        if var.name == name:
            return var.record
        
    return EMPTY_STRING

def Append_Data_To_File(var_list, name: str, data: str):
    success = False
    for var in var_list:
        if var.record == name:
            var.append_data(data)
            success = True
            break

    return success

def Sort_File(var_list, variables_list, name: str, key_fields):
    success = False
    start_positions = []
    sort_key_len = 0
    for key_field in key_fields:
        for var_list_name in variables_list:
            key_var = _find_variable(var_list_name, key_field)
            if key_var != None:
                parent_var = _find_variable(var_list_name, key_var.parent)
                if parent_var != None:
                    start_pos = key_var.main_memory_position - parent_var.main_memory_position
                    start_positions.append([start_pos, start_pos + key_var.length])
                    sort_key_len = sort_key_len + key_var.length
                    x = 0

    for var in var_list:
        if var.name == name:
            if var.is_in_memory:
                for x in range(0,len(var.in_memory_array)):
                    data = var.in_memory_array[x]
                    sort_key = EMPTY_STRING
                    for sp in start_positions:
                        sort_key = sort_key + data[sp[0]: sp[1]]
                    var.in_memory_array[x] = sort_key + var.in_memory_array[x]
                var.in_memory_array.sort()
                for x in range(0,len(var.in_memory_array)):
                    var.in_memory_array[x] = var.in_memory_array[x][sort_key_len:]
                
                success = True
                break

    return success

def Read_File(main_variable_memory, var_list, file_rec_var_list, name: str, into_rec = "", at_end_clause = ""):
    read_result = [False, main_variable_memory]
    for var in var_list:
        if var.name == name:
            read_result = var.read(main_variable_memory, file_rec_var_list)
            if read_result[1]:
                main_variable_memory = Set_Variable(main_variable_memory,file_rec_var_list,var.file_status,END_OF_FILE_STATUS,var.file_status)[1]
                read_result = [True, main_variable_memory]
                break
            # set the variable from the read
            into_record = var.record
            if into_rec != EMPTY_STRING:
                into_record = into_rec
            read_result = Set_Variable(main_variable_memory, file_rec_var_list, into_record, read_result[0], [into_record], 0)
            read_result[0] = not read_result[0]
            break

    return read_result

def Write_File(var_list, variables_list, main_variable_memory: str, name: str):
    for var in var_list:
        if var.record == name:
            data = Get_Variable_Value(main_variable_memory, variables_list, name, name, True)
            key_value = Get_Variable_Value(main_variable_memory, variables_list, var.record_key, var.record_key, True)
            # write the value from the variable indicated in 'name' parameter
            var.write(data, key_value)
            break

    return

def Set_File_Record(var_list, name: str, record: str):
    is_in_memory_array = False
    if name.endswith(SORT_IDENTIFIER):
        name = name.replace(SORT_IDENTIFIER, EMPTY_STRING)
        is_in_memory_array = True

    for var in var_list:
        if var.name == name:
            var.record = record
            var.is_in_memory = is_in_memory_array
            break

    return var_list

def Exec_Function(module: str, func_name: str):
    result = EMPTY_STRING
    if func_name == "CURRENT-DATE":
        result = datetime.today().strftime('%Y%m%d%H%M%S%f')
    elif func_name.startswith("RANDOM"):
        s = func_name.split("(")
        result = gen_rand_number(int(s[1].replace(")", EMPTY_STRING)))
    elif func_name.startswith("WHEN-COMPILED"):
        ti_c = os.path.getmtime('converted/' + module + '.py')
        date_time = datetime.fromtimestamp(ti_c)
        result = date_time.strftime('%Y%m%d%H%M%S')

    return result

def Add_File_Variable(list, name: str, assign: str, organization: str, access: str, record_key: str, file_status: str):
    for l in list:
        if l.name == name:
            return list

    list.append(COBOLFileVariable(name, assign, organization, access, record_key, file_status))

    return list

def Search_Variable_Array(main_variable_memory, variable_lists, target, operand1_list, operator_list, operand2_list, is_all_array, not_found_func, self_obj = None, boolean_list = None):
    if boolean_list == None:
        boolean_list = []
    return _search_Variable_Array(main_variable_memory, variable_lists, operand1_list, operator_list, operand2_list, is_all_array, target, not_found_func, self_obj, boolean_list)

def _search_Variable_Array(main_variable_memory, variable_lists, operand1_list: str, operator_list: str, operand2_list, is_all_array, target, not_found_func, self_obj, boolean_list):
    result = [False, main_variable_memory]
    found = False

    parent_var = None
    for var_list in variable_lists:
        array_var = _find_variable(var_list, target)
        if array_var != None:
            parent_var = _find_variable(var_list, array_var.parent)
            break

    if array_var == None or parent_var == None:
        return result

    start_at = 0

    for var_list in variable_lists:
        index_var = _find_variable(var_list, array_var.index_variable)
        if index_var != None:
            break

    if index_var == None:
        return result

    if is_all_array <= 0:
        start_at = int(Get_Variable_Value(main_variable_memory, variable_lists, index_var.name, index_var.name)) - 1
        if start_at < 0:
            start_at = 0

    compare_results = []
    found = False
    count = 0
    
    for operand1 in operand1_list:
        operand2 = operand2_list[count]
        operator = operator_list[count]
        main_variable_memory = Set_Variable(main_variable_memory, variable_lists, index_var.name, start_at + 1, index_var.name)[1]
        for x in range(start_at, array_var.occurs_length):
            if str(operand1).isnumeric():
                val = operand1
            else:
                val = Get_Variable_Value(main_variable_memory, variable_lists, operand1, operand1)
                if val == EMPTY_STRING:
                    val = operand1

            if str(operand2).isnumeric():
                val2 = operand2
            else:
                val2 = Get_Variable_Value(main_variable_memory, variable_lists, operand2, operand2)
                if val2 == EMPTY_STRING:
                    val2 = operand2
                    
            if operator == DOUBLE_EQUALS:
                found = val == val2
            elif operator == NOT_EQUALS:
                found = val != val2
            elif operator == GREATER_THAN:
                found = val > val2
            elif operator == GREATER_THAN_EQUAL:
                found = val >= val2
            elif operator == LESS_THAN:
                found = val < val2
            elif operator == LESS_THAN_EQUAL:
                found = val <= val2

            if found:
                break

            if x + 2 <= array_var.occurs_length:
                main_variable_memory = Set_Variable(main_variable_memory, variable_lists, index_var.name, x + 2, index_var.name)[1]

        count = count + 1
        compare_results.append(found)

    eval_string = EMPTY_STRING
    count = 0
    for compare_result in compare_results:
        eval_string = eval_string + str(compare_result) + " == True "
        if count < len(boolean_list):
            eval_string = eval_string + SPACE + boolean_list[count].lower() + SPACE
            count = count + 1
    
    found = eval(eval_string)

    result = [found, main_variable_memory]

    return result

def Set_Variable_Address(caller_module, main_variable_memory, variable_lists, name: str, value, parent: str):
    var = None
    for var_list in variable_lists:
        var = _find_variable(var_list, name)
        if var != None:
            break

    if var != None:
        if type(value) == AddressModule:
            var.value = ADDRESS_INDICATOR
            var.address_module = value

        else:
            var2 = None
            for var_list in variable_lists:
                var2 = _find_variable(var_list, value)
                if var2 != None:
                    break

            if var2 != None:
                var.value = ADDRESS_INDICATOR
                if var2.data_type == POINTER_DATATYPE:
                    var.address_module = var2.address_module
                else:
                    var.address_module = AddressModule(caller_module, var2.name)

    return [True, main_variable_memory]

def Set_Variable(main_variable_memory, variable_lists, name: str, value, parent: str, index_pos = 0, caller_module = None):
    if type(value) == AddressModule or str(value).startswith(ADDRESS_INDICATOR):
        if str(value).startswith(ADDRESS_INDICATOR):
            value = AddressModule(caller_module, str(value).replace(ADDRESS_INDICATOR, EMPTY_STRING))
        return Set_Variable_Address(caller_module, main_variable_memory, variable_lists, name, value, name)

    found = [False, main_variable_memory]
    for var_list in variable_lists:
        found = _set_variable(main_variable_memory, var_list, name, value, [parent], index_pos, variable_lists, caller_module)
        if found[0]:
            break
    return found

def _set_variable(main_variable_memory, var_list, name: str, value: str, parent, index_pos: int, orig_var_list, caller_module):
    count = 0
    occurrence = 1
    if type(value) == list:
        value = str(value[0])
    else:
        value = str(value)
    var_name = name
    new_value = EMPTY_STRING
    is_hex = False
    sub_string = []

    if OPEN_PARENS in name:
        s = name.split(OPEN_PARENS)
        var_name = s[0]
        offset_val = s[1].replace(CLOSE_PARENS, EMPTY_STRING)
        if offset_val.isnumeric():
            occurrence = int(offset_val)
        elif COLON in offset_val:
            occurrence = 1
            s1 = offset_val.split(COLON)
            s_start = 1
            s_end = 1
            if s1[0].isnumeric():
                s_start = int(s1[0])
            else:
                s_start = int(Get_Variable_Value(main_variable_memory, orig_var_list, s1[0], offset_val))
            if s1[1].isnumeric():
                s_end = int(s1[1])
            else:
                s_end = int(Get_Variable_Value(main_variable_memory, orig_var_list, s1[1], offset_val))
            sub_string = [s_start - 1, s_end]
        else:
            occurrence = int(Get_Variable_Value(main_variable_memory, orig_var_list, offset_val, offset_val))

    if str(value).startswith(ACCEPT_VALUE_FLAG):
        value = parse_accept_statement(value)

    for var in var_list:
        if var.name == var_name or var.parent in parent:
            count = count + 1
            if var.level == LEVEL_88:
                if value == 'True':
                    main_variable_memory = Set_Variable(main_variable_memory, orig_var_list, var.parent, var.level88value, var.parent)[1]
                else:
                    vp = _find_variable(var_list, var.parent)
                    l = ZERO
                    if vp != None:
                        l = vp.length
                        if l == ZERO:
                            l = vp.child_length
                    t = EMPTY_STRING
                    ch = SPACE
                    if value.isnumeric():
                        ch = ZERO_STRING
                    t = pad_char(l, ch)
                    t1 = t + value
                    value = t1[len(t1) - l:]
                    var.level88value.append(value)
                return [True, main_variable_memory]
            elif var.data_type == POINTER_DATATYPE or var.value.startswith(ADDRESS_INDICATOR):
                var.address_module.module.set_value(var.address_module.position, value)
                return [True, main_variable_memory]
            else:
                if var.data_type in NUMERIC_DATA_TYPES:
                    if var.data_type == NUMERIC_SIGNED_DATA_TYPE:
                        if value.startswith(NEGATIVE_SIGN):
                            var.sign = NEGATIVE_SIGN
                            if var.comp_indicator not in BINARY_COMP_LIST:
                                value = value[1:]
                        else:
                            var.sign = POSITIVE_SIGN
                    pad_length = var.unpacked_length
                    if var.comp_indicator == COMP_3_INDICATOR:
                        if not value.endswith(POSITIVE_SIGNED_HEX_FLAG) and not value.endswith(NEGATIVE_SIGNED_HEX_FLAG) and not value.endswith(UNSIGNED_HEX_FLAG):
                            if var.data_type == NUMERIC_SIGNED_DATA_TYPE:
                                if var.sign == NEGATIVE_SIGN:
                                    value = value + NEGATIVE_SIGNED_HEX_FLAG
                                else:
                                    value = value + POSITIVE_SIGNED_HEX_FLAG
                            else:
                                value = value + UNSIGNED_HEX_FLAG
                    value = str(value)
                    value = value.rjust(pad_length, ZERO_STRING)
                if var.comp_indicator == COMP_3_INDICATOR:
                    if value.startswith(HEX_PREFIX):
                        value = value.replace(HEX_PREFIX, EMPTY_STRING)
                    value = convert_to_comp3(value, var)
                elif var.comp_indicator in BINARY_COMP_LIST:
                    if value.startswith(HEX_PREFIX):
                        value = value.replace(HEX_PREFIX, EMPTY_STRING)
                        new_value = EMPTY_STRING
                        for x in range(0, len(value), 2):
                            new_value = new_value + find_hex_value(value[x:x+2]).EBCDIC_value
                        value = new_value
                    else:
                        value = convert_to_comp(value, var)
                length = var.length
                if length == ZERO:
                    length = var.child_length
                var_parent = _find_variable(var_list, var.parent)
                start = var.main_memory_position
                if var_parent != None:
                    pl = int(var_parent.child_length / var_parent.child_length_divisor)
                    start = (pl * (occurrence - 1)) + start
                if str(value).startswith(HEX_PREFIX):
                    is_hex = True
                    value = value.replace(HEX_PREFIX, EMPTY_STRING)
                    new_value = EMPTY_STRING
                    for x in range(0, len(value), 2):
                        eh = find_hex_value(value[x:x+2])
                        new_value = new_value + eh.EBCDIC_value
                    value = new_value[:length]
                    var.is_hex = is_hex
                elif str(value) == SPACES_INITIALIZER:
                    value = pad(length)
                elif var.data_type not in NUMERIC_DATA_TYPES:
                    value = value.ljust(length, SPACE)
                
                if len(sub_string) > 0:
                    start = start + sub_string[0]
                    length = sub_string[1]
                    value = value[0:length]
                if var.name == DFHCOMMAREA_NAME:
                    _write_file(orig_var_list[0][0].value + COMM_AREA_EXT, value)
                else:
                    main_variable_memory = main_variable_memory[:start] + value[:length] + main_variable_memory[start + length:]
            return [True, main_variable_memory]
        else:
            count = count + 1

    return [False, main_variable_memory]

def Update_Variable(main_variable_memory, variable_lists, value: str, name: str, giving: str, modifier = '', remainder_var = ''):
    curr_val = Get_Variable_Value(main_variable_memory, variable_lists, name, name)
    var = None
    for var_list in variable_lists:
        var = _find_variable(var_list, name)
        if var != None:
            break

    if var == None:
        curr_val = int(name)
    elif var.data_type not in NUMERIC_DATA_TYPES:
        return False

    if modifier == EMPTY_STRING:
        curr_val = int(value) + curr_val
    elif modifier == MULTIPLICATION_OPERATOR:
        curr_val = int(value) * curr_val
    elif modifier == DIVISION_OPERATOR:
        remainder = int(value) % int(curr_val)
        if remainder_var != EMPTY_STRING:
            main_variable_memory = Set_Variable(main_variable_memory, variable_lists, str(remainder_var), str(remainder), remainder_var, 0)[1] 
        curr_val = str(int(int(value) / int(curr_val)))
    else:
        curr_val = (int(value) * int(modifier)) + curr_val

    result = Set_Variable(main_variable_memory, variable_lists, giving, str(curr_val), giving)

    return result

def Replace_Variable_Value(main_variable_memory, variable_lists, name: str, orig: str, rep: str):
    result = Get_Variable_Value(main_variable_memory, variable_lists, name, name, False)
    if result != EMPTY_STRING:
        orig_array = list(orig)
        rep_array = list(rep)
        count = 0
        for o in orig_array:
            result = result.replace(o, rep_array[count])
            count = count + 1

        main_variable_memory = Set_Variable(main_variable_memory, variable_lists, name, result, name)[1]
        return [True, main_variable_memory]

    return [False, main_variable_memory]

def Build_String(main_variable_memory, variable_lists, target: str, strings):

    concat_string = EMPTY_STRING
    for string in strings:
        # [['GREG-MMDD-X', 'SIZE'], ['GREG-YYYY-X', 'SIZE']]
        val = Get_Variable_Value(main_variable_memory, variable_lists, string[0], string[0], True)
        if string[1] == "SIZE":
            concat_string = concat_string + val
        if string[1] == "SPACE":
            index = val.index(SPACE)
            concat_string = concat_string + val[:index]

    main_variable_memory = Set_Variable(main_variable_memory, variable_lists, target, concat_string, target)[1]

    return main_variable_memory

def Get_Variable_Length(variable_lists, name: str):
    for var_list in variable_lists:
        var = _find_variable(var_list, name)
        if var != None:
            if var.length == ZERO:
                return var.child_length

            return var.length
    return ZERO

def Get_Variable_Address(caller_module, main_variable_memory, variable_lists, name: str, parent: str, force_str = False):
    var = None

    for var_list in variable_lists:
        var = _find_variable(var_list, name)
        if var != None:
            break

    if var == None and caller_module != None:
        result = caller_module.retrieve_pointer(name)
    elif var != None:
        result = AddressModule(caller_module, var.name)
    else:
        result = AddressModule(caller_module, 'not found')

    return result

def Get_Variable_Value(main_variable_memory, variable_lists, name: str, parent: str, force_str = False):
    t = EMPTY_STRING

    if name == LOW_VALUES_NAME:
        return pad_char(100, '\x00')
    
    if name == HIGH_VALUES_NAME:
        return pad_char(100, '\xff')

    if name.startswith(LENGTH_FUNC_PREFIX):
        type_result = Get_Variable_Length(variable_lists, name[len(LENGTH_FUNC_PREFIX):])
        return type_result

    for var_list in variable_lists:
        t = _get_variable_value(main_variable_memory, var_list, name, [parent], force_str, variable_lists)
        if t[1] > 0:
            break

    return t[0]

def _get_variable_value(main_variable_memory, var_list, name: str, parent, force_str, orig_var_list):
    count = 0
    found_count = 0
    occurrence = 1
    result = EMPTY_STRING
    var_name = name
    type_result = EMPTY_STRING
    sub_string = EMPTY_STRING

    if OPEN_PARENS in name and COLON not in name:
        s = name.split(OPEN_PARENS)
        var_name = s[0]
        if COMMA in s[1]:
            occurrence = _get_multidimensional_array_values(var_name, s[1].replace(CLOSE_PARENS, EMPTY_STRING), main_variable_memory, orig_var_list)
        else:
            offset_val = s[1].replace(CLOSE_PARENS, EMPTY_STRING)
            if offset_val.isnumeric():
                occurrence = int(offset_val)
            else:
                occurrence = int(Get_Variable_Value(main_variable_memory, orig_var_list, offset_val, offset_val))
    elif OPEN_PARENS in name and COLON in name:
        s = var_name.split(OPEN_PARENS)
        var_name = s[0]
        temp_sub_string = s[1].replace(CLOSE_PARENS, EMPTY_STRING).split(COLON)
        sub_string = str(int(temp_sub_string[0]) - 1) + COLON + str(int(temp_sub_string[0]) + int(temp_sub_string[1]) - 1)

    var = _find_variable(var_list, var_name)

    if var != None:
        if var.name == var_name or var.parent in parent:
            if var.name == DFHCOMMAREA_NAME:
                result = result + _read_file(orig_var_list[0][0].value + COMM_AREA_EXT)
                count = len(var_list)
                found_count = 1
            elif var.level == LEVEL_88:
                var_parent = _find_variable(var_list, var.parent)
                if var_parent != None:
                    result = str(Get_Variable_Value(main_variable_memory, orig_var_list, var_parent.name, var_parent.name)) in var.level88value
                else:
                    result = False
                count = len(var_list)
                found_count = 1
            elif var.value == ADDRESS_INDICATOR:
                if var.data_type == POINTER_DATATYPE:
                    result = ADDRESS_INDICATOR + var.address_module.position
                else:
                    result = var.address_module.module.retrieve_pointer(var.address_module.position)
                found_count = 1
                count = 1
            else:
                length = var.length
                if length == ZERO:
                    length = var.child_length
                if length == ZERO and var.redefines != EMPTY_STRING:
                    rvar = _find_variable(var_list, var.redefines)
                    length = rvar.length
                    if length == ZERO:
                        length = rvar.child_length
                var_parent = _find_variable(var_list, var.parent)
                if occurrence > 0 and var_parent != None:
                    if var_parent.occurs_length > 0:
                        if occurrence > var_parent.occurs_length:
                            result = EMPTY_STRING
                            found_count = 1
                            return [result, found_count, result, 1, var]
                        
                start = var.main_memory_position
                start = _calc_start_pos(var_list, var_parent, start, occurrence)
                result = main_variable_memory[start:start + length]

                if sub_string != EMPTY_STRING:
                    ss = sub_string.split(COLON)
                    result = result[int(ss[0]):int(ss[1])]

                if var.data_type in NUMERIC_DATA_TYPES:
                    if var.comp_indicator == COMP_3_INDICATOR:
                        result = convert_from_comp3(result, var)
                    elif var.comp_indicator in BINARY_COMP_LIST:
                        result = convert_from_comp(var, result)
                    elif var.data_type == NUMERIC_SIGNED_DATA_TYPE:
                        if var.sign == NEGATIVE_SIGN:
                            result = var.sign + result
                elif var.level == LEVEL_88:
                    result = result in var.level88value
                count = len(var_list)
                found_count = 1
    
    if var != None:
        if var.data_type in NUMERIC_DATA_TYPES and result != EMPTY_STRING:
            if result.endswith(PERIOD):
                result = result[0:len(result) - 1]

            result = result.strip()
            if result == EMPTY_STRING:
                result = ZERO_STRING
                
            type_result = int(result)
        else:
            type_result = result
    else:
        type_result = result

    if force_str:
        type_result = str(result)

    return [type_result, found_count, result, count, var]

def _calc_start_pos(var_list, var_parent: COBOLFileVariable, start: int, occurrence: int):
    result = start
    if var_parent != None:
        if var_parent.child_length > 0:
            pl = int(var_parent.child_length / var_parent.child_length_divisor)
            start = (pl * (occurrence - 1)) + start
            result = start
        else:
            result = result = _calc_start_pos(var_list, _find_variable(var_list, var_parent.parent), start, occurrence)
    return result

def _get_multidimensional_array_values(var_name: str, w_indexes: str, main_variable_memory: str, variable_lists):
    indexes = w_indexes.split(COMMA)
    parent_var = None
    var = None
    field_var = None
    occurence = 0

    for var_list in variable_lists:
        field_var = _find_variable(var_list, var_name)
        if field_var != None:
            break

    major_index = 0

    index = indexes[0]

    if index.isnumeric():
        major_index = major_index + Get_Variable_Value(main_variable_memory, variable_lists, index, index)
    else:
        if index.isnumeric():
            occurence = occurence + Get_Variable_Value(main_variable_memory, variable_lists, index, index)
        else:
            if PLUS_SIGN in index:                
                i1 = index.split(PLUS_SIGN, maxsplit=1)
                for i in i1:
                    i = i.replace(PLUS_SIGN, EMPTY_STRING)
                    if i.isnumeric():
                        major_index = major_index + int(i)
                    else:
                        major_index = major_index + Get_Variable_Value(main_variable_memory, variable_lists, i, i)
            else:
                major_index = major_index + Get_Variable_Value(main_variable_memory, variable_lists, index, index)

    sub_occurrences = 0
    main_occurrences = 0

    index = indexes[1]

    for var_list in variable_lists:
        var = _find_variable(var_list, index)
        if var != None:
            parent_var = _find_variable(var_list, var.parent)
            if parent_var != None:
                sub_occurrences = parent_var.occurs_length
                parent_parent_var = _find_variable(var_list, parent_var.parent)
                if parent_parent_var != None:
                    main_occurrences = parent_parent_var.occurs_length

    occurence = ((major_index - 1) * (sub_occurrences - 1)) + major_index

    if occurence > main_occurrences * sub_occurrences:
        occurence = occurence - 2

    if occurence <= 0:
        occurence = 1

    return occurence

def convert_from_comp3(temp_result: str, var: COBOLVariable):
    t = EMPTY_STRING
    result = EMPTY_STRING
    if temp_result[0:1] in NUMERIC_SIGNS:
        temp_result = temp_result[1:]
    for x in range(0, var.length):
        hv = find_hex_value_by_ebcdic(temp_result[x:x+1])
        t = t + hv.hex_value
    if t == EMPTY_STRING:
        temp_result = ZERO_STRING
    elif var.data_type == NUMERIC_DATA_TYPE:
        temp_result = t[0:len(t) - 1]
    elif t.endswith(NEGATIVE_SIGNED_HEX_FLAG):
        if var.data_type == NUMERIC_SIGNED_DATA_TYPE:
            var.sign = NEGATIVE_SIGN
        else:
            var = EMPTY_STRING
        temp_result = t[0:len(t) - 1]
    else:
        if var.data_type == NUMERIC_SIGNED_DATA_TYPE:
            var.sign = POSITIVE_SIGN
        else:
            var.sign = EMPTY_STRING
        temp_result = t[0:len(t) - 1]
    result = result +  var.sign + temp_result

    return result

def convert_from_comp(var: COBOLVariable, temp_result: str):
    result = EMPTY_STRING
    signed = var.data_type == NUMERIC_SIGNED_DATA_TYPE
    t = EMPTY_STRING
    for x in range(0, len(temp_result), 1):
        t = t + find_hex_value_by_ebcdic(temp_result[x:x+1]).hex_value
    result = result + str(fromhex(t, signed))  

    return result

def convert_to_comp3(value: str, var: COBOLVariable):
    result = EMPTY_STRING
    if len(value) % 2 != ZERO:
        value = ZERO_STRING + value

    for x in range(0,len(value), 2):
        hv = find_hex_value(value[x:x+2])
        result = result + hv.EBCDIC_value

    return result

def convert_to_comp(value, var):
    return tohex(int(value), var.length)

def convert_multi_comp(var_list, var: COBOLVariable, value: str):
    children = _find_all_children(var_list, var.name)
    new_value = EMPTY_STRING
    start = 0
    for child in children:
        l = child.length
        if l == ZERO:
            new_value = new_value + convert_multi_comp(var_list, var, value[start:])
        else:
            new_value = new_value + convert_to_comp(value[start:start+l], child)

    return new_value

def Display_Variable(main_variable_memory, variable_lists, name: str, parent: str, is_literal: bool, is_last: bool):
    dv = name
    if is_literal == False:
        get_length_of = False
        if name.startswith(LENGTH_FUNC_PREFIX):
            get_length_of = True
            name = name[len(LENGTH_FUNC_PREFIX):]
            dv = Get_Variable_Length(variable_lists, name)
        else:
            for var_list in variable_lists:            
                r = _get_variable_value(main_variable_memory, var_list, name, [parent], False, variable_lists)
                if r[1] > 0:
                    if get_length_of:
                        dv = str(r[4].length)
                    else:
                        dv = r[2]
                    if r[4] != None:
                        var = r[4]
                        if var.display_mask != EMPTY_STRING:
                            if var.display_mask.endswith(DASH):
                                if (int(dv) < 0):
                                    dv = dv + DASH
                                else:
                                    dv = dv + SPACE 

                                dv = dv[1:]

                            if COMMA in var.display_mask:
                                indices = _find_indices(COMMA, var.display_mask)
                                dv = dv[len(indices):]
                                for i in indices:
                                    dv = dv[0:i] + COMMA + dv[i:]

                            if ZERO_MASK in var.display_mask:
                                pos = 0
                                for c in var.display_mask:
                                    if c == ZERO_MASK and dv[pos:pos + 1] == ZERO_STRING:
                                        dv = dv[0:pos] + SPACE + dv[pos + 1:]
                                    pos = pos + 1

                            pos = 0
                            for c in dv:
                                if c == COMMA and dv[pos + 1:pos + 2] == SPACE:
                                    dv = dv[0:pos] + SPACE + dv[pos + 1:]
                                pos = pos + 1
                                        
                    break

    print_value(dv)

    return

def Translate_Arguments(sig_args, args):
    if len(args) == ZERO or sig_args == "()":
        return EMPTY_STRING

    return args

def Build_Comm_Area(module_name: str, data, variable_lists,eib_memory: str, term_id = "TERM", trans_id = "XXXX"):
    comm_area = EMPTY_STRING
    for d in data:
        comm_area = comm_area + d

    _write_file(module_name + COMM_AREA_EXT, comm_area)

    eib_memory = Set_Variable(eib_memory, variable_lists, "EIBCALEN", len(comm_area), "EIBCALEN")[1]
    eib_memory = Set_Variable(eib_memory, variable_lists, "EIBDATE", format_date_cyyddd(), "EIBDATE")[1]
    eib_memory = Set_Variable(eib_memory, variable_lists, "EIBTIME", get_current_time(), "EIBTIME")[1]
    eib_memory = Set_Variable(eib_memory, variable_lists, "EIBTRMID", term_id, "EIBTRMID")[1]
    eib_memory = Set_Variable(eib_memory, variable_lists, "EIBTRNID", trans_id, "EIBTRNID")[1]

    _write_binary_file(module_name + EIB_EXT, bytes(eib_memory, 'utf-8'))

    return eib_memory    

def Retrieve_Comm_Area(main_variable_memory, variable_lists, variables, module_name: str):
    data = _read_file(module_name + COMM_AREA_EXT)
    for variable in variables:
        main_variable_memory = Set_Variable(main_variable_memory, variable_lists, variable, data, variable)[1]
    return main_variable_memory

def Retrieve_EIB_Area(module_name: str):
    eib_data = _read_file(module_name + EIB_EXT, False)
    return eib_data

def append_file_data(file: str, data: str):
    _append_file(file, data)
    return

def _append_file(file: str, data: str):
    _append_binary_file(file,bytes(data, 'utf-8'))
    return

def _append_binary_file(file: str, data):
    _write_file_data(file,data,"ab")
    return

def write_file_data(file: str, data: str):
    _write_file(file, data)
    return

def _write_file(file: str, data: str):
    _write_binary_file(file,bytes(data, 'utf-8'))
    return

def _write_binary_file(file: str, data):
    _write_file_data(file,data,"wb")
    return

def _write_file_data(file: str, data, method: str):
    f = open(file,method)
    f.write(data)
    f.close()
    return

def _read_file(file: str, remove_line_breaks = True):
    if exists(file) == False:
        return EMPTY_STRING
    result = EMPTY_STRING
    with open(file, mode="rb") as file:
        for line in file:
            line = str(line, encoding="utf-8")
            if remove_line_breaks:
                line = line.replace(NEWLINE, EMPTY_STRING)
            result = result + line
    return result

def cat_file(file: str):
    with open(file, 'r') as f:
        print(f.read())
    return

def format_date_cyyddd():
    now = datetime.now()
    century = str(now.year)[0:1]
    if century == '1':
        century = '0'
    else:
        century = '1'
    cyyddd = f"{century}{now.year % 100:02}{now.timetuple().tm_yday:03}".rjust(7, ZERO_STRING)
    return cyyddd

def get_current_time():
    now = datetime.now()
    time = now.strftime("%H%M%S").rjust(7, ZERO_STRING)
    return time

def milliseconds_since_1900():
    start = datetime(1900, 1, 1)
    now = datetime.now()
    diff = now - start
    milliseconds = diff.total_seconds() * 1000
    return int(milliseconds)

def print_value(l: str):
    end_l = EMPTY_STRING
    if l == EMPTY_STRING:
        end_l = NEWLINE
    print(l, end=end_l)
    return

def gen_rand(length: int):
    return ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=length))

def gen_rand_number(limit):
    return randint(0,limit)

def Check_Value_Numeric(value):
    return str(value).isnumeric()

def Get_Spaces(length: int):
    return pad(length)

def pad(l: int):
    return pad_char(l, SPACE)

def pad_char(l: int, ch: str):
    result = ""
    for x in range(l):
        result = result + ch

    return result

def _find_indices(ch: str, string: str):
    indexes = []
    index = -1
    while True:
        index = string.find(ch, index+1)
        if index == -1:
            break
        indexes.append(index)

    return indexes

def convert_open_method(method: str):
    if method == "INPUT":
        return "rb"
    elif method == "OUTPUT":
        return "ab"
    elif method == "INPUT-OUTPUT" or method == "I-O":
        return "ab+"
    
    return "ab+"

def convert_EBCDIC_hex_to_string(input: str, var: COBOLVariable):
    result = HEX_DISPLAY_PREFIX + input
    return result

def convert_string_to_EBCDIC_value(input: str, var: COBOLVariable):
    result = EMPTY_STRING
    for c in input:
        if (var.data_type == NUMERIC_DATA_TYPE or var.data_type == NUMERIC_SIGNED_DATA_TYPE) and var.comp_indicator != EMPTY_STRING:
            result = result + c.encode('utf-8').hex().upper()
        else:            
            result = result + find_hex_value(c).EBCDIC_value
    return result

def find_hex_value(value: str):
    for hv in EBCDIC_ASCII_CHART:
        if hv.hex_value == value:
            return hv

    return EBCDIC_ASCII_CHART[0]

def find_hex_value_by_ascii(value: str):
    for hv in EBCDIC_ASCII_CHART:
        if hv.ASCII_value == value:
            return hv

    return EBCDIC_ASCII_CHART[0]

def find_hex_value_by_ebcdic(value: str):
    for hv in EBCDIC_ASCII_CHART:
        if hv.EBCDIC_value == value:
            return hv

    return EBCDIC_ASCII_CHART[0]

def find_hex_value_by_comp3(value: str):
    for hv in EBCDIC_ASCII_CHART:
        if hv.COMP3_value == value:
            return hv

    return EBCDIC_ASCII_CHART[0]

def parse_accept_statement(accept: str):
    result = accept.replace(ACCEPT_VALUE_FLAG, EMPTY_STRING)
    if result != EMPTY_STRING:
        temp = EMPTY_STRING
        s = result.split(SPACE)
        if s[0] == "DAY":
            tt = datetime.today().timetuple()
            temp = str(tt.tm_year * 1000 + tt.tm_yday)
            if len(s) > 1:
                if s[1] != "YYYYDDD":
                    temp = str(temp)[2:]
            else:
                temp = str(temp)[2:]
        elif s[0] == 'DATE':
            temp = datetime.today().strftime("%Y%m%d")
            if len(s) > 1:
                if s[1] != "YYYYMMDD":
                    temp = str(temp)[2:]
            else:
                temp = str(temp)[2:]

        result = temp
    else:
        result = os.getenv(SYSIN_ENV_VARIABLE)
        if result == None:
            result = EMPTY_STRING

    return result

def get_hex_value(c: str):
    return hex(ord(c))

def tohex(val: int, bytes: int):
    step = 2
    nbits = bytes * 8
    h = hex((val + (1 << nbits)) % (1 << nbits))[2:]
    temp = h.rjust(bytes * 2, ZERO_STRING).upper()
    result = EMPTY_STRING
    for x in range(0, len(temp), step):
        result = result + find_hex_value(temp[x:x+step]).EBCDIC_value

    return result

def fromhex(val: str, sign: bool):
    v = val
    if v.startswith(HEX_DISPLAY_PREFIX):
        v = val[2:]
    return int.from_bytes(bytes.fromhex(v), byteorder=BIG_BYTE_ORDER, signed=sign)

def comp_conversion(var: COBOLVariable, value: str):
    result = EMPTY_STRING
    if var.comp_indicator == COMP_3_INDICATOR:
        if value.startswith(NEGATIVE_SIGN):
            var.sign = NEGATIVE_SIGN
            value = value[1:]
        if len(value) % 2 != 0:
            if var.data_type == NUMERIC_SIGNED_DATA_TYPE:
                if var.sign == NEGATIVE_SIGN:
                    value = value + NEGATIVE_SIGNED_HEX_FLAG
                else:
                    value = value + POSITIVE_SIGNED_HEX_FLAG            
            else:
                value = value + UNSIGNED_HEX_FLAG
        for x in range(0, len(value), 2):
            t = find_hex_value(value[x:x+2]).EBCDIC_value
            result = result + t
    else:
        result = value

    return result

def reverse_comparison_operator(operator: str):
    if operator == GREATER_THAN:
        return LESS_THAN
    elif operator == GREATER_THAN_EQUAL:
        return LESS_THAN_EQUAL
    elif operator == LESS_THAN:
        return GREATER_THAN
    elif operator == LESS_THAN_EQUAL:
        return GREATER_THAN_EQUAL
    
    return operator

def Cleanup():
    dir_name = Path.cwd()
    test = os.listdir(dir_name)

    for item in test:
        if item.endswith(COMM_AREA_EXT):
            os.remove(os.path.join(dir_name, item))

    for item in test:
        if item.endswith(EIB_EXT):
            os.remove(os.path.join(dir_name, item))

    return

def initialize():
    EBCDIC_ASCII_CHART.append(EBCDICASCII('00', '\x00', '\x00'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('01', '\x01', '\x01'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('02', '\x02', '\x02'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('03', '\x03', '\x03'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('04', '\xA6', '\x04'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('05', '\x09', '\x05'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('06', '\xA1', '\x06'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('07', '\x7F', '\x07'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('08', '\xA2', '\x08'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('09', '\xA3', '\x09'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('0A', '\xA4', '\x0A'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('0B', '\x0B', '\x0B'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('0C', '\x0C', '\x0C'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('0D', '\x0D', '\x0D'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('0E', '\x0E', '\x0E'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('0F', '\x0F', '\x0F'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('10', '\x10', '\x10'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('11', '\x11', '\x11'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('12', '\x12', '\x12'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('13', '\x13', '\x13'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('14', '\xAC', '\x14'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('15', '\xA5', '\x15'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('16', '\x08', '\x16'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('17', '\xA7', '\x17'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('18', '\x18', '\x18'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('19', '\x19', '\x19'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('1A', '\xA8', '\x1A'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('1B', '\xA9', '\x1B'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('1C', '\x1C', '\x1C'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('1D', '\x1D', '\x1D'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('1E', '\x1E', '\x1E'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('1F', '\x1F', '\x1F'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('20', '\xC3', ' '))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('21', '\xC4', '\x21'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('22', '\xC1', '"'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('23', '\xC5', '#'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('24', '\xC6', '$'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('25', '\x0A', '%'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('26', '\x17', '&'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('27', '\x1B', "'"))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('28', '\xC7', '('))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('29', '\xC8', ')'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('2A', '\xC9', '*'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('2B', '\xD0', '+'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('2C', '\xD1', ','))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('2D', '\x05', '\x2D'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('2E', '\x06', '.'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('2F', '\x07', '/'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('30', '\xD3', '0'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('31', '\xD4', '1'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('32', '\x16', '2'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('33', '\xD5', '3'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('34', '\xD6', '4'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('35', '\xC2', '5'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('36', '\xD7', '6'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('37', '\x04', '7'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('38', '\xD8', '8'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('39', '\xD9', '9'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('3A', '\xE0', ':'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('3B', '\xE2', ';'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('3C', '\x14', '<'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('3D', '\x15', '='))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('3E', '\x3E', '>'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('3F', '\x1A', '?'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('40', '\x20', '@'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('41', '\xE4', 'A'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('42', '\xE5', 'B'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('43', '\xE6', 'C'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('44', '\xE7', 'D'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('45', '\xE8', 'E'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('46', '\xE9', 'F'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('47', '\xF0', 'G'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('48', '\xF1', 'H'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('49', '\xF2', 'I'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('4A', '\x5B', 'J'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('4B', '\x2E', 'K'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('4C', '\x3C', 'L'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('4D', '\x28', 'M'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('4E', '\x2B', 'N'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('4F', '\x21', 'O'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('50', '\x26', 'P'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('51', '\xF3', 'Q'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('52', '\xF4', 'R'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('53', '\xF5', 'S'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('54', '\xF6', 'T'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('55', '\xF7', 'U'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('56', '\xF8', 'V'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('57', '\xF9', 'W'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('58', '\x90', 'X'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('59', '\x91', 'Y'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('5A', '\x5D', 'Z'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('5B', '\x24', '['))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('5C', '\x2A', '\\'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('5D', '\x29', ']'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('5E', '\x3B', '^'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('5F', '\x5E', '_'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('60', '\x2D', '`'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('61', '\x2F', 'a'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('62', '\x92', 'b'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('63', '\x93', 'c'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('64', '\x94', 'd'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('65', '\x95', 'e'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('66', '\x96', 'f'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('67', '\x97', 'g'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('68', '\x98', 'h'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('69', '\x99', 'i'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('6A', '\x7C', 'j'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('6B', '\x2C', 'k'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('6C', '\x25', 'l'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('6D', '\x5F', 'm'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('6E', '\x3E', 'n'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('6F', '\x3F', 'o'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('70', '\x82', 'p'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('71', '\x83', 'q'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('72', '\x84', 'r'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('73', '\x85', 's'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('74', '\x86', 't'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('75', '\x87', 'u'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('76', '\x88', 'v'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('77', '\x89', 'w'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('78', '\xD2', 'x'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('79', '\x60', 'y'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('7A', '\x3A', 'z'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('7B', '\x23', '{'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('7C', '\x40', '!'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('7D', "\x27", '}'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('7E', '\x3D', '~'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('7F', '\x22', '\x7F'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('80', '\x80', '\x80'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('81', '\x61', '\x5C'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('82', '\x62', '\x82'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('83', '\x63', '\x83'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('84', '\x64', '\x84'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('85', '\x65', '\x85'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('86', '\x66', '\x86'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('87', '\x67', '\x87'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('88', '\x68', '\x88'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('89', '\x69', '\x89'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('8A', '\x8A', '\x8A'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('8B', '\x8B', '\x8B'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('8C', '\x8C', '\x8C'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('8D', '\x8D', '\x8D'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('8E', '\x8E', '\x8E'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('8F', '\x8F', '\x8F'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('90', '\x81', '\x90'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('91', '\x6A', '\x91'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('92', '\x6B', '\x92'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('93', '\x6C', '\x93'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('94', '\x6D', '\x94'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('95', '\x6E', '\x95'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('96', '\x6F', '\x96'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('97', '\x70', '\x97'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('98', '\x71', '\x98'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('99', '\x72', '\x99'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('9A', '\x9A', '\x9A'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('9B', '\x9B', '\x9B'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('9C', '\x9C', '\x9C'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('9D', '\x9D', '\x9D'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('9E', '\x9E', '\x9E'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('9F', '\x9F', '\x9F'))  
    EBCDIC_ASCII_CHART.append(EBCDICASCII('A0', '\xA0', '\xA0'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('A1', '\x7E', '\xA1'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('A2', '\x73', '\xA2'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('A3', '\x74', '\xA3'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('A4', '\x75', '\xA4'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('A5', '\x76', '\xA5'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('A6', '\x77', '\xA6'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('A7', '\x78', '\xA7'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('A8', '\x79', '\xA8'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('A9', '\x7A', '\xA9'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('AA', '\xAA', '\xAA'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('AB', '\xAB', '\xAB'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('AC', '\xBD', '\xAC'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('AD', '\xAD', '\xAD'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('AE', '\xAE', '\xAE'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('AF', '\xAF', '\xAF'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('B0', '\xB0', '\xB0'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('B1', '\xB1', '\xB1'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('B2', '\xB2', '\xB2'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('B3', '\xB3', '\xB3'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('B4', '\xB4', '\xB4'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('B5', '\xB5', '\xB5'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('B6', '\xB6', '\xB6'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('B7', '\xB7', '\xB7'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('B8', '\xB8', '\xB8'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('B9', '\xB9', '\xB9'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('BA', '\xBA', '\xBA'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('BB', '\xBB', '\xBB'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('BC', '\xBC', '\xBC'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('BD', '\xC0', '\xBD'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('BE', '\xBE', '\xBE'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('BF', '\xBF', '\xBF'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('C0', '\x7B', '\xC0'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('C1', '\x41', '\xC1'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('C2', '\x42', '\xC2'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('C3', '\x43', '\xC3'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('C4', '\x44', '\xC4'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('C5', '\x45', '\xC5'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('C6', '\x46', '\xC6'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('C7', '\x47', '\xC7'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('C8', '\x48', '\xC8'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('C9', '\x49', '\xC9'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('CA', '\xCA', '\xCA'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('CB', '\xCB', '\xCB'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('CC', '\xCC', '\xCC'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('CD', '\xCD', '\xCD'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('CE', '\xCE', '\xCE'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('CF', '\xCF', '\xCF'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('D0', '\x7D', '\xD0'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('D1', '\x4A', '\xD1'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('D2', '\x4B', '\xD2'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('D3', '\x4C', '\xD3'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('D4', '\x4D', '\xD4'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('D5', '\x4E', '\xD5'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('d6', '\x4F', '\xD6'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('D7', '\x50', '\xD7'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('D8', '\x51', '\xD8'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('D9', '\x52', '\xD9'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('DA', '\xDA', '\xDA'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('DB', '\xDB', '\xDB'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('DC', '\xDC', '\xDC'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('DD', '\xDD', '\xDD'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('DE', '\xDE', '\xDE'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('DF', '\xDF', '\xDF'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('E0', '\x5C', '\xE0'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('E1', '\xE1', '\xE1'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('E2', '\x53', '\xE2'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('E3', '\x54', '\xE3'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('E4', '\x55', '\xE4'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('E5', '\x56', '\xE5'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('E6', '\x57', '\xE6'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('E7', '\x58', '\xE7'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('E8', '\x59', '\xE8'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('E9', '\x5A', '\xE9'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('EA', '\xEA', '\xEA'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('EB', '\xEB', '\xEB'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('EC', '\xEC', '\xEC'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('ED', '\xED', '\xED'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('EE', '\xEE', '\xEE'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('EF', '\xEF', '\xEF'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('F0', '\x30', '\xF0'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('F1', '\x31', '\xF1'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('F2', '\x32', '\xF2'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('F3', '\x33', '\xF3'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('F4', '\x34', '\xF4'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('F5', '\x35', '\xF5'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('F6', '\x36', '\xF6'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('F7', '\x37', '\xF7'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('F8', '\x38', '\xF8'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('F9', '\x39', '\xF9'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('FA', '\xFA', '\xFA'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('FB', '\xFB', '\xFB'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('FC', '\xFC', '\xFC'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('FD', '\xFD', '\xFD'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('FE', '\xFE', '\xFE'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('FF', '\xFF', '\xFF'))

    return

def print_out():
    print('Decimal,Hex,EBCDIC,ASCII,EBCDIC Char, ASCII Char')
    for eac in EBCDIC_ASCII_CHART:
        print(str(eac.decimal_value).rjust(3,ZERO_STRING) + COMMA + eac.hex_value.upper() + COMMA + HEX_DISPLAY_PREFIX \
            + hex(ord(eac.EBCDIC_value))[2:].rjust(2,ZERO_STRING).upper() + COMMA + HEX_DISPLAY_PREFIX \
            + hex(ord(eac.ASCII_value))[2:].rjust(2,ZERO_STRING).upper() + COMMA + chr(ord(eac.EBCDIC_value)) + COMMA + chr(ord(eac.ASCII_value)))
    return
        
if __name__ == "__main__":
    initialize()
    print_out()