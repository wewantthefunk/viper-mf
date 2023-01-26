from cobol_lexicon import *
from util import *

last_cmd_display = False
evaluate_compare = EMPTY_STRING
evaluate_compare_stack = []
nested_above_evaluate_compare = EMPTY_STRING
is_evaluating = False
is_first_when = True
is_perform_looping = False

def process_verb(tokens, name: str, indent: bool, level: int, args, current_line: LexicalInfo):
    global last_cmd_display, evaluate_compare, is_evaluating, evaluate_compare_stack, nested_above_evaluate_compare, is_first_when
    level = close_out_evaluate(tokens[0], name, level)
    
    if last_cmd_display == True:
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + "Display_Variable(" + SELF_REFERENCE + name + MEMORY + "," + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'','literal',True,True)" + NEWLINE)
        last_cmd_display = False

    verb = tokens[0]

    if tokens[0] == EXEC_KEYWORD and tokens[1] == CICS_KEYWORD:
        verb = EXEC_KEYWORD + SPACE + CICS_KEYWORD + SPACE + tokens[2]
        if tokens[2] == HANDLE_KEYWORD:
            verb = verb + SPACE + tokens[3]

    if verb == STOP_KEYWORD:
        if len(tokens) > 1:
            if tokens[1] == RUN_KEYWORD:
                tokens[0] = tokens[0] + SPACE + RUN_KEYWORD

    if verb == VERB_RESET:
        last_cmd_display = False
        
    elif verb in COBOL_END_BLOCK_VERBS:
        if verb != COBOL_VERB_READ_END:
            if verb == COBOL_VERB_PERFORM_END:
                level = close_out_perform_loop(tokens[0], name, level, current_line)
            elif verb == COBOL_VERB_EXEC_END:
                x = 0
            else:
                level = level - 1
        if len(evaluate_compare_stack) > 0:
            evaluate_compare_stack.pop()
            if len(evaluate_compare_stack) > 0:
                ec = evaluate_compare_stack[len(evaluate_compare_stack) - 1]
                evaluate_compare = ec[0]
                nested_above_evaluate_compare = ec[1]
        last_cmd_display = False
    elif verb == COBOL_VERB_MOVE:
        process_move_verb(tokens, name, indent, level)
        last_cmd_display = False
    elif verb == COBOL_VERB_SET:
        process_move_verb([COBOL_VERB_MOVE, tokens[3], tokens[2], tokens[1]], name, indent, level)
        last_cmd_display = False
    elif verb == COBOL_VERB_DISPLAY:
        process_display_verb(tokens, name, level)
        last_cmd_display = True
    elif verb == COBOL_VERB_ADD or tokens[0] == COBOL_VERB_SUBTRACT or tokens[0] == COBOL_VERB_MULTIPLY or tokens[0] == COBOL_VERB_DIVIDE:
        process_math_verb(tokens, name, level)
        last_cmd_display = False
    elif verb == COBOL_VERB_GOBACK or tokens[0] == COBOL_VERB_STOPRUN or tokens[0] == COBOL_VERB_EXIT:

        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + "return")

        if tokens[0] == COBOL_VERB_GOBACK or tokens[0] == COBOL_VERB_STOPRUN:
            level = BASE_LEVEL
            append_file(name + PYTHON_EXT, SPACE + OPEN_BRACKET)
            c = 0
            for a in args:
                if c > 3:
                    append_file(name + PYTHON_EXT, COMMA + SPACE)               
                if c > 2:
                    append_file(name + PYTHON_EXT, "Get_Variable_Value(" + SELF_REFERENCE + name + MEMORY + COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + a + "','" + a + "')")
                c = c + 1

            append_file(name + PYTHON_EXT, CLOSE_BRACKET)

        append_file(name + PYTHON_EXT, NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level - 1)) + PYTHON_EXCEPT_STATEMENT + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + SELF_REFERENCE + MAIN_ERROR_FUNCTION + OPEN_PARENS + "e" + CLOSE_PARENS + NEWLINE)
        
    elif verb == COBOL_VERB_PERFORM:
        level = process_perform_verb(tokens, name, level, current_line)
    elif verb == COBOL_VERB_IF:
        level = process_if_verb(tokens, name, level, False)
    elif verb == COBOL_VERB_ELSE:
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level - 1)) + ELSE + COLON + NEWLINE)
    elif len(tokens) == 2 and tokens[1] == PERIOD:
        level = BASE_LEVEL - 1
        func_name = UNDERSCORE + tokens[0].replace(PERIOD, EMPTY_STRING).replace(DASH, UNDERSCORE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level - 1)) + DEF_KEYWORD + SPACE + func_name + OPEN_PARENS + "self" + CLOSE_PARENS + COLON + NEWLINE)
        last_cmd_display = False
    elif verb == COBOL_VERB_EVALUATE:
        is_first_when = True
        evaluate_compare = tokens[1]
        evaluate_compare_stack.append([evaluate_compare, evaluate_compare])
        level = level + 1
    elif verb == COBOL_VERB_WHEN:
        if tokens[1] == WHEN_OTHER_KEYWORD:
            append_file(name + PYTHON_EXT, pad(len(INDENT) * (level - 1)) + ELSE + COLON + NEWLINE)
        else:
            level = level - 1
            process_evaluate_verb(tokens, name, level)  
            level = level + 1
    elif verb == COBOL_VERB_INSPECT:
        process_inspect_verb(tokens, name, level) 
    elif verb == COBOL_VERB_CONTINUE:
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "x = 0" + NEWLINE)
    elif verb == COBOL_VERB_OPEN:
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + SELF_REFERENCE + name + MEMORY + " = Open_File(" + SELF_REFERENCE + name + MEMORY +"," + SELF_REFERENCE + VARIABLES_LIST_NAME + ", self._FILE_CONTROLVars, '" + tokens[2] + "','" + tokens[1] + "')" + NEWLINE)
    elif verb == COBOL_VERB_CLOSE:
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "Close_File(self._FILE_CONTROLVars, '" + tokens[1] + "')" + NEWLINE)
    elif verb == COBOL_VERB_READ:
        at_end_clause = EMPTY_STRING
        
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "read_result = Read_File(" + SELF_REFERENCE + name + MEMORY + ",self._FILE_CONTROLVars,self._FILE_SECTIONVars, '" + tokens[1] + "','" + at_end_clause + "')" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + SELF_REFERENCE + name + MEMORY + " = read_result[1]" + NEWLINE)
        if len(tokens) > 3:
            if tokens[2] == AT_KEYWORD and tokens[3] == END_KEYWORD:
                append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "if read_result[0] == True:" + NEWLINE)
                process_move_verb(tokens[4:], name, True, level + 1)
    elif verb == COBOL_VERB_WRITE:
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "Write_File(self._FILE_SECTIONVars, '" + tokens[1] + "')" + NEWLINE)
    elif verb == COBOL_VERB_CALL:
        process_call_verb(tokens, name, indent, level, args, current_line)
    elif verb == COBOL_VERB_SEARCH:
        last_cmd_display = False
        process_search_verb(tokens, name, indent, level, args, current_line)
        level = level + 1
    elif verb == COBOL_VERB_COMPUTE:
        process_compute_verb(tokens, name, indent, level, args, current_line)
    elif verb == COBOL_VERB_ACCEPT:
        accept_value = UNDERSCORE + UNDERSCORE + COBOL_VERB_ACCEPT + SPACE
        if len(tokens) > 3:
            accept_value = accept_value + tokens[3]
            if len(tokens) > 4:
                accept_value = accept_value + SPACE + tokens[4]

        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + SELF_REFERENCE + name + MEMORY + " = Set_Variable(" + SELF_REFERENCE + name + MEMORY + COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + tokens[1] + "','" + accept_value + "','" + tokens[1] + "')[1]" + NEWLINE)
    elif verb == CICS_VERB_ASKTIME:
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + SELF_REFERENCE + EIB_MEMORY + " = Set_Variable(" + SELF_REFERENCE + EIB_MEMORY + COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'EIBTIME',get_current_time(),'EIBTIME')[1]" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + SELF_REFERENCE + EIB_MEMORY + " = Set_Variable(" + SELF_REFERENCE + EIB_MEMORY + COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'EIBDATE',format_date_cyyddd(),'EIBDATE')[1]" + NEWLINE)
        if len(tokens) > 3:
            if tokens[3].startswith("ABSTIME"):
                s = tokens[3].split(OPEN_PARENS)
                append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + SELF_REFERENCE + EIB_MEMORY + " = Set_Variable(" + SELF_REFERENCE + EIB_MEMORY + COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + s[1].replace(CLOSE_PARENS, EMPTY_STRING) + "',milliseconds_since_1900(),'" + s[1].replace(CLOSE_PARENS, EMPTY_STRING) + "')[1]" + NEWLINE)
    elif verb == CICS_VERB_LINK:
        process_cics_link(tokens, name, indent, level, args, current_line)
    elif verb == CICS_VERB_HANDLE_ABEND:
        for token in tokens:
            if token.startswith(LABEL_KEYWORD):
                s = token.split(OPEN_PARENS)

                append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + SELF_REFERENCE + CLASS_ERROR_FUNCTION_MEMBER + EQUALS + SELF_REFERENCE + UNDERSCORE + format(s[1].replace(CLOSE_PARENS, EMPTY_STRING)) + NEWLINE)
    else:
        append_file(name + PYTHON_EXT, "# unknown verb " + str(tokens) + NEWLINE)
    
    return level

def process_compute_verb(tokens, name: str, indent: bool, level: int, args, current_line: LexicalInfo):
    count = 0
    end_len = len(tokens)
    if tokens[len(tokens) - 1] == PERIOD:
        end_len = end_len - 1

    equals_pos = 0
    for token in tokens:
        if token.startswith(EQUALS):
            equals_pos = count
            break
        count = count + 1

    tokens[equals_pos] = tokens[equals_pos].replace(EQUALS, EMPTY_STRING)

    count = 0
    for token in tokens:
        if count < equals_pos:
            count = count + 1
            continue
        set_open_parens = False
        set_close_parens = False
        if token in COBOL_ARITHMATIC_OPERATORS or token == EMPTY_STRING:
            count = count + 1
            continue
        else:
            if token.startswith(OPEN_PARENS):
                set_open_parens = True
            elif token.endswith(CLOSE_PARENS):
                set_close_parens = True
            
            token = token.replace(OPEN_PARENS, EMPTY_STRING).replace(CLOSE_PARENS, EMPTY_STRING)

            if token.isnumeric() == False:
                token = "Get_Variable_Value(" + SELF_REFERENCE + name + MEMORY + "," + SELF_REFERENCE + VARIABLES_LIST_NAME + ",\"" + token + "\",\"" + token + "\")"

            if set_open_parens:
                token = OPEN_PARENS + token

            if set_close_parens:
                token = token + CLOSE_PARENS

        tokens[count] = token
        count = count + 1

    for x in range(1,equals_pos):
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + SELF_REFERENCE + name + MEMORY + " = Set_Variable(" + SELF_REFERENCE + name + MEMORY + "," + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + tokens[x] + "',str(eval('" + ''.join(tokens[equals_pos:end_len]) + "')),'" + tokens[x] + "')[1]" + NEWLINE) 
    

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
        at_end_func = SELF_REFERENCE + "_ae" + str(len(current_line.lambda_functions))

    operand2 = tokens[condition_index + 3]

    if operand2.isnumeric() == False:
        if operand2.startswith(SINGLE_QUOTE) == False:
            temp = "Get_Variable_Value(" + SELF_REFERENCE + name + MEMORY + "," + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + operand2 + "','" + operand2 + SINGLE_QUOTE + CLOSE_PARENS
            operand2 = temp

    append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "search_result = Search_Variable_Array(" + SELF_REFERENCE + name + MEMORY + "," + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + tokens[condition_index + 1] \
        + "','" + convert_operator(tokens[condition_index + 2]) + "'," + operand2 + "," + str(all_offset) + "," + at_end_func + COMMA + "self" + CLOSE_PARENS + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + SELF_REFERENCE + name + MEMORY + EQUALS + " search_result[1]" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "is_found = search_result[0]" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "if is_found == False:" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (level + 1)) + "x = 0" + NEWLINE)
    if at_end_func != "None":
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level + 1)) + at_end_func + OPEN_PARENS + CLOSE_PARENS + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "else:" + NEWLINE)

def process_call_verb(tokens, name: str, indent: bool, level: int, args, current_line: LexicalInfo):
    using_args = EMPTY_STRING
    comm_area_args = SELF_REFERENCE + name + MEMORY + COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + COMMA + OPEN_BRACKET
    params = []
    quoted = EMPTY_STRING

    if (len(tokens) > 2 and tokens[2] == USING_KEYWORD):
        params = parse_line_tokens(tokens[3], COMMA, EMPTY_STRING, False)
        param_count = 0
        for param in params:
            if param_count > 0:
                using_args = using_args + COMMA
                comm_area_args = comm_area_args + COMMA
            param_count = param_count + 1
            using_args = using_args + quoted + "Get_Variable_Value(" + SELF_REFERENCE + name + MEMORY + COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + param + "','" + param + "')" + quoted
            comm_area_args = comm_area_args + SINGLE_QUOTE + param + SINGLE_QUOTE

    called_program = tokens[1].replace(SINGLE_QUOTE, EMPTY_STRING)

    append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "call_result = None" + NEWLINE)
    
    if tokens[1].startswith(SINGLE_QUOTE):   
        mod_name = tokens[1].replace(SINGLE_QUOTE, EMPTY_STRING)
        if mod_name not in current_line.import_statement:     
            current_line.import_statement.append(mod_name)
        comm_area_args = comm_area_args + CLOSE_BRACKET + COMMA + SINGLE_QUOTE + called_program + SINGLE_QUOTE
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + called_program + "_obj = " + called_program + "Class()" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + SELF_REFERENCE + EIB_MEMORY + " = Build_Comm_Area" + OPEN_PARENS + SINGLE_QUOTE + called_program + SINGLE_QUOTE + COMMA + OPEN_BRACKET + using_args + CLOSE_BRACKET + COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + COMMA + SELF_REFERENCE + EIB_MEMORY + CLOSE_PARENS + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "sig_args = inspect.signature(" + called_program + "_obj.main)" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "cargs = Translate_Arguments" + OPEN_PARENS + "str(sig_args)" + COMMA + OPEN_BRACKET + using_args + CLOSE_BRACKET + CLOSE_PARENS + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "if cargs != '':" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level + 1)) + "call_result = " + called_program + "_obj.main" + OPEN_PARENS + using_args + CLOSE_PARENS + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "else:" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level + 1)) + "call_result = " + called_program + "_obj.main" + OPEN_PARENS + CLOSE_PARENS + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level + 1)) + SELF_REFERENCE + name + MEMORY + " = Retrieve_Comm_Area" + OPEN_PARENS + comm_area_args + CLOSE_PARENS + NEWLINE)
    else:
        comm_area_args = comm_area_args + CLOSE_BRACKET + COMMA + "module_name"
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "module_name = Get_Variable_Value(" + SELF_REFERENCE + name + MEMORY + "," + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + tokens[1] + "','" + tokens[1] + "')" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + SELF_REFERENCE + EIB_MEMORY + " = Build_Comm_Area" + OPEN_PARENS + "module_name," + OPEN_BRACKET + using_args + CLOSE_BRACKET + COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + COMMA + SELF_REFERENCE + EIB_MEMORY + CLOSE_PARENS + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "module = importlib.import_module(module_name)" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "module_class = getattr(module, module_name + 'Class')" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "module_instance = module_class()" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "sig_args = inspect.signature(module_instance.main)" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "cargs = Translate_Arguments" + OPEN_PARENS + "str(sig_args)" + COMMA + OPEN_BRACKET + using_args + CLOSE_BRACKET + CLOSE_PARENS + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "if cargs != '':" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level + 1)) + "call_result = module_instance.main" + OPEN_PARENS + using_args + CLOSE_PARENS + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "else:" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level + 1)) + "call_result = module_instance.main" + OPEN_PARENS + CLOSE_PARENS + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level + 1)) + SELF_REFERENCE + name + MEMORY + " = Retrieve_Comm_Area" + OPEN_PARENS + comm_area_args + CLOSE_PARENS + NEWLINE)
        #append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "call_result = module_instance.main(module_instance, Translate_Arguments" + OPEN_PARENS + "str(sig_args)" + COMMA + using_args + CLOSE_PARENS + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "if call_result != None and str(sig_args) != '()':" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (level + 1)) + "for cr in call_result:" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (level + 2)) + "x = 0" + NEWLINE)
    for param in params:
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level + 2)) + "result = Set_Variable(" + SELF_REFERENCE + name + MEMORY + "," + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + param + "', cr ,'" + param + "')" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level + 2)) + SELF_REFERENCE + name + MEMORY + " = result[1]" + NEWLINE)

def process_cics_link(tokens, name, indent, level, args, current_line):
    new_tokens = [COBOL_VERB_CALL, '', USING_KEYWORD, '', PERIOD]
    for token in tokens:
        if token.startswith(PROGRAM_KEYWORD):
            s = token.split(OPEN_PARENS)
            new_tokens[1] = s[1].replace(CLOSE_PARENS, EMPTY_STRING)
        elif token.startswith(COMMAREA_KEYWORD):
            s = token.split(OPEN_PARENS)
            new_tokens[3] = s[1].replace(CLOSE_PARENS, EMPTY_STRING)
    
    process_call_verb(new_tokens, name, indent, level, args, current_line)

def process_inspect_verb(tokens, name: str, level: int):
    if tokens[2] == CONVERTING_KEYWORD:
        func = "Replace_Variable_Value(" + SELF_REFERENCE + name + MEMORY + "," + SELF_REFERENCE + VARIABLES_LIST_NAME + ", '" + tokens[1] + "'," + tokens[3] + COMMA + tokens[5] + CLOSE_PARENS
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + func + NEWLINE)

def close_out_evaluate(verb: str, name: str, level: int):
    global is_evaluating
    if verb == COBOL_VERB_WHEN:
        return level

    if is_evaluating:
        append_file(name + PYTHON_EXT, COLON + NEWLINE)

    is_evaluating = False

    return level

def close_out_perform_loop(verb: str, name: str, level: int, current_line: LexicalInfo):
    global is_perform_looping
    if verb != COBOL_VERB_PERFORM_END:
        return level

    if is_perform_looping:
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + current_line.loop_modifier)

    is_perform_looping = False

    return level - 1
    
def process_evaluate_verb(tokens, name: str, level: int):
    global evaluate_compare, is_evaluating, evaluate_compare_stack, nested_above_evaluate_compare, is_first_when

    if len(tokens) >= 3 and comparison_operator_exists_in_list(tokens) == False and tokens[2] != NOT_KEYWORD:
        tokens.insert(2, IN_KEYWORD)
        x = 0

    reset_evaluate_compare = False
    operator = EQUALS
    operator_offset = 0
    if len(tokens) > 2:
        operator = tokens[2]
        if tokens[2] == NOT_KEYWORD:
            operator = NOT_EQUALS
            operator_offset = 1

    operand2 = tokens[1]
    if len(tokens) > 3:
        operand2 = tokens[3]
        
    if evaluate_compare == EMPTY_STRING:
        if len(evaluate_compare_stack) > 0:
            evaluate_compare_stack[len(evaluate_compare_stack) - 1] = [evaluate_compare, tokens[1]]
            nested_above_evaluate_compare = tokens[1]
            evaluate_compare = tokens[1]
            reset_evaluate_compare = True
            if len(tokens) > operator_offset + 3:
                operand2 = tokens[operator_offset + 3]
                if operator == IN_KEYWORD:
                    operand2 = "Get_Variable_Value(" + SELF_REFERENCE + name + MEMORY + "," + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + tokens[operator_offset + 3] + "','" + tokens[operator_offset + 3] + "')"
            elif len(tokens) == 3:
                if tokens[2].startswith(SINGLE_QUOTE) or tokens[2].isnumeric():
                    operand2 = tokens[2]
                else:
                    operand2 = "Get_Variable_Value(" + SELF_REFERENCE + name + MEMORY + "," + SELF_REFERENCE + name + MEMORY + "," + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + tokens[2] + "','" + tokens[2] + "')"
                operator = SPACE + IN_KEYWORD + SPACE
        else:
            evaluate_compare = tokens[1]
            if operand2.startswith(SINGLE_QUOTE) == False and operand2.isnumeric() == False:
                operand2 = "Get_Variable_Value(" + SELF_REFERENCE + name + MEMORY + "," + SELF_REFERENCE + name + MEMORY + "," + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + operand2 + "','" + operand2 + "')"
    elif evaluate_compare == TRUE_KEYWORD and operand2 != NUMERIC_KEYWORD:
        operand2 = 'True'
    elif evaluate_compare == FALSE_KEYWORD and operand2 != NUMERIC_KEYWORD:
        operand2 = 'False'



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

    operand1_name = evaluate_compare

    if operand2 == 'True' or operand2 == 'False' or operand2 == NUMERIC_KEYWORD:
        operand1_name = tokens[1]

    operand1 = "Get_Variable_Value(" + SELF_REFERENCE + name + MEMORY + "," + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + operand1_name + "','" + operand1_name + "') "
    if operand2 == NUMERIC_KEYWORD:
        operand1 = "Check_Value_Numeric(" + operand1 + CLOSE_PARENS + SPACE
        if evaluate_compare == TRUE_KEYWORD:
            operand2 = 'True'
        elif evaluate_compare == FALSE_KEYWORD:
            operand2 = "False"
    line = prefix + operand1 + convert_operator(operator) + SPACE + operand2 + SPACE

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
    last_known_operand1 = tokens[1]
    skip_next = False

    for token in tokens:
        if count == 0:
            count = count + 1
            continue
        if token in COBOL_VERB_LIST or token == PERIOD or token == NUMERIC_KEYWORD:
            continue
        count = count + 1
        if skip_next:
            skip_next = False
            continue
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
        elif OPEN_PARENS in token and CLOSE_PARENS in token or (token == OPEN_PARENS or token == CLOSE_PARENS):
            i = 0
        elif OPEN_PARENS in token and token.startswith(OPEN_PARENS) == False:
            s = token.split(OPEN_PARENS)
            if is_boolean_keyword(s[0]):
                tokens.insert(count, OPEN_PARENS + s[1])
                token = s[0]
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

        elif token.replace(PLUS_SIGN, EMPTY_STRING).isnumeric() or token.replace(MINUS_SIGN, EMPTY_STRING).isnumeric():
            line = line + token + SPACE
        elif token == NOT_KEYWORD:
            opposite_operator = True
        elif token == ALL_KEYWORD:
            line = line + "pad_char(" + str(slice_length) + COMMA + tokens[count + 1] + CLOSE_PARENS
            in_ALL_function = True
        elif token == ZERO_KEYWORD:
            line = line + ZERO
        elif is_comparison_operator(token):
            if opposite_operator:
                line = line + SPACE + convert_operator_opposite(token) + SPACE
            else:
                line = line + SPACE + convert_operator(token) + SPACE
            opposite_operator = False
        elif is_boolean_keyword(token):            
            line = line + SPACE + token.lower() + SPACE
            not_offset = 0
            if tokens[count] == NOT_KEYWORD and is_comparison_operator(tokens[count + 1]):
                not_offset = 1
            if is_comparison_operator(tokens[count + not_offset]): # and tokens[count + not_offset] == NOT_KEYWORD):
                line = line + last_known_operand1
        elif token == SPACE_KEYWORD:
            line = line + "Get_Spaces(Get_Variable_Length(" + SELF_REFERENCE + VARIABLES_LIST_NAME + ", '" + tokens[1] + "'))" + SPACE
        elif token == NEGATIVE_KEYWORD:
            line = line + " < 0"
        elif token == OPEN_PARENS or token == CLOSE_PARENS:
            line = line + token
        elif token in COBOL_ARITHMATIC_OPERATORS:
            line = line + SPACE + token + SPACE
        else:
            var = token
            if count < len(tokens):
                if tokens[count].startswith(OPEN_PARENS) and tokens[count].endswith(CLOSE_PARENS):
                    var = var + tokens[count]
                    skip_next = True
            last_known_operand1 = "Get_Variable_Value(" + SELF_REFERENCE + name + MEMORY + "," + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + var + "','" + var + SINGLE_QUOTE + CLOSE_PARENS + SPACE
            line = line + last_known_operand1

        if count < len(tokens):
            if tokens[count].startswith(tuple(COBOL_COMPARISON_OPERATORS)) and len(tokens[count]) > 2:
                operator = tokens[count][0:1]
                tokens[count] = tokens[count][1:]
                tokens.insert(count, operator)
                i = 0

        line = line + slice_compare
        if checking_function:
            checking_function = False
            line = line + CLOSE_PARENS + SPACE
        if need_closed_parens:
            line = line + CLOSE_PARENS + SPACE

    line = line + COLON + NEWLINE

    append_file(name + PYTHON_EXT, pad(num_spaces) + line)

    return level + 1

def process_perform_verb(tokens, name: str, level: int, current_line: LexicalInfo):
    global is_perform_looping
    if VARYING_KEYWORD in tokens:
        is_perform_looping = True
        process_varying_loop(tokens, name, level, current_line)
        level = level + 1
    elif len(tokens) == 3 or THROUGH_KEYWORD in tokens or THRU_KEYWORD in tokens:
        func_name = UNDERSCORE + tokens[1].replace(PERIOD, EMPTY_STRING).replace(DASH, UNDERSCORE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + SELF_REFERENCE + func_name + OPEN_PARENS + CLOSE_PARENS + NEWLINE)
        if THROUGH_KEYWORD in tokens or THRU_KEYWORD in tokens:
            func_name = UNDERSCORE + tokens[3].replace(PERIOD, EMPTY_STRING).replace(DASH, UNDERSCORE)
            append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + SELF_REFERENCE + func_name + OPEN_PARENS + CLOSE_PARENS + NEWLINE)
    else:
        if tokens[1] == UNTIL_KEYWORD:
            operand2 = tokens[4]
            if tokens[4].startswith(SINGLE_QUOTE) == False and tokens[4] != ZERO_KEYWORD:
                operand2 = "Get_Variable_Value(" + SELF_REFERENCE + name + MEMORY + "," + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + tokens[4] + "','" + tokens[4] + "')"
            elif tokens[4] == ZERO_KEYWORD:
                operand2 = ZERO
            append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + "while Get_Variable_Value(" + SELF_REFERENCE + name + MEMORY + "," + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + tokens[2] + "','" + tokens[2] + "') " \
                + convert_operator_opposite(tokens[3]) + operand2 + COLON + NEWLINE)
            level = level + 1

    return level

def process_varying_loop(tokens, name: str, level: int, current_line: LexicalInfo):
    from_index = tokens.index(FROM_KEYWORD)
    varying_index = tokens.index(VARYING_KEYWORD)
    until_index = tokens.index(UNTIL_KEYWORD)
    by_index = tokens.index(BY_KEYWORD)
    or_indices = get_all_indices(tokens, OR_KEYWORD)

    process_move_verb([COBOL_VERB_MOVE, tokens[from_index + 1], TO_KEYWORD, tokens[varying_index + 1]], name, True, level)
    line = "while Get_Variable_Value(" + SELF_REFERENCE + name + MEMORY + "," + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + tokens[varying_index + 1] + "','" + tokens[varying_index + 1] + SINGLE_QUOTE + CLOSE_PARENS + SPACE \
        + convert_operator_opposite(tokens[until_index + 2]) + SPACE + tokens[until_index + 3]

    append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + line)
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
                start_slice = "Get_Variable_Value(" + SELF_REFERENCE  + name + MEMORY + "," + SELF_REFERENCE  + name + MEMORY + "," + SELF_REFERENCE  + VARIABLES_LIST_NAME + ",'" + start_slice + "','" + start_slice + "')-1"
            end_slice = operand_slice[1]
            if end_slice.replace(PLUS_SIGN, EMPTY_STRING).isnumeric() == False:
                end_slice = "Get_Variable_Value(" + name + MEMORY + "," + SELF_REFERENCE  + VARIABLES_LIST_NAME + ",'" + end_slice + "','" + end_slice + "')"
            sub_string = OPEN_BRACKET + start_slice + COLON + start_slice + PLUS_SIGN + end_slice + CLOSE_BRACKET
        line = "\\" + NEWLINE + " and Get_Variable_Value(" + SELF_REFERENCE  + name + MEMORY + "," + SELF_REFERENCE  + VARIABLES_LIST_NAME + ",'" + operand1 + "','" + operand1 + SINGLE_QUOTE + CLOSE_PARENS + sub_string
        offset = 2
        if tokens[or_index + 2] == NOT_KEYWORD:
            line = line + SPACE + convert_operator(tokens[or_index + 3])
            offset = 3
        elif tokens[or_index + 2].startswith(OPEN_PARENS):
            offset = 3
            temp = tokens[or_index + 2].replace(OPEN_PARENS, EMPTY_STRING).replace(CLOSE_PARENS, EMPTY_STRING)
            split = temp.split(COLON)
            t = "[Get_Variable_Value(" + SELF_REFERENCE  + name + MEMORY + "," + SELF_REFERENCE  + VARIABLES_LIST_NAME + ",'" + split[0] + "','" + split[0] + "')-1" + COLON + "Get_Variable_Value(" + SELF_REFERENCE  + name + MEMORY + "," + SELF_REFERENCE  + VARIABLES_LIST_NAME + ",'" + split[0] + "','" + split[0] + "') + " + split[1] + "-1]"
            line = line + t + SPACE
        else:
            line = line + SPACE + tokens[or_index + 2] + SPACE
        line = line + convert_operator(tokens[or_index + offset + 1])
        if tokens[or_index + offset + 2] not in COBOL_VERB_LIST and tokens[or_index + offset + 2] != PERIOD:
            line = line + tokens[or_index + offset + 2]
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level + 1)) + line)
    append_file(name + PYTHON_EXT, COLON + NEWLINE)
    current_line.loop_modifier = SELF_REFERENCE + name + "Memory = Update_Variable(" + SELF_REFERENCE  + name + MEMORY + "," + SELF_REFERENCE  + VARIABLES_LIST_NAME + ",'" \
        + tokens[by_index + 1] + "','" + tokens[varying_index + 1] + "','" + tokens[varying_index + 1] + SINGLE_QUOTE + CLOSE_PARENS + "[1]" + NEWLINE

def process_move_verb(tokens, name: str, indent: bool, level: int):
    do_indent = pad(len(INDENT) * level)

    if not indent:
        do_indent = EMPTY_STRING

    value = tokens[1]
    if value == SPACE_KEYWORD:
        value = SINGLE_QUOTE + SPACES_INITIALIZER + SINGLE_QUOTE
    elif value == ZERO_KEYWORD:
        value = ZERO

    value = value.replace("X'", SINGLE_QUOTE + HEX_PREFIX)

    target_offset = 3

    if value.startswith(SINGLE_QUOTE) == False \
            and value.startswith(MAIN_ARG_VARIABLE_PREFIX) == False \
            and value.startswith(HEX_PREFIX) == False:
        if OPEN_PARENS in value:
            old_value = value
            s = value.split(OPEN_PARENS)
            
            get_var_value = "Get_Variable_Value(" + SELF_REFERENCE + name + MEMORY + COMMA + SELF_REFERENCE + "variables_list,'" + s[0] + "','" + s[0] + "')"
            end = s[1].replace(CLOSE_PARENS, EMPTY_STRING)
            end_offset = s[1].replace(CLOSE_PARENS, EMPTY_STRING)
            if COLON in s[1]:
                s1 = s[1].split(COLON)
                end = s1[1].replace(CLOSE_PARENS, EMPTY_STRING)
                end_offset = s1[0]
                if s1[0].isnumeric() == False:
                    end_offset = "Get_Variable_Value(" + SELF_REFERENCE + name + MEMORY + COMMA + SELF_REFERENCE + "variables_list,'" + s1[0] + "','" + s1[0] + "')"

                value = get_var_value + OPEN_BRACKET + end_offset + "- 1" + COLON + end_offset + " - 1 + " + end + CLOSE_BRACKET
            else:
                value = get_var_value = "Get_Variable_Value(" + SELF_REFERENCE + name + MEMORY + COMMA + SELF_REFERENCE + "variables_list,'" + old_value + "','" + old_value + "')"
        elif value == FUNCTION_KEYWORD:
            value = "Exec_Function('" + tokens[2] + "')"
            target_offset = 4
        elif value == TRUE_KEYWORD:
            value = 'True'
        elif value.replace(PLUS_SIGN, EMPTY_STRING).replace(MINUS_SIGN, EMPTY_STRING).replace(PERIOD, EMPTY_STRING).isnumeric() == False:
            value = "Get_Variable_Value(" + SELF_REFERENCE + name + MEMORY + COMMA + SELF_REFERENCE + "variables_list,'" + value + "','" + value + "')"
    elif value.startswith(SINGLE_QUOTE):
        x = 0

    target = tokens[target_offset].replace(PERIOD, EMPTY_STRING)

    append_file(name + PYTHON_EXT, do_indent + SELF_REFERENCE + name + MEMORY + " = Set_Variable(" + SELF_REFERENCE + name + MEMORY + "," + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + target + "', " + value + ",'" + target + "')[1]" + NEWLINE)

    if len(tokens) > 1 + target_offset and tokens[1 + target_offset] != PERIOD and tokens[1 + target_offset] != NEG_ONE and tokens[1 + target_offset] not in COBOL_END_BLOCK_VERBS and tokens[1 + target_offset] not in COBOL_VERB_LIST:
        limit = len(tokens)
        for x in range(4, limit):
            tokens[x - 1] = tokens[x]
        tokens.pop()
        process_move_verb(tokens, name, indent, level)


def process_display_verb(tokens, name: str, level: int):
    count = 0
    skip_the_rest = False
    skip_next = False
    for t in tokens:
        t = str(t)
        if t == PERIOD:
            continue
        if t == UPON_KEYWORD:
            skip_the_rest = True
            continue
        if skip_the_rest:
            continue
        if skip_next:
            skip_next = False
            continue
        if count > 0:
            if tokens[count] in COBOL_VERB_LIST:
                break

            if count + 1 < len(tokens):
                if tokens[count + 1].startswith(OPEN_PARENS) and tokens[count + 1].endswith(CLOSE_PARENS):
                    skip_next = True
                    t = t + tokens[count + 1]
            is_literal = False
            if t.endswith(PERIOD):
                is_literal = True
            elif t.startswith(SINGLE_QUOTE):
                is_literal = True
                
            if is_literal == False:
                t = t.replace(PERIOD, EMPTY_STRING)
            parent = t
            if (t.startswith(SINGLE_QUOTE) and t.endswith(SINGLE_QUOTE)) or t == EMPTY_STRING:
                t = t.replace(SINGLE_QUOTE, EMPTY_STRING)
                parent = LITERAL
            append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + "Display_Variable(" + SELF_REFERENCE + name + MEMORY + "," + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + t + "','" + parent + "'," + str(is_literal) + ",False)" + NEWLINE)
        count = count + 1

def process_math_verb(tokens, name: str, level: int):
    giving = tokens[3]
    if GIVING_KEYWORD in tokens:
        if TO_KEYWORD in tokens or BY_KEYWORD in tokens:
            giving = tokens[5]
        else:
            giving = tokens[4]
    mod = "'" + tokens[1] + "'"
    target = tokens[3]
    if tokens[1].lstrip('+-').isdigit() == False:
        mod = "Get_Variable_Value(" + SELF_REFERENCE + name + MEMORY + "," + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + tokens[1] + "','" + tokens[1] + "')"

    if tokens[0] == COBOL_VERB_MULTIPLY:
        mod = "'" + tokens[3] + "'"
        target = tokens[1]
        if tokens[3].lstrip('+-').isdigit() == False:
            mod = "Get_Variable_Value(" + SELF_REFERENCE + name + MEMORY + "," + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + tokens[3] + "','" + tokens[3] + "')"

    modifier = EMPTY_STRING
    remainder_var = EMPTY_STRING
    if tokens[0] == COBOL_VERB_SUBTRACT:
        modifier = "-1"
    elif tokens[0] == COBOL_VERB_MULTIPLY:
        modifier = "*"
    elif tokens[0] == COBOL_VERB_DIVIDE:
        modifier = "/"
        if REMAINDER_KEYWORD in tokens:
            i = tokens.index(REMAINDER_KEYWORD)
            remainder_var = tokens[i + 1]

    append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + SELF_REFERENCE + name + MEMORY + " = Update_Variable(" + SELF_REFERENCE + name + MEMORY + COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + "," + mod + ", '" + target + "', '" + giving + "','" + modifier + "','" + remainder_var + "')[1]" + NEWLINE)
    

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
    if operator == GREATER_THAN_EQUAL_TO:
        return LESS_THAN
    if operator == GREATER_THAN:
        return LESS_THAN_EQUAL_TO
    if operator == LESS_THAN_EQUAL_TO:
        return GREATER_THAN

    return operator

def convert_operator(operator: str):
    if operator == EQUALS:
        return DOUBLE_EQUALS
    
    return operator

def is_comparison_operator(operator: str):
    return operator in COBOL_COMPARISON_OPERATORS

def is_boolean_keyword(boolean: str):
    return boolean in COBOL_BOOLEAN_KEYWORDS

def comparison_operator_exists_in_list(list):
    for operator in COBOL_COMPARISON_OPERATORS:
        if operator in list:
            return True

    return False