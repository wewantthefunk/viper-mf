from util import *
from cobol_lexicon import *
import sys

def parse_map_file(map_name: str, target_dir: str):
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

    for x in range(0, len(lines)):
        line = lines[x].strip().replace(NEWLINE, SPACE)
        if line.startswith(COBOL_COMMENT):
            continue
        
        field_info = field_info + line + SPACE
        if line.endswith(MAP_CONTINUATION_CHARACTER) == False:
            build_field(field_info)
            field_info = EMPTY_STRING

    if field_info != EMPTY_STRING:
        build_field(field_info)

    return

def build_field(field_info: str):
    if field_info.startswith("LBL"):
        x = 0
    tokens = parse_line_tokens(field_info, SPACE, EMPTY_STRING, True)
    print(tokens)
    return

if __name__ == "__main__":
    prefix = "../"
    for file in os.listdir("./"):
        d = os.path.join("./", file)
        if os.path.isdir(d):
            if 'examples' in d:
                prefix = ""
                break
    if len(sys.argv) > 1:
        parse_map_file(sys.argv[1], sys.argv[2], prefix)
    else:
        parse_map_file("maps/RECVMAP.txt", "copybooks/")