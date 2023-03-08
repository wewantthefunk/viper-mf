import glob, sys, os
from parse_cobol_file import parse_cobol_file

def main(prefix: str):
    output_dir = prefix + "converted/"
    input_dir = prefix + "examples/"
    cobol_file_extensions = [".cbl", ".cob"]
    for x in range(0, len(cobol_file_extensions)):
        for file in glob.glob(input_dir + "*" + cobol_file_extensions[x]):
            print("converting " + file)
            parse_cobol_file(file, output_dir, prefix)

    print('')


if __name__ == "__main__":
    prefix = "../"
    for file in os.listdir("./"):
        d = os.path.join("./", file)
        if os.path.isdir(d):
            if 'examples' in d:
                prefix = ""
                break
    if len(sys.argv) > 1:
        parse_cobol_file(sys.argv[1], sys.argv[2], prefix)
    else:
        main(prefix)