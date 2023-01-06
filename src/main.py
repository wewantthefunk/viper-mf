import glob
from parse_cobol_file import parse_cobol_file

def main():
    output_dir = "../converted/"
    input_dir = "../examples/"
    cobol_file_extensions = [".cbl", ".cob"]
    for x in range(0, len(cobol_file_extensions)):
        for file in glob.glob(input_dir + "*" + cobol_file_extensions[x]):
            parse_cobol_file(file, output_dir)


if __name__ == "__main__":
    main()