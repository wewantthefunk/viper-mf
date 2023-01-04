from datetime import datetime
import os

ADD_COMMAND = "add"
DISP_COMMAND = "display"
EMPTY_STRING = ""
GET_COMMAND = "get"
LITERAL = "literal"
NEWLINE = "\n"
NUMERIC_DATA_TYPE = "9"
NUMERIC_SIGNED_DATA_TYPE = "S9"
SET_COMMAND = "set"
SPACE = " "
SPACES_INITIALIZER = "____spaces"
UPD_COMMAND = "update"
ZERO = "0"

last_command = ""

class COBOLVariable:
    def __init__(self, name: str, length: int, data_type: str, parent: str):
        self.name = name
        self.length = length
        self.data_type = data_type
        if parent != name:
            self.parent = parent
        else:
            self.parent = EMPTY_STRING
        self.value = EMPTY_STRING

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

    def open_file(self, method: str):
        filename = os.getenv(self.assign)
        if filename == None:
            filename = self.assign
            f = open(filename, "a")
            f.close()

        self.file_pointer = open(filename, method)

    def close_file(self):
        self.file_pointer.close()

    def read(self):
        line = self.file_pointer.readline().replace(NEWLINE, EMPTY_STRING)

        at_end = False

        if not line:
            at_end = True
            line = EMPTY_STRING

        return [line, at_end]

    def write(self, data: str):
        self.file_pointer.write(data)

def Open_File(var_list, name: str, method: str):
    for var in var_list:
        if var.name == name:
            var.open_file(convert_open_method(method))
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
            search_variable_list(file_rec_var_list, var.record, read_result[0], var.record, [])
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


def Add_Variable(list, name: str, length: int, data_type: str, parent: str):
    global last_command
    check_for_last_command(ADD_COMMAND)
    last_command = ADD_COMMAND
    for l in list:
        if l.name == name:
            return list

    if data_type == NUMERIC_SIGNED_DATA_TYPE:
        data_type = NUMERIC_DATA_TYPE

    list.append(COBOLVariable(name, length, data_type, parent))

    return list

def Set_Variable(variable_lists, name: str, value: str, parent: str):  
    global last_command
    check_for_last_command(SET_COMMAND)
    last_command = SET_COMMAND  
    sub_index = []
    if "(" in name:
        s = name.split("(")
        s1 = s[1].split(":")
        start = int(s1[0]) - 2
        if start < 0:
            start = 0
        sub_index = [start, int(s1[1].replace("(", EMPTY_STRING).replace(")", EMPTY_STRING)) + int(s1[0]) - 1]
        name = s[0]
    if "(" in parent:
        ps = parent.split("(")
        parent = ps[0]
    for var_list in variable_lists:
        result = search_variable_list(var_list, name, value, [parent], sub_index)
        if result:
            break

def search_variable_list(var_list, name: str, value: str, parent: str, sub_index: str):
    count = 0
    found = False
    for var in var_list:
        if "COBOLFileVariable" in str(type(var_list[0])):
            continue
        if var.name == name or var.parent in parent:
            name = var.name
            found = True
            count = var_list.index(var) + 1
            if var.length == 0:
                if (var.name not in parent):
                    parent.append(var.name)
                found = search_variable_list(var_list[count:], EMPTY_STRING, value, parent, sub_index)
            else:
                is_spaces = False
                if value == SPACES_INITIALIZER:
                    is_spaces = True
                    if var.data_type == NUMERIC_DATA_TYPE:
                        value = pad_char(var.length, ZERO)
                    else:
                        value = pad(var.length)
                if var.data_type == NUMERIC_DATA_TYPE:
                    if str(value).isnumeric() == False:
                        value = 0
                offset = var.length
                if len(sub_index) > 0:
                    if var.length >= sub_index[0]:
                        var.value = var.value[:sub_index[0]] + str(value) + var.value[sub_index[1]:]
                    else:
                        offset = 0
                else:
                    var.value = str(value)[0:var.length]
                if (len(str(value)) > var.length and (name not in parent or name == EMPTY_STRING) and var.parent != EMPTY_STRING) or is_spaces:
                    if var.parent not in parent:
                        parent.append(var.parent)
                    if is_spaces:
                        value = SPACES_INITIALIZER
                        offset = 0
                    found = search_variable_list(var_list[count:], EMPTY_STRING, value[offset:], parent, sub_index)

            break

    return found

def Update_Variable(variable_lists, value: str, name: str, parent: str):
    global last_command
    check_for_last_command(UPD_COMMAND)
    last_command = UPD_COMMAND
    orig = None 
    target = None  
    for var_list in variable_lists:
        orig = find_variable(var_list, name, [parent])
        target = find_variable(var_list, parent, [parent])
        if orig != None and target != None:
            v = value
            if orig.data_type == NUMERIC_DATA_TYPE:
                v = str(int(value) + int(orig.value))[0:target.length]
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
        if "COBOLFileVariable" in str(type(var_list[0])):
            continue
        if var.name == name or var.parent in parent:
            if var.length == 0:
                if (var.name not in parent):
                    parent.append(var.name)
            else:
                result = result + var.length

    return result

def Get_Variable_Value(variable_lists, name: str, parent: str):
    global last_command
    check_for_last_command(GET_COMMAND)
    last_command = GET_COMMAND
    t = EMPTY_STRING
    is_numeric_data_type = False
    for var_list in variable_lists:
        result = find_get_variable(var_list, name, [parent])
        t = t + result[0]
        if result[1] == True:
            is_numeric_data_type = result[1]

    if is_numeric_data_type:
        if t == EMPTY_STRING:
            t = "0"
        return int(t)

    return t

def find_get_variable(var_list, name: str, parent):
    result = EMPTY_STRING
    is_numeric_data_type = False
    for var in var_list:
        if "COBOLFileVariable" in str(type(var_list[0])):
            continue
        if var.name == name or var.parent in parent:
            if var.length == 0:
                if (var.name not in parent):
                    parent.append(var.name)
            else:
                padc = SPACE
                if var.data_type == NUMERIC_DATA_TYPE:
                    padc = ZERO
                    result = result + str(var.value).rjust(var.length, padc)[:var.length]
                    is_numeric_data_type = True
                else:
                    is_numeric_data_type = False
                    result = result + str(var.value).ljust(var.length, padc)[:var.length]

    return [result, is_numeric_data_type]


def find_variable(var_list, name: str, parent):
    count = 0
    result = EMPTY_STRING
    for var in var_list:
        if "COBOLFileVariable" in str(type(var_list[0])):
            continue
        if var.name == name or var.parent in parent:
            count = count + 1
            if var.length == 0:
                if (var.name not in parent):
                    parent.append(var.name)
                result = result + find_variable(var_list[count:], EMPTY_STRING, parent)
            else:
                return var
            
    return None

def Display_Variable(variable_lists, name: str, parent: str, is_literal: bool, is_last: bool):
    global last_command
    check_for_last_command(DISP_COMMAND)
    last_command = DISP_COMMAND
    if (parent == LITERAL):
        print(name, end =EMPTY_STRING)
        if is_last:
            print(EMPTY_STRING)
    else:
        for var_list in variable_lists:
            search_display_variable_list(var_list, name, parent, 0)

def search_display_variable_list(var_list, name: str, parent: str, level: int):
    count = 0
    found_count = 0
    level = level + 1
    while count < len(var_list):
        if "COBOLFileVariable" in str(type(var_list[0])):
            count = count + 1
            continue
        if var_list[count].name == name or var_list[count].parent == parent:
            if var_list[count].length == 0:
                found_count = found_count + search_display_variable_list(var_list[count:], EMPTY_STRING, var_list[count].name, level)
                count = count + found_count
            else:     
                found_count = found_count + 1           
                if var_list[count].data_type == NUMERIC_DATA_TYPE:
                    print(pad_char(var_list[count].length - len(var_list[count].value), ZERO) + str(var_list[count].value), end =EMPTY_STRING)
                else:
                    print(var_list[count].value.ljust(var_list[count].length), end =EMPTY_STRING)

        count = count + 1
        if count > len(var_list):
            break


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