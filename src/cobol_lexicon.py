ABEND = "/x"
ACCESS_KEYWORD ="ACCESS"
ALL_KEYWORD ="ALL"
AND_KEYWORD = "AND"
ASSIGN_KEYWORD ="ASSIGN"
AT_KEYWORD = "AT"
BY_KEYWORD = "BY"
CLOSE_BRACKET = ']'
CLOSE_PARENS = ")"
COBOL_COMMENT = "*"
COLON = ":"
COMMA = ","
CONVERTING_KEYWORD = "CONVERTING"
DASH = "-"
DATA_DIVISION_POS = 3
DEF_KEYWORD = "def"
DOUBLE_EQUALS = "=="
DOUBLE_QUOTE = "\""
ELSE = "else"
EMPTY_STRING = ""
END_KEYWORD = "END"
ENVIRONMENT_DIVISION_POS = 2
EQUALS = "="
FALSE_KEYWORD = "FALSE"
FILE_CONTROL_SECTION = "FILE-CONTROL."
FILE_KEYWORD = "FILE"
FILE_STATUS_KEYWORD = "FILE STATUS"
FROM_KEYWORD = "FROM"
FUNCTION_KEYWORD = "FUNCTION"
GIVING_KEYWORD = "GIVING"
GREATER_THAN_EQUAL_TO = ">="
IDENTIFICATION_DIVISION_POS = 0
ID_DIVISION_POS = 1
IN_KEYWORD = "in"
INDENT = "    "
INPUT_OUTPUT_SECTION = "INPUT-OUTPUT SECTION."
IS_KEYWORD ="IS"
KEY_KEYWORD = "KEY"
LESS_THAN = "<"
LINE_KEYWORD = "LINE"
LINES_AHEAD = 10
LITERAL = "literal"
MAIN_ARG_VARIABLE_PREFIX = "_arg"
NEWLINE = "\n"
NEG_ONE = -1
NOT_EQUALS = "!="
NOT_KEYWORD = "NOT"
NUMERIC_KEYWORD = "NUMERIC"
NUMERIC_DATATYPE = "9"
NUMERIC_SIGNED_DATATYPE = "S9"
OPEN_BRACKET = "["
OPEN_PARENS = "("
OR_KEYWORD = "OR"
ORGANIZATION_KEYWORD = "ORGANIZATION"
ORGANISATION_KEYWORD ="ORGANISATION"
PERIOD = "."
PIC_CLAUSE = "PIC"
PLUS_SIGN = "+"
PROCEDURE_DIVISION_POS = 4
PYTHON_EXT = ".py"
RECORD_KEYWORD ="RECORD"
RECORD_KEY_KEYWORD = "RECORD KEY"
REDEFINES_KEYWORD = "REDEFINES"
SELECT_KEYWORD = "SELECT"
SINGLE_QUOTE = "'"
SPACE = " "
SPACE_KEYWORD = "SPACE"
SPACES_INITIALIZER = "____spaces"
STATUS_KEYWORD ="STATUS"
THROUGH_KEYWORD = "THROUGH"
THRU_KEYWORD = "THRU"
TO_KEYWORD = "TO"
TRUE_KEYWORD = "TRUE"
UNDERSCORE = "_"
UNTIL_KEYWORD = "UNTIL"
USING_KEYWORD = "USING"
VALUE_CLAUSE = "VALUE"
VARIABLES_LIST_NAME = "variables_list"
VARYING_KEYWORD = "VARYING"
WHEN_OTHER_KEYWORD = "OTHER"
ZERO = "0"
ZERO_KEYWORD = "ZERO"

COBOL_VERB_ADD = "ADD"
COBOL_VERB_CALL = "CALL"
COBOL_VERB_CLOSE = "CLOSE"
COBOL_VERB_CONTINUE = "CONTINUE"
COBOL_VERB_DISPLAY = "DISPLAY"
COBOL_VERB_ELSE = "ELSE"
COBOL_VERB_EVALUATE = "EVALUATE"
COBOL_VERB_EVALUATE_END = "END-EVALUATE"
COBOL_VERB_EXIT = "EXIT"
COBOL_VERB_GOBACK = "GOBACK"
COBOL_VERB_IF = "IF"
COBOL_VERB_IF_END = "END-IF"
COBOL_VERB_INSPECT = "INSPECT"
COBOL_VERB_MOVE = "MOVE"
COBOL_VERB_OPEN = "OPEN"
COBOL_VERB_PERFORM = "PERFORM"
COBOL_VERB_PERFORM_END = "END-PERFORM"
COBOL_VERB_READ = "READ"
COBOL_VERB_READ_END = "END-READ"
COBOL_VERB_SEARCH = "SEARCH"
COBOL_VERB_SEARCH_END = "END-SEARCH"
COBOL_VERB_STOPRUN = "STOP RUN"
COBOL_VERB_WHEN = "WHEN"
COBOL_VERB_WRITE = "WRITE"

COBOL_VERB_LIST = [
    COBOL_VERB_ADD,
    COBOL_VERB_CALL,
    COBOL_VERB_DISPLAY,
    COBOL_VERB_GOBACK,
    COBOL_VERB_MOVE,
    COBOL_VERB_STOPRUN,
    COBOL_VERB_PERFORM,
    COBOL_VERB_PERFORM_END,
    COBOL_VERB_IF,
    COBOL_VERB_IF_END,
    COBOL_VERB_EXIT,
    COBOL_VERB_ELSE,
    COBOL_VERB_WHEN,
    COBOL_VERB_INSPECT,
    COBOL_VERB_EVALUATE,
    COBOL_VERB_EVALUATE_END,
    COBOL_VERB_CONTINUE,
    COBOL_VERB_OPEN,
    COBOL_VERB_CLOSE,
    COBOL_VERB_READ,
    COBOL_VERB_READ_END,
    COBOL_VERB_WRITE,
    COBOL_VERB_SEARCH
]

COBOL_BOOLEAN_KEYWORDS = [
    OR_KEYWORD
    , AND_KEYWORD
]

COBOL_END_BLOCK_VERBS = [
    COBOL_VERB_PERFORM_END
    , COBOL_VERB_IF_END
    , COBOL_VERB_EVALUATE_END
    , COBOL_VERB_READ_END
    , COBOL_VERB_SEARCH_END
]

COBOL_IDENTIFICATION_DIVISION_VERBS = [
    "PROGRAM-ID."
]

COBOL_DIVISIONS = [
    "IDENTIFICATION DIVISION"
    , "ID DIVISION"
    , "ENVIRONMENT DIVISION"
    , "DATA DIVISION"
    , "PROCEDURE DIVISION"
]

ENVIRONMENT_DIVISION_SECTIONS = [
    FILE_CONTROL_SECTION
]

DATA_DIVISION_SECTIONS = [
    "WORKING-STORAGE SECTION."
    , "LOCAL-STORAGE SECTION."
    , "LINKAGE SECTION."
    , "FILE SECTION."
]

WORKING_STORAGE_LEVELS = [
    "01"
    , "02"
    , "03"
    , "04"
    , "05"
    , "06"
    , "07"
    , "08"
    , "09"
    , "10"
    , "11"
    , "12"
    , "13"
    , "14"
    , "15"
    , "16"
    , "17"
    , "18"
    , "19"
    , "20"
    , "21"
    , "22"
    , "23"
    , "24"
    , "25"
    , "26"
    , "27"
    , "28"
    , "29"
    , "30"
    , "31"
    , "32"
    , "33"
    , "34"
    , "35"
    , "36"
    , "37"
    , "38"
    , "39"
    , "40"
    , "41"
    , "42"
    , "43"
    , "44"
    , "45"
    , "46"
    , "47"
    , "48"
    , "49"
    , "77"
    , "88"
]

COBOL_OPERATORS = [
    '='
    , '<'
    , '>'
    , '<='
    , '>='
]