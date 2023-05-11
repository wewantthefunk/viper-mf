from cobol_lexicon import *
from util import *
from cobol_verb_process import *
from cobol_util import *

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
    if tokens[len(tokens) - 1] != PERIOD:
        for next_line in next_few_lines:
            nl_tokens = parse_line_tokens(next_line, SPACE, EMPTY_STRING, True)
            if nl_tokens[len(nl_tokens) - 1].endswith(PERIOD) and nl_tokens[len(nl_tokens) - 1] != PERIOD:
                nl_tokens[len(nl_tokens) - 1] = nl_tokens[len(nl_tokens) - 1][0:len(nl_tokens[len(nl_tokens) - 1]) - 1]
                nl_tokens.append(PERIOD)
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
        elif (token == FILE_KEYWORD and tokens[count + 1] == STATUS_KEYWORD): 
            file_status = tokens[count + 2]
            if tokens[count + 2] == IS_KEYWORD:
                file_status = tokens[count + 3]
        elif token == STATUS_KEYWORD:
            file_status = tokens[count + 1]
            if tokens[count + 1] == IS_KEYWORD:
                file_status = tokens[count + 2]
        count = count + 1

    if assign.startswith("S-"):
        assign = assign[len("S-"):]

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
    else:
        tokens = parse_line_tokens(line, SPACE, EMPTY_STRING, True)
        if line.startswith(FD_KEYWORD) or line.startswith(SD_KEYWORD):
            data_division_file_record = tokens[1]
            if line.startswith(SD_KEYWORD):
                data_division_file_record = data_division_file_record + SORT_IDENTIFIER
        elif line.startswith(COPYBOOK_KEYWORD):
            insert_copybook(name + PYTHON_EXT, line.replace(COPYBOOK_KEYWORD, EMPTY_STRING).replace(PERIOD, EMPTY_STRING).strip(), current_line, name, current_section, next_few_lines, args)
        else:
            if line[0:2].isnumeric() == False:
                return [line, current_section, name, current_line]

            create_variable(line, current_line, name, current_section, next_few_lines, args)

            if data_division_file_record != EMPTY_STRING and tokens[0].isnumeric():
                fr = tokens[1]
                if len(data_division_var_stack) > 0:
                    fr = data_division_var_stack[0]
                append_file(name + PYTHON_EXT, "# this is where we will associate the record " + tokens[1] + " to the file " + data_division_file_record + NEWLINE)
                append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + "self._FILE_CONTROLVars = Set_File_Record(self._FILE_CONTROLVars, '" + data_division_file_record + "','" + fr + "')" + NEWLINE)
                data_division_file_record = EMPTY_STRING
    
    return [line, current_section, name, current_line]

def process_procedure_division_line(line: str, name: str, current_line: LexicalInfo, next_few_lines, args):
    temp_tokens = parse_line_tokens(line, SPACE, EMPTY_STRING, True)

    skip = 0
    level = current_line.level

    if temp_tokens[0] == COBOL_VERB_SEARCH or temp_tokens[0] == COBOL_RETURN_KEYWORD:
        current_line.end_of_search_criteria = True

    if temp_tokens[len(temp_tokens) - 1] == PERIOD:
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + SELF_REFERENCE + "debug_line = '" + current_line.current_line_number + "'" + NEWLINE)
        fix_parens(temp_tokens, temp_tokens[0], temp_tokens[len(temp_tokens) - 1])
        level = process_verb(temp_tokens, name, True, level, args, current_line, next_few_lines)
    else:
        compare_verb = temp_tokens[0]
        for nl in next_few_lines:
            nll = nl.split("^^^")
            nllt = nll[0]
            
            nlt = parse_line_tokens(nllt[6:], SPACE, EMPTY_STRING, True)
            if len(nlt) == 0:
                continue            
            if nlt[0] == COBOL_RETURN_KEYWORD:
                current_line.end_of_search_criteria = True
                compare_verb = COBOL_RETURN_KEYWORD

            if (check_valid_verb(nlt[0], compare_verb, current_line.end_of_search_criteria) or nlt[len(nlt) - 1] == PERIOD or (compare_verb == COBOL_RETURN_KEYWORD and (nlt[0] == NOT_KEYWORD and (nlt[1] == END_KEYWORD or nlt[2] == END_KEYWORD)))):
                if nlt[len(nlt) - 1] == PERIOD:
                    for t in nlt:
                        temp_tokens.append(t)
                    if check_valid_verb(nlt[0], compare_verb, current_line.end_of_search_criteria) == False:
                        skip = skip + 1

                if temp_tokens[0] != COBOL_VERB_WHEN and current_line.is_evaluating == False:
                    append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + SELF_REFERENCE + "debug_line = '" + current_line.current_line_number + "'" + NEWLINE)
                level = process_verb(temp_tokens, name, True, level, args, current_line, next_few_lines)
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
    return

def check_ignore_verbs(ignore_verbs, v: str):
    if len(ignore_verbs) == 0:
        return True

    return v in ignore_verbs

def create_variable(line: str, current_line: LexicalInfo, name: str, current_section: str, next_few_lines, args, is_eib = False):
    global data_division_var_stack, data_division_level_stack, var_init_list, data_division_cascade_stack, data_division_redefines_stack

    tokens = parse_line_tokens(line, SPACE, EMPTY_STRING, False)
    if len(tokens) == 0:
        return

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
            if nl[7:].startswith(COBOL_COMMENT):
                continue
            nlt = parse_line_tokens(nl[7:].replace(NEWLINE, EMPTY_STRING), SPACE, EMPTY_STRING, True)
            
            if len(nlt) == 0:
                continue

            if nlt[len(nlt) - 1].endswith(PERIOD) and nlt[len(nlt) - 1] != PERIOD:
                nlt[len(nlt) - 1] = nlt[len(nlt) - 1][0:len(nlt[len(nlt) - 1]) - 1]
                nlt.append(PERIOD)

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

    display_mask = EMPTY_STRING
    if "Z" in data_info[0] or COMMA in data_info[0]:
        display_mask = data_info[0]
        if data_info[0].startswith(DASH) or data_info[0].endswith(DASH):
            data_info[0] = NUMERIC_SIGNED_DATATYPE
        else:
            data_info[0] = NUMERIC_DATATYPE

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
    pic_clause_override = False
    if v_name == PIC_CLAUSE or v_name == "SYNC" or v_name in COMP_FIELD_TYPES:
        current_line.highest_var_name_subs = current_line.highest_var_name_subs + 1
        v_name = current_line.highest_var_name + "-SUB-" + str(current_line.highest_var_name_subs)
        pic_clause_override = True
    
    memory_name = SELF_REFERENCE + name + MEMORY 
    variable_list = "_DataDivisionVars"
    if is_eib:
        memory_name = SELF_REFERENCE + EIB_MEMORY 
        variable_list = EIB_VARIABLE_LIST
    append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + variable_list + " = Add_Variable(" + memory_name + "," + SELF_REFERENCE + variable_list + ",'" + v_name + "', " \
         + str(data_info[1]) + ", '" + data_info[0] + "','" + current_line.highest_var_name + "','" + current_line.redefines + "'," + str(occurs_length) + "," \
            + str(data_info[2]) + ",'" + data_info[3] + "','" + tokens[0] + "','" + index_var + "'," + is_top_redefines \
            + ",'" + display_mask + "')[0]" + NEWLINE)
    
    if pic_clause_override:
        current_line.highest_var_name = v_name
        data_division_var_stack[len(data_division_var_stack) - 1] = v_name

    if VALUE_CLAUSE in tokens or VALUES_CLAUSE in tokens or current_line.cascade_init_value != EMPTY_STRING:
        if current_line.cascade_init_value != EMPTY_STRING and tokens[0] != '88':
            value_index = 0
            init_val = current_line.cascade_init_value
        else:
            i = -1
            if VALUE_CLAUSE in tokens:
                i = tokens.index(VALUE_CLAUSE)
            elif VALUES_CLAUSE in tokens:
                i = tokens.index(VALUES_CLAUSE)
            value_index = i + 1
        if tokens[value_index] == IS_KEYWORD:
            value_index = tokens.index(VALUE_CLAUSE) + 2
        if value_index == len(tokens) - 1:
            init_val = tokens[value_index]
            var_init_list.append([COBOL_VERB_MOVE, init_val, EMPTY_STRING, v_name])
        else:
            for x in range(value_index, len(tokens) - 1):
                init_val = tokens[value_index].strip()
                if init_val.endswith(PERIOD):
                    init_val = init_val[0:len(init_val) - 1]
                if init_val.startswith(COBOL_COMMENT):
                    continue
                if init_val.startswith("X'"):
                    init_val = init_val.replace("X'", SINGLE_QUOTE + HEX_PREFIX)
                if init_val == LOW_VALUES_KEYWORD:
                    init_val = SINGLE_QUOTE + HEX_PREFIX + '00' + SINGLE_QUOTE
                if init_val == HIGH_VALUES_KEYWORD:
                    init_val = SINGLE_QUOTE + HEX_PREFIX + 'FF' + SINGLE_QUOTE
                if init_val == ALL_KEYWORD:
                    if int(data_info[1]) > 0:
                        init_val = SINGLE_QUOTE + pad_char(int(data_info[1]), tokens[value_index + 1].replace(SINGLE_QUOTE, EMPTY_STRING)) + SINGLE_QUOTE
                    else:
                        init_val = SINGLE_QUOTE + INIT_ALL_PREFIX + tokens[value_index + 1].replace(SINGLE_QUOTE, EMPTY_STRING) + SINGLE_QUOTE
                if init_val == THRU_KEYWORD:
                    is_hex = False
                    is_char = False
                    char_prefix = EMPTY_STRING
                    char_pad_len = 0
                    if tokens[value_index - 1].startswith("X'"):
                        val = int("0x" + tokens[value_index - 1].replace("X", EMPTY_STRING).replace(SINGLE_QUOTE, EMPTY_STRING), 16)
                        end = int("0x" + tokens[value_index + 1].replace("X", EMPTY_STRING).replace(SINGLE_QUOTE, EMPTY_STRING), 16)
                        is_hex = True
                    elif not tokens[value_index - 1].replace(SINGLE_QUOTE, EMPTY_STRING).isnumeric():
                        last_letter_index = find_pos_last_letter(tokens[value_index - 1].replace(SINGLE_QUOTE, EMPTY_STRING))
                        val = int(tokens[value_index - 1].replace(SINGLE_QUOTE, EMPTY_STRING)[last_letter_index:])
                        last_letter_index = find_pos_last_letter(tokens[value_index + 1].replace(SINGLE_QUOTE, EMPTY_STRING))
                        end = int(tokens[value_index + 1].replace(SINGLE_QUOTE, EMPTY_STRING)[last_letter_index:])
                        char_prefix = tokens[value_index + 1].replace(SINGLE_QUOTE, EMPTY_STRING)[0:last_letter_index]
                        char_pad_len = len(tokens[value_index - 1].replace(SINGLE_QUOTE, EMPTY_STRING)) - len(char_prefix) 
                        is_char = True
                    else:
                        val = int(tokens[value_index - 1].replace(SINGLE_QUOTE, EMPTY_STRING)) + 1
                        end = int(tokens[value_index + 1].replace(SINGLE_QUOTE, EMPTY_STRING))
                    while val < end:
                        if is_hex:
                            var_init_list.append([COBOL_VERB_MOVE, SINGLE_QUOTE + HEX_PREFIX + hex(val)[2:].upper() + SINGLE_QUOTE, EMPTY_STRING, v_name])
                        elif is_char:
                            var_init_list.append([COBOL_VERB_MOVE, SINGLE_QUOTE + char_prefix + pad_char(char_pad_len - len(str(val)), ZERO) + str(val) + SINGLE_QUOTE, EMPTY_STRING, v_name])
                        else:
                            var_init_list.append([COBOL_VERB_MOVE, SINGLE_QUOTE + str(val) + SINGLE_QUOTE, EMPTY_STRING, v_name])
                        
                        val = val + 1
                elif init_val == "SYNC" or init_val in COMP_FIELD_TYPES:
                    x = 0
                else:
                    var_init_list.append([COBOL_VERB_MOVE, init_val, EMPTY_STRING, v_name])
                value_index = value_index + 1

    if len(tokens) == 2:
        current_line.highest_var_name = tokens[1]
        current_line.highest_ws_level = int(tokens[0])

    current_line.cascade_data_type = cascade_data_type

    return

def create_index_variables(vars, name: str):
    for var in vars:
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + var[3] + " = Add_Variable(" + SELF_REFERENCE + name + MEMORY + "," + SELF_REFERENCE + var[3] + ",'" + var[0] + "', " \
            + "10, '9','" + var[1] + "','',0,0,'','" + var[2] + "')[0]" + NEWLINE)

def allocate_variables(current_line: LexicalInfo, name: str):
    append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + "result = Allocate_Memory(" + SELF_REFERENCE + "_DataDivisionVars," + SELF_REFERENCE + name + MEMORY + ")" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + "_DataDivisionVars" + SPACE + EQUALS + SPACE + "result[0]" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + name + MEMORY + SPACE + EQUALS + SPACE + "result[1]" + NEWLINE)

def init_vars(name: str, args, current_line):
    global var_init_list
    level = current_line.level
    current_line.level = 2
    for vil in var_init_list:
        process_verb(vil, name, True, 2, args, current_line, [])
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
    else:
        length = len(type_length[0])

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

def insert_copybook(outfile, copybook, current_line: LexicalInfo, name, current_section, next_few_lines, args):
    if "CIOCHMO" in copybook:
        x = 0
    result = prep_copybook(current_line, copybook, next_few_lines)

    lines = result[0]

    copybook_name = result[1]

    is_eib = False
    if copybook_name == EIB_COPYBOOK:
        is_eib = True

    if len(lines) > 0:
        append_file(outfile, "# Inserted Copybook: " + copybook_name + NEWLINE)

    total = len(lines)
    skip_the_next_lines_count = 0
    count = 0

    for line in lines:
        count = count + 1
        next_few_lines_count = LINES_AHEAD
        lines_left = total - count
        if lines_left < 0:
            while lines_left < 0:
                lines_left = lines_left - 1
            next_few_lines_count = lines_left
        next_few_lines = lines[count:count+next_few_lines_count]
        count2 = 0
        for nfl in next_few_lines:
            next_few_lines[count2] = "      " + next_few_lines[count2][6:]
            count2 = count2 + 1
        if skip_the_next_lines_count == current_line.skip_the_next_lines:
            skip_the_next_lines_count = 0
            current_line.skip_the_next_lines = 0
        else:
            skip_the_next_lines_count = skip_the_next_lines_count + 1
            continue
        create_variable(line, current_line, name, current_section, next_few_lines, args, is_eib)
    current_line.skip_the_next_lines = 0
    append_file(outfile, NEWLINE)
    append_file(outfile, NEWLINE)

    if is_eib:
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + "result = Allocate_Memory(self.EIBList,self.EIBMemory)\n")
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + "self.EIBList = result[0]\n")
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + "self.EIBMemory = result[1]\n")

    return