from util import *
from jcl_lexicon import *
import os

job_name = EMPTY_STRING

def parse_jcl_file(file: str, target_dir: str, dep_dir = EMPTY_STRING):
    r_lines = read_raw_file_lines(file, 0)

    count = 0
    job_name = EMPTY_STRING
    step_name = EMPTY_STRING
    program_name = EMPTY_STRING
    args = []

    for rl in r_lines:
        if not rl.startswith(JCL_LINE_START):
            continue
        index = rl.find(SPACE)
        temp = rl[2:index]
        if count == 0:
            job_name = temp
            write_out_job_info(job_name, target_dir)
        else:
            if JCL_EXEC_INDICATOR in rl:
                if step_name != EMPTY_STRING:
                    write_out_step_info(job_name, step_name, program_name, args, target_dir)
                step_name = EMPTY_STRING
                program_name = EMPTY_STRING
                args = []
                step_name = temp
                if JCL_PGM_NAME in rl:
                    s = rl.split(JCL_PGM_NAME)
                    p = s[1].split(COMMA)
                    program_name = p[0].replace(NEWLINE, EMPTY_STRING)
            elif JCL_DD_INDICATOR in rl:
                t = rl.split(JCL_DD_INDICATOR)
                args.append(t[0].replace(JCL_LINE_START, EMPTY_STRING).strip() + DD_ARG_DELIMITER + t[1].replace(NEWLINE, EMPTY_STRING).strip())

        count = count + 1

    write_out_step_info(job_name, step_name, program_name, args, target_dir)
    write_out_final_job_info(job_name, target_dir)
    return

def write_out_job_info(job_name, target_dir):
    write_file(target_dir + job_name + CONVERTED_JCL_EXT, "#" + job_name + NEWLINE)
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, "from io import StringIO\nfrom cobol_variable import *\nfrom datetime import datetime\n") 
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, "class " + job_name + "JCLClass:\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 1) + "def main(self):\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "start_time = datetime.now()\n")

def write_out_final_job_info(job_name, target_dir):
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, "\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "end_time = datetime.now()\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "print('Duration: {}'.format(end_time - start_time))\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, "if __name__ == '__main__':\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 1) + "main_obj = " + job_name + "JCLClass()\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 1) + "main_obj.main()\n")

def write_out_step_info(job_name, step_name, program_name, args, target_dir):
    insert_beginning_of_file(target_dir + job_name + CONVERTED_JCL_EXT, "from " + program_name + " import *\n")
    for arg in args:
        a = arg.split(DD_ARG_DELIMITER)
        for a1 in a:
            if a1[0] not in IGNORED_DD_STATEMENTS:
                os.environ[a1[0]] = a1[1]

    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "string_io = StringIO()\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "sys.stdout = string_io\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "step = " + program_name + "Class()" + NEWLINE)
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "step.main(self)\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "sys.stdout = sys.__stdout__\n")

    for arg in args:
        a = arg.split(DD_ARG_DELIMITER)
        if a[1] == "SYSOUT=*":
            append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "print(string_io.getvalue())\n")
        elif a[1].startswith("DSN") or a[1].startswith("DSNAME"):
            split = a[1].split(EQUALS)
            file_info = split[1].split(OPEN_PARENS)
            path = file_info[0].replace(PERIOD, FORWARD_SLASH)
            append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + 'Path("' + path + '").mkdir(parents=True, exist_ok=True)\n')
            append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "write_file_data('" + path + FORWARD_SLASH + file_info[1].replace(CLOSE_PARENS, EMPTY_STRING) + "', string_io.getvalue())\n")

if __name__ == "__main__":
    parse_jcl_file("examples/helloworld_tests.jcl", "converted/")