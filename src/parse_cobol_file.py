from util import read_raw_file_lines
from cobol_lexicon import (
    ABEND, BASE_LEVEL, EMPTY_STRING, INDENT, LINES_AHEAD, NEWLINE, PYTHON_EXT,
    ZERO,
)
from cobol_line_process import (
    process_identification_division_line, process_environment_division_line,
    process_data_division_line, process_procedure_division_line,
    create_index_variables, allocate_variables, init_vars, insert_copybook,
)
from cobol_verb_process import process_verb
from util import (
    LexicalInfo, insert_beginning_of_file,
    move_file, copy_file, parse_line_tokens, pad,
)
from cobol_util import prep_source
from codegen import CodeWriter
from translation_context import TranslationContext
from cobra_boilerplate import emit_class_header, emit_class_footer, emit_procedure_division_preamble
import cobol_pre_processor

# Lexicon constants used in this module for codegen
from cobol_lexicon import (
    ADDRESS_INDICATOR, CALLING_MODULE_MEMBER, CLASS_ERROR_FUNCTION_MEMBER,
    CLOSE_PARENS, COBOL_DIVISIONS, COLON, COMMA, EIB_COPYBOOK, EIB_MEMORY,
    ENVIRONMENT_DIVISION_POS, IDENTIFICATION_DIVISION_POS, ID_DIVISION_POS,
    JOB_NAME_MEMBER, JOB_STEP_MEMBER, MAIN_ARG_VARIABLE_PREFIX, MAIN_ERROR_FUNCTION,
    MEMORY, OPEN_PARENS, PROCEDURE_DIVISION_POS, SELF_REFERENCE, SINGLE_QUOTE,
    USING_KEYWORD, VARIABLES_LIST_NAME, VERB_RESET, DD_NAME_LIST,
    DATA_DIVISION_POS,
)

def parse_cobol_file(file: str, target_dir: str, dep_dir=EMPTY_STRING):
    c_file = cobol_pre_processor.main(file)
    r_lines = read_raw_file_lines(c_file, 0)
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

    writer = CodeWriter(name + PYTHON_EXT)
    context = TranslationContext(writer, current_line, name)

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
        result = parse_line(line, current_division, name, first_time, current_line, next_few_lines, writer, context)
        tmp = result[0]
        current_division = result[1]
        name = result[2]
        first_time = result[3]
        current_line = result[4]
        writer = result[5]
        context.program_name = name
        context.lexical_info = current_line
        context.writer = writer
        if tmp != EMPTY_STRING:
            lines.append(tmp)
        if current_division == ABEND:
            break

    emit_class_footer(context)

    if len(current_line.import_statement) > 0:
        insert(writer.output_path, current_line.import_statement)

    move_file(writer.output_path, target_dir + name + PYTHON_EXT)

    copy_file(dep_dir + "dependencies/cobol_variable.py", target_dir + "cobol_variable.py")

    print("completed conversion of " + file + " to --> " + target_dir + name + PYTHON_EXT)

    if current_line.total_copybooks_inserted > 0:
        print(pad(len(INDENT)) + "total copybooks inserted: " + str(current_line.total_copybooks_inserted))

    if current_line.unknown_cobol_verbs > 0:
        print(pad(len(INDENT)) + "unknown COBOL statements: " + str(current_line.unknown_cobol_verbs))

def insert(originalfile, imports):
    for imp in imports:
        insert_beginning_of_file(originalfile, "from " + imp + " import *" + NEWLINE)


def parse_line(line: str, current_division: str, name: str, first_time: bool, current_line: LexicalInfo, next_few_lines, writer: CodeWriter, context: TranslationContext):
    from cobol_lexicon import COBOL_COMMENT
    tmp = line[6:].replace(NEWLINE, EMPTY_STRING).strip()
    if tmp == EMPTY_STRING or tmp.startswith(COBOL_COMMENT):
        return [EMPTY_STRING, current_division, name, first_time, current_line, writer]
    else:
        result = parse_current_line(tmp, current_division, name, first_time, current_line, next_few_lines, writer, context)
        current_division = result[0]
        name = result[1]
        first_time = result[2]
        current_line = result[3]
        writer = result[4]
        if current_division == ABEND:
            return [EMPTY_STRING, ABEND, name, first_time, current_line, writer]

        return [tmp, current_division, name, first_time, current_line, writer]

def parse_current_line(line: str, current_division: str, name: str, first_time: bool, current_line: LexicalInfo, next_few_lines, writer: CodeWriter, context: TranslationContext):
    from cobol_lexicon import SPACE, EQUALS, PERIOD
    old_division_name = EMPTY_STRING
    if current_division == EMPTY_STRING:
        if not line.startswith(COBOL_DIVISIONS[0]) \
            and not line.startswith(COBOL_DIVISIONS[1]):
            print("invalid syntax -> first line MUST be 'IDENTIFICATION DIVISION.' or 'ID DIVISION.'")
            return [ABEND, name, first_time, current_line, writer]
        else:
            first_time = True

    new_division = False
    for division in COBOL_DIVISIONS:
        if line.startswith(division):
            old_division_name = current_division
            current_division = division
            new_division = True
            if division == COBOL_DIVISIONS[PROCEDURE_DIVISION_POS]:
                create_index_variables(current_line.index_variables, name, writer)
                allocate_variables(current_line, name, writer)
                init_vars(name, context, writer)
            break

    if not new_division:
        result = process_line(line, current_division, name, current_line, next_few_lines, writer, context)
        current_division = result[0]
        name = result[1]
        current_line = result[2]
        writer = result[3]
    else:
        if name != "abend":
            first_time = False
            if current_division == COBOL_DIVISIONS[PROCEDURE_DIVISION_POS]:
                emit_procedure_division_preamble(context, current_division, line, next_few_lines)
            else:
                writer.write("# " + current_division + NEWLINE)

    return [current_division, name, first_time, current_line, writer]

def process_line(line: str, current_division: str, name: str, current_line: LexicalInfo, next_few_lines, writer: CodeWriter, context: TranslationContext):
    from cobol_lexicon import NONE_KEYWORD, SPACE
    if current_division == COBOL_DIVISIONS[IDENTIFICATION_DIVISION_POS] \
        or current_division == COBOL_DIVISIONS[ID_DIVISION_POS]:
        name = process_identification_division_line(line, name, context)
        if name != "abend":
            writer = CodeWriter(name + PYTHON_EXT)
        emit_class_header(writer, name)
    elif current_division == COBOL_DIVISIONS[ENVIRONMENT_DIVISION_POS]:
        process_environment_division_line(line, current_line.current_section, name, current_line, next_few_lines, context, writer)
    elif current_division == COBOL_DIVISIONS[DATA_DIVISION_POS]:
        result = process_data_division_line(line, current_line.current_section, name, current_line, next_few_lines, context, writer)
        current_line.current_section = result[1]
        if result[1] not in current_line.sections_list:
            current_line.sections_list.append(result[1])
    elif current_division == COBOL_DIVISIONS[PROCEDURE_DIVISION_POS]:
        result = process_procedure_division_line(line, name, current_line, next_few_lines, context, writer)
        current_line.level = result[1]
        current_line.skip_the_next_lines = result[0]

    return [current_division, name, current_line, writer]

if __name__ == "__main__":
    #parse_cobol_file("examples/hellowo1_basic.cbl", "converted/")
    parse_cobol_file("work/CONVCOPY.cbl", "converted/")
