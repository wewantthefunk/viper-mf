"""
Emission of Python class skeleton and footer for Cobra-generated programs.
"""
from cobol_lexicon import (
    BASE_LEVEL, NEWLINE, INDENT, SELF_REFERENCE, MEMORY, VARIABLES_LIST_NAME,
    EIB_MEMORY, CALLING_MODULE_MEMBER, CLASS_ERROR_FUNCTION_MEMBER,
    JOB_NAME_MEMBER, JOB_STEP_MEMBER, DD_NAME_LIST, SINGLE_QUOTE,
    NONE_KEYWORD, SPACE, MAIN_ERROR_FUNCTION, OPEN_PARENS, CLOSE_PARENS, COMMA,
    PYTHON_EXT, USING_KEYWORD, MAIN_ARG_VARIABLE_PREFIX, ADDRESS_INDICATOR,
    EIB_COPYBOOK, COLON, EQUALS, PERIOD, EMPTY_STRING,
)
from util import parse_line_tokens
from cobol_line_process import insert_copybook, process_procedure_division_line


def emit_class_header(writer, name: str) -> None:
    """Emit the Python class skeleton (imports, class name, __init__, instance vars)."""
    writer.write_overwrite("from cobol_variable import *" + NEWLINE)
    writer.write("import importlib, inspect, os, sys" + NEWLINE)
    writer.write("# PROGRAM-ID: " + name + NEWLINE)
    writer.write("class " + name + "Class:" + NEWLINE)
    writer.write(writer.indent(1) + "def __init__(self):" + NEWLINE)
    writer.write(writer.indent(2) + SELF_REFERENCE + "is_batch = True" + NEWLINE)
    writer.write(writer.indent(2) + SELF_REFERENCE + "call_result = None" + NEWLINE)
    writer.write(writer.indent(2) + SELF_REFERENCE + "terminate = False" + NEWLINE)
    writer.write(writer.indent(2) + SELF_REFERENCE + "paragraph_list = []" + NEWLINE)
    writer.write(writer.indent(2) + SELF_REFERENCE + "last_fallthrough_paragraph = 0" + NEWLINE)
    writer.write(writer.indent(2) + SELF_REFERENCE + "debug_line = '0'" + NEWLINE)
    writer.write(writer.indent(2) + SELF_REFERENCE + "error_triggered = False" + NEWLINE)
    writer.write(writer.indent(2) + SELF_REFERENCE + CALLING_MODULE_MEMBER + " = None" + NEWLINE)
    writer.write(writer.indent(2) + SELF_REFERENCE + name + MEMORY + " = EMPTY_STRING" + NEWLINE)
    writer.write(writer.indent(2) + SELF_REFERENCE + EIB_MEMORY + " = EMPTY_STRING" + NEWLINE)
    writer.write(writer.indent(2) + SELF_REFERENCE + "SPECIALREGISTERSMemory" + " = EMPTY_STRING" + NEWLINE)
    writer.write(writer.indent(2) + SELF_REFERENCE + VARIABLES_LIST_NAME + " = []" + NEWLINE)
    writer.write(writer.indent(2) + SELF_REFERENCE + "_INTERNALVars = []" + NEWLINE)
    writer.write(writer.indent(2) + SELF_REFERENCE + VARIABLES_LIST_NAME + ".append(self._INTERNALVars)" + NEWLINE)
    writer.write(writer.indent(2) + SELF_REFERENCE + "_INTERNALVars = Add_Variable('', self._INTERNALVars, 'MODULE-NAME', 0, 'X', 'MODULE-NAME', '', 0, 0, '', '01')[0]" + NEWLINE)
    writer.write(writer.indent(2) + SELF_REFERENCE + "_INTERNALVars[0].value = " + SINGLE_QUOTE + name + SINGLE_QUOTE + NEWLINE)
    writer.write(writer.indent(2) + SELF_REFERENCE + "_INTERNALVars[0].address_module = AddressModule(self, 0)" + NEWLINE)
    writer.write(writer.indent(2) + SELF_REFERENCE + "_INTERNALVars = Add_Variable('', self._INTERNALVars, 'CALLING-MODULE-NAME', 0, 'X', 'CALLING-MODULE-NAME', '', 0, 0, '', '01')[0]" + NEWLINE)
    writer.write(writer.indent(2) + SELF_REFERENCE + "_INTERNALVars = Add_Variable(self.SPECIALREGISTERSMemory, self._INTERNALVars, 'SORT-RETURN', 4, '9', 'SORT-RETURN', '', 0, 0, '', '01')[0]" + NEWLINE)
    writer.write(writer.indent(2) + SELF_REFERENCE + "_INTERNALVars = Add_Variable(self.SPECIALREGISTERSMemory, self._INTERNALVars, 'RETURN-CODE', 4, '9', 'RETURN-CODE', '', 0, 0, '', '01')[0]" + NEWLINE)
    writer.write(writer.indent(2) + "result = Allocate_Memory(" + SELF_REFERENCE + "_INTERNALVars," + SELF_REFERENCE + "SPECIALREGISTERSMemory)" + NEWLINE)
    writer.write(writer.indent(2) + SELF_REFERENCE + "_INTERNALVars = result[0]" + NEWLINE)
    writer.write(writer.indent(2) + SELF_REFERENCE + "SPECIALREGISTERSMemory = result[1]" + NEWLINE)
    writer.write(writer.indent(2) + SELF_REFERENCE + "SPECIALREGISTERSMemory = Set_Variable(self.SPECIALREGISTERSMemory,self.variables_list,'SORT-RETURN', 0,'SORT-RETURN')[1]" + NEWLINE)
    writer.write(writer.indent(2) + SELF_REFERENCE + "SPECIALREGISTERSMemory = Set_Variable(self.SPECIALREGISTERSMemory,self.variables_list,'RETURN-CODE', 0,'RETURN-CODE')[1]" + NEWLINE)
    writer.write(writer.indent(2) + SELF_REFERENCE + CLASS_ERROR_FUNCTION_MEMBER + SPACE + "=" + SPACE + NONE_KEYWORD + NEWLINE)
    writer.write(writer.indent(2) + SELF_REFERENCE + CALLING_MODULE_MEMBER + SPACE + "=" + SPACE + NONE_KEYWORD + NEWLINE)
    writer.write(writer.indent(2) + SELF_REFERENCE + JOB_NAME_MEMBER + SPACE + "=" + SPACE + "EMPTY_STRING" + NEWLINE)
    writer.write(writer.indent(2) + SELF_REFERENCE + JOB_STEP_MEMBER + SPACE + "=" + SPACE + "EMPTY_STRING" + NEWLINE)
    writer.write(writer.indent(2) + SELF_REFERENCE + DD_NAME_LIST + SPACE + "=" + SPACE + "[]" + NEWLINE)
    writer.write(writer.indent(2) + "self._DataDivisionVars = []" + NEWLINE)
    writer.write(writer.indent(2) + SELF_REFERENCE + VARIABLES_LIST_NAME + ".append(" + SELF_REFERENCE + "_DataDivisionVars)" + NEWLINE)
    writer.write(writer.indent(2) + "self.EIBList = []" + NEWLINE)
    writer.write(writer.indent(2) + SELF_REFERENCE + VARIABLES_LIST_NAME + ".append(" + SELF_REFERENCE + "EIBList)" + NEWLINE)
    writer.write(writer.indent(2) + "self._FILE_CONTROLVars = []" + NEWLINE)
    writer.write(writer.indent(2) + "initialize()" + NEWLINE)
    writer.write(writer.indent(2) + "self.initialize2()" + NEWLINE)


def emit_procedure_division_preamble(context, division_name: str, line: str, next_few_lines) -> None:
    """Emit EIB copybook, def main(self, caller, ...), and USING arg handling."""
    writer = context.writer
    name = context.program_name
    current_line = context.lexical_info
    writer.write("# EIB Fields" + NEWLINE)
    insert_copybook(writer, EIB_COPYBOOK, current_line, name, current_line.current_section, next_few_lines, context)
    writer.write("# " + division_name + NEWLINE)
    writer.write(writer.indent(1) + "def main" + OPEN_PARENS + "self,caller")
    if USING_KEYWORD in line:
        context.args = parse_line_tokens(line, SPACE, EMPTY_STRING, False)
    count = 0
    arg_count = 0
    for arg in context.args:
        if count > 2:
            arg_count = arg_count + 1
            writer.write(COMMA + MAIN_ARG_VARIABLE_PREFIX + str(arg_count))
        count = count + 1
    writer.write(",*therest" + CLOSE_PARENS + COLON + NEWLINE)
    writer.write(writer.indent(2) + "try:" + NEWLINE)
    writer.write(writer.indent(3) + SELF_REFERENCE + EIB_MEMORY + EQUALS + "Retrieve_EIB_Area(" + SELF_REFERENCE + "_INTERNALVars[0].value" + CLOSE_PARENS + NEWLINE)
    writer.write(writer.indent(3) + SELF_REFERENCE + CALLING_MODULE_MEMBER + " = caller" + NEWLINE)
    writer.write(writer.indent(3) + SELF_REFERENCE + "_INTERNALVars[1].value = " + SINGLE_QUOTE + ADDRESS_INDICATOR + SINGLE_QUOTE + NEWLINE)
    writer.write(writer.indent(3) + SELF_REFERENCE + "_INTERNALVars[1].address_module = AddressModule(caller, 0)" + NEWLINE)
    count = 0
    arg_count = 0
    for arg in context.args:
        if count > 2:
            arg_count = arg_count + 1
            process_procedure_division_line("MOVE " + MAIN_ARG_VARIABLE_PREFIX + str(arg_count) + " TO " + arg.replace(COMMA, EMPTY_STRING) + PERIOD, name, current_line, [], context, writer)
        count = count + 1
    current_line.needs_except_block = True


def emit_class_footer(context) -> None:
    """Emit the class footer (lambda helpers, initialize2, fallthrough, retrieve_pointer, main block)."""
    from cobol_lexicon import VERB_RESET
    from cobol_verb_process import process_verb

    writer = context.writer
    name = context.program_name
    current_line = context.lexical_info
    indent = writer.indent

    lc = 0
    for lambda_func in current_line.lambda_functions:
        lc = lc + 1
        writer.write(NEWLINE)
        writer.write(indent(BASE_LEVEL - 2) + "def _ae" + str(lc) + "(self):" + NEWLINE)
        writer.write(indent(BASE_LEVEL - 1) + "try:" + NEWLINE)
        process_verb(lambda_func, name, True, BASE_LEVEL, context.args, current_line, [], writer, context)
        process_verb([VERB_RESET], name, True, BASE_LEVEL, [], current_line, [], writer, context)
        writer.write(indent(BASE_LEVEL) + "return" + NEWLINE)
        writer.write(indent(BASE_LEVEL - 1) + "except Exception as e:" + NEWLINE)
        writer.write(indent(BASE_LEVEL) + SELF_REFERENCE + MAIN_ERROR_FUNCTION + OPEN_PARENS + CLOSE_PARENS + NEWLINE)
        writer.write(NEWLINE)

    if len(current_line.paragraph_list) > 0:
        if current_line.last_cmd_display:
            writer.write(indent(BASE_LEVEL) + "Display_Variable(" + SELF_REFERENCE + name + MEMORY + "," + SELF_REFERENCE + VARIABLES_LIST_NAME + ",'','literal',True,True)" + NEWLINE)
        writer.write(indent(BASE_LEVEL) + "if fallthru:" + NEWLINE)
        writer.write(indent(BASE_LEVEL + 1) + "self.fallthrough('" + current_line.last_known_paragraph + SINGLE_QUOTE + CLOSE_PARENS + NEWLINE)

    if current_line.needs_except_block:
        writer.write(NEWLINE)
        writer.write(indent(BASE_LEVEL - 1) + "except Exception as e:" + NEWLINE)
        writer.write(indent(BASE_LEVEL) + SELF_REFERENCE + MAIN_ERROR_FUNCTION + OPEN_PARENS + "e" + CLOSE_PARENS + NEWLINE)

    writer.write(NEWLINE)
    writer.write(indent(BASE_LEVEL - 2) + "def initialize2(self):" + NEWLINE)
    writer.write(indent(BASE_LEVEL - 1) + SELF_REFERENCE + "is_batch = " + str(not current_line.is_cics) + NEWLINE)
    for pl in current_line.paragraph_list:
        writer.write(indent(BASE_LEVEL - 1) + "self.paragraph_list.append('" + pl + "')\n")
    writer.write(indent(BASE_LEVEL - 1) + "return" + NEWLINE)
    writer.write(NEWLINE)
    writer.write(indent(BASE_LEVEL - 2) + "def default_fallthrough(self):" + NEWLINE)
    writer.write(indent(BASE_LEVEL - 1) + "if len(self.paragraph_list) > self.last_fallthrough_paragraph:" + NEWLINE)
    writer.write(indent(BASE_LEVEL) + "exec('self.' + self.paragraph_list[self.last_fallthrough_paragraph] + '(True)')" + NEWLINE)
    writer.write(indent(BASE_LEVEL - 1) + "return" + NEWLINE)
    writer.write(NEWLINE)
    writer.write(indent(BASE_LEVEL - 2) + "def fallthrough(self, name):" + NEWLINE)
    writer.write(indent(BASE_LEVEL - 1) + "if self.error_triggered:" + NEWLINE)
    writer.write(indent(BASE_LEVEL) + "return" + NEWLINE)
    writer.write(indent(BASE_LEVEL - 1) + "count = 0" + NEWLINE)
    writer.write(indent(BASE_LEVEL - 1) + "for pl in self.paragraph_list:" + NEWLINE)
    writer.write(indent(BASE_LEVEL) + "if pl == name and count + 1 < len(self.paragraph_list):" + NEWLINE)
    writer.write(indent(BASE_LEVEL + 1) + "self.last_fallthrough_paragraph = count + 1" + NEWLINE)
    writer.write(indent(BASE_LEVEL + 1) + "# jump to the next paragraph" + NEWLINE)
    writer.write(indent(BASE_LEVEL + 1) + "exec('self.' + self.paragraph_list[count + 1] + '(True)')" + NEWLINE)
    writer.write(indent(BASE_LEVEL + 1) + "break" + NEWLINE)
    writer.write(indent(BASE_LEVEL) + "count = count + 1" + NEWLINE)
    writer.write(indent(BASE_LEVEL - 1) + "return" + NEWLINE)
    writer.write(NEWLINE)
    writer.write(indent(BASE_LEVEL - 2) + "def retrieve_pointer(self, name):" + NEWLINE)
    writer.write(indent(BASE_LEVEL - 1) + "return Get_Variable_Value(" + SELF_REFERENCE + name + MEMORY + COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + COMMA + 'name, name' + CLOSE_PARENS + NEWLINE)
    writer.write(NEWLINE)
    writer.write(indent(BASE_LEVEL - 2) + "def set_value(self, name, value):" + NEWLINE)
    writer.write(indent(BASE_LEVEL - 1) + SELF_REFERENCE + name + MEMORY + " = Set_Variable(" + SELF_REFERENCE + name + MEMORY + COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + COMMA + 'name, value, name' + CLOSE_PARENS + "[1]" + NEWLINE)
    writer.write(indent(BASE_LEVEL - 1) + "return" + NEWLINE)
    writer.write(NEWLINE)
    writer.write(indent(BASE_LEVEL - 2) + "def get_value(self, name):" + NEWLINE)
    writer.write(indent(BASE_LEVEL - 1) + "return Get_Variable_Value(" + SELF_REFERENCE + name + MEMORY + ", self.variables_list, name, name)" + NEWLINE)
    writer.write(NEWLINE)
    writer.write(indent(BASE_LEVEL - 2) + "def print_out(self, val, end_l):" + NEWLINE)
    writer.write(indent(BASE_LEVEL - 1) + "print(val, end=end_l)" + NEWLINE)
    writer.write(indent(BASE_LEVEL - 1) + "return" + NEWLINE)
    writer.write(NEWLINE)
    writer.write(indent(BASE_LEVEL - 2) + "def receive_control(self):" + NEWLINE)
    writer.write(indent(BASE_LEVEL - 1) + "pass" + NEWLINE)
    writer.write(NEWLINE)
    writer.write(indent(BASE_LEVEL - 2) + "def get_return_code(self):" + NEWLINE)
    writer.write(indent(BASE_LEVEL - 1) + "return Get_Variable_Value(" + SELF_REFERENCE + "SPECIALREGISTERSMemory" + COMMA + SELF_REFERENCE + VARIABLES_LIST_NAME + COMMA + '"RETURN-CODE", "RETURN-CODE"' + CLOSE_PARENS + NEWLINE)
    writer.write(NEWLINE)
    writer.write(indent(BASE_LEVEL - 2) + "def terminate_on_callback(self):" + NEWLINE)
    writer.write(indent(BASE_LEVEL - 1) + SELF_REFERENCE + "terminate = True" + NEWLINE)
    writer.write(indent(BASE_LEVEL - 1) + "return" + NEWLINE)
    writer.write(NEWLINE)
    writer.write(indent(BASE_LEVEL - 2) + "def get_dd_value(self, value: str):" + NEWLINE)
    writer.write(indent(BASE_LEVEL - 1) + "result = 'UNKNOWN'" + NEWLINE)
    writer.write(indent(BASE_LEVEL - 1) + "for dd in self.dd_name_list:" + NEWLINE)
    writer.write(indent(BASE_LEVEL) + "if len(dd) > 1:" + NEWLINE)
    writer.write(indent(BASE_LEVEL + 1) + "if dd[0].strip() == value.strip():" + NEWLINE)
    writer.write(indent(BASE_LEVEL + 2) + "result = dd[1].strip()" + NEWLINE)
    writer.write(indent(BASE_LEVEL + 2) + "break" + NEWLINE)
    writer.write(indent(BASE_LEVEL - 1) + "return result" + NEWLINE)
    writer.write(NEWLINE)
    writer.write(indent(BASE_LEVEL - 2) + "def process_key(self, keycode: int):\n")
    writer.write(indent(BASE_LEVEL - 1) + "return CheckAttentionKey(keycode)\n")
    writer.write(NEWLINE)
    writer.write(indent(BASE_LEVEL - 2) + "def _error_handler(self, e):" + NEWLINE)
    writer.write(indent(BASE_LEVEL - 1) + SELF_REFERENCE + "error_triggered = True" + NEWLINE)
    writer.write(indent(BASE_LEVEL - 1) + "if " + SELF_REFERENCE + CLASS_ERROR_FUNCTION_MEMBER + " != None:" + NEWLINE)
    writer.write(indent(BASE_LEVEL) + SELF_REFERENCE + CLASS_ERROR_FUNCTION_MEMBER + OPEN_PARENS + CLOSE_PARENS + NEWLINE)
    writer.write(indent(BASE_LEVEL - 1) + "else:" + NEWLINE)
    writer.write(indent(BASE_LEVEL) + SELF_REFERENCE + "SPECIALREGISTERSMemory = Set_Variable(self.SPECIALREGISTERSMemory,self.variables_list,'RETURN-CODE', 12,'RETURN-CODE')[1]" + NEWLINE)
    writer.write(indent(BASE_LEVEL) + "print('')" + NEWLINE)
    writer.write(indent(BASE_LEVEL) + "print('error encountered:')" + NEWLINE)
    writer.write(indent(BASE_LEVEL) + "print(e)" + NEWLINE)
    writer.write(indent(BASE_LEVEL) + "exc_type, exc_obj, exc_tb = sys.exc_info()" + NEWLINE)
    writer.write(indent(BASE_LEVEL) + "fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]" + NEWLINE)
    writer.write(indent(BASE_LEVEL) + "print(exc_type, fname, exc_tb.tb_lineno)" + NEWLINE)
    writer.write(indent(BASE_LEVEL) + "print('COBOL Source File:      " + current_line.source_filename + "')" + NEWLINE)
    writer.write(indent(BASE_LEVEL) + "print('COBOL File Line Number: ' + self.debug_line)" + NEWLINE)
    writer.write(indent(BASE_LEVEL - 1) + "return" + NEWLINE)
    writer.write(NEWLINE)
    writer.write("if __name__ == '__main__':" + NEWLINE)
    writer.write(writer.indent(1) + "main_obj = " + name + "Class()" + NEWLINE + writer.indent(1))

    if len(context.args) > 0:
        writer.write("print" + OPEN_PARENS)
    writer.write("main_obj.main" + OPEN_PARENS + "main_obj")
    arg_count = 0
    if len(context.args) > 0:
        for x in range(0, len(context.args)):
            if x > 2:
                writer.write(COMMA)
            if x > 2:
                arg_count = arg_count + 1
                writer.write("'arg" + str(arg_count) + SINGLE_QUOTE)
    writer.write(CLOSE_PARENS)
    if len(context.args) > 0:
        writer.write(CLOSE_PARENS)
    writer.write(NEWLINE + writer.indent(1) + "Cleanup()" + NEWLINE)
    writer.write(NEWLINE)
