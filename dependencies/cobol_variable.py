from datetime import datetime
import os, binascii
from os.path import exists

ACCEPT_VALUE_FLAG = "__ACCEPT "
ADD_COMMAND = "add"
CLOSE_PARENS = ")"
COBOL_FILE_VARIABLE_TYPE = "COBOLFileVariable"
COLON = ":"
DISP_COMMAND = "display"
DOUBLE_EQUALS = "=="
EMPTY_STRING = ""
GET_COMMAND = "get"
HEX_PREFIX = "_hex_"
LEVEL_88 = "88"
LITERAL = "literal"
NEWLINE = "\n"
NOT_EQUALS = "!="
NUMERIC_DATA_TYPE = "9"
NUMERIC_SIGNED_DATA_TYPE = "S9"
OPEN_PARENS = "("
SET_COMMAND = "set"
SPACE = " "
SPACES_INITIALIZER = "____spaces"
SYSIN_ENV_VARIABLE = "SYSIN"
UPD_COMMAND = "update"
ZERO = "0"

last_command = ""

EBCDIC_ASCII_CHART = [

]

class EBCDICASCII:
    def __init__(self, hex_val: str, ebcdic_val: str, ascii_val: str) -> None:
        self.hex_value = hex_val
        self.EBCDIC_value = ebcdic_val
        self.ASCII_value = ascii_val

class COBOLVariable:
    def __init__(self, name: str, length: int, data_type: str, parent: str, redefines: str, occurs_length: int, decimal_length, level: str, comp_indicator):
        self.name = name
        self.length = length
        self.data_type = data_type
        if parent != name and (redefines == EMPTY_STRING or length > 0):
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

    def open_file(self, variables_list, method: str):
        filename = os.getenv(self.assign)
        if filename == None:
            Set_Variable(variables_list, self.file_status, '35', self.file_status)
            return
        elif exists(filename) == False:
            Set_Variable(variables_list, self.file_status, '35', self.file_status)
            return

        self.file_pointer = open(filename, method)

        Set_Variable(variables_list, self.file_status, '00', self.file_status)
        return

    def close_file(self):
        if self.file_pointer != None:
            self.file_pointer.close()

    def read(self):
        line = self.file_pointer.readline().replace(NEWLINE, EMPTY_STRING)

        at_end = False

        if not line:
            at_end = True
            line = EMPTY_STRING

        return [line, at_end]

    def write(self, data: str):
        if self.file_pointer != None:
            self.file_pointer.write(data)

def Open_File(variables_list, var_list, name: str, method: str):
    for var in var_list:
        if var.name == name:
            var.open_file(variables_list, convert_open_method(method))
            break

def Close_File(var_list, name: str):
    for var in var_list:
        if var.name == name:
            var.close_file()
            break

def Read_File(var_list, file_rec_var_list, name: str, at_end_clause: str):
    read_result = [EMPTY_STRING, False]
    for var in var_list:
        if var.name == name:
            read_result = var.read()
            if read_result[1]:
                break
            search_variable_list(file_rec_var_list, var.record, read_result[0], [var.record], [], 0, file_rec_var_list)
            break

    return read_result[1]

def Write_File(var_list, file_rec_var_list, name: str):
    for var in var_list:
        if var.name == name:
            var.write(find_get_variable(file_rec_var_list, var.record, [var.record])[0])
            break

def Set_File_Record(var_list, name: str, record: str):
    for var in var_list:
        if var.name == name:
            var.record = record
            break

def Exec_Function(func_name: str):
    result = EMPTY_STRING
    if func_name == "CURRENT-DATE":
        result = datetime.today().strftime('%Y%m%d%H%M%S%f')

    return result

def Add_File_Variable(list, name: str, assign: str, organization: str, access: str, record_key: str, file_status: str):
    global last_command
    check_for_last_command(ADD_COMMAND)
    last_command = ADD_COMMAND
    for l in list:
        if l.name == name:
            return list

    list.append(COBOLFileVariable(name, assign, organization, access, record_key, file_status))

    return list


def Add_Variable(list, name: str, length: int, data_type: str, parent: str, redefines = EMPTY_STRING, occurs_length = 0, decimal_len = 0, comp_indicator = EMPTY_STRING, level = "01"):
    global last_command
    check_for_last_command(ADD_COMMAND)
    last_command = ADD_COMMAND
    for l in list:
        if l.name == name:
            return list

    if data_type == NUMERIC_SIGNED_DATA_TYPE:
        length = length + 1

    list.append(COBOLVariable(name, length, data_type, parent, redefines, occurs_length, decimal_len, level, comp_indicator))

    return list

def Search_Variable_Array(variable_lists, operand1: str, operator: str, operand2, is_all_array, not_found_func):
    found = False
    if OPEN_PARENS not in operand1:
        t = operand1
        operand1 = operand2
        operand2 = t

    operand1_split = operand1.split(OPEN_PARENS)

    start_at = 0

    if is_all_array <= 0:
        start_at = Get_Variable_Value(variable_lists, operand1_split[1].replace(CLOSE_PARENS, EMPTY_STRING), operand1_split[1].replace(CLOSE_PARENS, EMPTY_STRING)) - 1
        if start_at < 0:
            start_at = 0

    parent_var = None
    for var_list in variable_lists:
        array_var = find_variable(var_list, operand1_split[0], [operand1_split[0]])
        if array_var != None:
            parent_var = find_variable_parent(var_list, array_var.parent)
            break

    search_var = array_var
    if parent_var.occurs_length > 0 and (len(parent_var.occurs_indexes) > 0 or parent_var.redefines != EMPTY_STRING):
        search_var = parent_var

    for x in range(start_at, len(search_var.occurs_indexes)):
        array_index = search_var.occurs_indexes[x] - 1
        val1 = search_var.occurs_values[array_index]

        found = False

        if operator == DOUBLE_EQUALS:
            found = val1 == operand2
        elif operator == NOT_EQUALS:
            found = val1 != operand2
            
        if found:
            break

    if len(search_var.occurs_indexes) == 0:
        val = Get_Variable_Value(variable_lists, search_var.name, search_var.name)
        l = Get_Variable_Length(variable_lists, search_var.name)
        for x in range(start_at, search_var.occurs_length):
            r = val[x * l: (x * l) + (l)]
            if r[0:len(operand2)] == operand2:
                # add 1 to the found index to process the transformation of base 1 array to base 0 array properly
                Set_Variable(variable_lists, operand1_split[1].replace(CLOSE_PARENS, EMPTY_STRING), str(x + 1), operand1_split[1].replace(CLOSE_PARENS, EMPTY_STRING))
                found = True
                break

    if found == False and not_found_func != None:
        not_found_func()

    return found


def Set_Variable(variable_lists, name: str, value: str, parent: str, index_pos = 0):  
    global last_command
    check_for_last_command(SET_COMMAND)
    last_command = SET_COMMAND  
    sub_index = []
    if OPEN_PARENS in name:
        s = name.split(OPEN_PARENS)
        if COLON in s[1]:
            s1 = s[1].split(COLON)
            start = int(s1[0]) - 2
            if start < 0:
                start = 0
            sub_index = [start, int(s1[1].replace(OPEN_PARENS, EMPTY_STRING).replace(CLOSE_PARENS, EMPTY_STRING)) + int(s1[0]) - 1]
        else:
            if s[1].replace(CLOSE_PARENS, EMPTY_STRING).isnumeric():
                sub_index = [int(s[1].replace(CLOSE_PARENS, EMPTY_STRING)) - 1]
            else:
                val = Get_Variable_Value(variable_lists, s[1].replace(CLOSE_PARENS, EMPTY_STRING), s[1].replace(CLOSE_PARENS, EMPTY_STRING))
                sub_index = [val - 1]
        name = s[0]
    if OPEN_PARENS in parent:
        ps = parent.split(OPEN_PARENS)
        parent = ps[0]

    if str(value).startswith(ACCEPT_VALUE_FLAG):
        value = parse_accept_statement(value)

    for var_list in variable_lists:
        result = search_variable_list(var_list, name, value, [parent], sub_index, index_pos, var_list)
        if result:
            break

def search_variable_list(var_list, name: str, value: str, parent, sub_index: str, index_pos: str, orig_var_list):
    count = 0
    found = False
    for var in var_list:
        if COBOL_FILE_VARIABLE_TYPE in str(type(var_list[0])):
            continue
        if var.name == name or var.parent in parent:
            name = var.name
            found = True
            count = var_list.index(var) + 1
            hex_prefix = EMPTY_STRING
            if var.length == 0 and var.level != LEVEL_88:
                if (var.name not in parent):
                    parent.append(var.name)
                found = search_variable_list(var_list[count:], EMPTY_STRING, value, parent, sub_index, index_pos, orig_var_list)
            else:
                is_spaces = False
                if value == SPACES_INITIALIZER:
                    is_spaces = True
                    if var.data_type == NUMERIC_DATA_TYPE:
                        value = pad_char(var.length, ZERO)
                    else:
                        value = pad(var.length)
                if var.data_type == NUMERIC_DATA_TYPE:
                    if str(value).replace("+", EMPTY_STRING).replace("-", EMPTY_STRING).isdigit() == False:
                        value = 0
                offset = var.length
                if len(sub_index) > 0:
                    if str(sub_index[0]).isnumeric() == False:
                        offset = 0

                    elif var.length >= sub_index[0] or len(sub_index) == 1:
                        if str(value).startswith(HEX_PREFIX):
                            value = value.replace(HEX_PREFIX, EMPTY_STRING)
                            var.is_hex = True
                            hex_prefix = HEX_PREFIX
                        t_value = value

                        if len(sub_index) == 2:
                            var.value[:sub_index[0]] + str(value) + var.value[sub_index[1]:]
                            
                        _update_var_value(orig_var_list, var, t_value, sub_index)
                    else:
                        offset = 0
                elif var.level == LEVEL_88:
                    if str(value).startswith(HEX_PREFIX):
                        value = value.replace(HEX_PREFIX, EMPTY_STRING)
                        value = convert_EBCDIC_hex_to_string(value)
                        var.is_hex = True
                        hex_prefix = HEX_PREFIX
                    _update_var_value(orig_var_list, var, str(value), [])
                else:
                    hex_pad = 0
                    if str(value).startswith(HEX_PREFIX) or var.comp_indicator != EMPTY_STRING:
                        var.is_hex = True
                        hex_prefix = HEX_PREFIX
                        hex_pad = 2
                        value = str(value).replace(HEX_PREFIX, EMPTY_STRING)
                        
                        neg_indicator = "C"
                        if value.startswith("-"):
                            neg_indicator = "D"
                            value = value[1:]
                        orig_value = value
                        value = convert_EBCDIC_hex_to_string(value, var)
                        if var.comp_indicator != EMPTY_STRING:
                            if len(orig_value) % 2 == 0:
                                value = value.replace("0x", "0x0") + neg_indicator
                            else:
                                value = value + neg_indicator

                    _update_var_value(orig_var_list, var, str(value)[0:var.length + hex_pad], [])

                if (len(str(value)) > var.length and (name not in parent or name == EMPTY_STRING) and var.parent != EMPTY_STRING) or is_spaces:
                    if var.parent not in parent:
                        parent.append(var.parent)
                    if is_spaces:
                        value = SPACES_INITIALIZER
                        offset = 0
                    found = search_variable_list(var_list[count:], EMPTY_STRING, hex_prefix + value[offset:], parent, sub_index, index_pos, orig_var_list)

            break

    return found

def _update_var_value(var_list, var: COBOLVariable, value: str, sub_index: int):
    hex_pad = 0
    if var.is_hex:
        hex_pad = 2
    parent = find_variable_parent(var_list, var.parent)
    occurs_length = 0
    if parent != None:
        if parent.occurs_length > 0 and len(sub_index) > 0:
            if sub_index[0] > parent.occurs_length:
                return
            occurs_length = parent.occurs_length

    redefined_by = find_variable_redefined_by(var_list, var.parent)
    for rdb in redefined_by:
        if rdb.occurs_length > 0 and len(sub_index) > 0:
            if sub_index[0] < rdb.occurs_length:
                rdb.occurs_indexes.append(sub_index[0])
                rdb.occurs_values.append(value)
    
    if len(sub_index) == 2:
        var.value = var.value[:sub_index[0]] + str(value) + var.value[sub_index[1]:]
    elif len(sub_index) == 1 and occurs_length > 0:
        if sub_index[0] in var.occurs_indexes:
            var.occurs_values[sub_index[0]] = value
        else:
            var.occurs_indexes.append(sub_index[0])
            var.occurs_values.append(value)
    elif var.level == LEVEL_88:
        if value == "True":
            parent = find_variable_parent(var_list, var.parent)
            search_variable_list(var_list, parent.name, var.level88value, [parent.name], EMPTY_STRING, EMPTY_STRING, [])
        else:
            var.level88value = value
    else:
        var.value = str(value)[0:var.length + hex_pad]

def Update_Variable(variable_lists, value: str, name: str, parent: str, modifier = '', remainder_var = ''):
    global last_command
    check_for_last_command(UPD_COMMAND)
    last_command = UPD_COMMAND
    orig = None 
    target = None  
    for var_list in variable_lists:
        orig = find_variable(var_list, name, [parent])
        target = find_variable(var_list, parent, [parent])
        
        if orig != None and target != None:
            v = str(value)   
            val = orig.value.ljust(orig.length, ZERO)[:orig.length]       
        elif orig == None:
            #val = name
            continue
        if modifier != EMPTY_STRING:
            if modifier.lstrip('-+').isdigit():
                value = str(int(value) * int(modifier))

            if modifier == "*":
                v = str(int(value) * int(val))[0:target.length]
            elif modifier == "/":
                remainder = int(value) % int(val)
                if remainder_var != EMPTY_STRING:
                    Set_Variable(variable_lists, str(remainder_var), str(remainder), remainder_var, 0) 
                v = str(int(int(value) / int(val)))[0:target.length]
            else:
                v = str(int(value) + int(val))[0:target.length]
        else:
            v = str(int(value) + int(val))[0:target.length]
        target.value = v


def Replace_Variable_Value(variable_lists, name: str, orig: str, rep: str):
    global last_command
    check_for_last_command(GET_COMMAND)
    last_command = GET_COMMAND
    for var_list in variable_lists:
        var = find_variable(var_list, name, [])
        if var == None:
            continue
        orig_array = list(orig)
        rep_array = list(rep)

        result = var.value

        count = 0
        for o in orig_array:
            result = result.replace(o, rep_array[count])
            count = count + 1

        var.value = result

def Get_Variable_Length(variable_lists, name: str):
    global last_command
    check_for_last_command(GET_COMMAND)
    last_command = GET_COMMAND
    t = 0
    for var_list in variable_lists:
        result = find_get_variable_length(var_list, name, [name])
        t = t + result

    return t

def find_get_variable_length(var_list, name: str, parent):
    result = 0
    for var in var_list:
        if COBOL_FILE_VARIABLE_TYPE in str(type(var_list[0])):
            continue
        if var.name == name or var.parent in parent:
            if var.length == 0:
                if (var.name not in parent):
                    parent.append(var.name)
            else:
                result = result + var.length

    return result

def Get_Variable_Position(variable_lists, name: str):
    global last_command
    check_for_last_command(GET_COMMAND)
    last_command = GET_COMMAND
    pos = 0
    length = 0
    for var_list in variable_lists:
        result = find_get_variable_position(var_list, name, [name])
        pos = pos + result[0]
        length = result[1]

    return [pos, length]

def find_get_variable_position(var_list, name: str, parent):
    result = 0
    length = 0
    count = 0
    for var in var_list:
        if COBOL_FILE_VARIABLE_TYPE in str(type(var_list[0])):
            continue
        if var.parent == EMPTY_STRING:
            result = 0
            length = var.length
            if var.level == LEVEL_88:
                length = len(var.level88value)
            if var.name == name:
                break
        
        elif var.name == name:
            return [result, var.length]
        else:
            result = result + var.length
        
        count = count + 1

    return [result, length]

def Get_Variable_Value(variable_lists, name: str, parent: str, force_str = False):
    global last_command
    check_for_last_command(GET_COMMAND)
    last_command = GET_COMMAND
    t = EMPTY_STRING
    is_numeric_data_type = False

    sub_index = []
    if OPEN_PARENS in name:
        s1 = name.split(OPEN_PARENS)
        name = s1[0]
        if COLON in s1[1]:
            subs = s1[1].split(COLON)
            sub_index = [int(subs[0]), int(subs[1].replace(CLOSE_PARENS, EMPTY_STRING))]
        else:
            if s1[1].replace(CLOSE_PARENS, EMPTY_STRING).isnumeric():
                sub_index = [int(s1[1].replace(CLOSE_PARENS, EMPTY_STRING)) - 1]
            else:
                val = Get_Variable_Value(variable_lists, s1[1].replace(CLOSE_PARENS, EMPTY_STRING), s1[1].replace(CLOSE_PARENS, EMPTY_STRING))
                sub_index = [int(val) - 1]

    if OPEN_PARENS in parent:
        s1 = parent.split(OPEN_PARENS)
        parent = s1[0]

    for var_list in variable_lists:
        result = find_get_variable(var_list, name, parent, var_list, sub_index)
        if type(result[0]) == type(True):
            t = result[0]
            break
        else:
            t = t + result[0]
        if result[1] == True:
            is_numeric_data_type = result[1]

    if is_numeric_data_type and force_str == False and t.isnumeric():
        if t == EMPTY_STRING:
            t = "0"
        return int(t)

    return t

def find_get_variable(var_list, name: str, parent: str, orig_var_list, sub_index):
    result = EMPTY_STRING
    is_numeric_data_type = False
    count = 0
    found_count = 0
    while count < len(var_list):
        if COBOL_FILE_VARIABLE_TYPE in str(type(var_list[0])):
            count = count + 1
            continue
        if var_list[count].name == name or var_list[count].parent == parent:
            if var_list[count].length == 0 and var_list[count].level != LEVEL_88:
                r = find_get_variable(var_list[count:], EMPTY_STRING, var_list[count].name, orig_var_list, sub_index)
                found_count = found_count + r[2]
                result = result + r[0]
                is_numeric_data_type = r[1]
                if var_list[count].name == parent:
                    # drop out now, or else we will get the same data twice
                    break                
            else:     
                if var_list[count].redefines != EMPTY_STRING and var_list[count].redefines != parent:
                    pos_length = find_get_variable_position(var_list, var_list[count].name, var_list[count].name)
                    r1 = find_get_variable(orig_var_list, var_list[count].redefines, var_list[count].redefines, orig_var_list, [])[0]
                    if len(sub_index) > 0:
                        result = result + r1[(pos_length[0] + pos_length[1]) * sub_index[0] + pos_length[0]: (pos_length[0] + pos_length[1]) * sub_index[0] + pos_length[1]]
                        found_count = found_count + 1
                    else:
                        if var_list[count].level == LEVEL_88:
                            result = str(var_list[count].level88value) == r1[pos_length[0]: pos_length[0] + pos_length[1]]
                        else:
                            result = result + r1[pos_length[0]: pos_length[0] + pos_length[1]]
                        found_count = found_count + 1
                    break
                elif var_list[count].level == LEVEL_88 and var_list[count].name == name:
                    found_count = found_count + 1
                    if var_list[count].data_type == NUMERIC_DATA_TYPE:
                        is_numeric_data_type = True
                    r = find_get_variable(orig_var_list, var_list[count].parent, '----------', orig_var_list, sub_index)
                    if r[1]:
                        result = int(r[0]) == int(var_list[count].level88value)
                    else:
                        result = r[0] == str(var_list[count].level88value)
                elif var_list[count].data_type == NUMERIC_DATA_TYPE or var_list[count].data_type == NUMERIC_SIGNED_DATA_TYPE:
                    hex_pad = 0
                    if var_list[count].is_hex:
                        hex_pad = 2
                    r = str(var_list[count].value)[:var_list[count].length + hex_pad]
                    neg_sign = EMPTY_STRING
                    if r.startswith("-"):
                        neg_sign = "-"
                        r = r[1:]
                    if var_list[count].is_hex:
                        result = result + r[2:]
                    else:
                        result = result + neg_sign + pad_char(var_list[count].length - len(var_list[count].value), ZERO) + r
                    found_count = found_count + 1
                    is_numeric_data_type = True
                else:
                    if len(sub_index) == 1:
                        if sub_index[0] in var_list[count].occurs_indexes:
                            index = var_list[count].occurs_indexes.index(sub_index[0])
                            if (index >= 0):
                                result = result + var_list[count].occurs_values[index].ljust(var_list[count].length)[:var_list[count].length]
                                found_count = found_count + 1
                            else:
                                result = result + EMPTY_STRING.ljust(var_list[count].length)[:var_list[count].length]
                                found_count = found_count + 1
                        else:
                            result = result + EMPTY_STRING.ljust(var_list[count].length)[:var_list[count].length]
                    else:
                        result = result + var_list[count].value.ljust(var_list[count].length)[:var_list[count].length]
        elif var_list[count].name == parent and var_list[count].redefines != EMPTY_STRING:
            result = find_get_variable(orig_var_list, var_list[count].redefines, var_list[count].redefines, orig_var_list, sub_index)[0]
            found_count = found_count + 1
            break

        if var_list[count].name == name:
            break

        if found_count > 0:
            count = count + found_count
            found_count = 0
        else:
            count = count + 1
        if count > len(var_list):
            break

    return [result, is_numeric_data_type, found_count]

def find_variable(var_list, name: str, parent):
    count = 0
    for var in var_list:
        if COBOL_FILE_VARIABLE_TYPE in str(type(var_list[0])):
            continue
        if var.name == name or var.parent in parent:
            count = count + 1
            return check_var(var_list, count, var, parent)
        else:
            continue
            
    return None

def check_var(var_list, count: int, var: COBOLVariable, parent):
    if var.length == 0:
        if (var.name not in parent):
            parent.append(var.name)
            return find_variable(var_list[count:], EMPTY_STRING, parent)
        else:
            return var
    else:
        return var

def find_variable_parent(var_list, parent: str):
    result = None
    if parent != EMPTY_STRING:
        for var in var_list:
            if COBOL_FILE_VARIABLE_TYPE in str(type(var_list[0])):
                continue
            if var.name == parent:
                if var.parent != EMPTY_STRING and var.length == 0:
                    result = find_variable_parent(var_list, var.parent)
                else:
                    result = var
                    break
    
    return result

def find_variable_redefined_by(var_list, name: str):
    result = []
    if name != EMPTY_STRING:
        for var in var_list:
            if COBOL_FILE_VARIABLE_TYPE in str(type(var_list[0])):
                continue
            if var.redefines == name:
                result.append(var)

    return result

def Display_Variable(variable_lists, name: str, parent: str, is_literal: bool, is_last: bool):
    global last_command
    check_for_last_command(DISP_COMMAND)
    last_command = DISP_COMMAND

    sub_index = []
    if OPEN_PARENS in name:
        s1 = name.split(OPEN_PARENS)
        name = s1[0]
        if COLON in s1[1]:
            subs = s1[1].split(COLON)
            sub_index = [int(subs[0]), int(subs[1].replace(CLOSE_PARENS, EMPTY_STRING))]
        else:
            if s1[1].replace(CLOSE_PARENS, EMPTY_STRING).isnumeric():
                sub_index = [int(s1[1].replace(CLOSE_PARENS, EMPTY_STRING)) - 1]
            else:
                val = Get_Variable_Value(variable_lists, s1[1].replace(CLOSE_PARENS, EMPTY_STRING), s1[1].replace(CLOSE_PARENS, EMPTY_STRING))
                sub_index = [int(val) - 1]

    if OPEN_PARENS in parent:
        s1 = parent.split(OPEN_PARENS)
        parent = s1[0]

    if (parent == LITERAL):
        print(name, end =EMPTY_STRING)
        if is_last:
            print(EMPTY_STRING)
    else:
        for var_list in variable_lists:
            found_count = search_display_variable_list(var_list, name, parent, 0, var_list, sub_index)
            if found_count > 0:
                break

def search_display_variable_list(var_list, name: str, parent: str, level: int, orig_var_list, sub_index):
    found_count = 0
    level = level + 1
    result = find_get_variable(var_list, name, parent, orig_var_list, sub_index)
    if result[0] != EMPTY_STRING:
        print(result[0], end=EMPTY_STRING)
        found_count = found_count + 1

    return found_count

def Check_Value_Numeric(value):
    return str(value).isnumeric()

def Get_Spaces(length: int):
    return pad(length)

def check_for_last_command(cmd: str):
    global last_command

    if cmd == DISP_COMMAND:
        return

    if last_command == DISP_COMMAND:
        pass

def pad(l: int):
    return pad_char(l, SPACE)

def pad_char(l: int, ch: str):
    result = ""
    for x in range(l):
        result = result + ch

    return result

def convert_open_method(method: str):
    if method == "INPUT":
        return "r"
    elif method == "OUTPUT":
        return "a"
    elif method == "INPUT-OUTPUT":
        return "a+"

def convert_EBCDIC_hex_to_string(input: str, var: COBOLVariable):
    #result = EMPTY_STRING
    #for x in range(0, len(input), 2):
    #    result = result + chr(int(input[x: x + 2], 16))
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

def parse_accept_statement(accept: str):
    result = accept.replace(ACCEPT_VALUE_FLAG, EMPTY_STRING)
    if result != EMPTY_STRING:
        temp = EMPTY_STRING
        s = result.split(SPACE)
        if s[0] == "DAY":
            tt = datetime.today().timetuple()
            temp = tt.tm_year * 1000 + tt.tm_yday
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

    return result

def get_hex_value(c: str):
    return hex(ord(c))

def initialize():
    EBCDIC_ASCII_CHART.append(EBCDICASCII('00', '\x00', '\x00'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('01', '\x01', '\x01'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('02', '\x02', '\x02'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('03', '\x03', '\x03'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('04', '\x04', '\x04'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('05', '\x05', '\x05'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('06', '\x06', '\x06'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('07', '\x07', '\x07'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('08', '\x08', '\x08'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('09', '\x09', '\x09'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('10', '\x10', '\x10'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('11', '\x11', '\x11'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('12', '\x12', '\x12'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('13', '\x13', '\x13'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('14', '\x14', '\x14'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('15', '\x15', '\x15'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('16', '\x16', '\x16'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('17', '\x17', '\x17'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('18', '\x18', '\x18'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('19', '\x19', '\x19'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('20', '\x20', '\x20'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('21', '\x21', '\x21'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('22', '\x22', '\x22'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('23', '\x23', '\x23'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('24', '\x24', '\x24'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('25', '\x25', '\x25'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('26', '\x26', '\x26'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('27', '\x27', '\x27'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('28', '\x28', '\x28'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('29', '\x29', '\x29'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('30', '\x30', '\x30'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('31', '\x31', '\x31'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('32', '\x32', '\x32'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('33', '\x33', '\x33'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('34', '\x34', '\x34'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('35', '\x35', '\x35'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('36', '\x36', '\x36'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('37', '\x37', '\x37'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('38', '\x38', '\x38'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('39', '\x39', '\x39'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('40', ' ', '\x40'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('41', '\x41', '\x41'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('42', '\x42', '\x42'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('43', '\x43', '\x43'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('44', '\x44', '\x44'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('45', '\x45', '\x45'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('46', '\x46', '\x46'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('47', '\x47', '\x47'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('48', '\x48', '\x48'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('49', '\x49', '\x49'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('50', '&', 'P'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('51', '\x51', 'Q'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('52', '\x52', 'R'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('53', '\x53', 'S'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('54', '\x54', 'T'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('55', '\x55', 'U'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('56', '\x56', 'V'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('57', '\x57', 'W'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('58', '\x58', 'X'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('59', '\x59', 'Y'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('60', '-', '\x60'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('61', '/', 'a'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('62', '\x62', 'b'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('63', '\x63', 'c'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('64', '\x64', 'd'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('65', '\x65', 'e'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('66', '\x66', 'f'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('67', '\x67', 'g'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('68', '\x68', 'h'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('69', '\x69', 'i'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('70', '\x70', 'p'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('71', '\x71', 'q'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('72', '\x72', 'r'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('73', '\x73', 's'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('74', '\x74', 'u'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('75', '\x75', 'u'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('76', '\x76', 'v'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('77', '\x77', 'w'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('78', '\x78', 'x'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('79', '\x79', 'y'))
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
    EBCDIC_ASCII_CHART.append(EBCDICASCII('4C', '<', 'L'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('4D', '(', 'M'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('4E', '+', 'N'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('4F', '|', 'O'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('5A', '!', 'Z'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('5B', '$', '['))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('5C', '*', '/'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('5D', ')', ']'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('5E', ';', '\x5E'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('5F', '\x5F', '_'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('6A', '!', 'j'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('6B', '.', 'k'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('6C', '%', 'l'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('6D', '_', 'm'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('6E', '>', '\x5E'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('6F', '?', 'o'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('7A', ':', 'z'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('7B', '#', '{'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('7C', '@', '!'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('7D', "'", '}'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('7E', '=', '~'))
    EBCDIC_ASCII_CHART.append(EBCDICASCII('7F', '"', '\x7F'))