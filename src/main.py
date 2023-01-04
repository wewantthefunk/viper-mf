import glob
from parse_cobol_file import parse_cobol_file

def main():
    for file in glob.glob("../examples/*.cbl"):
        parse_cobol_file(file, "../converted/")
    for file in glob.glob("../examples/*.cob"):
        parse_cobol_file(file, "../converted/")


if __name__ == "__main__":
    main()