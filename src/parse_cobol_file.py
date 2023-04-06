from util import read_raw_file_lines
from cobol_lexicon import *
from cobol_line_process import *
from util import *

args = []

def parse_cobol_file(file: str, target_dir: str, dep_dir = EMPTY_STRING):
    global args
    args = []
    r_lines = read_raw_file_lines(file, 0)

    raw_lines = []

    count = 0
    start_tracking_line_number = False
    for rl in r_lines:
        count = count + 1
        rl = rl.replace(NEWLINE, EMPTY_STRING)
        if len(rl) < 7:
            rl = EMPTY_STRING

        if rl == EMPTY_STRING:
            continue
        if rl.strip().startswith("CBL "):
            continue
        if (rl[6] != COBOL_COMMENT and rl[7:] != EMPTY_STRING):
            if " PROCEDURE DIVISION" in rl:
                start_tracking_line_number = True

            if rl[6:7] == "-":
                line = rl[6:]
            else:
                line = rl[7:]
            t_line = line.split(SPACE, 1)
            l = pad(7) + t_line[0] + SPACE
            if len(t_line) > 1:
                if (SPACE + OPEN_PARENS) in t_line[1]:
                    sp = t_line[1].split(OPEN_PARENS)
                    pl = EMPTY_STRING
                    first = True
                    for s in sp:
                        if first == False:
                            pl = pl + OPEN_PARENS
                        else:
                            first = False
                        pl = pl + s.strip()

                    l = l + pl
                else:
                    l = l + t_line[1]
            if start_tracking_line_number:
                if " PROCEDURE DIVISION" not in rl:
                    l = l + "^^^" + str(count)
                else:
                    l = rl
            raw_lines.append(l)

    lines = []
    current_division = EMPTY_STRING
    name = "abend"
    first_time = False
    current_line = LexicalInfo()
    current_line.source_filename = file
    current_line.level = BASE_LEVEL
    current_line.current_line_number = ZERO

    total = len(raw_lines)
    count = 0
    skip_the_next_lines_count = 0
    for l1 in raw_lines:
        l1s = l1.split("^^^")
        line = l1s[0]
        if len(l1s) > 1:
            current_line.current_line_number = l1s[1]
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
        result = parse_line(line, current_division, name, first_time, current_line, next_few_lines)
        tmp = result[0]
        current_division = result[1]
        name = result[2]
        first_time = result[3]
        current_line = result[4]
        if tmp != EMPTY_STRING:
            lines.append(tmp)
        if current_division == ABEND:
            break

    x = get_last_line_of_file(name + PYTHON_EXT)
    lc = 0
    for lambda_func in current_line.lambda_functions:
        lc = lc + 1
        append_file(name + PYTHON_EXT, NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 2)) + "def _ae" + str(lc) + "(self):" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 1)) + PYTHON_TRY_STATEMENT + NEWLINE)
        process_verb(lambda_func, name, True, BASE_LEVEL, args, current_line)      
        process_verb([VERB_RESET], name, True, BASE_LEVEL, [], current_line)  
        append_file(name + PYTHON_EXT, pad(len(INDENT) * BASE_LEVEL) + RETURN_KEYWORD + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 1)) + PYTHON_EXCEPT_STATEMENT + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * BASE_LEVEL) + SELF_REFERENCE + MAIN_ERROR_FUNCTION + OPEN_PARENS + CLOSE_PARENS + NEWLINE)
        append_file(name + PYTHON_EXT, NEWLINE)

    if current_line.needs_except_block:
        append_file(name + PYTHON_EXT, NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 1)) + PYTHON_EXCEPT_STATEMENT + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL)) + SELF_REFERENCE + MAIN_ERROR_FUNCTION + OPEN_PARENS + "e" + CLOSE_PARENS + NEWLINE)

    append_file(name + PYTHON_EXT, NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 2)) + "def retrieve_pointer(self, pos):" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 1)) + "pass" + NEWLINE)
    append_file(name + PYTHON_EXT, NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 2)) + "def receive_control(self):" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 1)) + "pass" + NEWLINE)
    append_file(name + PYTHON_EXT, NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 2)) + "def terminate_on_callback(self):" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 1)) + SELF_REFERENCE + "terminate = True" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 1)) + "return" + NEWLINE)
    append_file(name + PYTHON_EXT, NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 2)) + "def _error_handler(self, e):" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 1)) + "if " + SELF_REFERENCE + CLASS_ERROR_FUNCTION_MEMBER  + " != None:" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL)) + SELF_REFERENCE + CLASS_ERROR_FUNCTION_MEMBER + OPEN_PARENS + CLOSE_PARENS + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 1)) + "else:" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL)) + "print('')" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL)) + "print('error encountered:')"+ NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL)) + "print(e)" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL)) + "exc_type, exc_obj, exc_tb = sys.exc_info()" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL)) + "fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL)) + "print(exc_type, fname, exc_tb.tb_lineno)" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL)) + "print('COBOL Source File:      " + current_line.source_filename + "')" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL)) + "print('COBOL File Line Number: ' + self.debug_line)" + NEWLINE)
    append_file(name + PYTHON_EXT, NEWLINE)
    append_file(name + PYTHON_EXT, "if __name__ == '__main__':" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT)) + "main_obj = " + name + "Class()" + NEWLINE + pad(len(INDENT)))
    
    if len(args) > 0:
        append_file(name + PYTHON_EXT, "print" + OPEN_PARENS)

    append_file(name + PYTHON_EXT, "main_obj.main" + OPEN_PARENS + "main_obj")

    arg_count = 0
    if len(args) > 0:
        for x in range(0, len(args)):
            if x > 2:
                append_file(name + PYTHON_EXT, COMMA)
            if x > 2:
                arg_count = arg_count + 1
                append_file(name + PYTHON_EXT, "'arg" + str(arg_count) + SINGLE_QUOTE)

    append_file(name + PYTHON_EXT, CLOSE_PARENS)

    if len(args) > 0:
        append_file(name + PYTHON_EXT, CLOSE_PARENS)

    append_file(name + PYTHON_EXT, NEWLINE + pad(len(INDENT)) + "Cleanup()" + NEWLINE)

    append_file(name + PYTHON_EXT, NEWLINE)

    if len(current_line.import_statement) > 0:
        insert(name + PYTHON_EXT, current_line.import_statement)

    move_file(name + PYTHON_EXT, target_dir + name + PYTHON_EXT)

    copy_file(dep_dir + "dependencies/cobol_variable.py", target_dir + "cobol_variable.py")

def insert(originalfile,imports):
    for imp in imports:
        insert_beginning_of_file(originalfile, "from " + imp + " import *" + NEWLINE)        

def parse_line(line: str, current_division: str, name: str, first_time: bool, current_line: LexicalInfo, next_few_lines):
    tmp = line[6:].replace(NEWLINE, EMPTY_STRING).strip()
    if tmp == EMPTY_STRING or tmp.startswith(COBOL_COMMENT):
        return [EMPTY_STRING, current_division, name, first_time, current_line]
    else:
        result = parse_current_line(tmp, current_division, name, first_time, current_line, next_few_lines)
        current_division = result[0]
        name = result[1]
        first_time = result[2]
        current_line = result[3]
        if current_division == ABEND:
            return [EMPTY_STRING, ABEND, name, first_time, current_line]

        return [tmp, current_division, name, first_time, current_line]

def parse_current_line(line: str, current_division: str, name: str, first_time: bool, current_line: LexicalInfo, next_few_lines):
    global args
    if current_division == EMPTY_STRING:
        if not line.startswith(COBOL_DIVISIONS[0]) \
            and not line.startswith(COBOL_DIVISIONS[1]):
            print("invalid syntax -> first line MUST be 'IDENTIFICATION DIVISION.' or 'ID DIVISION.'")
            return ABEND
        else:
            first_time = True

    new_division = False
    for division in COBOL_DIVISIONS:
        if line.startswith(division):
            current_division = division
            new_division = True
            if division == COBOL_DIVISIONS[PROCEDURE_DIVISION_POS]:
                create_index_variables(current_line.index_variables, name)
                allocate_variables(current_line, name)
                init_vars(name, args, current_line)
            break

    if not new_division:
        result = process_line(line, current_division, name, current_line, next_few_lines)
        current_division = result[0]
        name = result[1]
        current_line = result[2]
    else:
        if name != "abend":            
            first_time = False
            if current_division == COBOL_DIVISIONS[PROCEDURE_DIVISION_POS]:
                append_file(name + PYTHON_EXT, "# EIB Fields" + NEWLINE)
                insert_copybook(name + PYTHON_EXT, EIB_COPYBOOK, current_line, name, current_line.current_section, next_few_lines, args)
                append_file(name + PYTHON_EXT, "# " + current_division + NEWLINE)
                append_file(name + PYTHON_EXT, pad(len(INDENT) * 1) + "def main" + OPEN_PARENS + "self,caller")

                if USING_KEYWORD in line:
                    args = parse_line_tokens(line, SPACE, EMPTY_STRING, False)
                    count = 0
                    arg_count = 0
                    for arg in args:
                        if count > 2:
                            arg_count = arg_count + 1
                            append_file(name + PYTHON_EXT, COMMA + MAIN_ARG_VARIABLE_PREFIX + str(arg_count))
                        count = count + 1
                
                append_file(name + PYTHON_EXT, ",*therest" + CLOSE_PARENS + COLON + NEWLINE)
                append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + "try:" + NEWLINE)
                append_file(name + PYTHON_EXT, pad(len(INDENT) * 3) + SELF_REFERENCE + EIB_MEMORY + EQUALS + "Retrieve_EIB_Area(" + SELF_REFERENCE + "_INTERNALVars[0].value" + CLOSE_PARENS + NEWLINE)
                append_file(name + PYTHON_EXT, pad(len(INDENT) * 3) + SELF_REFERENCE + CALLING_MODULE_MEMBER + " = caller" + NEWLINE)
                append_file(name + PYTHON_EXT, pad(len(INDENT) * 3) + SELF_REFERENCE + "_INTERNALVars[1].value = " + SINGLE_QUOTE + ADDRESS_INDICATOR + SINGLE_QUOTE + NEWLINE)
                append_file(name + PYTHON_EXT, pad(len(INDENT) * 3) + SELF_REFERENCE + "_INTERNALVars[1].address_module = AddressModule(caller, 0)" + NEWLINE)

                count = 0
                arg_count = 0
                for arg in args:
                    if count > 2:
                        arg_count = arg_count + 1
                        process_procedure_division_line("MOVE " + MAIN_ARG_VARIABLE_PREFIX + str(arg_count) + " TO " + arg.replace(COMMA, EMPTY_STRING) + PERIOD, name, current_line, [], args)
                    count = count + 1

                current_line.needs_except_block = True
            else:
                append_file(name + PYTHON_EXT, "# " + current_division + NEWLINE)

    return [current_division, name, first_time, current_line]

def process_line(line: str, current_division: str, name: str, current_line: LexicalInfo, next_few_lines):
    global args
    if current_division == COBOL_DIVISIONS[IDENTIFICATION_DIVISION_POS] \
        or current_division == COBOL_DIVISIONS[ID_DIVISION_POS]:
        name = process_identification_division_line(line, name)
        write_file(name + PYTHON_EXT, "from cobol_variable import *" + NEWLINE)
        append_file(name + PYTHON_EXT, "import importlib, inspect, os, sys" + NEWLINE)
        
        append_file(name + PYTHON_EXT, "# PROGRAM-ID: " + name + NEWLINE)
        append_file(name + PYTHON_EXT, "class " + name + "Class:" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 1) + "def __init__(self):" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + "call_result = None" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + "terminate = False" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + "debug_line = '0'" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + CALLING_MODULE_MEMBER + " = None" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + name + MEMORY + " = EMPTY_STRING" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + EIB_MEMORY + " = EMPTY_STRING" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + "SPECIALREGISTERSMemory" + " = EMPTY_STRING" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + VARIABLES_LIST_NAME + " = []" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + "_INTERNALVars = []" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + VARIABLES_LIST_NAME + ".append(self._INTERNALVars)" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + "_INTERNALVars = Add_Variable('', self._INTERNALVars, 'MODULE-NAME', 0, 'X', 'MODULE-NAME', '', 0, 0, '', '01')[0]" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + "_INTERNALVars[0].value = " + SINGLE_QUOTE + name + SINGLE_QUOTE + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + "_INTERNALVars[0].address_module = AddressModule(self, 0)" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + "_INTERNALVars = Add_Variable('', self._INTERNALVars, 'CALLING-MODULE-NAME', 0, 'X', 'CALLING-MODULE-NAME', '', 0, 0, '', '01')[0]" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + "_INTERNALVars = Add_Variable(self.SPECIALREGISTERSMemory, self._INTERNALVars, 'SORT-RETURN', 4, '9', 'SORT-RETURN', '', 0, 0, '', '01')[0]" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + "result = Allocate_Memory(" + SELF_REFERENCE + "_INTERNALVars," + SELF_REFERENCE + "SPECIALREGISTERSMemory)" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + "_INTERNALVars = result[0]" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + "SPECIALREGISTERSMemory = result[1]" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + "SPECIALREGISTERSMemory = Set_Variable(self.SPECIALREGISTERSMemory,self.variables_list,'SORT-RETURN', 0,'SORT-RETURN')[1]" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + CLASS_ERROR_FUNCTION_MEMBER + SPACE + EQUALS + SPACE + NONE_KEYWORD + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + CALLING_MODULE_MEMBER + SPACE + EQUALS + SPACE + NONE_KEYWORD + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + JOB_NAME_MEMBER + SPACE + EQUALS + SPACE + "EMPTY_STRING" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + JOB_STEP_MEMBER + SPACE + EQUALS + SPACE + "EMPTY_STRING" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + DD_NAME_LIST + SPACE + EQUALS + SPACE + "[]" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + "self._DataDivisionVars = []" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + VARIABLES_LIST_NAME + ".append(" + SELF_REFERENCE + "_DataDivisionVars)" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + "self.EIBList = []" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + VARIABLES_LIST_NAME + ".append(" + SELF_REFERENCE + "EIBList)" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + "self._FILE_CONTROLVars = []" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + "initialize()" + NEWLINE)
    elif current_division == COBOL_DIVISIONS[ENVIRONMENT_DIVISION_POS]:
        result = process_environment_division_line(line, current_line.current_section, name, current_line, next_few_lines, args)
    elif current_division == COBOL_DIVISIONS[DATA_DIVISION_POS]:
        result = process_data_division_line(line, current_line.current_section, name, current_line, next_few_lines, args)
        current_line.current_section = result[1]
        if result[1] not in current_line.sections_list:
            current_line.sections_list.append(result[1])
    elif current_division == COBOL_DIVISIONS[PROCEDURE_DIVISION_POS]:
        result = process_procedure_division_line(line, name, current_line, next_few_lines, args)
        current_line.level = result[1]
        current_line.skip_the_next_lines = result[0]

    return [current_division, name, current_line]

if __name__ == "__main__":
    #parse_cobol_file("examples/CMNDATCV.cobol", "converted/")
    #parse_cobol_file("examples/CMNDATCT.cobol", "converted/")
    #parse_cobol_file("examples/COMPL001.cbl", "converted/")
    #parse_cobol_file("examples/cics02_link.cbl", "converted/")
    #parse_cobol_file("examples/hellowo1_basic.cbl", "converted/")
    #parse_cobol_file("examples/hellowo2_variable.cbl", "converted/")
    #parse_cobol_file("examples/hellowo3_hierarchical_variables.cbl", "converted/")
    #parse_cobol_file("examples/hellowo4_paragraph.cbl", "converted/")
    #parse_cobol_file("examples/hellow65_multi_dimensional_array.cbl", "converted/")
    #parse_cobol_file("examples/hellow38_search_table_redefined_literals.cbl", "converted/")
    #parse_cobol_file("examples/hellow23_search_statement.cbl", "converted/")
    #parse_cobol_file("examples/hellow64_dfhcommarea_receive.cbl", "converted/")
    #parse_cobol_file("examples/hellow37_call_receive_function_with_variables.cbl", "converted/")
    #parse_cobol_file("examples/cics06_return.cbl", "converted/")
    #parse_cobol_file("work/CUTE2B123.cobol", "converted/")
    #parse_cobol_file("work/cabbsmbd-work.cbl", "converted/")
    #parse_cobol_file("dependencies/GETDSNS.cbl", "converted/")
    #parse_cobol_file("dependencies/CEE3AB2.cbl", "converted/")
    parse_cobol_file("examples/hellow12_sequential_file_access.cbl", "converted/")
    #parse_cobol_file("examples/hellow75_indexed_file_access.cbl", "converted/")  
    #parse_cobol_file("examples/hellowo6_array.cbl", "converted/")
    #parse_cobol_file("examples/hellow76_indexed_file_write.cbl", "converted/")
    #parse_cobol_file("dependencies/RANDSTR.cbl", "converted/")
    parse_cobol_file("examples/hellow68_address_of_function.cbl", "converted/")