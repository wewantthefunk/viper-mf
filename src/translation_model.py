"""
Translation model types for Cobra (LexicalInfo, Replacement).
"""


class LexicalInfo:
    def __init__(self):
        self.current_section = ""
        self.highest_ws_level = 0
        self.first_line_section = False
        self.highest_var_name = ""
        self.highest_var_name_subs = 0
        self.level = 1
        self.import_statement = []
        self.redefines = ""
        self.redefines_level = "01"
        self.lambda_functions = []
        self.skip_the_next_lines = 0
        self.loop_modifier = []
        self.cascade_data_type = ""
        self.cascade_init_value = ""
        self.needs_except_block = False
        self.in_else_block = False
        self.nested_level = 0
        self.last_known_index = 0
        self.end_of_search_criteria = False
        self.source_filename = "unknown"
        self.is_evaluating = False
        self.index_variables = []
        self.sections_list = []
        self.total_copybooks_inserted = 0
        self.unknown_cobol_verbs = 0
        self.next_available_line = ""
        self.paragraph_list = []
        self.last_known_paragraph = ""
        self.last_cmd_display = False
        self.is_cics = False


class Replacement:
    def __init__(self) -> None:
        self.old_value = ""
        self.new_value = ""
