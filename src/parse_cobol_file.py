from util import read_raw_file_lines
from cobol_lexicon import *
from cobol_line_process import *
from util import *

args = []

def parse_cobol_file(file: str, target_dir: str):
    global args
    args = []
    r_lines = read_raw_file_lines(file, 0)

    raw_lines = []

    for rl in r_lines:
        rl = rl.replace(NEWLINE, EMPTY_STRING)
        if len(rl) < 7:
            rl = EMPTY_STRING

        if rl == EMPTY_STRING:
            continue
        if (rl[6] != COBOL_COMMENT and rl[7:] != EMPTY_STRING):
            raw_lines.append(rl)

    lines = []
    current_division = EMPTY_STRING
    name = "abend"
    first_time = False
    current_line = LexicalInfo()

    total = len(raw_lines)
    count = 0
    for line in raw_lines:
        count = count + 1
        next_few_lines_count = LINES_AHEAD
        lines_left = total - count
        if lines_left < 0:
            while lines_left < 0:
                lines_left = lines_left - 1
            next_few_lines_count = lines_left
        next_few_lines = raw_lines[count:count+next_few_lines_count]
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

    append_file(name + PYTHON_EXT, "if __name__ == '__main__':" + NEWLINE + INDENT)
    
    if len(args) > 0:
        append_file(name + PYTHON_EXT, "print" + OPEN_PARENS)

    append_file(name + PYTHON_EXT, "main_" + name.replace(DASH, UNDERSCORE) + OPEN_PARENS)

    arg_count = 0
    if len(args) > 0:
        for x in range(0, len(args)):
            if x > 3:
                append_file(name + PYTHON_EXT, COMMA)
            if x > 2:
                arg_count = arg_count + 1
                append_file(name + PYTHON_EXT, "'arg" + str(arg_count) + SINGLE_QUOTE)

    append_file(name + PYTHON_EXT, CLOSE_PARENS)

    if len(args) > 0:
        append_file(name + PYTHON_EXT, CLOSE_PARENS)

    append_file(name + PYTHON_EXT, NEWLINE)

    if len(current_line.import_statement) > 0:
        insert(name + PYTHON_EXT, current_line.import_statement)

    move_file(name + PYTHON_EXT, target_dir + name + PYTHON_EXT)

    copy_file("../dependencies/cobol_variable.py", target_dir + "cobol_variable.py")

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
                init_vars(name, args, current_line)
            break

    if not new_division:
        result = process_line(line, current_division, name, current_line, next_few_lines)
        current_division = result[0]
        name = result[1]
        current_line = result[2]
    else:
        if name != "abend":
            append_file(name + PYTHON_EXT, "# " + current_division + NEWLINE)
            first_time = False
            if current_division == COBOL_DIVISIONS[PROCEDURE_DIVISION_POS]:
                append_file(name + PYTHON_EXT, "def main_" + name.replace(DASH, UNDERSCORE) + OPEN_PARENS)

                if USING_KEYWORD in line:
                    args = parse_line_tokens(line, SPACE, EMPTY_STRING, False)
                    count = 0
                    arg_count = 0
                    for arg in args:
                        if count > 3:
                            append_file(name + PYTHON_EXT, COMMA)

                        if count > 2:
                            arg_count = arg_count + 1
                            append_file(name + PYTHON_EXT, MAIN_ARG_VARIABLE_PREFIX + str(arg_count))
                        count = count + 1
                
                append_file(name + PYTHON_EXT, CLOSE_PARENS + COLON + NEWLINE)

                count = 0
                arg_count = 0
                for arg in args:
                    if count > 2:
                        arg_count = arg_count + 1
                        process_procedure_division_line("MOVE " + MAIN_ARG_VARIABLE_PREFIX + str(arg_count) + " TO " + arg.replace(COMMA, EMPTY_STRING) + PERIOD, name, current_line, [], args)
                    count = count + 1

    return [current_division, name, first_time, current_line]

def process_line(line: str, current_division: str, name: str, current_line: LexicalInfo, next_few_lines):
    global args
    if current_division == COBOL_DIVISIONS[IDENTIFICATION_DIVISION_POS] \
        or current_division == COBOL_DIVISIONS[ID_DIVISION_POS]:
        name = process_identification_division_line(line, name)
        write_file(name + PYTHON_EXT, "from cobol_variable import *" + NEWLINE)
        append_file(name + PYTHON_EXT, "# PROGRAM-ID: " + name + NEWLINE)
        append_file(name + PYTHON_EXT, VARIABLES_LIST_NAME + " = []" + NEWLINE)
    elif current_division == COBOL_DIVISIONS[ENVIRONMENT_DIVISION_POS]:
        result = process_environment_division_line(line, current_line.current_section, name, current_line, next_few_lines, args)
    elif current_division == COBOL_DIVISIONS[DATA_DIVISION_POS]:
        result = process_data_division_line(line, current_line.current_section, name, current_line, next_few_lines, args)
        current_line.current_section = result[1]
    elif current_division == COBOL_DIVISIONS[PROCEDURE_DIVISION_POS]:
        result = process_procedure_division_line(line, name, current_line, next_few_lines, args)
        current_line.level = result[1]

    return [current_division, name, current_line]

if __name__ == "__main__":
    parse_cobol_file("../examples/hw.cbl", "../converted/")