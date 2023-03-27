from util import *
from cobol_lexicon import *
import sys, glob

def main(prefix: str):
    output_dir = prefix + "converted/"
    input_dir = prefix + "examples/"
    cobol_file_extensions = [".cbl", ".cob"]
    for x in range(0, len(cobol_file_extensions)):
        for file in glob.glob(input_dir + "*" + cobol_file_extensions[x]):
            print("converting " + file)
            calculate_cyclomatic_complexity(file, output_dir, prefix)

    print('')

def calculate_cyclomatic_complexity(file: str, target_dir: str):
    r_lines = read_raw_file_lines(file, 0)

    cyclomatic_keywords = []
    cyclomatic_keywords_count = []
    cyclomatic_complexity_score = 0
    calculate = False
    for rl in r_lines:
        if calculate:
            if any(keyword in rl for keyword in CYCLOMATIC_COMPLEXITY_VERBS):
                for cc_name in CYCLOMATIC_COMPLEXITY_VERBS:
                    if cc_name in rl:
                        index = rl.index(cc_name)
                        sq_index = rl.find(SINGLE_QUOTE, 0, index)
                        lq_index = rl.rfind(SINGLE_QUOTE, index)
                        if sq_index < index and lq_index > index:
                            continue
                        if cc_name in cyclomatic_keywords:
                            i = cyclomatic_keywords.index(cc_name)
                            if i > -1:
                                cyclomatic_keywords_count[i] = cyclomatic_keywords_count[i] + 1
                        else:
                            cyclomatic_keywords.append(cc_name)
                            cyclomatic_keywords_count.append(1)
                        cyclomatic_complexity_score = cyclomatic_complexity_score + 1
        elif PROCEDURE_DIVISION_NAME in rl:
            calculate = True

    print(" file: " + file + "\nscore: " + str(cyclomatic_complexity_score))
    count = 0
    for c in cyclomatic_keywords:
        print(c + COLON + SPACE + str(cyclomatic_keywords_count[count]))
        count = count + 1
    print()
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
        calculate_cyclomatic_complexity(sys.argv[1], sys.argv[2], prefix)
    else:
        calculate_cyclomatic_complexity("examples/hellowo1_basic.cbl", EMPTY_STRING)
        calculate_cyclomatic_complexity("examples/hellowo3_hierarchical_variables.cbl", EMPTY_STRING)
        calculate_cyclomatic_complexity("examples/hellowo9_if_statement_3.cbl", EMPTY_STRING)