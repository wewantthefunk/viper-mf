from util import *
from jcl_lexicon import *
import sys

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
    write_file(target_dir + job_name + CONVERTED_JCL_EXT, "# JOB NAME: " + job_name + NEWLINE)
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, "from io import StringIO\nfrom cobol_variable import *\nfrom datetime import datetime\nimport sys, os\n") 
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, "class " + job_name + "JCLClass:\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 1) + "def main(self):\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "start_time = datetime.now()\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + 'Path("JES2/OUTPUT/").mkdir(parents=True, exist_ok=True)\n')
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "jes_result_file = 'JES2/OUTPUT/" + job_name + "_' + datetime.strftime(start_time, '%d-%b-%Y-%H-%M-%S')" + NEWLINE)
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "string_io = StringIO()\n")    
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "append_file_data(jes_result_file, 'Executing Job: " + job_name + "' + NEWLINE)\n")

def write_out_final_job_info(job_name, target_dir):
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, "\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "end_time = datetime.now()\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "append_file_data(jes_result_file, '" + pad_char(20, DASH) + "' + NEWLINE)" + NEWLINE)
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "append_file_data(jes_result_file, 'Job Complete' + NEWLINE)\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "append_file_data(jes_result_file, '   Start: {}'.format(start_time) + NEWLINE)\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "append_file_data(jes_result_file, '     End: {}'.format(end_time) + NEWLINE)\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "append_file_data(jes_result_file, 'Duration: {}'.format(end_time - start_time) + NEWLINE)\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, "if __name__ == '__main__':\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 1) + "main_obj = " + job_name + "JCLClass()\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 1) + "main_obj.main()\n")

def write_out_step_info(job_name, step_name, program_name, args, target_dir):
    insert_beginning_of_file(target_dir + job_name + CONVERTED_JCL_EXT, "from " + program_name + " import *\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, NEWLINE + "# STEP: " + step_name + NEWLINE + "#  PGM: " + program_name + NEWLINE)
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "append_file_data(jes_result_file, '" + pad_char(20, DASH) + "' + NEWLINE)" + NEWLINE)
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "append_file_data(jes_result_file, 'Executing    Step: " + step_name + "' + NEWLINE)\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "append_file_data(jes_result_file, '          Program: " + program_name + "' + NEWLINE)" + NEWLINE)
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "sys.stdout = string_io\n")

    environment_vars = []
    for arg in args:
        a = arg.split(DD_ARG_DELIMITER)
        
        if a[0] not in IGNORED_DD_STATEMENTS:
            split = a[1].split(EQUALS)
            split1 = split[1].split(COMMA)
            file_info = split1[0].split(OPEN_PARENS)
            filename = file_info[0]
            path = EMPTY_STRING
            append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "os.environ['" + a[0] + "'] = '" + filename + "'\n")
            environment_vars.append(a[0])

    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "step = " + program_name + "Class()" + NEWLINE)
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "step.main(self)\n")

    for arg in args:
        a = arg.split(DD_ARG_DELIMITER)
        if a[1] == "SYSOUT=*":
            append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "sys.stdout = sys.__stdout__\n")
            append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "append_file_data(jes_result_file, string_io.getvalue() + NEWLINE)\n")
        elif a[1].startswith("DSN") or a[1].startswith("DSNAME"):
            split = a[1].split(EQUALS)
            split1 = split[1].split(COMMA)
            file_info = split1[0].split(OPEN_PARENS)
            filename = file_info[0]
            path = EMPTY_STRING
            if len(file_info) > 1:
                filename = file_info[1].replace(CLOSE_PARENS, EMPTY_STRING)
                path = file_info[0].replace(PERIOD, FORWARD_SLASH)
                append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + 'Path("' + path + '").mkdir(parents=True, exist_ok=True)\n')

            if a[0] == "SYSOUT":
                if path != EMPTY_STRING:
                    if path.endswith(FORWARD_SLASH) == False:
                        path = path + FORWARD_SLASH
                append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "append_file_data(jes_result_file, '          SYSOUT messages are stored in: " + path + filename + "' + NEWLINE)\n")
                append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "write_file_data('" + path + filename + "', string_io.getvalue())\n")
                append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "sys.stdout = sys.__stdout__\n")

    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "string_io.truncate(0)\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "string_io.seek(0)\n")

    for e in environment_vars:
        append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "os.unsetenv('" + e + "')\n")

if __name__ == "__main__":
    prefix = "../"
    for file in os.listdir("./"):
        d = os.path.join("./", file)
        if os.path.isdir(d):
            if 'examples' in d:
                prefix = ""
                break
    if len(sys.argv) > 1:
        parse_jcl_file(sys.argv[1], sys.argv[2], prefix)
    else:
        parse_jcl_file("examples/hellowo1_basic_sysout_to_file.jcl", "converted/")
        parse_jcl_file("examples/hellow12_sequential_file_access.jcl", "converted/")
        parse_jcl_file("examples/hellowor_mulitple_steps.jcl", "converted/")
        #parse_jcl_file("examples/hellow75_indexed_file_access.jcl", "converted/") 
        #parse_jcl_file("examples/hellow76_indexed_file_write.jcl", "converted/")   