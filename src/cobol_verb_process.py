from cobol_lexicon import *
from util import *

last_cmd_display = False
evaluate_compare = EMPTY_STRING
evaluate_compare_stack = []
nested_above_evaluate_compare = EMPTY_STRING
is_evaluating = False
is_first_when = True

def process_verb(tokens, name: str, indent: bool, level: int, args, current_line: LexicalInfo):
    global last_cmd_display, evaluate_compare, is_evaluating, evaluate_compare_stack, nested_above_evaluate_compare, is_first_when
    level = close_out_evaluate(tokens[0], name, level)
    
    if last_cmd_display == True:
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + "Display_Variable(" + VARIABLES_LIST_NAME + ",'','literal',True,True)" + NEWLINE)
        last_cmd_display = False

    if tokens[0] == STOP_KEYWORD:
        if len(tokens) > 1:
            if tokens[1] == RUN_KEYWORD:
                tokens[0] = tokens[0] + SPACE + RUN_KEYWORD

    if tokens[0] == VERB_RESET:
        last_cmd_display = False
        
    elif tokens[0] in COBOL_END_BLOCK_VERBS:
        if tokens[0] != COBOL_VERB_READ_END:
            level = level - 1
            if tokens[0] == COBOL_VERB_PERFORM_END:
                x = 0
        if len(evaluate_compare_stack) > 0:
            evaluate_compare_stack.pop()
            if len(evaluate_compare_stack) > 0:
                ec = evaluate_compare_stack[len(evaluate_compare_stack) - 1]
                evaluate_compare = ec[0]
                nested_above_evaluate_compare = ec[1]
        last_cmd_display = False
    elif tokens[0] == COBOL_VERB_MOVE:
        process_move_verb(tokens, name, indent, level)
        last_cmd_display = False
    elif tokens[0] == COBOL_VERB_SET:
        process_move_verb([COBOL_VERB_MOVE, tokens[3], tokens[2], tokens[1]], name, indent, level)
        last_cmd_display = False
    elif tokens[0] == COBOL_VERB_DISPLAY:
        process_display_verb(tokens, name, level)
        last_cmd_display = True
    elif tokens[0] == COBOL_VERB_ADD:
        process_add_verb(tokens, name, level)
        last_cmd_display = False
    elif tokens[0] == COBOL_VERB_GOBACK or tokens[0] == COBOL_VERB_STOPRUN or tokens[0] == COBOL_VERB_EXIT:

        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + "return")

        if tokens[0] == COBOL_VERB_GOBACK or tokens[0] == COBOL_VERB_STOPRUN:
            level = 1
            append_file(name + PYTHON_EXT, SPACE + OPEN_BRACKET)
            c = 0
            for a in args:
                if c > 3:
                    append_file(name + PYTHON_EXT, COMMA + SPACE)               
                if c > 2:
                    append_file(name + PYTHON_EXT, "Get_Variable_Value(" + VARIABLES_LIST_NAME + ",'" + a + "','" + a + "')")
                c = c + 1

            append_file(name + PYTHON_EXT, CLOSE_BRACKET)

        append_file(name + PYTHON_EXT, NEWLINE)
        
    elif tokens[0] == COBOL_VERB_PERFORM:
        level = process_perform_verb(tokens, name, level)
    elif tokens[0] == COBOL_VERB_IF:
        level = process_if_verb(tokens, name, level, False)
    elif tokens[0] == COBOL_VERB_ELSE:
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level - 1)) + ELSE + COLON + NEWLINE)
    elif len(tokens) == 2 and tokens[1] == PERIOD:
        level = 0
        func_name = tokens[0].replace(PERIOD, EMPTY_STRING).replace(DASH, UNDERSCORE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + DEF_KEYWORD + SPACE + func_name + OPEN_PARENS + CLOSE_PARENS + COLON + NEWLINE)
        level = level + 1
        last_cmd_display = False
    elif tokens[0] == COBOL_VERB_EVALUATE:
        is_first_when = True
        evaluate_compare = tokens[1]
        if tokens[1] == TRUE_KEYWORD or tokens[1] == FALSE_KEYWORD:
            evaluate_compare = EMPTY_STRING
        evaluate_compare_stack.append([evaluate_compare, evaluate_compare])
        level = level + 1
    elif tokens[0] == COBOL_VERB_WHEN:
        if tokens[1] == WHEN_OTHER_KEYWORD:
            append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + ELSE + COLON + NEWLINE)
            level = level + 1
        else:
            level = level - 1
            process_evaluate_verb(tokens, name, level)  
            level = level + 1
    elif tokens[0] == COBOL_VERB_INSPECT:
        process_inspect_verb(tokens, name, level) 
    elif tokens[0] == COBOL_VERB_CONTINUE:
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "x = 0" + NEWLINE)
    elif tokens[0] == COBOL_VERB_OPEN:
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "Open_File(" + VARIABLES_LIST_NAME + ", _FILE_CONTROLVars, '" + tokens[2] + "','" + tokens[1] + "')" + NEWLINE)
    elif tokens[0] == COBOL_VERB_CLOSE:
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "Close_File(_FILE_CONTROLVars, '" + tokens[1] + "')" + NEWLINE)
    elif tokens[0] == COBOL_VERB_READ:
        at_end_clause = EMPTY_STRING
        
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "read_result = Read_File(_FILE_CONTROLVars, _FILE_SECTIONVars, '" + tokens[1] + "','" + at_end_clause + "')" + NEWLINE)
        if len(tokens) > 3:
            if tokens[2] == AT_KEYWORD and tokens[3] == END_KEYWORD:
                append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "if read_result == True:" + NEWLINE)
                process_move_verb(tokens[4:], name, True, level + 1)
    elif tokens[0] == COBOL_VERB_WRITE:
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "Write_File(_FILE_CONTROLVars, _FILE_SECTIONVars, '" + tokens[1] + "')" + NEWLINE)
    elif tokens[0] == COBOL_VERB_CALL:
        process_call_verb(tokens, name, indent, level, args, current_line)
    elif tokens[0] == COBOL_VERB_SEARCH:
        last_cmd_display = False
        process_search_verb(tokens, name, indent, level, args, current_line)
        level = level + 1
    
    return level

def process_search_verb(tokens, name: str, indent: bool, level: int, args, current_line: LexicalInfo):
    all_offset = 0
    if tokens[1] == ALL_KEYWORD:
        all_offset = all_offset + 1

    condition_index = tokens.index(COBOL_VERB_WHEN)

    end_index = 0

    if AT_KEYWORD in tokens and END_KEYWORD in tokens:
        end_index = tokens.index(END_KEYWORD)

    at_end_func = 'None'
    if end_index > 0:
        at_end_slice = tokens[end_index + 1: condition_index]
        current_line.lambda_functions.append(at_end_slice)
        at_end_func = "_ae" + str(len(current_line.lambda_functions))

    operand2 = tokens[condition_index + 3]

    if operand2.isnumeric() == False:
        if operand2.startswith(SINGLE_QUOTE) == False:
            temp = "Get_Variable_Value(" + VARIABLES_LIST_NAME + ",'" + operand2 + "','" + operand2 + SINGLE_QUOTE + CLOSE_PARENS
            operand2 = temp

    append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "if Search_Variable_Array(" + VARIABLES_LIST_NAME + ",'" + tokens[condition_index + 1] \
        + "','" + convert_operator(tokens[condition_index + 2]) + "'," + operand2 + "," + str(all_offset) + ","  + at_end_func + CLOSE_PARENS + COLON + NEWLINE)

def process_call_verb(tokens, name: str, indent: bool, level: int, args, current_line: LexicalInfo):
    using_args = EMPTY_STRING
    params = []
    if (len(tokens) > 2 and tokens[2] == USING_KEYWORD):
        params = parse_line_tokens(tokens[3], COMMA, EMPTY_STRING, False)
        param_count = 0
        for param in params:
            if param_count > 0:
                using_args = using_args + COMMA
            param_count = param_count + 1
            using_args = using_args + "Get_Variable_Value(" + VARIABLES_LIST_NAME + ",'" + param + "','" + param + "')"

    current_line.import_statement.append(tokens[1].replace(SINGLE_QUOTE, EMPTY_STRING))
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "call_result = main_" + tokens[1].replace(SINGLE_QUOTE, EMPTY_STRING) + OPEN_PARENS)
    append_file(name + PYTHON_EXT, using_args)
    append_file(name + PYTHON_EXT, CLOSE_PARENS + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "if call_result != None:" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (level + 1)) + "for cr in call_result:" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (level + 2)) + "x = 0" + NEWLINE)
    for param in params:
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level + 2)) + "Set_Variable(" + VARIABLES_LIST_NAME + ",'" + param + "', cr ,'" + param + "')" + NEWLINE)

def process_inspect_verb(tokens, name: str, level: int):
    if tokens[2] == CONVERTING_KEYWORD:
        func = "Replace_Variable_Value(" + VARIABLES_LIST_NAME + ", '" + tokens[1] + "'," + tokens[3] + ", " + tokens[5] + CLOSE_PARENS
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + func + NEWLINE)

def close_out_evaluate(verb: str, name: str, level: int):
    global is_evaluating
    if verb == COBOL_VERB_WHEN:
        return level

    if is_evaluating:
        append_file(name + PYTHON_EXT, COLON + NEWLINE)

    is_evaluating = False

    return level
    
def process_evaluate_verb(tokens, name: str, level: int):
    global evaluate_compare, is_evaluating, evaluate_compare_stack, nested_above_evaluate_compare, is_first_when

    reset_evaluate_compare = False
    operator = EQUALS
    if len(tokens) > 2:
        operator = tokens[2]
        operator_offset = 0
        if tokens[2] == NOT_KEYWORD:
            operator = NOT_EQUALS
            operator_offset = 1

    operand2 = tokens[1]
    if evaluate_compare == EMPTY_STRING:
        evaluate_compare_stack[len(evaluate_compare_stack) - 1] = [evaluate_compare, tokens[1]]
        nested_above_evaluate_compare = tokens[1]
        evaluate_compare = tokens[1]
        reset_evaluate_compare = True
        if len(tokens) > operator_offset + 3:
            operand2 = tokens[operator_offset + 3]
        elif len(tokens) == 3:
            if tokens[2].startswith(SINGLE_QUOTE):
                operand2 = tokens[2]
            else:
                operand2 = "Get_Variable_Value(" + VARIABLES_LIST_NAME + ",'" + tokens[2] + "','" + tokens[2] + "')"
            operator = SPACE + IN_KEYWORD + SPACE

    prefix = "if "
    if is_first_when == False:
        prefix = "elif "
    else:
        is_first_when = False
    indent_len = len(INDENT) * level

    if is_evaluating:
        prefix = " or "
        indent_len = 0
    else:
        is_evaluating = True

    operand1 = "Get_Variable_Value(" + VARIABLES_LIST_NAME + ",'" + evaluate_compare + "','" + evaluate_compare + "') "
    line = prefix + operand1 + convert_operator(operator) + SPACE + operand2

    append_file(name + PYTHON_EXT, pad(indent_len) + line)

    if reset_evaluate_compare:
        evaluate_compare = EMPTY_STRING

    return level

def process_if_verb(tokens, name: str, level: int, is_elif: bool):
    line = "if "
    if is_elif:
        line = "elif "

    count = 0
    checking_function = False
    opposite_operator = False
    in_ALL_function = False
    slice_length = 0
    num_spaces = len(INDENT) * level
    for token in tokens:
        if count == 0:
            count = count + 1
            continue
        if token in COBOL_VERB_LIST or token == PERIOD or token == NUMERIC_KEYWORD:
            continue
        count = count + 1
        need_closed_parens = False
        slice_compare = EMPTY_STRING
        if len(tokens) > count:
            if tokens[count] == NUMERIC_KEYWORD:
                line = line + "Check_Value_Numeric("
                checking_function = True
        if OPEN_PARENS in token and CLOSE_PARENS in token and COLON in token:
            s = token.split(OPEN_PARENS)
            token = s[0]
            positions = s[1].replace(CLOSE_PARENS, EMPTY_STRING).split(COLON)
            slice_length = int(positions[0]) -1 + int(positions[1])
            slice_compare = OPEN_BRACKET + str(int(positions[0]) - 1) + COLON + str(slice_length) + CLOSE_BRACKET
        elif OPEN_PARENS in token and CLOSE_PARENS in token:
            i = 0
        else:
            if token.startswith(OPEN_PARENS):
                line = line + OPEN_PARENS
            token = token.replace(OPEN_PARENS, EMPTY_STRING)

            if token.endswith(CLOSE_PARENS):
                need_closed_parens = True
                token = token.replace(CLOSE_PARENS, EMPTY_STRING)

        if token.startswith(SINGLE_QUOTE):
            if in_ALL_function:
                in_ALL_function = False
            else:
                line = line + token + SPACE

        elif token.replace(PLUS_SIGN, EMPTY_STRING).isnumeric():
            line = line + token + SPACE
        elif token == NOT_KEYWORD:
            opposite_operator = True
        elif token == ALL_KEYWORD:
            line = line + "pad_char(" + str(slice_length) + COMMA + tokens[count + 1] + CLOSE_PARENS
            in_ALL_function = True
        elif token == ZERO_KEYWORD:
            line = line + "pad_char(" + str(slice_length) + COMMA + SINGLE_QUOTE + ZERO + SINGLE_QUOTE + CLOSE_PARENS
        elif is_operator(token):
            if opposite_operator:
                line = line + SPACE + convert_operator_opposite(token) + SPACE
            else:
                line = line + SPACE + convert_operator(token) + SPACE
            opposite_operator = False
        elif is_boolean_keyword(token):
            line = line + token.lower() + SPACE
        elif token == SPACE_KEYWORD:
            line = line + "Get_Spaces(Get_Variable_Length(" + VARIABLES_LIST_NAME + ", '" + tokens[1] + "'))" + SPACE
        else:
            line = line + "Get_Variable_Value(" + VARIABLES_LIST_NAME + ",'" + token + "','" + token + SINGLE_QUOTE + CLOSE_PARENS + SPACE

        line = line + slice_compare
        if checking_function:
            checking_function = False
            line = line + CLOSE_PARENS + SPACE
        if need_closed_parens:
            line = line + CLOSE_PARENS + SPACE

    line = line + COLON + NEWLINE

    append_file(name + PYTHON_EXT, pad(num_spaces) + line)

    return level + 1

def process_perform_verb(tokens, name: str, level: int):
    if VARYING_KEYWORD in tokens:
        process_varying_loop(tokens, name, level)
        level = level + 1
    elif len(tokens) == 3 or THROUGH_KEYWORD in tokens or THRU_KEYWORD in tokens:
        func_name = tokens[1].replace(PERIOD, EMPTY_STRING).replace(DASH, UNDERSCORE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + func_name + OPEN_PARENS + CLOSE_PARENS + NEWLINE)
        if THROUGH_KEYWORD in tokens or THRU_KEYWORD in tokens:
            func_name = tokens[3].replace(PERIOD, EMPTY_STRING).replace(DASH, UNDERSCORE)
            append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + func_name + OPEN_PARENS + CLOSE_PARENS + NEWLINE)
    else:
        if tokens[1] == UNTIL_KEYWORD:
            operand2 = tokens[4]
            if tokens[4].startswith(SINGLE_QUOTE) == False:
                operand2 = "Get_Variable_Value(" + VARIABLES_LIST_NAME + ",'" + tokens[4] + "','" + tokens[4] + "')"
            append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + "while Get_Variable_Value(" + VARIABLES_LIST_NAME + ",'" + tokens[2] + "','" + tokens[2] + "') " \
                + convert_operator_opposite(tokens[3]) + operand2 + COLON + NEWLINE)
            level = level + 1

    return level

def process_varying_loop(tokens, name: str, level: int):
    from_index = tokens.index(FROM_KEYWORD)
    varying_index = tokens.index(VARYING_KEYWORD)
    until_index = tokens.index(UNTIL_KEYWORD)
    by_index = tokens.index(BY_KEYWORD)
    or_indices = get_all_indices(tokens, OR_KEYWORD)

    process_move_verb([COBOL_VERB_MOVE, tokens[from_index + 1], TO_KEYWORD, tokens[varying_index + 1]], name, True, level)
    line = "while Get_Variable_Value(" + VARIABLES_LIST_NAME + ",'" + tokens[varying_index + 1] + "','" + tokens[varying_index + 1] + SINGLE_QUOTE + CLOSE_PARENS + SPACE \
        + convert_operator_opposite(tokens[until_index + 2]) + SPACE + tokens[until_index + 3]

    append_file(name + PYTHON_EXT, INDENT + line)
    for or_index in or_indices:
        # convert the 'or' to 'and' because we used the opposite operator above
        operand1 = tokens[or_index + 1]
        sub_string = EMPTY_STRING
        if OPEN_PARENS in operand1:
            temp_operands = operand1.split(OPEN_PARENS)
            operand1 = temp_operands[0]
            operand_slice = temp_operands[1].replace(CLOSE_PARENS, EMPTY_STRING).split(COLON)
            start_slice = operand_slice[0]
            if start_slice.replace(PLUS_SIGN, EMPTY_STRING).isnumeric() == False:
                start_slice = "Get_Variable_Value(" + VARIABLES_LIST_NAME + ",'" + start_slice + "','" + start_slice + "')-1"
            end_slice = operand_slice[1]
            if end_slice.replace(PLUS_SIGN, EMPTY_STRING).isnumeric() == False:
                end_slice = "Get_Variable_Value(" + VARIABLES_LIST_NAME + ",'" + end_slice + "','" + end_slice + "')"
            sub_string = OPEN_BRACKET + start_slice + COLON + start_slice + PLUS_SIGN + end_slice + CLOSE_BRACKET
        line = "\\" + NEWLINE + " and Get_Variable_Value(" + VARIABLES_LIST_NAME + ",'" + operand1 + "','" + operand1 + SINGLE_QUOTE + CLOSE_PARENS + sub_string
        offset = 2
        if tokens[or_index + 2] == NOT_KEYWORD:
            line = line + SPACE + convert_operator(tokens[or_index + 3])
            offset = 3
        elif tokens[or_index + 2].startswith(OPEN_PARENS):
            offset = 3
            temp = tokens[or_index + 2].replace(OPEN_PARENS, EMPTY_STRING).replace(CLOSE_PARENS, EMPTY_STRING)
            split = temp.split(COLON)
            t = "[Get_Variable_Value(" + VARIABLES_LIST_NAME + ",'" + split[0] + "','" + split[0] + "')-1" + COLON + "Get_Variable_Value(" + VARIABLES_LIST_NAME + ",'" + split[0] + "','" + split[0] + "') + " + split[1] + "-1]"
            line = line + t + SPACE
        else:
            line = line + SPACE + tokens[or_index + 2] + SPACE
        line = line + convert_operator(tokens[or_index + offset + 1])
        if tokens[or_index + offset + 2] not in COBOL_VERB_LIST and tokens[or_index + offset + 2] != PERIOD:
            line = line + tokens[or_index + offset + 2]
        append_file(name + PYTHON_EXT, INDENT + INDENT + line)
    append_file(name + PYTHON_EXT, COLON + NEWLINE)
    append_file(name + PYTHON_EXT, INDENT + INDENT + "Update_Variable(" + VARIABLES_LIST_NAME + ",'" \
        + tokens[by_index + 1] + "','" + tokens[varying_index + 1] + "','" + tokens[varying_index + 1] + SINGLE_QUOTE + CLOSE_PARENS + NEWLINE)

def process_move_verb(tokens, name: str, indent: bool, level: int):
    do_indent = pad(len(INDENT) * level)

    if not indent:
        do_indent = EMPTY_STRING

    value = tokens[1]
    if value == SPACE_KEYWORD:
        value = SINGLE_QUOTE + SPACES_INITIALIZER + SINGLE_QUOTE
    elif value == ZERO_KEYWORD:
        value = ZERO

    target_offset = 3

    if value.startswith(SINGLE_QUOTE) == False and value.startswith(MAIN_ARG_VARIABLE_PREFIX) == False:
        if OPEN_PARENS in value:
            s = value.split(OPEN_PARENS)
            s1 = s[1].split(COLON)
            get_var_value = "Get_Variable_Value(variables_list,'" + s[0] + "','" + s[0] + "')"
            end = s1[1].replace(CLOSE_PARENS, EMPTY_STRING)
            end_offset = s1[0]
            if s1[0].isnumeric() == False:
                end_offset = "Get_Variable_Value(variables_list,'" + s1[0] + "','" + s1[0] + "')"

            value = get_var_value + OPEN_BRACKET + end_offset + "- 1" + COLON + end_offset + " - 1 + " + end + CLOSE_BRACKET
        elif value == FUNCTION_KEYWORD:
            value = "Exec_Function('" + tokens[2] + "')"
            target_offset = 4
        elif value.replace(PLUS_SIGN, EMPTY_STRING).isnumeric() == False:
            value = "Get_Variable_Value(variables_list,'" + value + "','" + value + "')"
    elif value.startswith(SINGLE_QUOTE):
        x = 0

    target = tokens[target_offset].replace(PERIOD, EMPTY_STRING)

    append_file(name + PYTHON_EXT, do_indent + "Set_Variable(" + VARIABLES_LIST_NAME + ",'" + target + "', " + value + ",'" + target + "')" + NEWLINE)

    if len(tokens) > 1 + target_offset and tokens[1 + target_offset] != PERIOD and tokens[1 + target_offset] != NEG_ONE and tokens[1 + target_offset] not in COBOL_END_BLOCK_VERBS and tokens[1 + target_offset] not in COBOL_VERB_LIST:
        limit = len(tokens)
        for x in range(4, limit):
            tokens[x - 1] = tokens[x]
        tokens.pop()
        process_move_verb(tokens, name, indent, level)


def process_display_verb(tokens, name: str, level: int):
    count = 0
    for t in tokens:
        t = str(t)
        if t == PERIOD:
            continue
        if count > 0:
            if tokens[count] in COBOL_VERB_LIST:
                break

            is_literal = False
            if t.endswith(PERIOD):
                is_literal = True
            t = t.replace(PERIOD, EMPTY_STRING)
            parent = t
            if (t.startswith(SINGLE_QUOTE) and t.endswith(SINGLE_QUOTE)) or t == EMPTY_STRING:
                t = t.replace(SINGLE_QUOTE, EMPTY_STRING)
                parent = LITERAL
            append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + "Display_Variable(" + VARIABLES_LIST_NAME + ",'" + t + "','" + parent + "'," + str(is_literal) + ",False)" + NEWLINE)
        count = count + 1

def process_add_verb(tokens, name: str, level: int):
    giving = tokens[3]
    if GIVING_KEYWORD in tokens:
        giving = tokens[5]
    append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + "Update_Variable(" + VARIABLES_LIST_NAME + ",'" + tokens[1] + "', '" + tokens[3] + "', '" + giving + "')" + NEWLINE)
    

def check_valid_verb(v: str, compare_verb: str):
    for multi_verb in COBOL_VERB_MULTI_LIST:
        if multi_verb[0] == compare_verb and multi_verb[1] == v:
            return False

    if v in COBOL_VERB_LIST:
        return True
    
    return False

def convert_operator_opposite(operator: str):
    if operator == LESS_THAN:
        return GREATER_THAN_EQUAL_TO
    if operator == EQUALS:
        return NOT_EQUALS

    return operator

def convert_operator(operator: str):
    if operator == EQUALS:
        return DOUBLE_EQUALS
    
    return operator

def is_operator(operator: str):
    return operator in COBOL_OPERATORS

def is_boolean_keyword(boolean: str):
    return boolean in COBOL_BOOLEAN_KEYWORDS