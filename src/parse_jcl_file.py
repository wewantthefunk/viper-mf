from util import *
from jcl_lexicon import *
import sys

job_name = EMPTY_STRING

def parse_jcl_file(file: str, target_dir: str, dep_dir = EMPTY_STRING):

    print("Converting JCL: " + file + " --> " + prefix + target_dir)

    r_lines = read_raw_file_lines(file, 0)

    count = 0
    job_name = EMPTY_STRING
    step_name = EMPTY_STRING
    program_name = EMPTY_STRING
    args = []
    parm = EMPTY_STRING
    is_getting_inline = False
    is_getting_dd_info = False
    inline_args = EMPTY_STRING

    for rl in r_lines:
        if not rl.startswith(JCL_LINE_START) and not is_getting_inline:
            continue
        index = rl.find(SPACE)
        temp = rl[2:index]
        if count == 0:
            job_name = temp
            write_out_job_info(job_name, target_dir)
        else:
            if JCL_EXEC_INDICATOR in rl:
                is_getting_dd_info = False
                if program_name == "IDCAMS":
                    process_idcams_cmd(job_name, step_name, inline_args.strip(), target_dir, program_name)
                elif step_name != EMPTY_STRING:
                    write_out_step_info(job_name, step_name, program_name, args, target_dir, parm)
                step_name = EMPTY_STRING
                program_name = EMPTY_STRING
                args = []
                step_name = temp
                if JCL_PGM_NAME in rl:
                    s = rl.split(JCL_PGM_NAME)
                    p = s[1].split(COMMA)
                    program_name = p[0].replace(NEWLINE, EMPTY_STRING)
                if JCL_PARM_INDICATOR in rl:
                    s = rl.split(JCL_PARM_INDICATOR)
                    p = s[1].split(EQUALS)
                    p[1] = p[1].replace(NEWLINE, EMPTY_STRING).replace(SINGLE_QUOTE, EMPTY_STRING)
                    parm = p[1]
            elif JCL_PARM_INDICATOR in rl:
                s = rl.split(JCL_PARM_INDICATOR)
                p = s[1].split(EQUALS)
                p[1] = p[1].replace(NEWLINE, EMPTY_STRING).replace(SINGLE_QUOTE, EMPTY_STRING)
                parm = p[1]
            elif rl.startswith("/*"):
                is_getting_dd_info = False
                is_getting_inline = False
            elif is_getting_inline:
                inline_args = inline_args + rl.strip() + SPACE
            elif JCL_DD_INDICATOR in rl:
                is_getting_dd_info = True
                t = rl.split(JCL_DD_INDICATOR)
                dd_target = t[1].replace(NEWLINE, EMPTY_STRING).strip()
                if dd_target == "*":
                    is_getting_inline = True
                    inline_args = EMPTY_STRING
                args.append(t[0].replace(JCL_LINE_START, EMPTY_STRING).strip() + DD_ARG_DELIMITER + dd_target)
            elif is_getting_dd_info:
                args[len(args) - 1] = args[len(args) - 1] + rl.replace(JCL_LINE_START, EMPTY_STRING).strip()

        count = count + 1

    write_out_step_info(job_name, step_name, program_name, args, target_dir, parm)
    write_out_final_job_info(job_name, target_dir)

    print("completed conversion of " + file + " to --> " + target_dir + job_name + CONVERTED_JCL_EXT)

    return

def write_out_job_info(job_name, target_dir):
    write_file(target_dir + job_name + CONVERTED_JCL_EXT, "# JOB NAME: " + job_name + NEWLINE)
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, "from io import StringIO\nfrom cobol_variable import *\nfrom datetime import datetime\nimport sys, os\n") 
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, "class " + job_name + "JCLClass:\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 1) + "def terminate_on_callback(self):\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "return\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, "\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 1) + "def main(self):\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "start_time = datetime.now()\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "highest_return_code = 0\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + 'Path("JES2/OUTPUT/").mkdir(parents=True, exist_ok=True)\n')
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "jes_result_file = 'JES2/OUTPUT/" + job_name + "_' + datetime.strftime(start_time, '%d-%b-%Y-%H-%M-%S')" + NEWLINE)
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "string_io = StringIO()\n")    
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "append_file_data(jes_result_file, 'Executing Job: " + job_name + "' + NEWLINE)\n")

    return

def write_out_final_job_info(job_name, target_dir):
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, "\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "Cleanup()\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "end_time = datetime.now()\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "append_file_data(jes_result_file, '" + pad_char(20, DASH) + "' + NEWLINE)" + NEWLINE)
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "append_file_data(jes_result_file, 'Job Complete' + NEWLINE)\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "append_file_data(jes_result_file, '              Start: {}'.format(start_time) + NEWLINE)\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "append_file_data(jes_result_file, '                End: {}'.format(end_time) + NEWLINE)\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "append_file_data(jes_result_file, '           Duration: {}'.format(end_time - start_time) + NEWLINE)\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "append_file_data(jes_result_file, 'Highest Return Code: ' + str(highest_return_code) + NEWLINE)\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "cat_file(jes_result_file)\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "print('Job Results stored in file: ' + jes_result_file)\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, "if __name__ == '__main__':\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 1) + "main_obj = " + job_name + "JCLClass()\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 1) + "main_obj.main()\n")

    return

def write_out_step_info(job_name, step_name, program_name, args, target_dir, parm=EMPTY_STRING):
    insert_beginning_of_file(target_dir + job_name + CONVERTED_JCL_EXT, "from " + program_name + " import *\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, NEWLINE + "# STEP: " + step_name + NEWLINE + "#  PGM: " + program_name + NEWLINE)
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "append_file_data(jes_result_file, '" + pad_char(20, DASH) + "' + NEWLINE)" + NEWLINE)
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "append_file_data(jes_result_file, 'Executing    Step: " + step_name + "' + NEWLINE)\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "append_file_data(jes_result_file, '          Program: " + program_name + "' + NEWLINE)" + NEWLINE)
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "sys.stdout = string_io\n")

    environment_vars = []

    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "step = " + program_name + "Class()" + NEWLINE)
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "step.job_name = '" + job_name + "'\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "step.job_step = '" + step_name + "'\n")

    for arg in args:
        a = arg.split(DD_ARG_DELIMITER)
        
        append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "step.dd_name_list.append(['" + a[0] + "','" + a[1].split(EQUALS)[1].split(COMMA)[0] + "'])\n")
        if a[0] not in IGNORED_DD_STATEMENTS:
            split = a[1].split(EQUALS)
            split1 = split[1].split(COMMA)
            file_info = split1[0].split(OPEN_PARENS)
            if len(file_info) > 1:
                append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + 'Path("' + file_info[0].replace(PERIOD, FORWARD_SLASH) + FORWARD_SLASH + '").mkdir(parents=True, exist_ok=True)\n')
                filename = file_info[0].replace(PERIOD, FORWARD_SLASH) + FORWARD_SLASH + file_info[1].replace(")", EMPTY_STRING)
            else:
                filename = file_info[0].replace(")", EMPTY_STRING)
            path = EMPTY_STRING
            append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "os.environ['" + a[0] + "'] = '" + filename + "'\n")
            environment_vars.append(a[0])

    if parm == EMPTY_STRING:
        append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "step.main(self)\n")
    else:
        append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "var = COBOLVariable('parm-var', 2, 'S9', '', '', 0, 0, '01', 'COMP', 0, 4, '', 0, False)\n")
        append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "ls = str(" + str(len(parm)) + ").zfill(4)\n")
        append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "l = convert_to_comp(ls, var)\n")
        append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "step.main(self,str(l) + '" + parm + "')\n")
    # write the RETURN-CODE from the called program to the output 
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "rc = step.get_return_code()\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "if rc > highest_return_code:\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 3) + "highest_return_code = step.get_return_code()\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "append_file_data(jes_result_file, '      Return Code: ' + str(rc) + NEWLINE + '--------------------' + NEWLINE + NEWLINE)\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + NEWLINE)

    cleanup_normal = []
    cleanup_abnormal = []
    for arg in args:
        a1 = arg.split(DD_ARG_DELIMITER)
        a = a1[1].split(COMMA)
        dsn_index = check_for_dsn(a)
        disp_index = check_for_disp(a)
        if "SYSOUT=*" in a:
            append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "sys.stdout = sys.__stdout__\n")
            append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "append_file_data(jes_result_file, string_io.getvalue() + NEWLINE)\n")
        if dsn_index > -1:
            split = a[dsn_index].split(EQUALS)
            split1 = split[1].split(COMMA)
            file_info = split1[0].split(OPEN_PARENS)
            filename = file_info[0]
            path = EMPTY_STRING
            if len(file_info) > 1:
                filename = file_info[1].replace(CLOSE_PARENS, EMPTY_STRING)
                path = file_info[0].replace(PERIOD, FORWARD_SLASH)
                if not path.endswith(FORWARD_SLASH):
                    path = path + FORWARD_SLASH
                append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + 'Path("' + path + '").mkdir(parents=True, exist_ok=True)\n')

            if a1[0] == "SYSOUT":
                if path != EMPTY_STRING:
                    if path.endswith(FORWARD_SLASH) == False:
                        path = path + FORWARD_SLASH
                append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "append_file_data(jes_result_file, '===> SYSOUT messages are stored in: " + path + filename + "' + NEWLINE + NEWLINE)\n\n")
                append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "write_file_data('" + path + filename + "', string_io.getvalue())\n")
                append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "sys.stdout = sys.__stdout__\n")
        if disp_index > -1:
            disp_clause = a[disp_index].replace("DISP=", EMPTY_STRING)
            if OPEN_PARENS in a[disp_index]:
                disp_clause = disp_clause.replace(OPEN_PARENS, EMPTY_STRING)
                for x in range (disp_index, len(a)):
                    if x != disp_index:
                        disp_clause = disp_clause + COMMA + a[x]
                    if CLOSE_PARENS in a[x]:
                        disp_clause = disp_clause.replace(CLOSE_PARENS, EMPTY_STRING)
                        break 

            disp = disp_clause.split(COMMA)
            for x in range(0,len(disp)):
                if x == 1:
                    if disp[x] == "DELETE":
                        cleanup_normal.append(path + filename)
                elif x == 2:
                    if disp[x] == "DELETE":
                        cleanup_abnormal.append(path + filename)


    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "string_io.truncate(0)\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "string_io.seek(0)\n")

    for e in environment_vars:
        append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "os.unsetenv('" + e + "')\n")

    if len(cleanup_normal) > 0:
        append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "if rc == 0:\n")
        for a in cleanup_normal:
            append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 3) + "if os.path.exists('" + a + "'):\n")
            append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 4) + "os.remove('" + a + "')\n")

    if len(cleanup_abnormal) > 0:
        append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "if rc > 0:\n")
        for a in cleanup_abnormal:
            append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 3) + "if os.path.exists('" + a + "'):\n")
            append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 4) + "os.remove('" + a + "')\n")

    return

def process_idcams_cmd(job_name: str, step_name: str, inline_args: str, target_dir: str, program_name: str):
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, NEWLINE + "# STEP: " + step_name + NEWLINE + "#  PGM: " + program_name + NEWLINE)
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "append_file_data(jes_result_file, '" + pad_char(20, DASH) + "' + NEWLINE)" + NEWLINE)
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "append_file_data(jes_result_file, 'Executing    Step: " + step_name + "' + NEWLINE)\n")
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "append_file_data(jes_result_file, '          Program: " + program_name + "' + NEWLINE)" + NEWLINE)
    append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "sys.stdout = string_io\n")

    args = inline_args.split(SPACE)

    if args[0] == "DELETE":
        path_info = args[1].split("(")
        path = path_info[0].replace(PERIOD, FORWARD_SLASH)
        temp = path.split(FORWARD_SLASH)
        filename = temp[len(temp) - 1]
        if len(path_info) > 1:
            filename = path_info[1].replace(")", EMPTY_STRING)

        append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "if os.path.exists('" + path + FORWARD_SLASH + filename + "'):\n")
        append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 3) + "os.remove('" + path + FORWARD_SLASH + filename + "')\n")
        append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 3) + "rc = 0\n")
        append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "else:\n")
        append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 3) + "rc = 8\n")
        append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 3) + "append_file_data(jes_result_file, 'IDC3009I ** VSAM CATALOG RETURN CODE IS 8 - REASON CODE IS IGG0CLEG-42' + NEWLINE)\n")
        append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 3) + "append_file_data(jes_result_file, 'IDC0551I ** ENTRY " + args[1] + "' + NEWLINE)\n")
        append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 3) + "append_file_data(jes_result_file, 'IDC0001I FUNCTION COMPLETED, HIGHEST CONDITION CODE WAS 8' + NEWLINE)\n")
        append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "append_file_data(jes_result_file, '      Return Code: ' + str(rc) + NEWLINE)\n")
        append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 2) + "if rc > highest_return_code:\n")
        append_file(target_dir + job_name + CONVERTED_JCL_EXT, pad(len(INDENT) * 3) + "highest_return_code = rc\n")

    return

def check_for_disp(dd_list: list):
    return check_for_value(dd_list, "DISP")

def check_for_dsn(dd_list: list):
    result = check_for_value(dd_list, "DSNAME")
    if result == -1:
        result = check_for_value(dd_list, "DSN")

    return result

def check_for_value(l: list, value: str):
    count = 0
    for x in l:
        if x.startswith(value):
            return count
        count = count + 1
    
    return -1

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
        #parse_jcl_file("examples/hellow83_sort_2.jcl", "converted/")
        parse_jcl_file("examples/hellow86_parm_example.jcl", "converted/")
        parse_jcl_file("examples/hellowo1_basic.jcl", "converted/")
        #parse_jcl_file("examples/hellowo1_basic_sysout_to_file.jcl", "converted/")
        #parse_jcl_file("examples/hellow12_sequential_file_access.jcl", "converted/")
        #parse_jcl_file("examples/hellow79_sequential_file_access_into.jcl", "converted/")
        #parse_jcl_file("examples/hellowor_mulitple_steps.jcl", "converted/")
        #parse_jcl_file("examples/hellow75_indexed_file_access.jcl", "converted/") 
        #parse_jcl_file("examples/hellow76_indexed_file_write.jcl", "converted/")   