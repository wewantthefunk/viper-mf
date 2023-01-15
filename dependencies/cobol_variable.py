from datetime import datetime
import os
from os.path import exists

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
UPD_COMMAND = "update"
ZERO = "0"

last_command = ""

class COBOLVariable:
    def __init__(self, name: str, length: int, data_type: str, parent: str, redefines: str, occurs_length: int, decimal_length, level: str):
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


def Add_Variable(list, name: str, length: int, data_type: str, parent: str, redefines = EMPTY_STRING, occurs_length = 0, decimal_len = 0, level = "01"):
    global last_command
    check_for_last_command(ADD_COMMAND)
    last_command = ADD_COMMAND
    for l in list:
        if l.name == name:
            return list

    if data_type == NUMERIC_SIGNED_DATA_TYPE:
        data_type = NUMERIC_DATA_TYPE
        length = length + 1

    list.append(COBOLVariable(name, length, data_type, parent, redefines, occurs_length, decimal_len, level))

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
                        if value.startswith(HEX_PREFIX):
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
                        var.is_hex = True
                        hex_prefix = HEX_PREFIX
                    _update_var_value(orig_var_list, var, str(value), [])
                else:
                    if str(value).startswith(HEX_PREFIX):
                        value = value.replace(HEX_PREFIX, EMPTY_STRING)
                        var.is_hex = True
                        hex_prefix = HEX_PREFIX
                    _update_var_value(orig_var_list, var, str(value)[0:var.length], [])

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
        var.value = str(value)[0:var.length]

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
            val = orig.value             
        elif orig == None:
            val = name
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
    for var in var_list:
        if COBOL_FILE_VARIABLE_TYPE in str(type(var_list[0])):
            continue
        if var.parent == EMPTY_STRING:
            result = 0
            length = var.length
            if var.name == name:
                break
        
        elif var.name == name:
            return [result, var.length]
        else:
            result = result + var.length

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
        else:
            t = t + result[0]
        if result[1] == True:
            is_numeric_data_type = result[1]

    if is_numeric_data_type and force_str == False:
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
            #if var_list[count].level == LEVEL_88:
            #    count = count + 1
            #    continue
            if var_list[count].length == 0 and var_list[count].level != LEVEL_88:
                r = find_get_variable(var_list[count:], EMPTY_STRING, var_list[count].name, orig_var_list, sub_index)
                found_count = found_count + r[2]
                result = result + r[0]
                is_numeric_data_type = r[1]
                if var_list[count].name == parent:
                    is_numeric_data_type = var_list[count].data_type != 'X'
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
                        result = result + r1[pos_length[0]: pos_length[0] + pos_length[1]]
                        found_count = found_count + 1
                    break
                elif var_list[count].level == LEVEL_88 and var_list[count].name == name:
                    found_count = found_count + 1
                    if var_list[count].data_type == NUMERIC_DATA_TYPE:
                        is_numeric_data_type = True
                    r = find_get_variable(orig_var_list, var_list[count].parent, '----------', orig_var_list, sub_index)
                    result = r[0] == str(var_list[count].level88value)
                elif var_list[count].data_type == NUMERIC_DATA_TYPE:
                    result = result + pad_char(var_list[count].length - len(var_list[count].value), ZERO) + str(var_list[count].value)[:var_list[count].length]
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

def convert_EBCDIC_hex(input: str):
    return input

def convert_string_EBCDIC_hex(input: str):
    return input