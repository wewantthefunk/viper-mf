from cobol_lexicon import *
from util import *
from cobol_verb_process import *

data_division_var_stack = []
data_division_level_stack = []
data_division_cascade_stack = []
data_division_redefines_stack = []
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
        if current_section not in current_line.sections_list:
            current_line.sections_list.append(current_section)    
        append_file(name + PYTHON_EXT, "# " + current_section + NEWLINE)
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
        if current_section not in current_line.sections_list:
            current_line.sections_list.append(current_section)
        append_file(name + PYTHON_EXT, "# " + current_section + NEWLINE)
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
    append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + "result = Add_Variable(" + SELF_REFERENCE + name + MEMORY + COMMA + SELF_REFERENCE + "_DataDivisionVars,'" + tokens[1] + "', " \
         + str(len(val)) + ", '" + "X" + "','" + EMPTY_STRING + "','" + EMPTY_STRING + "')" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + "_DataDivisionVars = result[0]" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + name + MEMORY + " = result[1]" + NEWLINE)

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

    append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + "result = Add_File_Variable(" + SELF_REFERENCE + "_FILE_CONTROLVars, '" + tokens[1] + "','" + assign \
        + "','" + organization + "','" + access + "','" + record_key + "','" + file_status + "')" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + "_FILE_CONTROLVars = result" + NEWLINE)

def process_data_division_line(line: str, current_section: str, name: str, current_line: LexicalInfo, next_few_lines, args):
    global data_division_var_stack, data_division_level_stack, data_division_file_record, data_division_cascade_stack
    if line in DATA_DIVISION_SECTIONS:
        current_section = line
        current_line.first_line_section = True
        current_line.highest_ws_level = 99
        data_division_var_stack = []
        data_division_level_stack = []
        data_division_cascade_stack = []
        current_line.skip_the_next_lines = 0
        append_file(name + PYTHON_EXT, "# " + current_section + NEWLINE)
        #append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + VARIABLES_LIST_NAME + ".append(" + SELF_REFERENCE + "_DataDivisionVars)" + NEWLINE)
    else:
        tokens = parse_line_tokens(line, SPACE, EMPTY_STRING, True)
        if line.startswith(FD_KEYWORD) or line.startswith(SD_KEYWORD):
            data_division_file_record = tokens[1]
            if line.startswith(SD_KEYWORD):
                data_division_file_record = data_division_file_record + SORT_IDENTIFIER
        elif line.startswith(COPYBOOK_KEYWORD):
            insert_copybook(name + PYTHON_EXT, line.replace(COPYBOOK_KEYWORD, EMPTY_STRING).replace(PERIOD, EMPTY_STRING).strip(), current_line, name, current_section, next_few_lines, args)
        else:
            if data_division_file_record != EMPTY_STRING and tokens[0].isnumeric():
                append_file(name + PYTHON_EXT, "# this is where we will associate the record " + tokens[1] + " to the file " + data_division_file_record + NEWLINE)
                append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + "self._FILE_CONTROLVars = Set_File_Record(self._FILE_CONTROLVars, '" + data_division_file_record + "','" + tokens[1] + "')" + NEWLINE)
                data_division_file_record = EMPTY_STRING
            if line[0:2].isnumeric() == False:
                return [line, current_section, name, current_line]

            create_variable(line, current_line, name, current_section, next_few_lines, args)
    
    return [line, current_section, name, current_line]

def process_procedure_division_line(line: str, name: str, current_line: LexicalInfo, next_few_lines, args):
    temp_tokens = parse_line_tokens(line, SPACE, EMPTY_STRING, True)
    skip = 0
    level = current_line.level

    fix_parens(temp_tokens, temp_tokens[0], temp_tokens[len(temp_tokens) - 1])

    if temp_tokens[0] == COBOL_VERB_SEARCH:
        current_line.end_of_search_criteria = True

    if temp_tokens[len(temp_tokens) - 1] == PERIOD:
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + SELF_REFERENCE + "debug_line = '" + current_line.current_line_number + "'" + NEWLINE)
        level = process_verb(temp_tokens, name, True, level, args, current_line)
    else:
        for nl in next_few_lines:
            nll = nl.split("^^^")
            nllt = nll[0]
            nlt = parse_line_tokens(nllt[6:], SPACE, EMPTY_STRING, True)
            if len(nlt) == 0:
                continue

            if (check_valid_verb(nlt[0], temp_tokens[0], current_line.end_of_search_criteria) or nlt[len(nlt) - 1] == PERIOD):
                if nlt[len(nlt) - 1] == PERIOD:
                    for t in nlt:
                        temp_tokens.append(t)
                    if check_valid_verb(nlt[0], temp_tokens[0], current_line.end_of_search_criteria) == False:
                        skip = skip + 1

                if temp_tokens[0] != COBOL_VERB_WHEN and current_line.is_evaluating == False:
                    append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + SELF_REFERENCE + "debug_line = '" + current_line.current_line_number + "'" + NEWLINE)
                level = process_verb(temp_tokens, name, True, level, args, current_line)
                break
            else:
                skip = skip + 1
                for t in nlt:
                    temp_tokens.append(t)
                    fix_parens(temp_tokens, temp_tokens[0], temp_tokens[len(temp_tokens) - 1])
            if nlt[0] == COBOL_VERB_WHEN:
                current_line.end_of_search_criteria = False

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

def create_variable(line: str, current_line: LexicalInfo, name: str, current_section: str, next_few_lines, args, is_eib = False):
    global data_division_var_stack, data_division_level_stack, var_init_list, data_division_cascade_stack, data_division_redefines_stack

    tokens = parse_line_tokens(line, SPACE, EMPTY_STRING, False)

    if tokens[0].isnumeric() == False:
        return

    cascade_data_type = current_line.cascade_data_type
    hard_cascade_type = False

    if COMP_3_KEYWORD in tokens:
        cascade_data_type = COMP_3_KEYWORD
        hard_cascade_type = True
    elif COMP_KEYWORD in tokens or BINARY_KEYWORD in tokens:
        cascade_data_type = COMP_KEYWORD
        hard_cascade_type = True
    elif COMP_5_KEYWORD in tokens:
        cascade_data_type = COMP_5_KEYWORD
        hard_cascade_type = True

    skip_lines_count = 0

    if not line.endswith(PERIOD):
        for nl in next_few_lines:
            skip_lines_count = skip_lines_count + 1
            nlt = parse_line_tokens(nl[6:].replace(NEWLINE, EMPTY_STRING), SPACE, EMPTY_STRING, True)
            
            skip_next = False
            count = 0
            for t in nlt:
                if skip_next:
                    count = count + 1
                    skip_next = False
                    continue

                if t.startswith(COBOL_CONTINUATION_CHAR):
                    skip_next = True
                    l = nlt[count + 1]
                    if l.startswith(SINGLE_QUOTE):
                        l = nlt[count + 1][1:]
                    tokens[len(tokens) - 1] = tokens[len(tokens) - 1] + l
                else:
                    tokens.append(t)

                count = count + 1

            if PERIOD in nlt:
                break

    current_line.skip_the_next_lines = skip_lines_count

    if len(tokens) < 1:
        return
    if len(tokens) < 2:
        tokens.append(gen_rand(5))
        if tokens[0] == "01":
            cascade_data_type = EMPTY_STRING

    if VALUE_CLAUSE == tokens[1] or OCCURS_CLAUSE == tokens[1]:
        tokens.insert(1, gen_rand(5))

    is_top_redefines = 'False'
    if REDEFINES_KEYWORD in tokens:
        is_top_redefines = 'True'
        if tokens[1] == REDEFINES_KEYWORD:
            tokens.insert(1, REDEFINES_KEYWORD + gen_rand(4))
        current_line.redefines = tokens[tokens.index(REDEFINES_KEYWORD) + 1]
        current_line.redefines_level = tokens[0]
        if current_line.redefines not in data_division_redefines_stack:
            data_division_redefines_stack.append(current_line.redefines)
    elif int(tokens[0]) <= int(current_line.redefines_level):
        if len(data_division_redefines_stack) > 0:
            data_division_redefines_stack.pop()
        if len(data_division_redefines_stack) > 0:
            current_line.redefines = data_division_redefines_stack[len(data_division_redefines_stack) - 1]
        else:
            current_line.redefines = EMPTY_STRING
        current_line.redefines_level = tokens[0]
    tokens[1] = tokens[1].replace(PERIOD, EMPTY_STRING)
    tokens[0] = tokens[0].replace(PERIOD, EMPTY_STRING)

    occurs_length = 0
    index_var = EMPTY_STRING

    if len(tokens) == 2 or (PIC_CLAUSE not in tokens and POINTER_CLAUSE not in tokens):  
        new_level = tokens[0]
        while len(data_division_level_stack) > 0 and int(new_level) <= int(data_division_level_stack[len(data_division_level_stack) - 1]):
                data_division_level_stack.pop()
                data_division_var_stack.pop()
                data_division_cascade_stack.pop()

        if len(data_division_cascade_stack) > 0:
            if data_division_cascade_stack[len(data_division_cascade_stack) - 1] != cascade_data_type and cascade_data_type not in tokens:
                cascade_data_type = data_division_cascade_stack[len(data_division_cascade_stack) - 1]

        if len(data_division_var_stack) == 0:
            data_division_level_stack.append(tokens[0])
            data_division_var_stack.append(tokens[1])
            data_division_cascade_stack.append(cascade_data_type)
            current_line.highest_var_name = data_division_var_stack[len(data_division_var_stack) - 1]
            current_line.highest_ws_level = int(data_division_level_stack[len(data_division_level_stack) - 1])
            
        if current_line.highest_var_name == EMPTY_STRING:
            current_line.highest_ws_level = int(tokens[0])
            current_line.highest_var_name = tokens[1] 
            if (tokens[1] not in data_division_var_stack):
                data_division_var_stack.append(tokens[1])
                data_division_level_stack.append(tokens[0])
                data_division_cascade_stack.append(cascade_data_type)
        elif int(tokens[0]) == int(data_division_level_stack[len(data_division_level_stack) - 1]):
            if len(data_division_var_stack) > 0:
                data_division_var_stack.pop()
            if len(data_division_level_stack) > 0:
                data_division_level_stack.pop()
            if len(data_division_cascade_stack) > 0:
                data_division_cascade_stack.pop()
            if len(data_division_var_stack) == 0:
                data_division_level_stack.append(tokens[0])
                data_division_var_stack.append(tokens[1])
                data_division_cascade_stack.append(cascade_data_type)
            current_line.highest_var_name = data_division_var_stack[len(data_division_var_stack) - 1]
            current_line.highest_ws_level = int(data_division_level_stack[len(data_division_level_stack) - 1])
            cascade_data_type = data_division_cascade_stack[len(data_division_cascade_stack) - 1]
            if tokens[1] not in data_division_var_stack:
                data_division_level_stack.append(tokens[0])
                data_division_var_stack.append(tokens[1])
                data_division_cascade_stack.append(cascade_data_type)
        elif len(data_division_var_stack) > 0:            
            if len(data_division_var_stack) == 0:
                data_division_var_stack.append(tokens[1])
                data_division_level_stack.append(tokens[0])
                data_division_cascade_stack.append(cascade_data_type)
            current_line.highest_var_name = data_division_var_stack[len(data_division_var_stack) - 1]
            current_line.highest_ws_level = int(data_division_level_stack[len(data_division_level_stack) - 1])
            
            if (tokens[1] not in data_division_var_stack):
                data_division_var_stack.append(tokens[1])
                data_division_level_stack.append(tokens[0])
                data_division_cascade_stack.append(cascade_data_type)

            cascade_data_type = data_division_cascade_stack[len(data_division_cascade_stack) - 1]

    elif current_line.highest_ws_level < int(tokens[0]):
        if len(data_division_var_stack) > 0:
            current_line.highest_var_name = data_division_var_stack[len(data_division_var_stack) - 1]
            current_line.highest_ws_level = int(tokens[0])
        data_division_var_stack.append(tokens[1])
        data_division_level_stack.append(tokens[0])
        data_division_cascade_stack.append(cascade_data_type)
    else:
        while len(data_division_var_stack) > 0:
            if int(data_division_level_stack[len(data_division_level_stack) - 1]) >= int(tokens[0]):
                if len(data_division_var_stack) > 0:
                    data_division_var_stack.pop()
                if len(data_division_level_stack) > 0:
                    data_division_level_stack.pop()
                if len(data_division_cascade_stack) > 0:
                    data_division_cascade_stack.pop()

                if len(data_division_var_stack) > 0:
                    current_line.highest_var_name = data_division_var_stack[len(data_division_var_stack) - 1]
                    current_line.cascade_data_type = data_division_cascade_stack[len(data_division_cascade_stack) - 1]
                    
                    if hard_cascade_type:
                        current_line.cascade_data_type = cascade_data_type
                        data_division_cascade_stack.append(cascade_data_type)
                    else:
                        cascade_data_type = current_line.cascade_data_type
                else:
                    current_line.cascade_data_type = EMPTY_STRING
                    cascade_data_type = EMPTY_STRING
            else:
                break
        if len(data_division_var_stack) > 0:
            if current_line.highest_ws_level < int(tokens[0]):
                current_line.highest_var_name = data_division_var_stack[len(data_division_var_stack) - 1]
                current_line.highest_ws_level = int(data_division_level_stack[len(data_division_level_stack) - 1])
            data_division_level_stack.append(tokens[0])
            data_division_var_stack.append(tokens[1])
            data_division_cascade_stack.append(cascade_data_type)
        else:
            data_division_level_stack.append(tokens[0])
            data_division_var_stack.append(tokens[1])
            data_division_cascade_stack.append(cascade_data_type)
            current_line.highest_var_name = data_division_var_stack[len(data_division_var_stack) - 1]
            current_line.highest_ws_level = int(data_division_level_stack[len(data_division_level_stack) - 1])
    
    data_info = get_data_info(tokens)
    if len(data_info) < 1:
        data_info.append(ALPHANUMERIC_DATA_TYPE)
    if len(data_info) < 2:
        data_info.append(0)
    if len(data_info) < 3:
        data_info.append(0)
    if len(data_info) < 4:
        data_info.append(EMPTY_STRING)

    if cascade_data_type == COMP_KEYWORD and data_info[0] != ALPHANUMERIC_DATA_TYPE:
        data_info[3] = COMP_KEYWORD
    elif (data_info[3] == COMP_1_KEYWORD or cascade_data_type == COMP_1_KEYWORD) and data_info[0] != ALPHANUMERIC_DATA_TYPE:
        data_info[3] = COMP_1_KEYWORD
    elif (data_info[3] == COMP_2_KEYWORD or cascade_data_type == COMP_2_KEYWORD) and data_info[0] != ALPHANUMERIC_DATA_TYPE:
        data_info[3] = COMP_2_KEYWORD
    elif (data_info[3] == COMP_3_KEYWORD or cascade_data_type == COMP_3_KEYWORD) and data_info[0] != ALPHANUMERIC_DATA_TYPE:
        data_info[3] = COMP_3_KEYWORD
    elif (data_info[3] == COMP_4_KEYWORD or cascade_data_type == COMP_4_KEYWORD) and data_info[0] != ALPHANUMERIC_DATA_TYPE:
        data_info[3] = COMP_4_KEYWORD
    elif (data_info[3] == COMP_5_KEYWORD or cascade_data_type == COMP_5_KEYWORD) and data_info[0] != ALPHANUMERIC_DATA_TYPE:
        data_info[3] = COMP_5_KEYWORD

    if INDEXED_CLAUSE in tokens:
        i = tokens.index(INDEXED_CLAUSE) + 1
        if BY_KEYWORD in tokens:
            i = i + 1
        current_line.index_variables.append([tokens[i], tokens[i], "01", "_DataDivisionVars"])
        index_var = tokens[i]

    if OCCURS_CLAUSE in tokens:
        i = tokens.index(OCCURS_CLAUSE)
        occurs_length = int(tokens[i + 1])
        if tokens[i + 2] == TO_KEYWORD:
            occurs_length = int(tokens[i + 3])

    v_name = tokens[1]
    if v_name == PIC_CLAUSE:
        current_line.highest_var_name_subs = current_line.highest_var_name_subs + 1
        v_name = current_line.highest_var_name + "-SUB-" + str(current_line.highest_var_name_subs)
    memory_name = SELF_REFERENCE + name + MEMORY 
    variable_list = "_DataDivisionVars"
    if is_eib:
        memory_name = SELF_REFERENCE + EIB_MEMORY 
        variable_list = EIB_VARIABLE_LIST
    append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + variable_list + " = Add_Variable(" + memory_name + "," + SELF_REFERENCE + variable_list + ",'" + v_name + "', " \
         + str(data_info[1]) + ", '" + data_info[0] + "','" + current_line.highest_var_name + "','" + current_line.redefines + "'," + str(occurs_length) + "," \
            + str(data_info[2]) + ",'" + data_info[3] + "','" + tokens[0] + "','" + index_var + "'," + is_top_redefines + ")[0]" + NEWLINE)
    if VALUE_CLAUSE in tokens:
        value_index = tokens.index(VALUE_CLAUSE) + 1
        if tokens[value_index] == IS_KEYWORD:
            value_index = tokens.index(VALUE_CLAUSE) + 2
        if value_index == len(tokens) - 1:
            init_val = tokens[value_index]
            var_init_list.append([COBOL_VERB_MOVE, init_val, EMPTY_STRING, v_name])
        else:
            for x in range(value_index, len(tokens) - 1):
                init_val = tokens[value_index]
                if init_val.startswith("X'"):
                    init_val = init_val.replace("X'", SINGLE_QUOTE + HEX_PREFIX)
                if init_val == LOW_VALUES_KEYWORD:
                    init_val = SINGLE_QUOTE + HEX_PREFIX + '00' + SINGLE_QUOTE
                if init_val == THRU_KEYWORD:
                    val = int(tokens[value_index - 1].replace(SINGLE_QUOTE, EMPTY_STRING)) + 1
                    end = int(tokens[value_index + 1].replace(SINGLE_QUOTE, EMPTY_STRING))
                    while val < end:
                        var_init_list.append([COBOL_VERB_MOVE, SINGLE_QUOTE + str(val) + SINGLE_QUOTE, EMPTY_STRING, v_name])
                        val = val + 1
                else:
                    var_init_list.append([COBOL_VERB_MOVE, init_val, EMPTY_STRING, v_name])
                value_index = value_index + 1

    if len(tokens) == 2:
        current_line.highest_var_name = tokens[1]
        current_line.highest_ws_level = int(tokens[0])

    current_line.cascade_data_type = cascade_data_type

def create_index_variables(vars, name: str):
    for var in vars:
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + var[3] + " = Add_Variable(" + SELF_REFERENCE + name + MEMORY + "," + SELF_REFERENCE + var[3] + ",'" + var[0] + "', " \
            + "10, '9','" + var[1] + "','',0,0,'','" + var[2] + "')[0]" + NEWLINE)

def allocate_variables(current_line: LexicalInfo, name: str):
    #for cs in current_line.sections_list:
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + "result = Allocate_Memory(" + SELF_REFERENCE + "_DataDivisionVars," + SELF_REFERENCE + name + MEMORY + ")" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + "_DataDivisionVars" + SPACE + EQUALS + SPACE + "result[0]" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + name + MEMORY + SPACE + EQUALS + SPACE + "result[1]" + NEWLINE)

def init_vars(name: str, args, current_line):
    global var_init_list
    level = current_line.level
    current_line.level = 2
    for vil in var_init_list:
        process_verb(vil, name, True, 2, args, current_line)
    current_line.level = level

def is_valid_verb(line: str, verb_list):
    for verb in verb_list:
        if line.startswith(verb):
            return True

    return False

def get_data_info(tokens):
    info = [ALPHANUMERIC_DATA_TYPE, 0]
    count = 0
    for t in tokens:
        if (t == PIC_CLAUSE):
            info = get_type_length(tokens, count)
            break
        elif (t == POINTER_CLAUSE):
            info = [POINTER_DATATYPE, 0, 0, EMPTY_STRING]
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

    comp_indicator = EMPTY_STRING

    if COMP_KEYWORD in tokens:
        comp_indicator = COMP_KEYWORD
    if COMP_1_KEYWORD in tokens:
        comp_indicator = COMP_1_KEYWORD
    if COMP_2_KEYWORD in tokens:
        comp_indicator = COMP_2_KEYWORD
    if COMP_3_KEYWORD in tokens:
        comp_indicator = COMP_3_KEYWORD
    if COMP_4_KEYWORD in tokens:
        comp_indicator = COMP_4_KEYWORD
    if COMP_5_KEYWORD in tokens:
        comp_indicator = COMP_5_KEYWORD

    return [type_length[0], length, decimal_length, comp_indicator]

def insert_copybook(outfile, copybook, current_line, name, current_section, next_few_lines, args):
    current_line.skip_the_next_lines = 0
    is_eib = False
    if copybook == EIB_COPYBOOK:
        is_eib = True
    replace_info = [copybook, EMPTY_STRING, EMPTY_STRING, EMPTY_STRING]
    replacement_list = []
    if REPLACING_KEYWORD in copybook:
        replace_info = copybook.split(REPLACING_DELIMITER)
        copybook = replace_info[0].replace(REPLACING_KEYWORD, EMPTY_STRING).strip()
        if replace_info[len(replace_info) - 1] != PERIOD:
            for next_line in next_few_lines:
                replace_info.append(next_line)
                if next_line.endswith(PERIOD):
                    break
        indices = [i for i in range(len(replace_info)) if BY_KEYWORD in replace_info[i]]
        for index in indices:
            count = index
            found = False
            s = replace_info[count].split(BY_KEYWORD)
            replacement_list.append(Replacement())
            last = len(replacement_list) - 1
            if s[0].strip() != EMPTY_STRING:
                replacement_list[last].old_value = s[0].strip().replace("==.", EMPTY_STRING).replace("==", EMPTY_STRING)
            while not found:                
                if replace_info[count].strip().startswith("==") or replace_info[count].endswith("==."):
                    if count != index:
                        t = replace_info[count].replace("==.", EMPTY_STRING).strip()
                        t = t.replace("==", EMPTY_STRING)
                        replacement_list[last].old_value = t + NEWLINE + replacement_list[last].old_value
                    found = True
                else:
                    if count != index:
                        t = replace_info[count].replace("==.", EMPTY_STRING).strip()
                        t = t.replace("==", EMPTY_STRING)
                        replacement_list[last].old_value = t + NEWLINE + replacement_list[last].old_value
                    count = count - 1
                    if count < 0:
                        count = 0

            replacement_list[last].old_value = replacement_list[last].old_value.strip()
            count = index
            found = False
            if s[1].strip() != EMPTY_STRING:
                replacement_list[last].new_value = s[1].strip().replace("==.", EMPTY_STRING).replace("==", EMPTY_STRING)
            while not found:
                if replace_info[count].strip().endswith("==") or replace_info[count].endswith("==."):
                    if count != index:
                        t = replace_info[count].replace("==.", EMPTY_STRING).strip()
                        t = t.replace("==", EMPTY_STRING)
                        replacement_list[last].new_value = replacement_list[last].new_value + NEWLINE + t
                    found = True
                else:
                    if count != index:
                        t = replace_info[count].replace("==.", EMPTY_STRING).strip()
                        t = t.replace("==", EMPTY_STRING)
                        replacement_list[last].new_value = replacement_list[last].new_value + NEWLINE + t
                    count = count + 1
                    if count > len(replace_info) - 1:
                        count = len(replace_info) - 1
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

    file_lines = read_file(copybook, True)
    for repl in replacement_list:
        file_lines = file_lines.replace(repl.old_value, repl.new_value)

    write_file("temp_cpybook.txt", file_lines)
    raw_lines = read_raw_file_lines("temp_cpybook.txt", 0)
    
    append_file(outfile, "# Inserted Copybook: " + copybook + NEWLINE)
    total = len(raw_lines)
    count = 0
    skip_the_next_lines_count = 0
    for line in raw_lines:
        line = "      " + line
        count = count + 1
        next_few_lines_count = LINES_AHEAD
        lines_left = total - count
        if lines_left < 0:
            while lines_left < 0:
                lines_left = lines_left - 1
            next_few_lines_count = lines_left
        next_few_lines = raw_lines[count:count+next_few_lines_count]
        count2 = 0
        for nfl in next_few_lines:
            next_few_lines[count2] = "      " + next_few_lines[count2]
            count2 = count2 + 1
        if skip_the_next_lines_count == current_line.skip_the_next_lines:
            skip_the_next_lines_count = 0
            current_line.skip_the_next_lines = 0
        else:
            skip_the_next_lines_count = skip_the_next_lines_count + 1
            continue
        line = line[6:].strip()
        if line == EMPTY_STRING:
            continue
        if line != EMPTY_STRING and line.startswith(COBOL_COMMENT) == False:
            create_variable(line, current_line, name, current_section, next_few_lines, args, is_eib)
    current_line.skip_the_next_lines = 0
    append_file(outfile, NEWLINE)
    append_file(outfile, NEWLINE)
    delete_file("temp_cpybook.txt")

    return