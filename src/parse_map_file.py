from util import *
from cobol_lexicon import *
import sys

def parse_map_file(map_name: str, target_dir: str):
    if not target_dir.endswith("/"):
        target_dir = target_dir + "/"

    map_name = map_name.strip()

    map = read_file(map_name, False)
    if map == EMPTY_STRING:
        map = read_file(map_name + ".txt", False)
        if map == EMPTY_STRING:
            map = read_file(map_name + ".map", False)
            if map == EMPTY_STRING:
                map = read_file("maps/" + map_name + ".map", False)
                if map == EMPTY_STRING:
                    map = read_file("maps/" + map_name + ".txt", False)
                    if map == EMPTY_STRING:
                        print("MAP " + map_name + " NOT FOUND")
                        return

    lines = map.split(NEWLINE)

    field_info = EMPTY_STRING
    first_level = EMPTY_STRING
    output = EMPTY_STRING

    for x in range(0, len(lines)):
        line = lines[x].strip().replace(NEWLINE, SPACE)
        if line.startswith(COBOL_COMMENT):
            continue
        
        field_info = field_info + line + SPACE
        if line.endswith(MAP_CONTINUATION_CHARACTER) == False:
            if field_info != EMPTY_STRING:
                tokens = parse_line_tokens(field_info, SPACE, EMPTY_STRING, True)
                if "DFHMSD" in tokens:
                    first_level = tokens[0]
                    output = pad(7) + "01 " + first_level + "O REDEFINES " + first_level + "I.\n"
                    delete_file(target_dir + first_level + ".CPY")
                    append_file(target_dir + first_level + ".CPY", pad(7) + "01 " + first_level + "I.\n")
                elif "DFHMDF" in tokens:
                    output = build_field(tokens, target_dir + first_level + ".CPY", output)

            field_info = EMPTY_STRING 

    append_file(target_dir + first_level + ".CPY", output)

    return

def build_field(tokens: list, name: str, output: str):
    datatype = "X"
    length = 0
    initial = "SPACES"
    for token in tokens:
        if token.startswith("ATTRB"):
            if "NUM" in token:
                datatype = "9"
        elif token.startswith("LENGTH"):
            t = token.split("=")
            length = t[1].replace(COMMA, EMPTY_STRING)
        elif token.startswith("INITIAL"):
            t = token.split("=")
            initial = t[1]
    
    append_file(name, pad(10) + "02 " + tokens[0] + "I PIC " + datatype + "(" + length + ") VALUE " + initial + ".\n")
    append_file(name, pad(10) + "02 " + tokens[0] + "F PIC S9(4) COMP VALUE " + length + ".\n")
    append_file(name, pad(10) + "02 " + tokens[0] + "L PIC S9(4) COMP.\n")

    output = output + pad(10) + "02 " + tokens[0] + "O PIC " + datatype + "(" + length + ").\n"
    output = output + pad(10) + "02 FILLER PIC X(2).\n"
    output = output + pad(10) + "02 FILLER PIC X(2).\n"

    return output

if __name__ == "__main__":
    prefix = "../"
    for file in os.listdir("./"):
        d = os.path.join("./", file)
        if os.path.isdir(d):
            if 'examples' in d:
                prefix = ""
                break
    if len(sys.argv) > 1:
        parse_map_file(sys.argv[1], prefix + sys.argv[2])
    else:
        parse_map_file("maps/RECVMAP.txt", prefix + "copybooks/")