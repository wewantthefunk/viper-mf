"""
Translation context for a single COBOL-to-Python conversion.
Holds all mutable state that was previously module-level globals,
so conversion is reentrant and testable.
"""
from typing import List, Any

from codegen import CodeWriter


class TranslationContext:
    """
    Carries all state for one conversion run.
    Replaces globals: args, verb state (evaluate/perform), data-division stacks.
    """

    def __init__(self, writer: CodeWriter, lexical_info, program_name: str = "abend"):
        self.writer = writer
        self.lexical_info = lexical_info
        self.program_name = program_name
        self.args: List[Any] = []

        # Verb state (from cobol_verb_process)
        self.last_cmd_display = False
        self.evaluate_compare = ""
        self.evaluate_compare_stack: List[tuple] = []
        self.nested_above_evaluate_compare = ""
        self.is_evaluating = False
        self.is_first_when = True
        self.is_perform_looping = False

        # Data division state (from cobol_line_process)
        self.data_division_var_stack: List[str] = []
        self.data_division_level_stack: List[str] = []
        self.data_division_cascade_stack: List[str] = []
        self.data_division_redefines_stack: List[str] = []
        self.data_division_file_record = ""
        self.var_init_list: List[Any] = []
