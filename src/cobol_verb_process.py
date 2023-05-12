from cobol_lexicon import *
from util import *
from decimal import Decimal

last_cmd_display = False
evaluate_compare = EMPTY_STRING
evaluate_compare_stack = []
nested_above_evaluate_compare = EMPTY_STRING
is_evaluating = False
is_first_when = True
is_perform_looping = False

def process_verb(tokens, name: str, indent: bool, level: int, args, current_line: LexicalInfo, next_few_lines):
    global last_cmd_display, evaluate_compare, is_evaluating, evaluate_compare_stack, nested_above_evaluate_compare, is_first_when
    level = close_out_evaluate(tokens[0], name, level)

    if last_cmd_display == True:
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + "Display_Variable(" + SELF_REFERENCE + name + MEMORY + "," + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'','literal',True,True)" + NEWLINE)
        last_cmd_display = False

    if tokens[0] == COBOL_VERB_CALL and P2C_TERMINATE in tokens[1]:
        tokens[0] = P2C_TERMINATE

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
            elif verb == COBOL_VERB_IF_END:
                current_line.in_else_block = False
                current_line.nested_level = current_line.nested_level - 1
                level = level - 1
            else:
                level = level - 1
        if verb == COBOL_VERB_EVALUATE_END:
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
        ind = tokens.index(TO_KEYWORD)

        offset = 1
        start = 1
        prefix = EMPTY_STRING
        prefix2 = EMPTY_STRING

        if ADDRESS_KEYWORD in tokens:
            prefix = ADDRESS_OF_PREFIX
            prefix2 = EMPTY_STRING
            x = tokens.index(ADDRESS_KEYWORD) + 2
            if x > ind:
                offset = x - ind
            else:
                prefix = EMPTY_STRING
                prefix2 = ADDRESS_OF_PREFIX
                start = 3

        for x in range(start, ind):
            process_move_verb([COBOL_VERB_MOVE, prefix + tokens[ind + offset], TO_KEYWORD, prefix2 + tokens[x]], name, indent, level)
        last_cmd_display = False
    elif verb == COBOL_VERB_DISPLAY:
        process_display_verb(tokens, name, level)
        last_cmd_display = True
    elif verb == COBOL_VERB_ADD or tokens[0] == COBOL_VERB_SUBTRACT or tokens[0] == COBOL_VERB_MULTIPLY or tokens[0] == COBOL_VERB_DIVIDE:
        process_math_verb(tokens, name, level)
        last_cmd_display = False
    elif verb == COBOL_VERB_GOBACK or tokens[0] == COBOL_VERB_STOPRUN or tokens[0] == COBOL_VERB_EXIT or tokens[0] == P2C_TERMINATE:
        process_exit_verbs(level, name, tokens, current_line, args)
        
    elif verb == COBOL_VERB_PERFORM:
        level = process_perform_verb(tokens, name, level, current_line, next_few_lines, args)
    elif verb == COBOL_VERB_GO:
        level = process_perform_verb([COBOL_VERB_PERFORM, tokens[2], PERIOD], name, level, current_line, next_few_lines, args)
        process_exit_verbs(level, name, [COBOL_VERB_GOBACK], current_line, args)
    elif verb == COBOL_VERB_IF:
        if current_line.in_else_block:
            current_line.nested_level = current_line.nested_level - 1
        current_line.in_else_block = False
        level = process_if_verb(tokens, name, level, False, current_line)
    elif verb == COBOL_VERB_ELSE:
        if current_line.in_else_block:
            current_line.nested_level = current_line.nested_level - 1
            level = level - 1
        current_line.in_else_block = True
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level - 1)) + ELSE + COLON + NEWLINE)
    elif len(tokens) == 2 and tokens[1] == PERIOD:
        x = get_last_line_of_file(name + PYTHON_EXT)
        if x.startswith(RETURN_KEYWORD) == False:
            process_exit_verbs(level, name, [COBOL_VERB_GOBACK], current_line, args, True)
        current_line.nested_level = 0
        if current_line.needs_except_block:
            append_file(name + PYTHON_EXT, NEWLINE)
            append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 1)) + PYTHON_EXCEPT_STATEMENT + NEWLINE)
            append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL)) + SELF_REFERENCE + MAIN_ERROR_FUNCTION + OPEN_PARENS + "e" + CLOSE_PARENS + NEWLINE)
        current_line.needs_except_block = True
        level = BASE_LEVEL
        func_name = UNDERSCORE + tokens[0].replace(PERIOD, EMPTY_STRING).replace(DASH, UNDERSCORE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level - 2)) + DEF_KEYWORD + SPACE + func_name + OPEN_PARENS + "self" + CLOSE_PARENS + COLON + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level - 1)) + "try:" + NEWLINE)
        last_cmd_display = False
    elif verb == COBOL_VERB_EVALUATE:
        is_first_when = True
        long_evaluate_compare = EMPTY_STRING
        for x in range (2,len(tokens)):
            long_evaluate_compare = long_evaluate_compare + tokens[x] + SPACE

        evaluate_compare = tokens[1]
        evaluate_compare_stack.append([evaluate_compare, long_evaluate_compare])
        level = level + 1
    elif verb == COBOL_VERB_WHEN:
        if tokens[1] == WHEN_OTHER_KEYWORD:
            append_file(name + PYTHON_EXT, pad(len(INDENT) * (level - 1)) + ELSE + COLON + NEWLINE)
        else:
            level = level - 1
            process_evaluate_verb(tokens, name, level, current_line)  
            level = level + 1
    elif verb == COBOL_VERB_INSPECT:
        process_inspect_verb(tokens, name, level) 
    elif verb == COBOL_VERB_CONTINUE:
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "x = 0" + NEWLINE)
    elif verb == COBOL_VERB_OPEN:
        process_open_verb(name, tokens, level)
    elif verb == COBOL_VERB_CLOSE:
        process_close_verb(name, tokens, level)
    elif verb == COBOL_VERB_READ:
        at_end_clause = EMPTY_STRING
        into_rec = EMPTY_STRING
        into_index = 0
        if INTO_KEYWORD in tokens:
            into_index = tokens.index(INTO_KEYWORD)
            into_rec = tokens[into_index + 1]
        
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "read_result = Read_File(" + SELF_REFERENCE + name + MEMORY + ",self._FILE_CONTROLVars," + SELF_REFERENCE + VARIABLES_LIST_NAME + ", '" + tokens[1] + "','" + into_rec + "','" + at_end_clause + "')" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + SELF_REFERENCE + name + MEMORY + " = read_result[1]" + NEWLINE)
        if len(tokens) > 3 + into_index:
            if tokens[into_index + 2] == AT_KEYWORD and tokens[into_index + 3] == END_KEYWORD:
                append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "if read_result[0] == True:" + NEWLINE)
                process_move_verb(tokens[into_index + 4:], name, True, level + 1)
    elif verb == COBOL_VERB_WRITE:
        process_write_verb(name, level, tokens)
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
    elif verb == CICS_VERB_LINK or verb == CICS_VERB_XCTL:
        process_cics_link(tokens, name, indent, level, args, current_line)
        if verb == CICS_VERB_XCTL:
            # add a program quit here because XCTL doesn't return control to the calling program.
            # we will emulate this behavior by quitting the program on return
            append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + "sys.exit(0)" + NEWLINE)
    elif verb == CICS_VERB_HANDLE_ABEND:
        for token in tokens:
            if token.startswith(LABEL_KEYWORD):
                s = token.split(OPEN_PARENS)

                append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + SELF_REFERENCE + CLASS_ERROR_FUNCTION_MEMBER + EQUALS + SELF_REFERENCE + UNDERSCORE + format(s[1].replace(CLOSE_PARENS, EMPTY_STRING)) + NEWLINE)
    elif verb == CICS_VERB_SEND:
        process_send_map(tokens, level, name)
    elif verb == CICS_VERB_RECEIVE:
        process_send_map(tokens, level, name)
    elif verb == COBOL_VERB_NEXT:
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + "x = 0" + NEWLINE)
    elif verb == CICS_VERB_RETURN:
        process_cics_return(level, name, tokens, current_line)
    elif verb == CICS_VERB_READQ:
        process_readq_verb(level, name, tokens, current_line, args)
    elif verb == CICS_VERB_WRITEQ:
        process_writeq_verb(level, name, tokens, current_line, args)
    elif verb == COBOL_VERB_STRING:
        process_string_verb(tokens, level, name, current_line)
    elif verb == COBOL_VERB_SORT:
        process_sort_verb(tokens, level, name, current_line, args)
    elif verb == COBOL_VERB_RELEASE:
        process_release_verb(tokens, level, name, current_line)
    elif verb == END_RETURN_KEYWORD or verb == NOT_KEYWORD:
        x = 0
    elif verb == ASSEMBLER_FAKE_VERB_GET_DD:
        process_get_dd(tokens, level, name, current_line)
    else:
        append_file(name + PYTHON_EXT, "# unknown verb " + str(tokens) + NEWLINE)
        current_line.unknown_cobol_verbs = current_line.unknown_cobol_verbs + 1
    
    current_line.is_evaluating = is_evaluating
    
    return level

def process_open_verb(name: str, tokens: list, level: int):
    current_open_type = tokens[1]
    for x in range(2,len(tokens)):
        if tokens[x] in COBOL_OPEN_KEYWORDS:
            current_open_type = tokens[x]
            continue
        elif tokens[x] == PERIOD:
            continue

        if tokens[x].endswith(PERIOD):
            tokens[x] = tokens[x][0:len(tokens) - 1]

        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + SELF_REFERENCE + name + MEMORY + " = Open_File(" + SELF_REFERENCE + name + MEMORY +"," + SELF_REFERENCE + VARIABLES_LIST_NAME + ", self._FILE_CONTROLVars, '" + tokens[x] + "','" + current_open_type + "')" + NEWLINE)

def process_close_verb(name: str, tokens: list, level: int):
    current_open_type = tokens[1]
    for x in range(1,len(tokens)):
        if tokens[x] == PERIOD:
            continue
        elif tokens[x] in COBOL_VERB_LIST:
            break

        if tokens[x].endswith(PERIOD):
            tokens[x] = tokens[x][0:len(tokens) - 1]

        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "Close_File(self._FILE_CONTROLVars, '" + tokens[x] + "')" + NEWLINE)

def process_cics_return(level: int, name: str, tokens: list, current_line: LexicalInfo):
    func_params = "(True)"
    trans_id = SINGLE_QUOTE + EMPTY_STRING + SINGLE_QUOTE
    for t in tokens:
        if t.startswith("TRANSID"):
            t1 = t.split(OPEN_PARENS)
            trans_id = t1[1].replace(CLOSE_PARENS, EMPTY_STRING)
            if not trans_id.startswith(SINGLE_QUOTE):
                trans_id = "Get_Variable_Value(" + SELF_REFERENCE + name + MEMORY + COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + COMMA + t1[1] + COMMA + t1[1] + CLOSE_PARENS + NEWLINE
            func_params = "(False, " + trans_id  + ")"
    append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + SELF_REFERENCE + CALLING_MODULE_MEMBER + PERIOD + RETURN_CONTROL_METHOD + func_params + NEWLINE)
    #process_exit_verbs(level, name, [COBOL_VERB_GOBACK], current_line, args)

def process_writeq_verb(level: int, name: str, tokens, current_line: LexicalInfo, args):
    queue = EMPTY_STRING
    data = EMPTY_STRING
    resp = EMPTY_STRING
    for token in tokens:
        if token.startswith(QUEUE_KEYWORD):
            t = token.split(OPEN_PARENS)
            queue = t[1].replace(CLOSE_PARENS, EMPTY_STRING)
            if not queue.startswith(SINGLE_QUOTE):
                queue = "Get_Variable_Value(" + SELF_REFERENCE + name + MEMORY + COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + COMMA + SINGLE_QUOTE + queue + SINGLE_QUOTE + COMMA + SINGLE_QUOTE + queue + SINGLE_QUOTE + CLOSE_PARENS
        elif token.startswith(FROM_KEYWORD):
            t = token.split(OPEN_PARENS)
            data = t[1].replace(CLOSE_PARENS, EMPTY_STRING)
            if not data.startswith(SINGLE_QUOTE):
                data = "Get_Variable_Value(" + SELF_REFERENCE + name + MEMORY + COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + COMMA + SINGLE_QUOTE + data + SINGLE_QUOTE + COMMA + SINGLE_QUOTE + data + SINGLE_QUOTE + CLOSE_PARENS    
        elif token.startswith(RESP_KEYWORD):
            t = token.split(OPEN_PARENS)
            resp = t[1].replace(CLOSE_PARENS, EMPTY_STRING)

    append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + "r = self.calling_module.writeq(" + queue + COMMA + data + CLOSE_PARENS + NEWLINE)
    
    if resp != EMPTY_STRING:
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + SELF_REFERENCE + name + MEMORY + " = Set_Variable(" + SELF_REFERENCE + name + MEMORY + COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + COMMA + SINGLE_QUOTE + resp + SINGLE_QUOTE + COMMA + "r[1],'" + resp + SINGLE_QUOTE + CLOSE_PARENS + "[1]" + NEWLINE)

    return

def process_readq_verb(level: int, name: str, tokens, current_line: LexicalInfo, args):
    queue = EMPTY_STRING
    item = "1"
    into = EMPTY_STRING
    resp = EMPTY_STRING
    for token in tokens:
        if token.startswith(QUEUE_KEYWORD):
            t = token.split(OPEN_PARENS)
            queue = t[1].replace(CLOSE_PARENS, EMPTY_STRING)
            if not queue.startswith(SINGLE_QUOTE):
                queue = "Get_Variable_Value(" + SELF_REFERENCE + name + MEMORY + COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + COMMA + SINGLE_QUOTE + queue + SINGLE_QUOTE + COMMA + SINGLE_QUOTE + queue + SINGLE_QUOTE + CLOSE_PARENS
        elif token.startswith(ITEM_KEYWORD):
            t = token.split(OPEN_PARENS)
            item = t[1].replace(CLOSE_PARENS, EMPTY_STRING)
            if not item.isnumeric():
                item = "Get_Variable_Value(" + SELF_REFERENCE + name + MEMORY + COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + COMMA + SINGLE_QUOTE + item + SINGLE_QUOTE + COMMA + SINGLE_QUOTE + item + SINGLE_QUOTE + CLOSE_PARENS
            item = item + " - 1"
        elif token.startswith(INTO_KEYWORD):
            t = token.split(OPEN_PARENS)
            into = t[1].replace(CLOSE_PARENS, EMPTY_STRING)
        elif token.startswith(RESP_KEYWORD):
            t = token.split(OPEN_PARENS)
            resp = t[1].replace(CLOSE_PARENS, EMPTY_STRING)

    append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + "r = self.calling_module.readq(" + queue + COMMA + item + CLOSE_PARENS + NEWLINE)

    if into != EMPTY_STRING:
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + SELF_REFERENCE + name + MEMORY + " = Set_Variable(" + SELF_REFERENCE + name + MEMORY + COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + COMMA + SINGLE_QUOTE + into + SINGLE_QUOTE + COMMA + "r[0],'" + into + SINGLE_QUOTE + CLOSE_PARENS + "[1]" + NEWLINE)
    
    if resp != EMPTY_STRING:
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + SELF_REFERENCE + name + MEMORY + " = Set_Variable(" + SELF_REFERENCE + name + MEMORY + COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + COMMA + SINGLE_QUOTE + resp + SINGLE_QUOTE + COMMA + "r[1],'" + resp + SINGLE_QUOTE + CLOSE_PARENS + "[1]" + NEWLINE)
    
    return

def process_get_dd(tokens, level: int, name: str, current_line: LexicalInfo):
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "result = self.calling_module.get_dd_value(Get_Variable_Value(self.GETDSNSMemory,self.variables_list,'" + tokens[1] + "','" + tokens[1] + "'))" + NEWLINE)
    process_move_verb([COBOL_VERB_MOVE, '1', TO_KEYWORD, tokens[3]], name, True, level)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + SELF_REFERENCE + name + MEMORY + EQUALS + "Set_Variable(" + SELF_REFERENCE + name + MEMORY + COMMA \
                + SELF_REFERENCE + VARIABLES_LIST_NAME + COMMA + SINGLE_QUOTE + tokens[2] + OPEN_PARENS + tokens[3] + CLOSE_PARENS + SINGLE_QUOTE + COMMA + "result" \
                + COMMA + SINGLE_QUOTE + tokens[2] + OPEN_PARENS + tokens[3] + CLOSE_PARENS  + SINGLE_QUOTE + CLOSE_PARENS + OPEN_BRACKET + '1' + CLOSE_BRACKET + NEWLINE) 
    return

def process_write_verb(name, level, tokens):
    if FROM_KEYWORD not in tokens:
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "Write_File(self._FILE_CONTROLVars," + SELF_REFERENCE + VARIABLES_LIST_NAME + COMMA + SELF_REFERENCE + name + MEMORY + COMMA + " '" + tokens[1] + "')" + NEWLINE)
    else:
        idx = tokens.index(FROM_KEYWORD)
        process_move_verb([COBOL_VERB_MOVE, tokens[idx + 1], TO_KEYWORD, tokens[1]], name, True, level)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "Write_File(self._FILE_CONTROLVars," + SELF_REFERENCE + VARIABLES_LIST_NAME + COMMA + SELF_REFERENCE + name + MEMORY + COMMA + " '" + tokens[1] + "')" + NEWLINE)

def process_release_verb(tokens, level: int, name: str, current_line: LexicalInfo):
    append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + "Append_Data_To_File(self._FILE_CONTROLVars, '" + tokens[1] + "', Get_Variable_Value(" + SELF_REFERENCE + name + MEMORY + COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + COMMA + SINGLE_QUOTE + tokens[1] + SINGLE_QUOTE + COMMA + SINGLE_QUOTE + tokens[1] + SINGLE_QUOTE + CLOSE_PARENS + CLOSE_PARENS + NEWLINE)
    return

def process_sort_verb(tokens, level: int, name: str, current_line: LexicalInfo, args):
    input_index = 0
    output_index = 0
    end_of_key_index = 0
    thru_tokens = []

    ascending = True

    if tokens[2] == DESCENDING_KEYWORD:
        ascending = False

    if OUTPUT_KEYWORD in tokens:
        output_index = tokens.index(OUTPUT_KEYWORD)

    if INPUT_KEYWORD in tokens:
        input_index = tokens.index(INPUT_KEYWORD)
        end_of_key_index = input_index
        if tokens[input_index + 1] == PROCEDURE_KEYWORD:
            input_index = input_index + 1
        if tokens[input_index + 1] == IS_KEYWORD:
            input_index = input_index + 1

        if THRU_KEYWORD in tokens:
            end_index = output_index
            if output_index < input_index:
                end_index = len(tokens)
            thru_index = tokens.index(THRU_KEYWORD, input_index, end_index)
            thru_tokens.append(THRU_KEYWORD)
            thru_tokens.append(tokens[thru_index + 1])

        perform_tokens = [COBOL_VERB_PERFORM, tokens[input_index + 1]]

        perform_tokens.extend(thru_tokens)

        process_perform_verb(perform_tokens, name, level, current_line, [], args)

        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + "# sort the records\n")
        key_fields = OPEN_BRACKET
        for x in range(3,end_of_key_index):
            if x > 3:
                key_fields = key_fields + COMMA
            key_fields = key_fields + SINGLE_QUOTE + tokens[x] + SINGLE_QUOTE
        key_fields = key_fields + CLOSE_BRACKET
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + "key_fields = " + key_fields + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + "Sort_File(self._FILE_CONTROLVars,self." + VARIABLES_LIST_NAME + ",'" + tokens[1] + SINGLE_QUOTE + COMMA + "key_fields)\n")


        if OUTPUT_KEYWORD in tokens:
            thru_tokens = []
            output_index = tokens.index(OUTPUT_KEYWORD)
            if tokens[output_index + 1] == PROCEDURE_KEYWORD:
                output_index = output_index + 1
            if tokens[output_index + 1] == IS_KEYWORD:
                output_index = output_index + 1

            if THRU_KEYWORD in tokens:
                thru_index = tokens.index(THRU_KEYWORD, output_index)
                thru_tokens.append(THRU_KEYWORD)
                thru_tokens.append(tokens[thru_index + 1])

            perform_tokens = [COBOL_VERB_PERFORM, tokens[output_index + 1]]

            perform_tokens.extend(thru_tokens)

            process_perform_verb(perform_tokens, name, level, current_line, [], args)
    elif USING_KEYWORD in tokens:
        using_index = tokens.index(USING_KEYWORD)
        giving_index = tokens.index(GIVING_KEYWORD)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + "Open_File(" + SELF_REFERENCE + name + MEMORY + COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + COMMA + SELF_REFERENCE + "_FILE_CONTROLVars,'" + tokens[using_index + 1] + "','INPUT')" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + "Open_File(" + SELF_REFERENCE + name + MEMORY + COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + COMMA + SELF_REFERENCE + "_FILE_CONTROLVars,'" + tokens[giving_index + 1] + "','OUTPUT')" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + "work_rec = Get_Sort_Record_Name(self._FILE_CONTROLVars,'" + tokens[using_index + 1] + "')\n")
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + "out_rec = Get_Sort_Record_Name(self._FILE_CONTROLVars,'" + tokens[giving_index + 1] + "')\n")
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + "sort_rec = Get_Sort_Record_Name(self._FILE_CONTROLVars,'" + tokens[1] + "')\n")
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + "seof = False\n")
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + "while not seof:" + NEWLINE) 
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level + 1)) + "r_res = Read_File(" + SELF_REFERENCE + name + MEMORY + COMMA + SELF_REFERENCE + "_FILE_CONTROLVars" + COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + COMMA + SINGLE_QUOTE + tokens[using_index + 1] + SINGLE_QUOTE + CLOSE_PARENS + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level + 1)) + "seof = r_res[0]\n")
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level + 1)) + "if seof:\n")
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level + 2)) + "break\n")
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level + 1)) + "self." + name + MEMORY + "= r_res[1]\n")
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level + 1)) + "Append_Data_To_File(self._FILE_CONTROLVars,sort_rec,Get_Variable_Value(self." + name + MEMORY + COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + ",work_rec,work_rec))\n")
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + "Sort_File(self._FILE_CONTROLVars,self." + VARIABLES_LIST_NAME + COMMA + SINGLE_QUOTE + tokens[1] + SINGLE_QUOTE + COMMA + SINGLE_QUOTE + tokens[3] + "')" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + "sort_array = Get_Sort_Array(" + SELF_REFERENCE + "_FILE_CONTROLVars,'" + tokens[1] + "')" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + "for rec in sort_array:\n")
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level + 1)) + "self." + name + MEMORY + " = Set_Variable(self." + name + MEMORY + COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + ", out_rec, rec, out_rec)[1]\n")
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level + 1)) + "Write_File(self._FILE_CONTROLVars,self." + VARIABLES_LIST_NAME + COMMA + SELF_REFERENCE + name + MEMORY  + ",out_rec)\n")
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + "Close_File(" + SELF_REFERENCE + "_FILE_CONTROLVars,'" + tokens[using_index + 1] + "')" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + "Close_File(" + SELF_REFERENCE + "_FILE_CONTROLVars,'" + tokens[giving_index + 1] + "')" + NEWLINE)

    return 

def process_string_verb(tokens, level: int, name: str, current_line: LexicalInfo):

    into_index = tokens.index(INTO_KEYWORD)

    target = tokens[into_index + 1]

    string_list = EMPTY_STRING

    indices = [i for i, x in enumerate(tokens) if x == DELIMITED_KEYWORD]

    for x in range(0, len(indices)):
        start_at = 1
        end_at = indices[x]
        if tokens[end_at + 1] == BY_KEYWORD:
            end_at = end_at + 1
        for y in range(start_at, end_at):
            if y > start_at:
                string_list = string_list + COMMA
            var_name = SINGLE_QUOTE + tokens[y] + SINGLE_QUOTE
            delim_by = tokens[end_at + 1]
            if tokens[y].startswith(SINGLE_QUOTE):
                var_name = tokens[y]
                delim_by = 'LITERAL'

            string_list = string_list + OPEN_BRACKET + var_name + COMMA + SINGLE_QUOTE + delim_by + SINGLE_QUOTE + CLOSE_BRACKET

    build_string_func = "Build_String(" + SELF_REFERENCE + name + MEMORY + COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + COMMA \
        + SINGLE_QUOTE + target + SINGLE_QUOTE + COMMA + OPEN_BRACKET + string_list + CLOSE_BRACKET + CLOSE_PARENS
    append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + SELF_REFERENCE + name + MEMORY + SPACE + EQUALS + SPACE + build_string_func + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + "x = 0" + NEWLINE)
    return

def process_exit_verbs(level:int, name: str, tokens, current_line: LexicalInfo, args, skip_except_block = False):
    if tokens[0] == P2C_TERMINATE or (len(tokens) > 1 and tokens[0] == STOP_KEYWORD + SPACE + RUN_KEYWORD):
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + "#inform calling module that termination has happened" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + SELF_REFERENCE + "calling_module.terminate_on_callback()" + NEWLINE)

    append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + "return")

    if tokens[0] == COBOL_VERB_GOBACK or tokens[0] == COBOL_VERB_STOPRUN or tokens[0] == P2C_TERMINATE:
        level = BASE_LEVEL
        append_file(name + PYTHON_EXT, SPACE + OPEN_BRACKET)
        c = 0
        for a in args:
            if c > 3:
                append_file(name + PYTHON_EXT, COMMA + SPACE)               
            if c > 2:
                memory_area = SELF_REFERENCE + name + MEMORY
                if a in EIB_VARIABLES:
                    memory_area = SELF_REFERENCE + EIB_MEMORY
                elif a in SPECIAL_REGISTERS_VARIABLES:
                    memory_area = SELF_REFERENCE + "SPECIALREGISTERSMemory"
                append_file(name + PYTHON_EXT, "Get_Variable_Value(" + memory_area + COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + a + "','" + a + "')")
            c = c + 1

        append_file(name + PYTHON_EXT, CLOSE_BRACKET)

    append_file(name + PYTHON_EXT, NEWLINE)

    if not skip_except_block:
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level - 1)) + PYTHON_EXCEPT_STATEMENT + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + SELF_REFERENCE + MAIN_ERROR_FUNCTION + OPEN_PARENS + "e" + CLOSE_PARENS + NEWLINE)
        current_line.needs_except_block = False

    return

def process_send_map(tokens, level: int, name: str):
    map_name = EMPTY_STRING
    map_only = 'False'
    data_only = 'False'
    data = "''"
    length = 0
    for token in tokens:
        if token.startswith("TEXT"):
            map_name = "'text'"
        elif token.startswith("MAP"):
            s = token.split(OPEN_PARENS)
            map_name = s[1].replace(CLOSE_PARENS, EMPTY_STRING)
            if map_name.startswith(SINGLE_QUOTE) == False:
                memory_area = SELF_REFERENCE + name + MEMORY
                if map_name in EIB_VARIABLES:
                    memory_area = SELF_REFERENCE + EIB_MEMORY
                elif map_name in SPECIAL_REGISTERS_VARIABLES:
                    memory_area = SELF_REFERENCE + "SPECIALREGISTERSMemory"
                map_name = "Get_Variable_Value(" + memory_area + COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + COMMA + SINGLE_QUOTE + map_name + SINGLE_QUOTE + COMMA + SINGLE_QUOTE + map_name + SINGLE_QUOTE + CLOSE_PARENS
            break
        elif token == "MAPONLY":
            map_only = 'True'
        elif token == "DATAONLY":
            data_only = 'True'
        elif token.startswith("FROM"):
            s = token.split(OPEN_PARENS)
            memory_area = SELF_REFERENCE + name + MEMORY
            if s[1].replace(CLOSE_PARENS, EMPTY_STRING) in EIB_VARIABLES:
                memory_area = SELF_REFERENCE + EIB_MEMORY
            elif s[1].replace(CLOSE_PARENS, EMPTY_STRING) in SPECIAL_REGISTERS_VARIABLES:
                memory_area = SELF_REFERENCE + "SPECIALREGISTERSMemory"
            data = "Get_Variable_Value(" + memory_area+ COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + COMMA + SINGLE_QUOTE + s[1].replace(CLOSE_PARENS, EMPTY_STRING) + SINGLE_QUOTE + COMMA + SINGLE_QUOTE + s[1].replace(CLOSE_PARENS, EMPTY_STRING) + SINGLE_QUOTE + CLOSE_PARENS

    append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + "if " + SELF_REFERENCE + CALLING_MODULE_MEMBER + " != None:" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (level + 1)) + SELF_REFERENCE + CALLING_MODULE_MEMBER +".build_map(" + map_name + COMMA + data + COMMA + map_only + COMMA + data_only + CLOSE_PARENS + NEWLINE)

    return

def process_compute_verb(tokens, name: str, indent: bool, level: int, args, current_line: LexicalInfo):
    count = 0

    temp_tokens = []
    skip_next = False
    skip_next_2 = False
    for t in tokens:
        if skip_next_2:
            skip_next = True
            skip_next_2 = False
            count = count + 1
            continue
        if skip_next:
            skip_next = False
            count = count + 1
            continue
        if t.startswith(OPEN_PARENS) or t.endswith(CLOSE_PARENS):
            if len(temp_tokens) > 0:
                temp_tokens[len(temp_tokens) - 1] = temp_tokens[len(temp_tokens) - 1] + t.replace(OPEN_PARENS, "{").replace(CLOSE_PARENS, "}")
        elif t == EMPTY_STRING or t == PERIOD:
            count = count + 1
            continue
        elif t == FUNCTION_KEYWORD:
            skip_next = True
            temp_tokens.append("Exec_Function(\"" + name +  "\",\"" + tokens[count + 1] + "\")")
        elif t == LENGTH_KEYWORD:
            offset = 1
            if tokens[count + 1] == OF_KEYWORD:
                skip_next_2 = True
                skip_next = False
                offset = 2

            temp_tokens.append('len_' + tokens[count + offset])
        else:
            if len(temp_tokens) > 0 and check_valid_verb(t, t, True) == False:
                temp_tokens.append(t)
            elif len(temp_tokens) == 0:
                temp_tokens.append(t)

        count = count + 1

    tokens = temp_tokens
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
        elif token.startswith("Exec_Function(\"" + name +  "\","):
            x = 0
        else:
            if token.startswith(OPEN_PARENS):
                set_open_parens = True
            elif token.endswith(CLOSE_PARENS):
                set_close_parens = True
            
            token = token.replace(OPEN_PARENS, EMPTY_STRING).replace(CLOSE_PARENS, EMPTY_STRING)

            if token.isnumeric() == False:
                memory_area = SELF_REFERENCE + name + MEMORY
                if token in EIB_VARIABLES:
                    memory_area = SELF_REFERENCE + EIB_MEMORY
                elif token in SPECIAL_REGISTERS_VARIABLES:
                    memory_area = SELF_REFERENCE + "SPECIALREGISTERSMemory"
                v = token.replace("{", OPEN_PARENS).replace("}", CLOSE_PARENS)
                if v.startswith(PLUS_SIGN):
                    token = v
                elif v.startswith('len_'):
                    token = "Get_Variable_Length(" + SELF_REFERENCE + VARIABLES_LIST_NAME + COMMA + "\"" + v[len('len_'):] + "\")"
                else:
                    token = "Get_Variable_Value(" + memory_area + "," + SELF_REFERENCE + VARIABLES_LIST_NAME + ",\"" + v + "\",\"" + v + "\")"

            if set_open_parens:
                token = OPEN_PARENS + token

            if set_close_parens:
                token = token + CLOSE_PARENS

        tokens[count] = token
        count = count + 1

    for x in range(1,equals_pos):
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + SELF_REFERENCE + name + MEMORY + " = Set_Variable(" + SELF_REFERENCE + name + MEMORY + "," + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + tokens[x] + "',str(eval('" + ''.join(tokens[equals_pos:end_len]) + "')),'" + tokens[x] + "')[1]" + NEWLINE) 
    
    return

def process_search_verb(tokens, name: str, indent: bool, level: int, args, current_line: LexicalInfo):
    
    temp_tokens = []
    orig_tokens = tokens

    in_parens = False
    temp = EMPTY_STRING
    for token in tokens:
        if in_parens:
            temp = temp + token
        elif OPEN_PARENS in token:
            in_parens = True
            temp = temp + token
        else:
            temp_tokens.append(token)
            continue

        if CLOSE_PARENS in token:
            in_parens = False
            temp_tokens.append(temp)
            temp = EMPTY_STRING

    tokens = temp_tokens
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
 
    creating_check = True
    operand1_list = EMPTY_STRING
    operand2_list = EMPTY_STRING
    operator_list = EMPTY_STRING
    boolean_list = EMPTY_STRING
    first = True
    while creating_check and condition_index < len(tokens):
        operand2 = tokens[condition_index + 3]
        operator = convert_operator(tokens[condition_index + 2]) 

        if operand2.startswith(PLUS_SIGN):
            operand2 = operand2[1:]

        if operand2.isnumeric() == False:
            if operand2.startswith(SINGLE_QUOTE) == False:
                operand2 = SINGLE_QUOTE + operand2 + SINGLE_QUOTE

        if first == False:
            operand1_list = operand1_list + COMMA
            operand2_list = operand2_list + COMMA
            operator_list = operator_list + COMMA
        else:
            first = False

        o1 = tokens[condition_index + 1]
        if o1.startswith(SINGLE_QUOTE) == False:
            o1 = SINGLE_QUOTE + o1
        if o1.endswith(SINGLE_QUOTE) == False:
            o1 = o1 + SINGLE_QUOTE
        operand1_list = operand1_list + o1
        operand2_list = operand2_list + operand2
        operator_list = operator_list + SINGLE_QUOTE + operator + SINGLE_QUOTE

        if condition_index + 4 < len(tokens):
            if tokens[condition_index + 4] not in COBOL_BOOLEAN_KEYWORDS:
                creating_check = False
            else:
                if boolean_list != EMPTY_STRING:
                    boolean_list = boolean_list + COMMA

                boolean_list = boolean_list + SINGLE_QUOTE + tokens[condition_index + 4] + SINGLE_QUOTE

        condition_index = condition_index + 4

    append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "search_result = Search_Variable_Array(" + SELF_REFERENCE + name + MEMORY + "," + SELF_REFERENCE + VARIABLES_LIST_NAME \
        + COMMA + SINGLE_QUOTE + tokens[1 + all_offset] + "',[" + operand1_list \
        + "],[" + operator_list + "],[" + operand2_list + "]," + str(all_offset) + COMMA + at_end_func + COMMA + "self" + COMMA + OPEN_BRACKET + boolean_list + CLOSE_BRACKET + CLOSE_PARENS + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + SELF_REFERENCE + name + MEMORY + EQUALS + " search_result[1]" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "is_found = search_result[0]" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "if is_found == False:" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (level + 1)) + "x = 0" + NEWLINE)
    if at_end_func != "None":
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level + 1)) + at_end_func + OPEN_PARENS + CLOSE_PARENS + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "else:" + NEWLINE)

    return

def process_call_verb(tokens, name: str, indent: bool, level: int, args, current_line: LexicalInfo):
    if tokens[len(tokens) - 1] != PERIOD:
        tokens.append(PERIOD)
    using_args = EMPTY_STRING
    comm_area_args = SELF_REFERENCE + name + MEMORY + COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + COMMA + OPEN_BRACKET
    params = []
    quoted = EMPTY_STRING
    pass_by_content = False

    if (len(tokens) > 2 and tokens[2] == USING_KEYWORD):
        start = 3
        if tokens[3] == CONTENT_KEYWORD:
            start = 4
            pass_by_content = True
        for x in range(start,len(tokens) - 1):
            params = parse_line_tokens(tokens[x], COMMA, EMPTY_STRING, False)
            param_count = 0
            if x > start:
                using_args = using_args + COMMA
                comm_area_args = comm_area_args + COMMA
            for param in params:
                if param_count > 0:
                    using_args = using_args + COMMA
                    comm_area_args = comm_area_args + COMMA
                param_count = param_count + 1
                if tokens[3] == CONTENT_KEYWORD:
                    if param.startswith("X'"):
                        param = param.replace("X'", "'" + HEX_PREFIX)
                    using_args = using_args + param
                    comm_area_args = OPEN_BRACKET
                else:
                    memory_area = SELF_REFERENCE + name + MEMORY
                    if param in EIB_VARIABLES:
                        memory_area = SELF_REFERENCE + EIB_MEMORY
                    elif param in SPECIAL_REGISTERS_VARIABLES:
                        memory_area = SELF_REFERENCE + "SPECIALREGISTERSMemory"
                    using_args = using_args + quoted + "Get_Variable_Value(" + memory_area + COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + param + "','" + param + "',True)" + quoted
                    comm_area_args = comm_area_args + SINGLE_QUOTE + param + SINGLE_QUOTE

    called_program = tokens[1].replace(SINGLE_QUOTE, EMPTY_STRING)

    append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "call_result = None" + NEWLINE)
    
    if tokens[1].startswith(SINGLE_QUOTE):   
        mod_name = tokens[1].replace(SINGLE_QUOTE, EMPTY_STRING)
        if mod_name not in current_line.import_statement:     
            current_line.import_statement.append(mod_name)
        comm_area_args = comm_area_args + CLOSE_BRACKET + COMMA + SINGLE_QUOTE + called_program + SINGLE_QUOTE
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + called_program + "_obj = " + called_program + "Class()" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + SELF_REFERENCE + EIB_MEMORY + " = Build_Comm_Area" + OPEN_PARENS + SINGLE_QUOTE + \
            called_program + SINGLE_QUOTE + COMMA + OPEN_BRACKET + using_args + CLOSE_BRACKET + COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + COMMA + \
                SELF_REFERENCE + EIB_MEMORY + COMMA + "Get_Variable_Value(" + SELF_REFERENCE + EIB_MEMORY + COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + \
                COMMA + "'EIBTERM'" + COMMA + "'EIBTERM'" + CLOSE_PARENS + COMMA + "Get_Variable_Value(" + SELF_REFERENCE + EIB_MEMORY + COMMA + SELF_REFERENCE + \
                VARIABLES_LIST_NAME + COMMA + "'EIBTRANS'" + COMMA + "'EIBTRANS'" + CLOSE_PARENS + CLOSE_PARENS + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "sig_args = inspect.signature(" + called_program + "_obj.main)" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "cargs = Translate_Arguments" + OPEN_PARENS + "str(sig_args)" + COMMA + OPEN_BRACKET + using_args + CLOSE_BRACKET + CLOSE_PARENS + NEWLINE)
        if using_args == EMPTY_STRING:
            using_args = "None"
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "if cargs != '':" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level + 1)) + "call_result = " + called_program + "_obj.main" + OPEN_PARENS + "self," + using_args + CLOSE_PARENS + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "else:" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level + 1)) + "call_result = " + called_program + "_obj.main" + OPEN_PARENS + "self" + CLOSE_PARENS + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "if self.terminate:" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level + 1)) + SELF_REFERENCE + "calling_module.terminate_on_callback()" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level + 1)) + "return" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + SELF_REFERENCE + name + MEMORY + " = Retrieve_Comm_Area" + OPEN_PARENS + comm_area_args + CLOSE_PARENS + NEWLINE)
    else:
        comm_area_args = comm_area_args + CLOSE_BRACKET + COMMA + "module_name"
        memory_area = SELF_REFERENCE + name + MEMORY
        if tokens[1] in EIB_VARIABLES:
            memory_area = SELF_REFERENCE + EIB_MEMORY
        elif tokens[1] in SPECIAL_REGISTERS_VARIABLES:
            memory_area = SELF_REFERENCE + "SPECIALREGISTERSMemory"
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "module_name = Get_Variable_Value(" + memory_area + "," + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + tokens[1] + "','" + tokens[1] + "')" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + SELF_REFERENCE + EIB_MEMORY + " = Build_Comm_Area" + OPEN_PARENS + \
            "Get_Variable_Value(" + SELF_REFERENCE + name + MEMORY + COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + COMMA + SINGLE_QUOTE + called_program + SINGLE_QUOTE \
                + COMMA + SINGLE_QUOTE + called_program + SINGLE_QUOTE + CLOSE_PARENS + COMMA + OPEN_BRACKET + using_args + CLOSE_BRACKET + COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + COMMA + \
                SELF_REFERENCE + EIB_MEMORY + COMMA + "Get_Variable_Value(" + SELF_REFERENCE + EIB_MEMORY + COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + \
                COMMA + "'EIBTERM'" + COMMA + "'EIBTERM'" + CLOSE_PARENS + COMMA + "Get_Variable_Value(" + SELF_REFERENCE + EIB_MEMORY + COMMA + SELF_REFERENCE + \
                VARIABLES_LIST_NAME + COMMA + "'EIBTRANS'" + COMMA + "'EIBTRANS'" + CLOSE_PARENS + CLOSE_PARENS + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "module = importlib.import_module(module_name)" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "module_class = getattr(module, module_name + 'Class')" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "module_instance = module_class()" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "sig_args = inspect.signature(module_instance.main)" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "cargs = Translate_Arguments" + OPEN_PARENS + "str(sig_args)" + COMMA + OPEN_BRACKET + using_args + CLOSE_BRACKET + CLOSE_PARENS + NEWLINE)
        if using_args == EMPTY_STRING:
            using_args = "None"
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "if cargs != '':" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level + 1)) + "call_result = module_instance.main" + OPEN_PARENS + "self," + using_args + CLOSE_PARENS + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "else:" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level + 1)) + "call_result = module_instance.main" + OPEN_PARENS + "self" + CLOSE_PARENS + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "if self.terminate:" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level + 1)) + "return" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + SELF_REFERENCE + name + MEMORY + " = Retrieve_Comm_Area" + OPEN_PARENS + comm_area_args + CLOSE_PARENS + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (level)) + "if call_result != None and str(sig_args) != '()':" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (level + 1)) + "for cr in call_result:" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (level + 2)) + "x = 0" + NEWLINE)
    if not pass_by_content:
        for param in params:
            append_file(name + PYTHON_EXT, pad(len(INDENT) * (level + 2)) + "result = Set_Variable(" + SELF_REFERENCE + name + MEMORY + "," + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + param + "', cr ,'" + param + "')" + NEWLINE)
            append_file(name + PYTHON_EXT, pad(len(INDENT) * (level + 2)) + SELF_REFERENCE + name + MEMORY + " = result[1]" + NEWLINE)
    return

def process_cics_link(tokens, name, indent, level, args, current_line):
    new_tokens = [COBOL_VERB_CALL, '', USING_KEYWORD, '', PERIOD]
    count = 0
    for token in tokens:
        if token.startswith(PROGRAM_KEYWORD):
            s = token.split(OPEN_PARENS)
            new_tokens[1] = s[1].replace(CLOSE_PARENS, EMPTY_STRING)
        elif token.startswith(COMMAREA_KEYWORD):
            s = token.split(OPEN_PARENS)
            new_tokens[3] = s[1].replace(CLOSE_PARENS, EMPTY_STRING)
        elif token.startswith(LENGTH_KEYWORD):
            s = token.split(OPEN_PARENS)

        count = count + 1
    
    process_call_verb(new_tokens, name, indent, level, args, current_line)

    return

def process_inspect_verb(tokens, name: str, level: int):
    if tokens[2] == CONVERTING_KEYWORD:
        func = SELF_REFERENCE + name + MEMORY +  " = Replace_Variable_Value(" + SELF_REFERENCE + name + MEMORY + "," + SELF_REFERENCE + VARIABLES_LIST_NAME + ", '" + tokens[1] + "'," + tokens[3] + COMMA + tokens[5] + CLOSE_PARENS + OPEN_BRACKET + "1" + CLOSE_BRACKET
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + func + NEWLINE)
    elif tokens[2] == REPLACING_KEYWORD:
        only_first = "False"
        offset = 0
        if tokens[3] == FIRST_KEYWORD:
            only_first = "True"
            offset = 1
        func = SELF_REFERENCE + name + MEMORY +  " = Replace_Variable_Value(" + SELF_REFERENCE + name + MEMORY + "," + SELF_REFERENCE + VARIABLES_LIST_NAME + ", '" + tokens[1] + "'," + tokens[3 + offset] + COMMA + tokens[5 + offset] + COMMA + only_first + CLOSE_PARENS + OPEN_BRACKET + "1" + CLOSE_BRACKET
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + func + NEWLINE)

    return

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
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + current_line.loop_modifier[len(current_line.loop_modifier) - 1])
        current_line.loop_modifier.pop()

    if len(current_line.loop_modifier) == 0:
        is_perform_looping = False

    return level - 1
    
def process_evaluate_verb(tokens, name: str, level: int, current_line: LexicalInfo):
    global evaluate_compare, is_evaluating, evaluate_compare_stack, nested_above_evaluate_compare, is_first_when

    if current_line.current_line_number == "378":
        x = 0

    if AND_KEYWORD in tokens:
        is_elif = not is_first_when
        is_first_when = False
        return process_if_verb(tokens, name, level, is_elif, current_line)

    if len(tokens) >= 3 and comparison_operator_exists_in_list(tokens) == False and tokens[2] != NOT_KEYWORD and tokens[2] != NUMERIC_KEYWORD:
        tokens.insert(2, IN_KEYWORD)

    temp_evaluate_compare = evaluate_compare
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
                    memory_area = SELF_REFERENCE + name + MEMORY
                    if tokens[operator_offset + 1] in EIB_VARIABLES:
                        memory_area = SELF_REFERENCE + EIB_MEMORY
                    elif tokens[operator_offset + 1] in SPECIAL_REGISTERS_VARIABLES:
                        memory_area = SELF_REFERENCE + "SPECIALREGISTERSMemory"
                    operand2 = "Get_Variable_Value(" + memory_area + "," + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + tokens[operator_offset + 3] + "','" + tokens[operator_offset + 3] + "')"
            elif len(tokens) == 3:
                if tokens[2].startswith(SINGLE_QUOTE) or tokens[2].isnumeric():
                    operand2 = tokens[2]
                else:
                    memory_area = SELF_REFERENCE + name + MEMORY
                    if tokens[2] in EIB_VARIABLES:
                        memory_area = SELF_REFERENCE + EIB_MEMORY
                    elif tokens[2] in SPECIAL_REGISTERS_VARIABLES:
                        memory_area = SELF_REFERENCE + "SPECIALREGISTERSMemory"
                    operand2 = "Get_Variable_Value(" + memory_area + "," + SELF_REFERENCE + name + MEMORY + "," + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + tokens[2] + "','" + tokens[2] + "')"
                operator = SPACE + IN_KEYWORD + SPACE
        else:
            evaluate_compare = tokens[1]
            if operand2.startswith(SINGLE_QUOTE) == False and operand2.isnumeric() == False:
                memory_area = SELF_REFERENCE + name + MEMORY
                if operand2 in EIB_VARIABLES:
                    memory_area = SELF_REFERENCE + EIB_MEMORY
                elif operand2 in SPECIAL_REGISTERS_VARIABLES:
                    memory_area = SELF_REFERENCE + "SPECIALREGISTERSMemory"
                operand2 = "Get_Variable_Value(" + memory_area + COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + operand2 + "','" + operand2 + "')"
    elif (evaluate_compare == TRUE_KEYWORD or evaluate_compare == FALSE_KEYWORD) and operand2 != NUMERIC_KEYWORD and operator == IN_KEYWORD:
        memory_area = SELF_REFERENCE + name + MEMORY
        if operand2 in EIB_VARIABLES:
            memory_area = SELF_REFERENCE + EIB_MEMORY
        elif operand2 in SPECIAL_REGISTERS_VARIABLES:
            memory_area = SELF_REFERENCE + "SPECIALREGISTERSMemory"
        operand2 = "Get_Variable_Value(" + memory_area + COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + operand2 + "','" + operand2 + "')"
    elif evaluate_compare == TRUE_KEYWORD and operand2 != NUMERIC_KEYWORD and operator != IN_KEYWORD and operator != NUMERIC_KEYWORD and operator not in COBOL_COMPARISON_OPERATORS:
        operand2 = 'True'
    elif evaluate_compare == FALSE_KEYWORD and operand2 != NUMERIC_KEYWORD and operator != IN_KEYWORD:
        operand2 = 'False'
    elif operator == NUMERIC_KEYWORD:
        operand2 = NUMERIC_KEYWORD
    else:
        if len(evaluate_compare_stack) > 0:
            if evaluate_compare_stack[len(evaluate_compare_stack) - 1][1] != EMPTY_STRING:
                operand2 = EMPTY_STRING
                et = evaluate_compare_stack[len(evaluate_compare_stack) - 1][1].split(SPACE)
                if tokens[1] == TRUE_KEYWORD:
                    operand2 = operand2 + convert_operator(et[0]) + SPACE + et[1]
                else:
                    operand2 = operand2 + convert_operator_opposite(et[0]) + SPACE + et[1]

                if et[2] == ALSO_KEYWORD:
                    also_index = tokens.index(ALSO_KEYWORD)
                    operand2 = operand2 + " and "
                    if et[3].startswith(SINGLE_QUOTE) == False and et[3].isnumeric() == False:
                        memory_area = SELF_REFERENCE + name + MEMORY
                        if et[3] in EIB_VARIABLES:
                            memory_area = SELF_REFERENCE + EIB_MEMORY
                        elif et[3] in SPECIAL_REGISTERS_VARIABLES:
                            memory_area = SELF_REFERENCE + "SPECIALREGISTERSMemory"
                        operand2 = operand2 + "Get_Variable_Value(" + memory_area + COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + et[3] + "','" + et[3] + "') "
                    else:
                        operand2 = operand2 + et[3]
                    if tokens[also_index + 1] == TRUE_KEYWORD:
                        operand2 = operand2 + convert_operator(et[4]) + SPACE + et[5]
                    else:
                        operand2 = operand2 + convert_operator_opposite(et[4]) + SPACE + et[5]

                operator = EMPTY_STRING
            elif evaluate_compare == TRUE_KEYWORD:
                evaluate_compare = tokens[1]

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

    if operand2 == 'True' or operand2 == 'False' or operand2 == NUMERIC_KEYWORD or operand2.startswith("Get_Variable_Value("):
        operand1_name = tokens[1]

    memory_area = SELF_REFERENCE + name + MEMORY
    if operand1_name in EIB_VARIABLES:
        memory_area = SELF_REFERENCE + EIB_MEMORY
    elif operand1_name in SPECIAL_REGISTERS_VARIABLES:
        memory_area = SELF_REFERENCE + "SPECIALREGISTERSMemory"
    if operand1_name == NOT_KEYWORD:
        operand1 = "not"
        operator = EMPTY_STRING
    else:
        operand1 = "Get_Variable_Value(" + memory_area + "," + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + operand1_name + "','" + operand1_name + "') "
    if operand2 == NUMERIC_KEYWORD:
        operand1 = "Check_Value_Numeric(" + operand1 + CLOSE_PARENS + SPACE
        if evaluate_compare == TRUE_KEYWORD or temp_evaluate_compare == TRUE_KEYWORD:
            operand2 = 'True'
        elif evaluate_compare == FALSE_KEYWORD or temp_evaluate_compare == FALSE_KEYWORD:
            operand2 = "False"
    if operand1_name == operand2:
        line = prefix + operand1
    elif operator == NUMERIC_KEYWORD:
        line = prefix + operand1
    else:
        line = prefix + operand1 + convert_operator(operator) + SPACE + operand2 + SPACE

    append_file(name + PYTHON_EXT, pad(indent_len) + line)

    evaluate_compare = temp_evaluate_compare

    if reset_evaluate_compare:
        evaluate_compare = EMPTY_STRING

    return level

def process_if_verb(tokens, name: str, level: int, is_elif: bool, current_line: LexicalInfo):
    line = "if "
    if is_elif:
        line = "elif "
    else:
        current_line.nested_level = current_line.nested_level + 1
        current_line.last_known_index = 0

    count = 0
    checking_function = False
    opposite_operator = False
    in_ALL_function = False
    slice_length = 0
    num_spaces = len(INDENT) * level
    last_known_operand1 = tokens[1]
    last_known_slice_compare = EMPTY_STRING
    skip_next = False
    inside_of_bracket = False

    for token in tokens:
        if count == 0:
            count = count + 1
            continue
        count = count + 1
        count_1 = count
        open_parens_count = 0
        if count_1 > len(tokens) - 1:
            count_1 = count
        if token in COBOL_VERB_LIST or token == PERIOD or token == NUMERIC_KEYWORD or (token == NOT_KEYWORD and tokens[count_1] == NUMERIC_KEYWORD):
            continue
        if skip_next:
            skip_next = False
            continue
        need_closed_parens = False
        need_closed_bracket = False
        slice_compare = EMPTY_STRING
        if len(tokens) > count:
            if tokens[count] == NUMERIC_KEYWORD or (tokens[count] == NOT_KEYWORD and tokens[count_1] == NUMERIC_KEYWORD):
                if tokens[count] == NOT_KEYWORD:
                    line = line + " not "
                line = line + "Check_Value_Numeric("
                checking_function = True
        if OPEN_PARENS in token and CLOSE_PARENS in token and COLON in token:
            #TODO: inside of here we need to reset last_known_operand1 if we are dealing with a whole new 
            #      if statement generated by either an indented if or a boolean operator
            o_token = token
            open_parens_count = count_chars(o_token, OPEN_PARENS) - 1
            s = [t for t in token.split(OPEN_PARENS) if t]
            token = s[0]
            if is_boolean_keyword(token):
                if token != s[len(s) - 2]:
                    t = s[len(s) - 2]
                    if t.startswith(SINGLE_QUOTE):
                        last_known_operand1 = t
                    else:
                        memory_area = SELF_REFERENCE + name + MEMORY 
                        if var in EIB_VARIABLES:
                            memory_area = SELF_REFERENCE + EIB_MEMORY
                        elif var in SPECIAL_REGISTERS_VARIABLES:
                            memory_area = SELF_REFERENCE + "SPECIALREGISTERSMemory"
                        last_known_operand1 = "Get_Variable_Value(" + memory_area + "," + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + t + "','" + t + SINGLE_QUOTE + CLOSE_PARENS + SPACE
            positions = s[len(s) - 1].replace(CLOSE_PARENS, EMPTY_STRING).split(COLON)
            slice_length = int(positions[0]) -1 + int(positions[1])
            slice_compare = OPEN_BRACKET + str(int(positions[0]) - 1) + COLON + str(slice_length) + CLOSE_BRACKET
            last_known_slice_compare = slice_compare
            if count < len(tokens):
                if tokens[count] not in COBOL_COMPARISON_OPERATORS and tokens[count] != IN_KEYWORD and tokens[count] != IS_KEYWORD and tokens[count] != NOT_KEYWORD and tokens[count] != NUMERIC_KEYWORD:
                    tokens.insert(count, IN_KEYWORD + UNDERSCORE)

            if o_token.startswith(OPEN_PARENS):
                token = OPEN_PARENS + token
        elif OPEN_PARENS in token and CLOSE_PARENS in token or (token == OPEN_PARENS or token == CLOSE_PARENS):
            i = 0
        elif OPEN_PARENS in token and token.startswith(OPEN_PARENS) == False:
            s = token.split(OPEN_PARENS)
            if is_boolean_keyword(s[0]):
                tokens.insert(count, OPEN_PARENS + s[1])
                token = s[0]
            elif tokens[count] == OR_KEYWORD:
                token = IN_KEYWORD
                tokens[count] = COMMA
                tokens.insert(count, s[1])
                if line[len(line) - 4:] == " == ":
                    line = line[0:len(line) - 4]
        elif token.startswith(OPEN_PARENS):
            s = token.split(OPEN_PARENS)
            if is_boolean_keyword(s[0]):
                tokens.insert(count, OPEN_PARENS + s[1])
                token = s[0]
            elif tokens[count] == OR_KEYWORD:
                token = IN_KEYWORD
                tokens[count] = COMMA
                tokens.insert(count, s[1])
                if line[len(line) - 4:] == " == ":
                    line = line[0:len(line) - 4]
            if token.startswith(OPEN_PARENS) == False:
                token = OPEN_PARENS + token
        elif token == OR_KEYWORD and inside_of_bracket:
            token = COMMA            
        else:
            if token.startswith(OPEN_PARENS):
                line = line + OPEN_PARENS
            token = token.replace(OPEN_PARENS, EMPTY_STRING)

            if token.endswith(CLOSE_PARENS):
                if inside_of_bracket:
                    token = token.replace(CLOSE_PARENS, EMPTY_STRING)
                    need_closed_bracket = True
                else:
                    need_closed_parens = True
                    token = token.replace(CLOSE_PARENS, EMPTY_STRING)

        if token.startswith(SINGLE_QUOTE):
            if in_ALL_function:
                in_ALL_function = False
            else:
                line = line + token + SPACE
        elif token.startswith("X'"):
            line = line + "convert_EBCDIC_hex_to_string('" + token.replace("X", EMPTY_STRING).replace(SINGLE_QUOTE, EMPTY_STRING) + "', None)"
        elif token.replace(PLUS_SIGN, EMPTY_STRING).isnumeric() or token.replace(MINUS_SIGN, EMPTY_STRING).isnumeric():
            line = line + token + SPACE
        elif token == NOT_KEYWORD:
            if count == 2 and len(tokens) == 3:
                line = line + " not "
            else:
                opposite_operator = True
        elif token == ALL_KEYWORD:
            line = line + "pad_char(" + str(slice_length) + COMMA + tokens[count] + CLOSE_PARENS
            in_ALL_function = True
        elif token == ZERO_KEYWORD:
            temp_line = line[:current_line.last_known_index]
            work_line = line[current_line.last_known_index:]
            current_line.last_known_index = len(line)
            pattern = "Get_V"
            last_index = work_line.rfind(pattern)

            if last_index != -1:
                work_line = work_line[:last_index] + work_line[last_index:].replace(pattern, "int(Get_V", 1)

            if CLOSE_BRACKET in work_line:
                pattern = CLOSE_BRACKET
            else:
                pattern = ")"
            last_index = work_line.rfind(pattern)

            if last_index != -1:
                work_line = work_line[:last_index] + work_line[last_index:].replace(pattern, pattern + ")", 1)

            line = temp_line + work_line
            line = line + ZERO
        elif is_comparison_operator(token):
            if opposite_operator:
                line = line + SPACE + convert_operator_opposite(token) + SPACE
            else:
                line = line + SPACE + convert_operator(token) + SPACE
                if tokens[count] == THAN_KEYWORD:
                    skip_next = True
            opposite_operator = False
        elif is_boolean_keyword(token):            
            line = line + SPACE + token.lower() + SPACE
            for x in range (0,open_parens_count):
                line = line + OPEN_PARENS
            not_offset = 0
            if tokens[count] == NOT_KEYWORD and is_comparison_operator(tokens[count + 1]):
                not_offset = 1
            if is_comparison_operator(tokens[count + not_offset]):
                line = line + last_known_operand1
                if slice_compare == EMPTY_STRING:
                    line = line + last_known_slice_compare
        elif token == SPACE_KEYWORD or token == SPACES_KEYWORD:
            line = line + "Get_Spaces(Get_Variable_Length(" + SELF_REFERENCE + VARIABLES_LIST_NAME + ", '" + tokens[1] + "'))" + SPACE
        elif token == LOW_VALUES_KEYWORD:
            line = line + "pad_char(Get_Variable_Length(" + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + tokens[1] + "'), '\\x00')" + SPACE
        elif token == HIGH_VALUES_KEYWORD:
            line = line + "pad_char(Get_Variable_Length(" + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + tokens[1] + "'), '\\xff')" + SPACE
        elif token == NEGATIVE_KEYWORD:
            line = line + " < 0"
        elif token == OPEN_PARENS or token == CLOSE_PARENS or token == COMMA:
            line = line + token
        elif token in COBOL_ARITHMATIC_OPERATORS:
            if token == DIVISION_OPERATOR:
                token = DIVISION_OPERATOR + DIVISION_OPERATOR
            line = line + SPACE + token + SPACE
        elif token == IN_KEYWORD:
            line = line + SPACE + IN_KEYWORD + SPACE + OPEN_BRACKET
            inside_of_bracket = True
        elif token == IN_KEYWORD + UNDERSCORE:
            line = line + SPACE + IN_KEYWORD + SPACE
        else:
            var = token
            if var.startswith(OPEN_PARENS) and var.endswith(CLOSE_PARENS) == False:
                var = var[1:]
            if count < len(tokens):
                if tokens[count].startswith(OPEN_PARENS) and tokens[count].endswith(CLOSE_PARENS):
                    var = var + tokens[count]
                    skip_next = True
            memory_area = SELF_REFERENCE + name + MEMORY 
            if var in EIB_VARIABLES:
                memory_area = SELF_REFERENCE + EIB_MEMORY
            elif var in SPECIAL_REGISTERS_VARIABLES:
                memory_area = SELF_REFERENCE + "SPECIALREGISTERSMemory"
            last_known_operand1 = "Get_Variable_Value(" + memory_area + "," + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + var + "','" + var + SINGLE_QUOTE + CLOSE_PARENS + SPACE
            if token.startswith(OPEN_PARENS):
                line = line + OPEN_PARENS
            line = line + last_known_operand1

        if count < len(tokens):
            if tokens[count].startswith(tuple(COBOL_COMPARISON_OPERATORS)) and len(tokens[count]) > 2:
                if tokens[count] == GREATER_KEYWORD or tokens[count] == EQUAL_KEYWORD:
                    operator = tokens[count]
                else:
                    operator = tokens[count][0:1]
                    tokens[count] = tokens[count][1:]
                    tokens.insert(count, operator)

        line = line + slice_compare
        if checking_function:
            checking_function = False
            line = line + CLOSE_PARENS + SPACE
        if need_closed_parens:
            keep_going = True
            c = 0
            rev = tokens[count - 1][::-1]
            while keep_going:
                if rev[c: c + 1] == CLOSE_PARENS:
                    line = line + CLOSE_PARENS + SPACE
                else:
                    break
                c = c + 1
                if c > len(tokens[count - 1]):
                    break
        if need_closed_bracket:
            line = line + CLOSE_BRACKET + SPACE
            inside_of_bracket = False

    line = line + COLON + NEWLINE

    append_file(name + PYTHON_EXT, pad(num_spaces) + line)

    return level + 1

def process_perform_verb(tokens, name: str, level: int, current_line: LexicalInfo, next_few_lines, args):
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
    elif COBOL_RETURN_KEYWORD in tokens:
        if tokens[len(tokens) - 1] != PERIOD:
            tokens.append(PERIOD)
        return_index = tokens.index(COBOL_RETURN_KEYWORD)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + "work_array = Get_Sort_Array(self._FILE_CONTROLVars,'" + tokens[return_index + 1] + "')\n")
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + "rec_name = Get_Sort_Record_Name(self._FILE_CONTROLVars,'" + tokens[return_index + 1] + "')" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + "work_counter = 0\n")
        level = build_perform_while_statement(level, name, tokens, return_index - 1)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + SELF_REFERENCE + name + MEMORY + " = Set_Variable(self." + name + MEMORY + ",self." + VARIABLES_LIST_NAME + ",rec_name,work_array[work_counter],rec_name)[1]" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + "work_counter = work_counter + 1\n")
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + "if work_counter >= len(work_array):\n")
        end_index = tokens.index("END")
        end_index_2 = len(tokens)
        if NOT_KEYWORD in tokens[end_index:]:
            end_index_2 = tokens.index(NOT_KEYWORD, end_index)
        process_verb(tokens[end_index + 1: end_index_2], name, True, level + 1, args, current_line, [])
    elif len(tokens) == 2:
        func_name = UNDERSCORE + tokens[1].replace(PERIOD, EMPTY_STRING).replace(DASH, UNDERSCORE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + SELF_REFERENCE + func_name + OPEN_PARENS + CLOSE_PARENS + NEWLINE)
    else:
        if tokens[1] == UNTIL_KEYWORD:
            if len(tokens) > 4:
                operand2 = tokens[4]
                if tokens[4].startswith(PLUS_SIGN):
                    operand2 = tokens[4].replace(PLUS_SIGN, EMPTY_STRING)
                elif tokens[4].startswith(SINGLE_QUOTE) == False and tokens[4] != ZERO_KEYWORD:
                    memory_area = SELF_REFERENCE + name + MEMORY
                    if tokens[4] in EIB_VARIABLES:
                        memory_area = SELF_REFERENCE + EIB_MEMORY
                    elif tokens[4] in SPECIAL_REGISTERS_VARIABLES:
                        memory_area = SELF_REFERENCE + "SPECIALREGISTERSMemory"
                    operand2 = "Get_Variable_Value(" + memory_area + "," + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + tokens[4] + "','" + tokens[4] + "')"
                elif tokens[4] == ZERO_KEYWORD:
                    operand2 = ZERO
                memory_area = SELF_REFERENCE + name + MEMORY
                if tokens[2] in EIB_VARIABLES:
                    memory_area = SELF_REFERENCE + EIB_MEMORY
                elif tokens[2] in SPECIAL_REGISTERS_VARIABLES:
                    memory_area = SELF_REFERENCE + "SPECIALREGISTERSMemory"
                append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + "while Get_Variable_Value(" + memory_area + "," + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + tokens[2] + "','" + tokens[2] + "') " \
                    + convert_operator_opposite(tokens[3]) + operand2 + COLON + NEWLINE)
                level = level + 1
            else:
                not_op = EMPTY_STRING
                if tokens[2] == NOT_KEYWORD:
                    operand2 = tokens[3]
                    #not_op = " not "
                else:
                    operand2 = tokens[2]
                memory_area = SELF_REFERENCE + name + MEMORY
                if operand2 in EIB_VARIABLES:
                    memory_area = SELF_REFERENCE + EIB_MEMORY
                elif operand2 in SPECIAL_REGISTERS_VARIABLES:
                    memory_area = SELF_REFERENCE + "SPECIALREGISTERSMemory"
                append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + "while" + not_op + " Get_Variable_Value(" + memory_area + "," + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + operand2 + "','" + operand2 + "') " \
                    + COLON + NEWLINE)
                level = level + 1                

    return level

def build_perform_while_statement(level: int, name: str, tokens, operand2_location: int):
    if len(tokens) > operand2_location and operand2_location > 2:
        operand2 = tokens[operand2_location]
        if tokens[operand2_location].startswith(PLUS_SIGN):
            operand2 = tokens[operand2_location].replace(PLUS_SIGN, EMPTY_STRING)
        elif tokens[operand2_location].startswith(SINGLE_QUOTE) == False and tokens[operand2_location] != ZERO_KEYWORD:
            memory_area = SELF_REFERENCE + name + MEMORY
            if tokens[operand2_location] in EIB_VARIABLES:
                memory_area = SELF_REFERENCE + EIB_MEMORY
            elif tokens[operand2_location] in SPECIAL_REGISTERS_VARIABLES:
                memory_area = SELF_REFERENCE + "SPECIALREGISTERSMemory"
            operand2 = "Get_Variable_Value(" + memory_area + "," + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + tokens[operand2_location] + "','" + tokens[operand2_location] + "')"
        elif tokens[operand2_location] == ZERO_KEYWORD:
            operand2 = ZERO
        memory_area = SELF_REFERENCE + name + MEMORY
        if tokens[2] in EIB_VARIABLES:
            memory_area = SELF_REFERENCE + EIB_MEMORY
        elif tokens[2] in SPECIAL_REGISTERS_VARIABLES:
            memory_area = SELF_REFERENCE + "SPECIALREGISTERSMemory"
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + "while Get_Variable_Value(" + memory_area + "," + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + tokens[2] + "','" + tokens[2] + "') " \
            + convert_operator_opposite(tokens[3]) + operand2 + COLON + NEWLINE)
        level = level + 1
    else:
        not_op = EMPTY_STRING
        if tokens[2] == NOT_KEYWORD:
            operand2 = tokens[3]
            not_op = " not "
        else:
            operand2 = tokens[2]
        if tokens[operand2_location + 1] == COBOL_RETURN_KEYWORD:
            not_op = " not " 
        memory_area = SELF_REFERENCE + name + MEMORY
        if operand2 in EIB_VARIABLES:
            memory_area = SELF_REFERENCE + EIB_MEMORY
        elif operand2 in SPECIAL_REGISTERS_VARIABLES:
            memory_area = SELF_REFERENCE + "SPECIALREGISTERSMemory"
        append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + "while" + not_op + " Get_Variable_Value(" + memory_area + "," + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + operand2 + "','" + operand2 + "') " \
            + COLON + NEWLINE)
        level = level + 1

    return level

def process_varying_loop(tokens, name: str, level: int, current_line: LexicalInfo):
    from_index = tokens.index(FROM_KEYWORD)
    varying_index = tokens.index(VARYING_KEYWORD)
    until_index = tokens.index(UNTIL_KEYWORD)
    by_index = tokens.index(BY_KEYWORD)
    or_indices = get_all_indices(tokens, OR_KEYWORD)

    process_move_verb([COBOL_VERB_MOVE, tokens[from_index + 1], TO_KEYWORD, tokens[varying_index + 1]], name, True, level)
    memory_area = SELF_REFERENCE + name + MEMORY
    if tokens[varying_index + 1] in EIB_VARIABLES:
        memory_area = SELF_REFERENCE + EIB_MEMORY
    elif tokens[varying_index + 1] in SPECIAL_REGISTERS_VARIABLES:
        memory_area = SELF_REFERENCE + "SPECIALREGISTERSMemory"
    operand2 = tokens[until_index + 3]
    if operand2.startswith(PLUS_SIGN):
        operand2 = operand2.replace(PLUS_SIGN, EMPTY_STRING)
    elif operand2.isnumeric() == False and operand2.startswith(SINGLE_QUOTE) == False:
        operand2 = "Get_Variable_Value(" + memory_area + COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + operand2 + "','" + operand2 + SINGLE_QUOTE + CLOSE_PARENS
    line = "while Get_Variable_Value(" + memory_area + "," + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + tokens[varying_index + 1] + "','" + tokens[varying_index + 1] + SINGLE_QUOTE + CLOSE_PARENS + SPACE \
        + convert_operator_opposite(tokens[until_index + 2]) + SPACE + operand2

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
                memory_area = SELF_REFERENCE + name + MEMORY
                if start_slice in EIB_VARIABLES:
                    memory_area = SELF_REFERENCE + EIB_MEMORY
                elif start_slice in SPECIAL_REGISTERS_VARIABLES:
                    memory_area = SELF_REFERENCE + "SPECIALREGISTERSMemory"
                start_slice = "Get_Variable_Value(" + memory_area + "," + SELF_REFERENCE  + VARIABLES_LIST_NAME + ",'" + start_slice + "','" + start_slice + "')-1"
            end_slice = operand_slice[1]
            if end_slice.replace(PLUS_SIGN, EMPTY_STRING).isnumeric() == False:
                memory_area = SELF_REFERENCE + name + MEMORY
                if end_slice in EIB_VARIABLES:
                    memory_area = SELF_REFERENCE + EIB_MEMORY
                elif end_slice in SPECIAL_REGISTERS_VARIABLES:
                    memory_area = SELF_REFERENCE + "SPECIALREGISTERSMemory"
                end_slice = "Get_Variable_Value(" + memory_area + "," + SELF_REFERENCE  + VARIABLES_LIST_NAME + ",'" + end_slice + "','" + end_slice + "')"
            sub_string = OPEN_BRACKET + start_slice + COLON + start_slice + PLUS_SIGN + end_slice + CLOSE_BRACKET
        memory_area = SELF_REFERENCE + name + MEMORY
        if operand1 in EIB_VARIABLES:
            memory_area = SELF_REFERENCE + EIB_MEMORY
        elif operand1 in SPECIAL_REGISTERS_VARIABLES:
            memory_area = SELF_REFERENCE + "SPECIALREGISTERSMemory"
        line = "\\" + NEWLINE + " and Get_Variable_Value(" + memory_area + "," + SELF_REFERENCE  + VARIABLES_LIST_NAME + ",'" + operand1 + "','" + operand1 + SINGLE_QUOTE + CLOSE_PARENS + sub_string
        offset = 2
        if tokens[or_index + 2] == NOT_KEYWORD:
            line = line + SPACE + convert_operator(tokens[or_index + 3])
            offset = 3
        elif tokens[or_index + 2].startswith(OPEN_PARENS):
            offset = 3
            temp = tokens[or_index + 2].replace(OPEN_PARENS, EMPTY_STRING).replace(CLOSE_PARENS, EMPTY_STRING)
            split = temp.split(COLON)
            memory_area = SELF_REFERENCE + name + MEMORY
            if split[0] in EIB_VARIABLES:
                memory_area = SELF_REFERENCE + EIB_MEMORY
            elif split[0] in SPECIAL_REGISTERS_VARIABLES:
                memory_area = SELF_REFERENCE + "SPECIALREGISTERSMemory"
            t = "[Get_Variable_Value(" + memory_area + "," + SELF_REFERENCE  + VARIABLES_LIST_NAME + ",'" + split[0] + "','" + split[0] + "')-1" + COLON + "Get_Variable_Value(" + SELF_REFERENCE  + name + MEMORY + "," + SELF_REFERENCE  + VARIABLES_LIST_NAME + ",'" + split[0] + "','" + split[0] + "') + " + split[1] + "-1]"
            line = line + t + SPACE
        else:
            line = line + SPACE + tokens[or_index + 2] + SPACE
        line = line + convert_operator(tokens[or_index + offset + 1])
        if (or_index + offset + 2) < len(tokens):
            if tokens[or_index + offset + 2] not in COBOL_VERB_LIST and tokens[or_index + offset + 2] != PERIOD:
                line = line + tokens[or_index + offset + 2]
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (level + 1)) + line)
    append_file(name + PYTHON_EXT, COLON + NEWLINE)
    current_line.loop_modifier.append(SELF_REFERENCE + name + "Memory = Update_Variable(" + SELF_REFERENCE  + name + MEMORY + "," + SELF_REFERENCE  + VARIABLES_LIST_NAME + ",'" \
        + tokens[by_index + 1] + "','" + tokens[varying_index + 1] + "','" + tokens[varying_index + 1] + SINGLE_QUOTE + CLOSE_PARENS + "[1]" + NEWLINE)

    return

def process_move_verb(tokens, name: str, indent: bool, level: int):
    do_indent = pad(len(INDENT) * level)

    if not indent:
        do_indent = EMPTY_STRING

    value = tokens[1]
    if value == SPACE_KEYWORD or value == SPACES_KEYWORD:
        value = SINGLE_QUOTE + SPACES_INITIALIZER + SINGLE_QUOTE
    elif value == ZERO_KEYWORD or value == ZEROS_KEYWORD:
        value = ZERO
    elif value == NULL_KEYWORD:
        value = SINGLE_QUOTE + ADDRESS_INDICATOR + NULL_KEYWORD + SINGLE_QUOTE

    if value.startswith("X'"):
        value = value.replace("X'", SINGLE_QUOTE + HEX_PREFIX)

    target_offset = 3

    memory_area = SELF_REFERENCE + name + MEMORY

    if value.startswith(SINGLE_QUOTE) == False \
            and value.startswith(MAIN_ARG_VARIABLE_PREFIX) == False \
            and value.startswith(HEX_PREFIX) == False \
            and value.startswith(DOUBLE_QUOTE) == False \
            and value.startswith(LENGTH_KEYWORD) == False:
        if OPEN_PARENS in value:
            old_value = value
            s = value.split(OPEN_PARENS)
            
            memory_area = SELF_REFERENCE + name + MEMORY
            if s[0] in EIB_VARIABLES:
                memory_area = SELF_REFERENCE + EIB_MEMORY
            elif s[0] in SPECIAL_REGISTERS_VARIABLES:
                memory_area = SELF_REFERENCE + "SPECIALREGISTERSMemory"
            get_var_value = "Get_Variable_Value(" + memory_area + COMMA + SELF_REFERENCE + "variables_list,'" + s[0] + "','" + s[0] + "')"
            end = s[1].replace(CLOSE_PARENS, EMPTY_STRING)
            end_offset = s[1].replace(CLOSE_PARENS, EMPTY_STRING)
            if COLON in s[1]:
                s1 = s[1].split(COLON)
                end = s1[1].replace(CLOSE_PARENS, EMPTY_STRING)
                end_offset = s1[0]
                if s1[0].isnumeric() == False:
                    memory_area = SELF_REFERENCE + name + MEMORY
                    if s1[0] in EIB_VARIABLES:
                        memory_area = SELF_REFERENCE + EIB_MEMORY
                    elif s1[0] in SPECIAL_REGISTERS_VARIABLES:
                        memory_area = SELF_REFERENCE + "SPECIALREGISTERSMemory"
                    end_offset = "Get_Variable_Value(" + memory_area + COMMA + SELF_REFERENCE + "variables_list,'" + s1[0] + "','" + s1[0] + "')"

                value = get_var_value + OPEN_BRACKET + end_offset + "- 1" + COLON + end_offset + " - 1 + " + end + CLOSE_BRACKET
            else:
                memory_area = SELF_REFERENCE + name + MEMORY
                if old_value in EIB_VARIABLES:
                    memory_area = SELF_REFERENCE + EIB_MEMORY
                elif old_value in SPECIAL_REGISTERS_VARIABLES:
                    memory_area = SELF_REFERENCE + "SPECIALREGISTERSMemory"
                value = get_var_value = "Get_Variable_Value(" + memory_area + COMMA + SELF_REFERENCE + "variables_list,'" + old_value + "','" + old_value + "')"
        elif value == FUNCTION_KEYWORD:
            value = "Exec_Function('" + name +  "','" + tokens[2] + "')"
            target_offset = 4
        elif value == TRUE_KEYWORD:
            value = 'True'
        elif value.replace(PLUS_SIGN, EMPTY_STRING).replace(MINUS_SIGN, EMPTY_STRING).replace(PERIOD, EMPTY_STRING).isnumeric() == False:
            func_name = "Get_Variable_Value("
            if value.startswith(ADDRESS_OF_PREFIX):
                func_name = "Get_Variable_Address(" + SELF_REFERENCE + CALLING_MODULE_MEMBER + COMMA
                value = value.replace(ADDRESS_OF_PREFIX, EMPTY_STRING)
            memory_area = SELF_REFERENCE + name + MEMORY
            if value in EIB_VARIABLES:
                memory_area = SELF_REFERENCE + EIB_MEMORY
            elif value in SPECIAL_REGISTERS_VARIABLES:
                memory_area = SELF_REFERENCE + "SPECIALREGISTERSMemory"
            value = func_name + memory_area + COMMA + SELF_REFERENCE + "variables_list,'" + value + "','" + value + "')"
        elif value.replace(PLUS_SIGN, EMPTY_STRING).replace(MINUS_SIGN, EMPTY_STRING).replace(PERIOD, EMPTY_STRING).isnumeric():
            if PERIOD not in value:
                value = str(int(value))
    elif value.startswith(SINGLE_QUOTE):
        x = 0
    elif value.startswith(LENGTH_KEYWORD):
        target_offset = 5
        value = "Get_Variable_Value(" + memory_area + COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + COMMA + SINGLE_QUOTE + 'len_' + tokens[3] + SINGLE_QUOTE + COMMA + SINGLE_QUOTE + tokens[3] + SINGLE_QUOTE + CLOSE_PARENS

    target = tokens[target_offset].replace(PERIOD, EMPTY_STRING)

    set_func_name = "Set_Variable("

    suffix = EMPTY_STRING

    if target.startswith(ADDRESS_OF_PREFIX):
        target = target.replace(ADDRESS_OF_PREFIX, EMPTY_STRING)
        set_func_name = "Set_Variable_Address(" + SELF_REFERENCE + CALLING_MODULE_MEMBER + COMMA
        if value.startswith("Get_Variable_Value"):
            t = value.split(COMMA)
            value = t[2]

    if value.startswith(MAIN_ARG_VARIABLE_PREFIX):
        suffix = ",0, self.calling_module"

    append_file(name + PYTHON_EXT, do_indent + SELF_REFERENCE + name + MEMORY + " = " + set_func_name + SELF_REFERENCE + name + MEMORY + COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + target + "', " + value + ",'" + target + "'" + suffix + ")[1]" + NEWLINE)

    if len(tokens) > 1 + target_offset and tokens[1 + target_offset] != PERIOD and tokens[1 + target_offset] != NEG_ONE and tokens[1 + target_offset] not in COBOL_END_BLOCK_VERBS and tokens[1 + target_offset] not in COBOL_VERB_LIST:
        limit = len(tokens)
        for x in range(4, limit):
            tokens[x - 1] = tokens[x]
        tokens.pop()
        process_move_verb(tokens, name, indent, level)

    return

def process_display_verb(tokens, name: str, level: int):
    count = 0
    skip_the_rest = False
    skip_next = False
    skip_next_2 = False
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
        if skip_next_2:
            skip_next = True
            skip_next_2 = False
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
            if t == SPACE_KEYWORD:
                t = SPACE
                parent = LITERAL
            if t.startswith(LENGTH_KEYWORD) and is_literal == False:
                skip_next_2 = True
                skip_next = False
                if tokens[count + 1] == OF_KEYWORD:
                    t = 'len_' + tokens[count + 2]
                    parent = tokens[count + 2]
            append_file(name + PYTHON_EXT, pad(len(INDENT) * level) + "Display_Variable(" + SELF_REFERENCE + name + MEMORY + "," + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + t + "','" + parent + "'," + str(is_literal) + ",False)" + NEWLINE)
        count = count + 1

    return

def process_math_verb(tokens, name: str, level: int):
    giving = tokens[3]
    if GIVING_KEYWORD in tokens:
        if TO_KEYWORD in tokens or BY_KEYWORD in tokens:
            giving = tokens[5]
        else:
            giving = tokens[4]
    mod = "'" + tokens[1] + "'"
    target = tokens[3]
    if tokens[1].lstrip('+-').isdigit() == False and tokens[1] != LENGTH_KEYWORD:
        memory_area = SELF_REFERENCE + name + MEMORY
        if tokens[1] in EIB_VARIABLES:
            memory_area = SELF_REFERENCE + EIB_MEMORY
        elif tokens[3] in SPECIAL_REGISTERS_VARIABLES:
                memory_area = SELF_REFERENCE + "SPECIALREGISTERSMemory"
        mod = "Get_Variable_Value(" + memory_area + COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + tokens[1] + "','" + tokens[1] + "')"
    elif tokens[1] == LENGTH_KEYWORD:
        t = 2
        if tokens[2] == OF_KEYWORD:
            t = 3
        mod = "Get_Variable_Length(" + SELF_REFERENCE + VARIABLES_LIST_NAME + COMMA + SINGLE_QUOTE + tokens[t] + SINGLE_QUOTE + CLOSE_PARENS

    if tokens[0] == COBOL_VERB_MULTIPLY:
        mod = "'" + tokens[3] + "'"
        target = tokens[1]
        if tokens[3].lstrip('+-').isdigit() == False:
            memory_area = SELF_REFERENCE + name + MEMORY
            if tokens[3] in EIB_VARIABLES:
                memory_area = SELF_REFERENCE + EIB_MEMORY
            elif tokens[3] in SPECIAL_REGISTERS_VARIABLES:
                memory_area = SELF_REFERENCE + "SPECIALREGISTERSMemory"
            mod = "Get_Variable_Value(" + memory_area + "," + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'" + tokens[3] + "','" + tokens[3] + "')"

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
    
    return

def check_valid_verb(v: str, compare_verb: str, include_search_multi_verb):
    if v.endswith(PERIOD):
        v = v[0:len(v) - 1]
    if include_search_multi_verb == True:
        for multi_verb in COBOL_VERB_MULTI_LIST:
            if multi_verb[0] == compare_verb and multi_verb[1] == v:
                return False
            elif multi_verb[0] == compare_verb and multi_verb[1].startswith('!') and v != multi_verb[1:]:
                return False

    if v in COBOL_VERB_LIST or v in PYTHON_TO_COBOL_VERBS or v.startswith(COBOL_VERB_WHEN + OPEN_PARENS):
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
    elif operator == EQUAL_KEYWORD:
        return DOUBLE_EQUALS
    elif operator == GREATER_KEYWORD:
        return GREATER_THAN
    elif operator == DIVISION_OPERATOR:
        return DIVISION_OPERATOR + DIVISION_OPERATOR
    
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