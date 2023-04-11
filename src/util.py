import os
import random
import shutil
import string
from datetime import datetime
from os.path import exists

class LexicalInfo:
    def __init__(self):
        self.current_section = ""
        self.highest_ws_level = 0
        self.first_line_section = False
        self.highest_var_name = ""
        self.highest_var_name_subs = 0
        self.level = 1
        self.import_statement = []
        self.redefines = ""
        self.redefines_level = "01"
        self.lambda_functions = []
        self.skip_the_next_lines = 0
        self.loop_modifier = []
        self.cascade_data_type = ""
        self.needs_except_block = False
        self.in_else_block = False
        self.nested_level = 0
        self.last_known_index = 0
        self.end_of_search_criteria = False
        self.source_filename = "unknown"
        self.is_evaluating = False
        self.index_variables = []
        self.sections_list = []

class Replacement:
    def __init__(self) -> None:
        self.old_value = ""
        self.new_value = ""

def read_file(file: str, should_strip = False):
    result = ""
    with open(file) as file:
        for line in file:
            if should_strip:
                line = line.strip() + "\n"
            result = result + line
    return result

def read_raw_file_lines(file: str, skip: str):
    result = []
    count = 0
    with open(file) as file:
        
        for line in file:
            if count >= skip:
                result.append(line)
            count = count + 1
    return result

def get_last_line_of_file(file: str):
    with open(file, 'rb') as f:
        try:  # catch OSError in case of a one line file 
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR)
        except OSError:
            f.seek(0)
        last_line = f.readline().decode()

    return last_line

def write_file(file: str, data: str):
    _write_file_data(file,data,"w")

def _write_file_data(file: str, data: str, method: str):
    f = open(file,method)
    f.write(data)
    f.close()

def append_file(file: str, data: str):
    _write_file_data(file,data,"a")

def delete_file(file: str):
    if exists(file):
        os.remove(file)

def file_exists(file: str):
    return exists(file)

def insert_beginning_of_file(originalfile,string):
    with open(originalfile,'r') as f:
        with open('newfile.txt','w') as f2: 
            f2.write(string)
            f2.write(f.read())
    os.remove(originalfile)
    os.rename('newfile.txt',originalfile)

def move_file(source: str, target: str):
    shutil.move(source, target)

def copy_file(source: str, target: str):
    shutil.copyfile(source, target)

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

def has_key(array, key: str):
    count = -1
    for item in array:
        count = count + 1
        if item.key == key:
            return count

    return -1

def get_time():
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    return "Current Time = " + current_time

def sort_array(array):
    if hasattr(array, "sortOrder"):
        return array.sortOrder

    return array.key

def get_value_safe(dict,key: str, default: str):
    if key in dict.keys():
        return str(dict[key])
    else:
        return default

def parse_line_tokens(line: str, split_on: str, ignore_value: str, keep_period: bool):
    line = line.replace("'''", "'")
    t_elements = line.split(split_on)
    line_elements = []
    literal = ""
    in_literal = False
    has_period = False
    skip_next = False
    count = 0
    if t_elements[len(t_elements) - 1].endswith("."):
        has_period = keep_period
        t_elements[len(t_elements) - 1] = t_elements[len(t_elements) - 1].replace(".", "")
    for e in t_elements:
        if skip_next:
            skip_next = False
            continue

        t = e.strip()
        if ((t.startswith("'") or t.startswith("X'")) and not in_literal):
            literal = literal + t
            in_literal = True
            if (t.endswith("'") and t != "'"):
                in_literal = False
                literal = ''
        elif (t.endswith("'")):
            literal = literal + " " + t
            t = literal
            in_literal = False
            literal = ""
        elif in_literal:
            literal = literal + " " + t
        elif count + 1 < len(t_elements):
            if t_elements[count + 1].startswith("(") and t_elements[count + 1].endswith(")") and ":" in t_elements[count + 1]:
                skip_next = True
                t = t + t_elements[count + 1]

        if t != ignore_value and not in_literal:
            line_elements.append(t)
            t = ''

        count = count + 1

    if in_literal:
        line_elements.append(literal)
    if has_period:
        line_elements.append(".")
    return line_elements

def format(s: str):
    return s.replace(".", "").replace(" ", "_").replace("-", "_").strip()

def get_all_indices(list, search: str):
    indices = [i for i, x in enumerate(list) if x == search]

    return indices

def pad(l: int):
    return pad_char(l, " ")

def pad_char(l: int, c: str):
    result = ""
    for x in range(l):
        result = result + c

    return result

def find(s: str, ch: str):
    return [i for i, ltr in enumerate(s) if ltr == ch]

def gen_rand(length: int):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def count_chars(s: str, char: str):
    count = 0

    for c in s:
        if c == char:
            count += 1

    return count