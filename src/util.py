"""
File I/O and general utilities. Re-exports translation model and string helpers
for backward compatibility with JCL/Krait and other scripts.
"""
import os
from datetime import datetime
from os.path import exists

# Re-export for backward compatibility
from translation_model import LexicalInfo, Replacement
from string_util import (
    parse_line_tokens, pad, pad_char, format,
    get_all_indices, find, find_pos_last_letter, count_chars, gen_rand,
)


def read_file(file: str, should_strip=False):
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
        try:
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR)
        except OSError:
            f.seek(0)
        last_line = f.readline().decode()
    return last_line


def write_file(file: str, data: str):
    _write_file_data(file, data, "w")


def _write_file_data(file: str, data: str, method: str):
    f = open(file, method)
    f.write(data)
    f.close()


def append_file(file: str, data: str):
    _write_file_data(file, data, "a")


def delete_file(file: str):
    if exists(file):
        os.remove(file)


def file_exists(file: str):
    return exists(file)


def insert_beginning_of_file(originalfile, string):
    with open(originalfile, 'r') as f:
        with open('newfile.txt', 'w') as f2:
            f2.write(string)
            f2.write(f.read())
    os.remove(originalfile)
    os.rename('newfile.txt', originalfile)


def move_file(source: str, target: str):
    import shutil
    shutil.move(source, target)


def copy_file(source: str, target: str):
    import shutil
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


def get_value_safe(dict, key: str, default: str):
    if key in dict.keys():
        return str(dict[key])
    else:
        return default
