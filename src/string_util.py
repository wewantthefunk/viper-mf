"""
String and token helpers used by Cobra and other modules.
"""
import random
import string


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
        if ((t.startswith("'") or t.startswith("X'") or t.startswith("INITIAL='")) and not in_literal):
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
            if count == 0:
                x = 0
            elif t_elements[count + 1].startswith("(") and t_elements[count + 1].endswith(")") and ":" in t_elements[count + 1]:
                skip_next = True
                t = t + t_elements[count + 1]
            elif t_elements[count + 1].startswith("("):
                if t_elements[count + 1][1:2] == "'" and t_elements[count + 2] == "'":
                    t_elements.pop(count + 2)
                    t_elements[count + 1] = t_elements[count + 1] + "'"

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


def find_pos_last_letter(s: str):
    count = 1
    for r in s:
        if not r.isnumeric():
            break
        count = count + 1
    return count


def gen_rand(length: int):
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def count_chars(s: str, char: str):
    count = 0
    for c in s:
        if c == char:
            count += 1
    return count
