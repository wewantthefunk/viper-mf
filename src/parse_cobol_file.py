from util import read_raw_file_lines
from cobol_lexicon import *
from cobol_line_process import *
from util import *
from cobol_util import *
import cobol_pre_processor

args = []

def parse_cobol_file(file: str, target_dir: str, dep_dir = EMPTY_STRING):
    global args
    args = []
    c_file = cobol_pre_processor.main(file)
    r_lines = read_raw_file_lines(c_file, 0) 
    #delete_file(c_file)
    raw_lines = prep_source(r_lines)

    lines = []
    current_division = EMPTY_STRING
    name = "abend"
    first_time = False
    current_line = LexicalInfo()
    current_line.source_filename = file
    current_line.level = BASE_LEVEL
    current_line.current_line_number = ZERO
    current_line.last_cmd_display = False
    current_line.last_known_paragraph = EMPTY_STRING
    current_line.paragraph_list = []

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
        if current_line.next_available_line != EMPTY_STRING:
            if current_line.next_available_line == line:
                current_line.next_available_line = EMPTY_STRING
            else:
                continue
        elif skip_the_next_lines_count == current_line.skip_the_next_lines:
            skip_the_next_lines_count = 0
            current_line.skip_the_next_lines = 0
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
        process_verb(lambda_func, name, True, BASE_LEVEL, args, current_line, [])      
        process_verb([VERB_RESET], name, True, BASE_LEVEL, [], current_line, [])  
        append_file(name + PYTHON_EXT, pad(len(INDENT) * BASE_LEVEL) + RETURN_KEYWORD + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 1)) + PYTHON_EXCEPT_STATEMENT + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * BASE_LEVEL) + SELF_REFERENCE + MAIN_ERROR_FUNCTION + OPEN_PARENS + CLOSE_PARENS + NEWLINE)
        append_file(name + PYTHON_EXT, NEWLINE)

    if len(current_line.paragraph_list) > 0:
        if current_line.last_cmd_display:
            append_file(name + PYTHON_EXT, pad(len(INDENT) * BASE_LEVEL) + "Display_Variable(" + SELF_REFERENCE + name + MEMORY + "," + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'','literal',True,True)" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * BASE_LEVEL) + "if fallthru:" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL + 1)) + "self.fallthrough('" + current_line.last_known_paragraph + SINGLE_QUOTE + CLOSE_PARENS + NEWLINE)
        

    if current_line.needs_except_block:
        append_file(name + PYTHON_EXT, NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 1)) + PYTHON_EXCEPT_STATEMENT + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL)) + SELF_REFERENCE + MAIN_ERROR_FUNCTION + OPEN_PARENS + "e" + CLOSE_PARENS + NEWLINE)

    append_file(name + PYTHON_EXT, NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 2)) + "def initialize2(self):" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 1)) + SELF_REFERENCE + "is_batch = " + str(not current_line.is_cics) + NEWLINE)
    for pl in current_line.paragraph_list:
        append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 1)) + "self.paragraph_list.append('" + pl + "')\n")
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 1)) + "return" + NEWLINE)
    append_file(name + PYTHON_EXT, NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 2)) + "def default_fallthrough(self):" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 1)) + "if len(self.paragraph_list) > self.last_fallthrough_paragraph:" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL)) + "exec('self.' + self.paragraph_list[self.last_fallthrough_paragraph] + '(True)')" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 1)) + "return" + NEWLINE)
    append_file(name + PYTHON_EXT, NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 2)) + "def fallthrough(self, name):" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 1)) + "if self.error_triggered:" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL)) + "return" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 1)) + "count = 0" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 1)) + "for pl in self.paragraph_list:" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL)) + "if pl == name and count + 1 < len(self.paragraph_list):" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL + 1)) + "self.last_fallthrough_paragraph = count + 1" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL + 1)) + "# jump to the next paragraph" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL + 1)) + "exec('self.' + self.paragraph_list[count + 1] + '(True)')" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL + 1)) + "break" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL)) + "count = count + 1" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 1)) + "return" + NEWLINE)
    append_file(name + PYTHON_EXT, NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 2)) + "def retrieve_pointer(self, name):" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 1)) + "return Get_Variable_Value(" + SELF_REFERENCE + name + MEMORY + COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + COMMA + 'name, name' + CLOSE_PARENS + NEWLINE)
    append_file(name + PYTHON_EXT, NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 2)) + "def set_value(self, name, value):" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 1)) + SELF_REFERENCE + name + MEMORY + " = Set_Variable(" + SELF_REFERENCE + name + MEMORY + COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + COMMA + 'name, value, name' + CLOSE_PARENS + "[1]" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 1)) + "return" + NEWLINE)
    append_file(name + PYTHON_EXT, NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 2)) + "def get_value(self, name):" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 1)) + "return Get_Variable_Value(" + SELF_REFERENCE + name + MEMORY + ", self.variables_list, name, name)" + NEWLINE)
    append_file(name + PYTHON_EXT, NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 2)) + "def print_out(self, val, end_l):" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 1)) + "print(val, end=end_l)" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 1)) + "return" + NEWLINE)
    append_file(name + PYTHON_EXT, NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 2)) + "def receive_control(self):" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 1)) + "pass" + NEWLINE)
    append_file(name + PYTHON_EXT, NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 2)) + "def get_return_code(self):" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 1)) + "return Get_Variable_Value(" + SELF_REFERENCE + "SPECIALREGISTERSMemory" + COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + COMMA + '"RETURN-CODE", "RETURN-CODE"' + CLOSE_PARENS + NEWLINE)
    append_file(name + PYTHON_EXT, NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 2)) + "def terminate_on_callback(self):" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 1)) + SELF_REFERENCE + "terminate = True" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 1)) + "return" + NEWLINE)
    append_file(name + PYTHON_EXT, NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 2)) + "def get_dd_value(self, value: str):" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 1)) + "result = 'UNKNOWN'" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 1)) + "for dd in self.dd_name_list:" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL))     + "if len(dd) > 1:" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL + 1)) + "if dd[0].strip() == value.strip():" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL + 2)) + "result = dd[1].strip()" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL + 2)) + "break" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 1)) + "return result" + NEWLINE)
    append_file(name + PYTHON_EXT, NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 2)) + "def process_key(self, keycode: int):\n")
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 1)) + "if keycode == 27 or keycode == 13 or (keycode >= 110 and keycode <= 123):\n")
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 0)) + "return True\n")
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 1)) + "return False\n")
    append_file(name + PYTHON_EXT, NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 2)) + "def _error_handler(self, e):" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 1)) + SELF_REFERENCE + "error_triggered = True" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 1)) + "if " + SELF_REFERENCE + CLASS_ERROR_FUNCTION_MEMBER  + " != None:" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL)) + SELF_REFERENCE + CLASS_ERROR_FUNCTION_MEMBER + OPEN_PARENS + CLOSE_PARENS + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 1)) + "else:" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL)) + SELF_REFERENCE + "SPECIALREGISTERSMemory = Set_Variable(self.SPECIALREGISTERSMemory,self.variables_list,'RETURN-CODE', 12,'RETURN-CODE')[1]" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL)) + "print('')" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL)) + "print('error encountered:')"+ NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL)) + "print(e)" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL)) + "exc_type, exc_obj, exc_tb = sys.exc_info()" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL)) + "fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL)) + "print(exc_type, fname, exc_tb.tb_lineno)" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL)) + "print('COBOL Source File:      " + current_line.source_filename + "')" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL)) + "print('COBOL File Line Number: ' + self.debug_line)" + NEWLINE)
    append_file(name + PYTHON_EXT, pad(len(INDENT) * (BASE_LEVEL - 1)) + "return" + NEWLINE)
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

    print("completed conversion of " + file + " to --> " + target_dir + name + PYTHON_EXT)

    if current_line.total_copybooks_inserted > 0:
        print(pad(len(INDENT)) + "total copybooks inserted: " + str(current_line.total_copybooks_inserted))

    if current_line.unknown_cobol_verbs > 0:
        print(pad(len(INDENT)) + "unknown COBOL statements: " + str(current_line.unknown_cobol_verbs))

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
    old_division_name = EMPTY_STRING
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
            old_division_name = current_division
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
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + "is_batch = True" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + "call_result = None" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + "terminate = False" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + "paragraph_list = []" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + "last_fallthrough_paragraph = 0" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + "debug_line = '0'" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + "error_triggered = False" + NEWLINE)
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
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + "_INTERNALVars = Add_Variable(self.SPECIALREGISTERSMemory, self._INTERNALVars, 'RETURN-CODE', 4, '9', 'RETURN-CODE', '', 0, 0, '', '01')[0]" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + "result = Allocate_Memory(" + SELF_REFERENCE + "_INTERNALVars," + SELF_REFERENCE + "SPECIALREGISTERSMemory)" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + "_INTERNALVars = result[0]" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + "SPECIALREGISTERSMemory = result[1]" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + "SPECIALREGISTERSMemory = Set_Variable(self.SPECIALREGISTERSMemory,self.variables_list,'SORT-RETURN', 0,'SORT-RETURN')[1]" + NEWLINE)
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + SELF_REFERENCE + "SPECIALREGISTERSMemory = Set_Variable(self.SPECIALREGISTERSMemory,self.variables_list,'RETURN-CODE', 0,'RETURN-CODE')[1]" + NEWLINE)
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
        append_file(name + PYTHON_EXT, pad(len(INDENT) * 2) + "self.initialize2()" + NEWLINE)
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
    #parse_cobol_file("examples/hellowo1_basic.cbl", "converted/")
    parse_cobol_file("work/CONVCOPY.cbl", "converted/")
