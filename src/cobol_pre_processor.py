from util import *
from cobol_lexicon import *

def main(file: str):
    delete_file("pre_processed.cbl")
    r_lines = read_raw_file_lines(file, 0) 

    out_line = EMPTY_STRING
    count = 0
    start = False
    skip = False

    for line in r_lines:
        finished_line = True
        line = line[:72]
        if count + 1 < len(r_lines):
            work_line = r_lines[count + 1][7:72].strip()
        else:
            work_line = EMPTY_STRING

        count = count + 1

        if skip:
            skip = False
            result = preprocess(out_line, work_line)
            out_line = result[0]
            skip = result[1]
            if result[2]:
                out_line = out_line + NEWLINE
            finished_line = result[2]
        elif start:
            result = preprocess(line, work_line)
            out_line = result[0]
            skip = result[1]

            if result[2]:
                out_line = out_line + NEWLINE
            finished_line = result[2]
        elif line[7:].startswith(PROCEDURE_DIVISION_NAME):
            start = True
            out_line = line
        else:
            out_line = line

        if finished_line:
            if not out_line.startswith(pad(7)):
                out_line = pad(7) + out_line.strip() + NEWLINE
            append_file("pre_processed.cbl", out_line)

            out_line = EMPTY_STRING

    return "pre_processed.cbl"
        
def preprocess(line: str, work_line: str):
    line = line.replace(NEWLINE, EMPTY_STRING)
    result_line = line
    result_skip = False
    finished_line = False

    if not line.endswith(PERIOD):
        tokens = work_line.split(SPACE)
        if tokens[0] not in COBOL_VERB_LIST:
            result_line = result_line + SPACE + work_line.replace(NEWLINE, EMPTY_STRING)
            result_skip = True
            if work_line.endswith(PERIOD):
                finished_line = True
        else:
            finished_line = True
    else:
        finished_line = True

    return [result_line, result_skip, finished_line]

if __name__ == "__main__":
    main("examples/hellowo4_paragraph.cbl")