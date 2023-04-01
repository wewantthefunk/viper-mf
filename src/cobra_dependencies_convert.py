from parse_cobol_file import parse_cobol_file
import os

if __name__ == "__main__":
    prefix = "../"
    for file in os.listdir("./"):
        d = os.path.join("./", file)
        if os.path.isdir(d):
            if 'examples' in d:
                prefix = ""
                break
    print("Converting: " + prefix + "dependencies/CEE3AB2.cbl --> " + prefix + "converted/")
    parse_cobol_file(prefix + "dependencies/CEE3AB2.cbl", prefix + "converted/",  prefix)
    print("Converting: " + prefix + "dependencies/RANDSTR.cbl --> " + prefix + "converted/")
    parse_cobol_file(prefix + "dependencies/RANDSTR.cbl", prefix + "converted/",  prefix)
    print("Converting: " + prefix + "dependencies/GETDSNS.cbl --> " + prefix + "converted/")
    parse_cobol_file(prefix + "dependencies/GETDSNS.cbl", prefix + "converted/",  prefix)
