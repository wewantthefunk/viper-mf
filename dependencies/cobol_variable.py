from datetime import datetime
import os, math
from pathlib import Path
from os.path import exists

ACCEPT_VALUE_FLAG = "__ACCEPT "
ADD_COMMAND = "add"
ALPHANUMERIC_DATA_TYPE = "X"
CLOSE_PARENS = ")"
COBOL_FILE_VARIABLE_TYPE = "COBOLFileVariable"
COLON = ":"
COMMA = ","
COMM_AREA_EXT = "comm.txt"
COMP_INDICATOR = "COMP"
COMP_3_INDICATOR = "COMP-3"
COMP_5_INDICATOR = "COMP-5"
DFHCOMMAREA_NAME = "DFHCOMMAREA"
DISP_COMMAND = "display"
DIVISION_OPERATOR = "/"
DOUBLE_EQUALS = "=="
EIB_EXT = "eib.txt"
EMPTY_STRING = ""
GET_COMMAND = "get"
GREATER_THAN = ">"
GREATER_THAN_EQUAL = ">="
HEX_PREFIX = "_hex_"
LEVEL_88 = "88"
LESS_THAN = "<"
LESS_THAN_EQUAL = "<="
LITERAL = "literal"
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
POSITIVE_SIGN = "+"
POSITIVE_SIGNED_HEX_FLAG = "C"
SET_COMMAND = "set"
SPACE = " "
SPACES_INITIALIZER = "____spaces"
SYSIN_ENV_VARIABLE = "SYSIN"
UNSIGNED_HEX_FLAG = "F"
UPD_COMMAND = "update"
ZERO = 0
ZERO_STRING = "0"

BINARY_COMP_LIST = [
    COMP_5_INDICATOR
    , COMP_INDICATOR
]

COMP_DATA_TYPES = [
    COMP_INDICATOR
    , COMP_3_INDICATOR
    , COMP_5_INDICATOR
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
    def __init__(self, hex_val: str, ebcdic_val: str, ascii_val: str) -> None:
        self.hex_value = hex_val
        self.EBCDIC_value = ebcdic_val
        self.ASCII_value = ascii_val
        self.decimal_value = int(hex_val, 16)

class COBOLVariable:
    def __init__(self, name: str, length: int, data_type: str, parent: str, redefines: str, occurs_length: int, decimal_length: int, level: str, comp_indicator: str, pos: int, unpacked_length: int, index: str):
        self.name = name
        self.length = length
        self.data_type = data_type
        self.parent = parent
        if parent != name:
            self.parent = parent
        else:
            self.parent = EMPTY_STRING
        self.value = EMPTY_STRING
        self.level88value = EMPTY_STRING
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
        self.sign = EMPTY_STRING
        self.unpacked_length = unpacked_length
        self.index_variable = index

class COBOLFileVariable:
    def __init__(self, name: str, assign: str, organization: str, access: str, record_key: str, file_status: str):
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

    def open_file(self, main_variable_memory, variables_list, method: str):
        filename = os.getenv(self.assign)
        if filename == None:
            result = Set_Variable(main_variable_memory, variables_list, self.file_status, '35', self.file_status)
            return result[1]
        elif exists(filename) == False:
            result = Set_Variable(main_variable_memory, variables_list, self.file_status, '35', self.file_status)
            return result[1]

        self.file_pointer = open(filename, method)

        result = Set_Variable(main_variable_memory, variables_list, self.file_status, '00', self.file_status)
        return result[1]

    def close_file(self):
        if self.file_pointer != None:
            self.file_pointer.close()

    def read(self):
        line = self.file_pointer.readline().decode().replace(NEWLINE, EMPTY_STRING).replace("\r", EMPTY_STRING)

        at_end = False

        if not line:
            at_end = True
            line = EMPTY_STRING

        return [line, at_end]

    def write(self, data: str):
        if self.file_pointer != None:
            self.file_pointer.write(data)

def Add_Variable(main_variable_memory, list, name: str, length: int, data_type: str, parent: str, redefines = EMPTY_STRING, occurs_length = 0, decimal_len = 0, comp_indicator = EMPTY_STRING, level = "01", index = EMPTY_STRING):
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
    elif comp_indicator == COMP_5_INDICATOR and data_type in NUMERIC_DATA_TYPES:
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

    list.append(COBOLVariable(name, length, data_type, parent, redefines, occurs_length, decimal_len, level, comp_indicator, next_pos, unpacked_length, index))

    update_length = length
    if redefines != EMPTY_STRING:
        update_length = 0
    result = _update_parent_child_length(main_variable_memory, list, parent, update_length)
    skip_add = result[0]
    main_variable_memory = result[1]

    pc = SPACE
    if data_type in NUMERIC_DATA_TYPES:
        pc = ZERO_STRING
    if redefines == EMPTY_STRING and length > 0 and skip_add == False:
        main_variable_memory = main_variable_memory + pad_char(length, pc)
    elif occurs_length > 0:
        for x in range(0, occurs_length):
            main_variable_memory = main_variable_memory + pad_char(length, pc)

    return [list, main_variable_memory]

def _update_parent_child_length(main_variable_memory, list, name: str, length: int):
    skip_add = False
    if name == EMPTY_STRING:
        return skip_add

    for l in list:
        if l.name == name:
            l.child_length = l.child_length + length
            if l.occurs_length > 0:
                pc = SPACE
                if l.data_type in NUMERIC_DATA_TYPES:
                    pc = ZERO_STRING
                main_variable_memory = main_variable_memory + pad_char(l.occurs_length * length, pc)
                skip_add = True
            if l.parent != EMPTY_STRING:
                result = _update_parent_child_length(main_variable_memory, list, l.parent, length)
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

def Read_File(main_variable_memory, var_list, file_rec_var_list, name: str, at_end_clause: str):
    read_result = [False, main_variable_memory]
    for var in var_list:
        if var.name == name:
            read_result = var.read()
            if read_result[1]:
                read_result = [True, main_variable_memory]
                break
            # set the variable from the read
            read_result = _set_variable(main_variable_memory, file_rec_var_list, var.record, read_result[0], [var.record], 0, file_rec_var_list)
            read_result[0] = not read_result[0]
            break

    return read_result

def Write_File(var_list, file_rec_var_list, name: str):
    for var in var_list:
        if var.name == name:
            # write the value from the variable indicated in 'name' parameter
            var.write(EMPTY_STRING)
            break

def Set_File_Record(var_list, name: str, record: str):
    for var in var_list:
        if var.name == name:
            var.record = record
            break

    return var_list

def Exec_Function(func_name: str):
    result = EMPTY_STRING
    if func_name == "CURRENT-DATE":
        result = datetime.today().strftime('%Y%m%d%H%M%S%f')

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

def Set_Variable(main_variable_memory, variable_lists, name: str, value: str, parent: str, index_pos = 0):  
    found = [False, EMPTY_STRING]
    for var_list in variable_lists:
        found = _set_variable(main_variable_memory, var_list, name, value, [parent], index_pos, variable_lists)
        if found[0]:
            break
    return found

def _set_variable(main_variable_memory, var_list, name: str, value: str, parent, index_pos: int, orig_var_list):
    count = 0
    occurrence = 1
    value = str(value)
    var_name = name
    new_value = EMPTY_STRING
    is_hex = False
    raw_value = str(value)
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
            sub_string = [int(s1[0]) - 1, int(s1[1])]
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
                    var.level88value = value
                return [True, main_variable_memory]
            else:
                if var.data_type in NUMERIC_DATA_TYPES:
                    if var.data_type == NUMERIC_SIGNED_DATA_TYPE:
                        if value.startswith(NEGATIVE_SIGN):
                            var.sign = NEGATIVE_SIGN
                            value = value[1:]
                        else:
                            var.sign = POSITIVE_SIGN
                    pad_length = var.unpacked_length
                    if var.comp_indicator == COMP_3_INDICATOR or (var.comp_indicator == COMP_5_INDICATOR and var.data_type == NUMERIC_SIGNED_DATA_TYPE):
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
                length = var.length
                if length == ZERO:
                    length = var.child_length
                var_parent = _find_variable(var_list, var.parent)
                start = var.main_memory_position
                if var_parent != None:
                    pl = var_parent.child_length
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

    return Set_Variable(main_variable_memory, variable_lists, giving, str(curr_val), giving)

def Replace_Variable_Value(main_variable_memory, variable_lists, name: str, orig: str, rep: str):
    result = Get_Variable_Value(main_variable_memory, variable_lists, name, name, False)
    if result != EMPTY_STRING:
        orig_array = list(orig)
        rep_array = list(rep)
        count = 0
        for o in orig_array:
            result = result.replace(o, rep_array[count])
            count = count + 1

        Set_Variable(main_variable_memory, variable_lists, name, result, name)

        return True

    return False

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
    return 0

def Get_Variable_Value(main_variable_memery, variable_lists, name: str, parent: str, force_str = False):
    t = EMPTY_STRING

    for var_list in variable_lists:
        t = _get_variable_value(main_variable_memery, var_list, name, [parent], force_str, variable_lists)
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
    array_lookup = False
    
    if OPEN_PARENS in name:
        array_lookup = True
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

    var = _find_variable(var_list, var_name)

    for x in range(0, len(var_list)):
        if var_list[count].name == var_name or var_list[count].parent in parent:
            var = var_list[count]
            length = var.length
            if length == ZERO:
                length = var.child_length
            var_parent = _find_variable(var_list, var_list[count].parent)
            start = var_list[count].main_memory_position
            if var_parent != None:
                pl = var_parent.child_length
                start = (pl * (occurrence - 1)) + start
            result = main_variable_memory[start:start + length]

            if var.data_type in NUMERIC_DATA_TYPES:
                if var.comp_indicator == COMP_3_INDICATOR:
                    result = convert_from_comp3(result, var)
                elif var.comp_indicator == COMP_5_INDICATOR:
                    result = convert_from_comp(var, result)
                elif var.data_type == NUMERIC_SIGNED_DATA_TYPE:
                    if var.sign == NEGATIVE_SIGN:
                        result = var.sign + result
            elif var.level == LEVEL_88:
                result = result == var.level88value
            count = len(var_list)
            found_count = 1
        else:
            count = count + 1

        if count >= len(var_list):
            break
    
    if var != None:
        if var.data_type in NUMERIC_DATA_TYPES and result != EMPTY_STRING:
            if result.endswith(PERIOD):
                result = result[0:len(result) - 1]
            type_result = int(result)
        else:
            type_result = result
    else:
        type_result = result

    return [type_result, found_count, result, count]

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

    index = indexes[1]

    for var_list in variable_lists:
        var = _find_variable(var_list, index)
        if var != None:
            parent_var = _find_variable(var_list, var.parent)
            if parent_var != None:
                sub_occurrences = parent_var.occurs_length

    occurence = ((major_index - 1) * (sub_occurrences - 1)) + major_index

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
    

def Display_Variable(main_variable_memory, variable_lists, name: str, parent: str, is_literal: bool, is_last: bool):
    dv = name
    if is_literal == False:
        for var_list in variable_lists:
            r = _get_variable_value(main_variable_memory, var_list, name, [parent], False, variable_lists)
            dv = r[2]
            if r[1] > 0:
                break

    print_value(dv)

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

def _write_file(file: str, data: str):
    _write_binary_file(file,bytes(data, 'utf-8'))

def _write_binary_file(file: str, data):
    _write_file_data(file,data,"wb")

def _write_file_data(file: str, data, method: str):
    f = open(file,method)
    f.write(data)
    f.close()

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

def convert_open_method(method: str):
    if method == "INPUT":
        return "rb"
    elif method == "OUTPUT":
        return "ab"
    elif method == "INPUT-OUTPUT":
        return "ab+"

def convert_EBCDIC_hex_to_string(input: str, var: COBOLVariable):
    result = "0x" + input
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
    if v.startswith('0x'):
        v = val[2:]
    return int.from_bytes(bytes.fromhex(v), byteorder='big', signed=sign)

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

def initialize():
    EBCDIC_ASCII_CHART.append(EBCDICASCII('00', '\x00', '\x00'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('01', '\x01', '\x01'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('02', '\x02', '\x02'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('03', '\x03', '\x03'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('04', '\x09', '\x04'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('05', '\x05', '\x05'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('06', '\x06', '\x06'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('07', '\x7F', '\x07'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('08', '\x08', '\x08'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('09', '\x09', '\x09'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('0A', '\x0A', '\x0A'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('0B', '\x0B', '\x0B'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('0C', '\x0C', '\x0C'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('0D', '\x0D', '\x0D'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('0E', '\x0E', '\x0E'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('0F', '\x0F', '\x0F'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('10', '\x10', '\x10'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('11', '\x11', '\x11'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('12', '\x12', '\x12'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('13', '\x13', '\x13'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('14', '\x14', '\x14'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('15', '\x15', '\x15'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('16', '\x08', '\x16'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('17', '\x17', '\x17'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('18', '\x18', '\x18'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('19', '\x19', '\x19'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('1A', '\x1A', '\x1A'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('1B', '\x1B', '\x1B'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('1C', '\x1C', '\x1C'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('1D', '\x1D', '\x1D'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('1E', '\x1E', '\x1E'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('1F', '\x1F', '\x1F'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('20', '\x20', '\x20'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('21', '\x21', '\x21'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('22', '\x22', '\x22'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('23', '\x23', '\x23'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('24', '\x24', '\x24'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('25', '\x0A', '\x25'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('26', '\x17', '&'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('27', '\x27', '\x27'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('28', '\x28', '\x28'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('29', '\x29', '\x29'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('2A', '\x5C', '\x2A'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('2B', '\x2B', '\x2B'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('2C', '\x2C', '\x2C'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('2D', '\x05', '\x2D'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('2E', '\x06', '\x2E'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('2F', '\x07', '\x2F'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('30', '\x00', '0'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('31', '\x31', '1'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('32', '\x16', '2'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('33', '\x33', '3'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('34', '☺', '4'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('35', '\x1E', '5'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('36', '\x36', '6'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('37', '\x04', '7'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('38', '\x38', '8'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('39', '\x39', '9'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('3A', '\x3A', ':'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('3B', '\x3B', ';'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('3C', '\x14', '<'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('3D', '\x15', '='))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('3E', '\x3E', '>'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('3F', '\x1A', '?'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('40', ' ', '@'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('41', '\x41', 'A'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('42', '\x42', 'B'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('43', '\x43', 'C'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('44', '\x44', 'D'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('45', '\x45', 'E'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('46', '\x46', 'F'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('47', '\x47', 'G'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('48', '\x48', 'H'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('49', '\x49', 'I'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('4A', '╜', 'J'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('4B', '\x4B', 'K'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('4C', '<', 'L'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('4D', '(', 'M'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('4E', '+', 'N'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('4F', '|', 'O'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('50', '&', 'P'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('51', '\xD8', 'Q'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('52', '\xD9', 'R'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('53', '\xE2', 'S'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('54', '\xE3', 'T'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('55', '\xE4', 'U'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('56', '\xE5', 'V'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('57', '\xE6', 'W'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('58', '\xE7', 'X'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('59', '\xE8', 'Y'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('5A', '!', 'Z'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('5B', '$', '['))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('5C', '*', '\x5C'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('5D', ')', ']'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('5E', ';', '\x5E'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('5F', '\x5F', '_'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('60', '-', '\x60'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('61', '/', 'a'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('62', '\x82', 'b'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('63', '\x83', 'c'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('64', '\x84', 'd'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('65', '\x85', 'e'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('66', '\x86', 'f'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('67', '\x87', 'g'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('68', '\x88', 'h'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('69', '\x89', 'i'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('6A', '!', 'j'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('6B', '.', 'k'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('6C', '%', 'l'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('6D', '_', 'm'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('6E', '>', '\x5E'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('6F', '?', 'o'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('70', '\x70', 'p'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('71', '\x71', 'q'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('72', '\x72', 'r'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('73', '\x73', 's'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('74', '\x74', 't'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('75', '\x75', 'u'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('76', '\x76', 'v'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('77', '\x77', 'w'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('78', '\x78', 'x'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('79', '\x79', 'y'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('7A', ':', 'z'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('7B', '#', '{'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('7C', '@', '!'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('7D', "'", '}'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('7E', '=', '~'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('7F', '"', '\x7F'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('80', '\x80', '\x80'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('81', 'a', '\x81'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('82', 'b', '\x82'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('83', 'c', '\x83'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('84', 'd', '\x84'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('85', 'e', '\x85'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('86', 'f', '\x86'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('87', 'g', '\x87'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('88', 'h', '\x88'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('89', 'i', '\x89'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('8A', '\x8A', '\x8A'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('8B', '\x8B', '\x8B'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('8C', '\x8C', '\x8C'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('8D', '\x8D', '\x8D'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('8E', '\x8E', '\x8E'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('8F', '\x8F', '\x8F'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('90', '\x90', '\x90'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('91', 'j', '\x91'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('92', 'k', '\x92'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('93', 'l', '\x93'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('94', 'm', '\x94'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('95', 'n', '\x95'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('96', 'o', '\x96'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('97', 'p', '\x97'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('98', 'q', '\x98'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('99', 'r', '\x99'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('9A', '\x9A', '\x9A'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('9B', '\x9B', '\x9B'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('9C', '\x9C', '\x9C'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('9D', '\x9D', '\x9D'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('9E', '\x9E', '\x9E'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('9F', '\x9F', '\x9F'))  
    EBCDIC_ASCII_CHART.append(EBCDICASCII('A0', '\xA0', '\xA0'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('A1', '\xA1', '\xA1'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('A2', 's', '\xA2'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('A3', 't', '\xA3'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('A4', 'u', '\xA4'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('A5', 'v', '\xA5'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('A6', 'w', '\xA6'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('A7', 'x', '\xA7'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('A8', 'y', '\xA8'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('A9', 'z', '\xA9'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('AA', '\xAA', '\xAA'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('AB', '\xAB', '\xAB'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('AC', '\xAC', '\xAC'))
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
    EBCDIC_ASCII_CHART.append(EBCDICASCII('BD', '\xBD', '\xBD'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('BE', '\xBE', '\xBE'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('BF', '\xBF', '\xBF'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('C0', '{', '\xC0'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('C1', 'A', '\xC1'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('C2', 'B', '\xC2'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('C3', 'C', '\xC3'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('C4', 'D', '\xC4'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('C5', 'E', '\xC5'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('C6', 'F', '\xC6'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('C7', 'G', '\xC7'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('C8', 'H', '\xC8'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('C9', 'I', '\xC9'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('CA', '\xCA', '\xCA'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('CB', '\xCB', '\xCB'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('CC', '\xCC', '\xCC'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('CD', '\xCD', '\xCD'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('CE', '\xCE', '\xCE'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('CF', '\xCF', '\xCF'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('D0', '}', '\xD0'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('D1', 'J', '\xD1'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('D2', 'K', '\xD2'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('D3', 'L', '\xD3'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('D4', 'M', '\xD4'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('D5', 'N', '\xD5'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('d6', 'O', '\xD6'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('D7', 'P', '\xD7'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('D8', 'Q', '\xD8'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('D9', 'R', '\xD9'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('DA', '\xDA', '\xDA'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('DB', '\xDB', '\xDB'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('DC', '\xDC', '\xDC'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('DD', '\xDD', '\xDD'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('DE', '\xDE', '\xDE'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('DF', '\xDF', '\xDF'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('E0', '\xE0', '\xE0'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('E1', 'X\E1', '\xE1'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('E2', 'S', '\xE2'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('E3', 'T', '\xE3'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('E4', 'U', '\xE4'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('E5', 'V', '\xE5'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('E6', 'W', '\xE6'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('E7', 'X', '\xE7'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('E8', 'Y', '\xE8'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('E9', 'Z', '\xE9'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('EA', '\xEA', '\xEA'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('EB', '\xEB', '\xEB'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('EC', '\xEC', '\xEC'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('ED', '\xED', '\xED'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('EE', '\xEE', '\xEE'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('EF', '\xEF', '\xEF'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('F0', '0', '\xF0'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('F1', '1', '\xF1'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('F2', '2', '\xF2'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('F3', '3', '\xF3'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('F4', '4', '\xF4'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('F5', '5', '\xF5'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('F6', '6', '\xF6'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('F7', '7', '\xF7'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('F8', '8', '\xF8'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('F9', '9', '\xF9'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('FA', '\xFA', '\xFA'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('FB', '\xFB', '\xFB'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('FC', '\xFC', '\xFC'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('FD', '\xFD', '\xFD'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('FE', '\xFE', '\xFE'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('FF', '\xFF', '\xFF'))