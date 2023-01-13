from cobol_lexicon import *
from util import *
from cobol_verb_process import *

data_division_var_stack = []
data_division_level_stack = []
data_division_file_record = EMPTY_STRING
var_init_list = []


def process_identification_division_line(line: str, name: str):
    global var_init_list
    var_init_list = []
    if is_valid_verb(line, COBOL_IDENTIFICATION_DIVISION_VERBS):
        if COBOL_IDENTIFICATION_DIVISION_VERBS[0] in line:
            tmp = line.replace(COBOL_IDENTIFICATION_DIVISION_VERBS[0], EMPTY_STRING, 1)
            tmp = tmp.replace(PERIOD, EMPTY_STRING)
            return tmp.strip()

    return name

def process_environment_division_line(line: str, current_section: str, name: str, current_line, next_few_lines, args):
    tokens = parse_line_tokens(line, SPACE, EMPTY_STRING, True)

    if line == FILE_CONTROL_SECTION:
        current_section = FILE_CONTROL_SECTION
        current_line.current_section = current_section
        append_file(name + PYTHON_EXT, "# " + current_section + NEWLINE)
        append_file(name + PYTHON_EXT, UNDERSCORE + format(current_section) + "Vars = []" + NEWLINE)
        append_file(name + PYTHON_EXT, VARIABLES_LIST_NAME + ".append(" + "_" + format(current_section) + "Vars)" + NEWLINE)
    elif tokens[0] == SELECT_KEYWORD:
        create_file_variable(tokens, name, next_few_lines, current_section)
    elif line == INPUT_OUTPUT_SECTION:
        current_section = INPUT_OUTPUT_SECTION
        current_line.current_section = current_section
        append_file(name + PYTHON_EXT, "# " + current_section + NEWLINE)
    elif line == CONFIGURATION_SECTION:
        current_section = CONFIGURATION_SECTION
        current_line.current_section = current_section
        append_file(name + PYTHON_EXT, "# " + current_section + NEWLINE)
    elif line == SPECIAL_NAMES_SECTION:
        current_section = SPECIAL_NAMES_SECTION
        current_line.current_section = current_section
        append_file(name + PYTHON_EXT, "# " + current_section + NEWLINE)
        append_file(name + PYTHON_EXT, UNDERSCORE + format(current_section) + "Vars = []" + NEWLINE)
        append_file(name + PYTHON_EXT, VARIABLES_LIST_NAME + ".append(" + "_" + format(current_section) + "Vars)" + NEWLINE)
    elif tokens[0] == CLASS_KEYWORD:
        create_class_variable(tokens, name, next_few_lines, current_section)

    return [line, current_line, name, current_section, next_few_lines, args]

def create_class_variable(tokens, name: str, next_few_lines, current_section: str):
    done_class_line = False
    for next_line in next_few_lines:
        nl_tokens = parse_line_tokens(next_line, SPACE, EMPTY_STRING, True)
        for nl_token in nl_tokens:
            if nl_token != PERIOD and nl_token not in [CLASS_KEYWORD]:
                tokens.append(nl_token)
            else:
                done_class_line = True
                break

        if done_class_line:
            break

    val = tokens[2].replace(SINGLE_QUOTE, EMPTY_STRING)
    append_file(name + PYTHON_EXT, "_" + format(current_section) + "Vars = Add_Variable(_" + format(current_section) + "Vars,'" + tokens[1] + "', " \
         + str(len(val)) + ", '" + "X" + "','" + EMPTY_STRING + "','" + EMPTY_STRING + "')" + NEWLINE)

    var_init_list.append([COBOL_VERB_MOVE, tokens[2], EMPTY_STRING, tokens[1]])

def create_file_variable(tokens, name: str, next_few_lines, current_section: str):
    done_file_line = False
    for next_line in next_few_lines:
        nl_tokens = parse_line_tokens(next_line, SPACE, EMPTY_STRING, True)
        for nl_token in nl_tokens:
            if nl_token != PERIOD:
                tokens.append(nl_token)
            else:
                done_file_line = True
                break

        if done_file_line:
            break

    count = 0
    assign = EMPTY_STRING
    organization = EMPTY_STRING
    access = EMPTY_STRING
    record_key = EMPTY_STRING
    file_status = EMPTY_STRING
    for token in tokens:
        if token == ASSIGN_KEYWORD:
            assign = tokens[count + 1]
            if tokens[count + 1] == TO_KEYWORD:
                assign = tokens[count + 2]
        elif token == ORGANIZATION_KEYWORD or token == ORGANISATION_KEYWORD:
            organization = tokens[count + 1]
            if tokens[count + 1] == IS_KEYWORD:
                organization = tokens[count + 2]
                if tokens[count + 2] == LINE_KEYWORD:
                    organization = tokens[count + 2] + tokens[count + 3]
            elif organization == LINE_KEYWORD:
                organization = organization + SPACE + tokens[count + 2]
        elif token == ACCESS_KEYWORD:
            access = tokens[count + 1]
            if tokens[count + 1] == IS_KEYWORD:
                access = tokens[count + 2]
        elif token == RECORD_KEYWORD and tokens[count + 1] == KEY_KEYWORD:
            record_key = tokens[count + 2]
            if tokens[count + 2] == IS_KEYWORD:
                record_key = tokens[count + 3]
        elif token == FILE_KEYWORD and tokens[count + 1] == STATUS_KEYWORD:
            file_status = tokens[count + 2]
            if tokens[count + 2] == IS_KEYWORD:
                file_status = tokens[count + 3]
        count = count + 1

    append_file(name + PYTHON_EXT, "Add_File_Variable(_" + format(current_section) + "Vars, '" + tokens[1] + "','" + assign \
        + "','" + organization + "','" + access + "','" + record_key + "','" + file_status + "')" + NEWLINE)

def process_data_division_line(line: str, current_section: str, name: str, current_line: LexicalInfo, next_few_lines, args):
    global data_division_var_stack, data_division_level_stack, data_division_file_record
    if line in DATA_DIVISION_SECTIONS:
        current_section = line
        current_line.first_line_section = True
        current_line.highest_ws_level = 99
        data_division_var_stack = []
        data_division_level_stack = []
        current_line.skip_the_next_lines = 0
        append_file(name + PYTHON_EXT, "# " + current_section + NEWLINE)
        append_file(name + PYTHON_EXT, "_" + format(current_section) + "Vars = []" + NEWLINE)
        append_file(name + PYTHON_EXT, VARIABLES_LIST_NAME + ".append(" + "_" + format(current_section) + "Vars)" + NEWLINE)
    else:
        tokens = parse_line_tokens(line, SPACE, EMPTY_STRING, True)
        if line.startswith(FD_KEYWORD):
            data_division_file_record = tokens[1]
        elif line.startswith(COPYBOOK_KEYWORD):
            insert_copybook(name + PYTHON_EXT, line.replace(COPYBOOK_KEYWORD, EMPTY_STRING).replace(PERIOD, EMPTY_STRING).strip(), current_line, name, current_section, next_few_lines, args)
        else:
            if data_division_file_record != EMPTY_STRING and tokens[0].isnumeric():
                append_file(name + PYTHON_EXT, "# this is where we will associate the record " + tokens[1] + " to the file " + data_division_file_record + NEWLINE)
                append_file(name + PYTHON_EXT, "Set_File_Record(_FILE_CONTROLVars, '" + data_division_file_record + "','" + tokens[1] + "')" + NEWLINE)
                data_division_file_record = EMPTY_STRING
            if line[0:2].isnumeric() == False:
                return [line, current_section, name, current_line]

            create_variable(line, current_line, name, current_section, next_few_lines, args)
    
    return [line, current_section, name, current_line]

def process_procedure_division_line(line: str, name: str, current_line: LexicalInfo, next_few_lines, args):
    temp_tokens = parse_line_tokens(line, SPACE, EMPTY_STRING, True)
    skip = 0
    level = current_line.level
    ignore_until_verbs = []

    if temp_tokens[0] == COBOL_VERB_SEARCH:
        ignore_until_verbs.append(COBOL_VERB_WHEN)

    fix_parens(temp_tokens, temp_tokens[0], temp_tokens[len(temp_tokens) - 1])

    if temp_tokens[len(temp_tokens) - 1] == PERIOD:
        level = process_verb(temp_tokens, name, True, level, args, current_line)
    else:
        for nl in next_few_lines:
            nlt = parse_line_tokens(nl[6:], SPACE, EMPTY_STRING, True)
            if len(nlt) == 0:
                continue
            if (check_valid_verb(nlt[0], temp_tokens[0]) or nlt[len(nlt) - 1] == PERIOD):
                if nlt[len(nlt) - 1] == PERIOD:
                    for t in nlt:
                        temp_tokens.append(t)
                    if check_valid_verb(nlt[0], temp_tokens[0]) == False:
                        skip = skip + 1
                level = process_verb(temp_tokens, name, True, level, args, current_line)
                break
            else:
                skip = skip + 1
                for t in nlt:
                    temp_tokens.append(t)
                    fix_parens(temp_tokens, temp_tokens[0], temp_tokens[len(temp_tokens) - 1])

    return [skip, level]

def fix_parens(temp_tokens, value: str, value2: str):
    if value.startswith("IF(") or value.startswith('AND(') or value.startswith("OR("):
        s = value.split(OPEN_PARENS)
        temp_tokens[0] = s[0]
        temp_tokens.insert(1,  OPEN_PARENS)
        temp_tokens.insert(2, s[1])
        if value2.endswith(CLOSE_PARENS):
            s = value.split(CLOSE_PARENS)
            value = s[0]
            temp_tokens.append(CLOSE_PARENS)

def check_ignore_verbs(ignore_verbs, v: str):
    if len(ignore_verbs) == 0:
        return True

    return v in ignore_verbs

def create_variable(line: str, current_line: LexicalInfo, name: str, current_section: str, next_few_lines, args):
    global data_division_var_stack, data_division_level_stack, var_init_list
    tokens = parse_line_tokens(line, SPACE, EMPTY_STRING, False)

    skip_lines_count = 0

    if not line.endswith(PERIOD):
        for nl in next_few_lines:
            skip_lines_count = skip_lines_count + 1
            nlt = parse_line_tokens(nl[6:].replace(NEWLINE, EMPTY_STRING), SPACE, EMPTY_STRING, True)
            for t in nlt:
                tokens.append(t)

            if PERIOD in nlt:
                break

    current_line.skip_the_next_lines = skip_lines_count

    if len(tokens) < 1:
        return
    if len(tokens) < 2:
        return

    if VALUE_CLAUSE == tokens[1]:
        tokens.insert(1, gen_rand(5))

    if REDEFINES_KEYWORD in tokens:
        if tokens[1] == REDEFINES_KEYWORD:
            tokens.insert(1, REDEFINES_KEYWORD + gen_rand(4))
        current_line.redefines = tokens[tokens.index(REDEFINES_KEYWORD) + 1]
        current_line.redefines_level = tokens[0]
    elif int(tokens[0]) <= int(current_line.redefines_level):
        current_line.redefines = EMPTY_STRING
        current_line.redefines_level = tokens[0]
    tokens[1] = tokens[1].replace(PERIOD, EMPTY_STRING)
    tokens[0] = tokens[0].replace(PERIOD, EMPTY_STRING)

    occurs_length = 0
   
    if len(tokens) == 2 or PIC_CLAUSE not in tokens:  
        new_level = tokens[0]
        while len(data_division_level_stack) > 0 and int(new_level) < int(data_division_level_stack[len(data_division_level_stack) - 1]):
                data_division_level_stack.pop()
                data_division_var_stack.pop()
                if len(data_division_level_stack) > 0:
                    new_level = data_division_level_stack[len(data_division_level_stack) - 1]

        if len(data_division_var_stack) == 0:
            data_division_level_stack.append(tokens[0])
            data_division_var_stack.append(tokens[1])
            current_line.highest_var_name = data_division_var_stack[len(data_division_var_stack) - 1]
            current_line.highest_ws_level = int(data_division_level_stack[len(data_division_level_stack) - 1])
            
        if current_line.highest_var_name == EMPTY_STRING:
            current_line.highest_ws_level = int(tokens[0])
            current_line.highest_var_name = tokens[1] 
            if (tokens[1] not in data_division_var_stack):
                data_division_var_stack.append(tokens[1])
                data_division_level_stack.append(tokens[0])
        elif int(tokens[0]) == int(data_division_level_stack[len(data_division_level_stack) - 1]):
            if len(data_division_var_stack) > 0:
                data_division_var_stack.remove(data_division_var_stack[len(data_division_var_stack) - 1])
            if len(data_division_level_stack) > 0:
                data_division_level_stack.remove(data_division_level_stack[len(data_division_level_stack) - 1])
            if len(data_division_var_stack) == 0:
                data_division_level_stack.append(tokens[0])
                data_division_var_stack.append(tokens[1])
            current_line.highest_var_name = data_division_var_stack[len(data_division_var_stack) - 1]
            current_line.highest_ws_level = int(data_division_level_stack[len(data_division_level_stack) - 1])
            if tokens[1] not in data_division_var_stack:
                data_division_level_stack.append(tokens[0])
                data_division_var_stack.append(tokens[1])
        elif len(data_division_var_stack) > 0:            
            if len(data_division_var_stack) == 0:
                data_division_var_stack.append(tokens[1])
                data_division_level_stack.append(tokens[0])
            current_line.highest_var_name = data_division_var_stack[len(data_division_var_stack) - 1]
            current_line.highest_ws_level = int(data_division_level_stack[len(data_division_level_stack) - 1])
            if (tokens[1] not in data_division_var_stack):
                data_division_var_stack.append(tokens[1])
                data_division_level_stack.append(tokens[0])

        if OCCURS_CLAUSE in tokens:
            i = tokens.index(OCCURS_CLAUSE)
            occurs_length = int(tokens[i + 1])

        if INDEXED_CLAUSE in tokens:
            i = tokens.index(INDEXED_CLAUSE) + 1
            if BY_KEYWORD in tokens:
                i = i + 1
            append_file(name + PYTHON_EXT, "_" + format(current_section) + "Vars = Add_Variable(_" + format(current_section) + "Vars,'" + tokens[i] + "', " \
                + "10, '9','" + tokens[i] + "','',0,'" + tokens[0] + "')" + NEWLINE)
            

    elif current_line.highest_ws_level < int(tokens[0]):
        if len(data_division_var_stack) > 0:
            current_line.highest_var_name = data_division_var_stack[len(data_division_var_stack) - 1]
            current_line.highest_ws_level = int(tokens[0])
    else:
        while len(data_division_var_stack) > 0:
            if int(data_division_level_stack[len(data_division_level_stack) - 1]) >= int(tokens[0]):
                if len(data_division_var_stack) > 0:
                    data_division_var_stack.remove(data_division_var_stack[len(data_division_var_stack) - 1])
                if len(data_division_level_stack) > 0:
                    data_division_level_stack.remove(data_division_level_stack[len(data_division_level_stack) - 1])

                if len(data_division_var_stack) > 0:
                    current_line.highest_var_name = data_division_var_stack[len(data_division_var_stack) - 1]
            else:
                break
        if len(data_division_var_stack) > 0:
            if current_line.highest_ws_level < int(tokens[0]):
                current_line.highest_var_name = data_division_var_stack[len(data_division_var_stack) - 1]
                current_line.highest_ws_level = int(data_division_level_stack[len(data_division_level_stack) - 1])
            data_division_level_stack.append(tokens[0])
            data_division_var_stack.append(tokens[1])
        else:
            data_division_level_stack.append(tokens[0])
            data_division_var_stack.append(tokens[1])
            current_line.highest_var_name = data_division_var_stack[len(data_division_var_stack) - 1]
            current_line.highest_ws_level = int(data_division_level_stack[len(data_division_level_stack) - 1])
    
    data_info = get_data_info(tokens)
    if len(data_info) < 1:
        data_info.append("X")
    if len(data_info) < 2:
        data_info.append(0)
    if len(data_info) < 3:
        data_info.append(0)
    v_name = tokens[1]
    if v_name == PIC_CLAUSE:
        current_line.highest_var_name_subs = current_line.highest_var_name_subs + 1
        v_name = current_line.highest_var_name + "-SUB-" + str(current_line.highest_var_name_subs)
    append_file(name + PYTHON_EXT, "_" + format(current_section) + "Vars = Add_Variable(_" + format(current_section) + "Vars,'" + v_name + "', " \
         + str(data_info[1]) + ", '" + data_info[0] + "','" + current_line.highest_var_name + "','" + current_line.redefines + "'," + str(occurs_length) + "," \
            + str(data_info[2]) + ",'" + tokens[0] + "')" + NEWLINE)

    if VALUE_CLAUSE in tokens:
        var_init_list.append([COBOL_VERB_MOVE, tokens[tokens.index(VALUE_CLAUSE) + 1], EMPTY_STRING, v_name])

    if len(tokens) == 2:
        current_line.highest_var_name = tokens[1]

def init_vars(name: str, args, current_line):
    global var_init_list
    for vil in var_init_list:
        process_verb(vil, name, False, 1, args, current_line)

def is_valid_verb(line: str, verb_list):
    for verb in verb_list:
        if line.startswith(verb):
            return True

    return False

def get_data_info(tokens):
    info = ['X', 0]
    count = 0
    for t in tokens:
        if (t == PIC_CLAUSE):
            info = get_type_length(tokens, count)
            break
        count = count + 1

    return info

def get_type_length(tokens, count: int):
    length = 1
    type_length = tokens[count + 1].split(OPEN_PARENS)
    decimal_length = 0
    if len(type_length) > 1:
        final_length = type_length[1].replace(CLOSE_PARENS, EMPTY_STRING).replace(PERIOD, EMPTY_STRING)
        if DECIMAL_INDICATOR in final_length:
            t = final_length.split(DECIMAL_INDICATOR)
            final_length = str(int(t[0]) + len(t[1]))
            decimal_length = len(t[1])

        length = int(final_length)

    return [type_length[0], length, decimal_length]

def insert_copybook(outfile, copybook, current_line, name, current_section, next_few_lines, args):
    replace_info = [copybook, EMPTY_STRING, EMPTY_STRING, EMPTY_STRING]
    if REPLACING_KEYWORD in copybook:
        replace_info = copybook.split(REPLACING_DELIMITER)
        copybook = replace_info[0].replace(REPLACING_KEYWORD, EMPTY_STRING).strip()
        print(copybook)
    file_exists = exists(copybook)
    if file_exists == False:
        copybook = copybook + COPYBOOK_EXT
        file_exists = exists(copybook)
        if file_exists == False:
            copybook = COPYBOOK_FOLDER + copybook
            file_exists = exists(copybook)
            if file_exists == False:
                copybook = copybook.replace(COPYBOOK_EXT, EMPTY_STRING)
                file_exists = exists(copybook)
                if file_exists == False:
                    return

    raw_lines = read_raw_file_lines(copybook, 0)
    total = len(raw_lines)
    count = 0
    skip_the_next_lines_count = 0
    for line in raw_lines:
        count = count + 1
        next_few_lines_count = LINES_AHEAD
        lines_left = total - count
        if lines_left < 0:
            while lines_left < 0:
                lines_left = lines_left - 1
            next_few_lines_count = lines_left
        next_few_lines = raw_lines[count:count+next_few_lines_count]
        if skip_the_next_lines_count == current_line.skip_the_next_lines:
            skip_the_next_lines_count = 0
        else:
            skip_the_next_lines_count = skip_the_next_lines_count + 1
            continue
        line = line.replace(replace_info[1], replace_info[3]).replace(NEWLINE, EMPTY_STRING).strip()
        if line != EMPTY_STRING:
            create_variable(line, current_line, name, current_section, next_few_lines, args)
    append_file(outfile, NEWLINE)
    append_file(outfile, NEWLINE)