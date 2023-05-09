from util import *
from cobol_lexicon import *

def prep_source(r_lines: list, track_debug_lines = True):
    count = 0
    start_tracking_line_number = False
    raw_lines = []
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
            if " PROCEDURE DIVISION" in rl and track_debug_lines:
                start_tracking_line_number = True

            if rl[6:7] == "-":
                line = rl[6:72].rstrip()
            else:
                line = rl[7:72].rstrip()
            t_line = line.split(SPACE, 1)
            l = pad(7) + t_line[0] + SPACE
            if len(t_line) > 1:
                if (SPACE + OPEN_PARENS) in t_line[1]:
                    sp = t_line[1].split(OPEN_PARENS)
                    pl = EMPTY_STRING
                    first = True
                    for s in sp:
                        if first == False:
                            t = s.strip().split(SPACE)
                            if pl in COBOL_VERB_LIST or pl in COBOL_COMPARISON_OPERATORS:
                                pl = pl + SPACE + OPEN_PARENS
                            else:
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

    return raw_lines

def prep_copybook(current_line: LexicalInfo, copybook: str, next_few_lines):
    current_line.skip_the_next_lines = 0
    has_replacing_keyword = False
    if not copybook.endswith(PERIOD) and REPLACING_KEYWORD not in copybook:
        not_end = True
        count = 0
        while not_end:
            if REPLACING_KEYWORD in next_few_lines[count]:
                has_replacing_keyword = True
                not_end = False
            count = count + 1
            if count >= len(next_few_lines):
                not_end = False
    elif REPLACING_KEYWORD in copybook:
        has_replacing_keyword = True

    replace_info = [copybook, EMPTY_STRING, EMPTY_STRING, EMPTY_STRING]
    array_by = []
    array_before_by = []
    if has_replacing_keyword:
        replace_info = copybook.split(REPLACING_KEYWORD)
        copybook = replace_info[0].replace(REPLACING_KEYWORD, EMPTY_STRING).strip()
        temp = replace_info[0].replace(SPACE, EMPTY_STRING)
        if len(replace_info) == 1:
            replace_info.pop()
        if len(replace_info) == 0 or replace_info[len(replace_info) - 1] != PERIOD:
            for next_line in next_few_lines:
                replace_info.append(next_line.replace(REPLACING_KEYWORD, EMPTY_STRING))
                if next_line.rstrip().endswith(PERIOD):
                    break
        if temp == copybook + REPLACING_KEYWORD:
            replace_info.pop(0)
        indices = [i for i in range(len(replace_info)) if BY_KEYWORD in replace_info[i]]
        array_by = []
        array_before_by = []
        for index in indices:
            line = replace_info[index].strip()
            if "==" not in line:
                p = line.split(BY_KEYWORD)[0]
                i = index - 1
                while p == EMPTY_STRING and i > -1:
                    p = replace_info[i].strip()
                before_by_items = [p]
            elif not line.startswith("=="):
                i = index - 1
                while not replace_info[i].strip().startswith("=="):
                    i -= 1
                before_by_items = replace_info[i:index]
            else:
                before_by_items = line.split('BY')[0].split('==')[1:]
            array_before_by.append('\n'.join([item.strip() for item in before_by_items]))
            #items = line.split('BY')[1].split('==')
            #array_by.append('\n'.join([item.strip() for item in items]))
            if "==" not in line or line.endswith(BY_KEYWORD):
                p = line.split(BY_KEYWORD)[1]
                i = index + 1
                while p == EMPTY_STRING and i <= len(replace_info):
                    p = p + replace_info[i].strip()
                    i = i + 1
                items = [p]
            elif not line.endswith("==") and not line.endswith("==."):
                line = line.replace(BY_KEYWORD, EMPTY_STRING).strip()
                if line.startswith("=="):
                    offset = 0
                    i = index
                else:
                    offset = 1
                    i = index + 1
                while not replace_info[i].endswith("==") and not replace_info[i].endswith("==."):
                    i += 1
                    items = replace_info[index+offset:i+1]
            else:
                items = line.split('BY')[1].split('==')[1:-1]
            array_by.append('\n'.join([item.strip() for item in items]))

        for x in range(0, len(array_by)):
            array_by[x] = array_by[x].replace("==.", EMPTY_STRING)
            array_by[x] = array_by[x].replace("==", EMPTY_STRING).replace(BY_KEYWORD, EMPTY_STRING).strip()

        for x in range(0, len(array_before_by)):
            array_before_by[x] = array_before_by[x].replace("==.", EMPTY_STRING)
            array_before_by[x] = array_before_by[x].replace("==", EMPTY_STRING).replace(BY_KEYWORD, EMPTY_STRING).strip()

    ogc = copybook
    file_exists = exists(copybook)
    if file_exists == False:
        copybook = copybook + COPYBOOK_EXT
        file_exists = exists(copybook)
        if file_exists == False:
            copybook = COPYBOOK_FOLDER + copybook
            file_exists = exists(copybook)
            if file_exists == False:
                copybook = copybook.replace(COPYBOOK_EXT, EMPTY_STRING)
                file_exists = exists(copybook)
                if file_exists == False:
                    print("Copybook NOT FOUND: " + ogc)
                    print("Aborting conversion!")
                    return

    current_line.total_copybooks_inserted = current_line.total_copybooks_inserted + 1
    file_lines = read_file(copybook, False)
    for x in range(0, len(array_by)):
        before = array_before_by[x]
        if before.startswith(NEWLINE):
            before = before[1:]
        after = array_by[x]
        if after.startswith(NEWLINE):
            after = after[1:]
        repl_old_list = before.split(NEWLINE)
        repl_new_list = after.split(NEWLINE)
        while len(repl_new_list) > len(repl_old_list):
            repl_new_list[len(repl_new_list) - 2] = repl_new_list[len(repl_new_list) - 2] + NEWLINE + pad(11) + repl_new_list[len(repl_new_list) - 1]
            repl_new_list.pop()
        while len(repl_old_list) > len(repl_new_list):
            repl_new_list.append(EMPTY_STRING)
        c = 0
        for repl_old in repl_old_list:
            file_lines = file_lines.replace(repl_old, repl_new_list[c])
            c = c + 1

    write_file("temp_cpybook.txt", file_lines)
    raw_lines = read_raw_file_lines("temp_cpybook.txt", 0)
      
    result_lines = []

    for line in raw_lines:
        line = line[6:].strip()
        line = pad(7) + line
        if line == EMPTY_STRING:
            continue
        if line != EMPTY_STRING and line.startswith(COBOL_COMMENT) == False:
            result_lines.append(line)

    #delete_file("temp_cpybook.txt")
    copy_file("temp_cpybook.txt", copybook + "_copybook.txt")

    return [result_lines, copybook, next_few_lines]