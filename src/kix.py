from tkinter import *
from tkinter import font
from io import StringIO
import importlib, sys, os
import cobol_variable

ATTRB_KEYWORD = "ATTRB"
BOTH_OPTION = "both"
CARRIAGE_RETURN = "\r"
CLOSE_PARENS = ")"
COBOL_COMMENT = "*"
COLON = ":"
COMMA = ","
COMMAND_PROMPT_PREFIX = "> "
CYCLE_DOWN = 1
CYCLE_UP = -1
DD_CONFIG_FILE = "dd.config"
DOWN_ARROW = 40
EMPTY_STRING = ""
ENTER_KEY = "\r"
ENTRY_BOX_BACKGROUND = "white"
ENTRY_BOX_TEXT_COLOR = "black"
EQUALS = "="
ERROR_TEXT_COLOR = "red"
ESCAPE = 27
HIDE_SYSOUT = "hide sysout"
INVALID_COMMAND_MSG = "INVALID COMMAND:"
LINE_SPACING = 6
LINUX_DOWN_ARROW = 116
LINUX_ENTER_KEY = 36
LINUX_ESCAPE_KEY = 9
LINUX_UP_ARROW = 111
LINUX_OS = "posix"
LIST_TRANSACTIONS = "list trans"
MAP_CONTINUATION_CHARACTER = "X"
MAP_FIELD_IDENTIFIER = 'DFHMDF'
NEWLINE = "\n"
OPEN_PARENS = "("
OS_LABEL = "OS: "
PIPE_FLAG = "<"
SET_DD = "set dd"
SET_TRANSACTION = "set tran"
SHOW_SYSOUT = "show sysout"
SPACE = " "
STANDARD_BACKGROUND_COLOR = "black"
STANDARD_CURSOR_SIZE = 10
STANDARD_FONT = "Courier"
STANDARD_FONT_SIZE = 14
STANDARD_TEXT_COLOR = "white"
START_COMMAND = "start"
SYSOUT_TITLE = "KIX SYSOUT Display"
SYSOUT_WINDOW_SIZE = '300x300'
TRANSACTION_CONFIG_FILE = "trans.config"
UP_ARROW = 38
WINDOW_TITLE = "KIX CICS Emulator"
WINDOW_SIZE = '1520x768'
WINDOWS_OS = "nt"
ZERO = 0

class KIXEntry:
    def __init__(self, name: str, length: int) -> None:
        self.name = name
        self.length = length
        self.field = StringVar()
        self.entry_field = None

class KIX:     
    def __init__(self):
        self.window = Tk()

        self.window.title(WINDOW_TITLE)
        self.window.geometry(WINDOW_SIZE)
        self.window.configure(bg=STANDARD_BACKGROUND_COLOR)
        self.window.resizable(width=False, height=False)
        self.command_input = None
        self.message_label = None
        self.sysout_label = None
        self.main_frame = None
        self.character_height = STANDARD_FONT_SIZE
        self.character_width = 10
        self.map_entry_fields = []

        self.command_list = []
        self.current_command_entry = len(self.command_list)

        self.sysout = Toplevel()
        self.sysout.protocol("WM_DELETE_WINDOW", self.hide_sysout_window)
        self.show_sysout = False

        cobol_variable.initialize()

        self.set_dd_values()

        return

    def Launch(self):
        lbl = Label(self.window, text=COMMAND_PROMPT_PREFIX, font=(STANDARD_FONT, STANDARD_FONT_SIZE),background=STANDARD_BACKGROUND_COLOR,foreground=STANDARD_TEXT_COLOR)
        lbl.place(x=5,y=4,in_=self.window)

        txt = Entry(self.window,width=127,font=(STANDARD_FONT, STANDARD_FONT_SIZE),background=ENTRY_BOX_BACKGROUND,foreground=ENTRY_BOX_TEXT_COLOR)
        txt.place(x=25,y=4,in_=self.window)
        txt.bind("<Key>", self.on_keypress)
        txt.config(insertbackground=STANDARD_TEXT_COLOR)
        txt.config(insertwidth=STANDARD_CURSOR_SIZE)
        txt.focus_set()
        self.command_input = txt

        cmd_btn = Button(self.window,width=7,font=(STANDARD_FONT, STANDARD_FONT_SIZE), text="Submit",command=self.cmd_click)
        cmd_btn.place(x=1430,y=1,in_=self.window)

        f1 = Frame(self.window,background=STANDARD_BACKGROUND_COLOR)
        f1.pack(padx=0,pady=30,fill=BOTH_OPTION, expand=True)
        self.main_frame = f1

        temp_lbl = Label(self.window, text=EMPTY_STRING, font=(STANDARD_FONT, STANDARD_FONT_SIZE),name="message_label",background=STANDARD_BACKGROUND_COLOR,foreground=STANDARD_TEXT_COLOR)
        temp_lbl.place(x=5,y=740)
        self.message_label = temp_lbl

        self.sysout_label = self.create_label(self.sysout, EMPTY_STRING, "sysout_label", 5, 5)
        self.sysout.geometry(SYSOUT_WINDOW_SIZE)
        self.sysout.title(SYSOUT_TITLE)
        self.sysout.configure(bg=STANDARD_BACKGROUND_COLOR)

        self.sysout.withdraw()

        self.write_to_sysout(OS_LABEL + os.name + NEWLINE)

        f = font.Font(size=STANDARD_FONT_SIZE, family=STANDARD_BACKGROUND_COLOR)
        self.character_width = f.measure('W')
        self.character_height = f.metrics("linespace")
        self.window.mainloop()

        return

    def create_label(self, widget, text: str, name: str, place_x:int, place_y: int, spacing = 0):
        label = Label(widget, text=text, name=name, background=STANDARD_BACKGROUND_COLOR, foreground=STANDARD_TEXT_COLOR, justify=LEFT, font=(STANDARD_FONT, STANDARD_FONT_SIZE))
        label.place(x=(place_x - 1) * self.character_width, y=place_y * (self.character_height + spacing))
        return label

    def create_map_entry(self, widget, text: str, name: str, place_x:int, place_y: int, length: int, has_cursor: bool):
        t = StringVar()
        found = False
        if len(self.map_entry_fields) > ZERO:
            t = self.map_entry_fields[len(self.map_entry_fields) - 1].field
            found = True
        entry_field = Entry(widget, text=text, name=name, background=ENTRY_BOX_BACKGROUND, foreground=ENTRY_BOX_TEXT_COLOR, justify=LEFT, font=(STANDARD_FONT, STANDARD_FONT_SIZE), width=length, textvariable=t)
        entry_field.place(x=place_x * self.character_width, y=place_y * (self.character_height + LINE_SPACING))
        if has_cursor:
            entry_field.focus()

        if found:
            self.map_entry_fields[len(self.map_entry_fields) - 1].entry_field = entry_field
        return entry_field

    def validate(self, name, index, mode):
        for entry in self.map_entry_fields:
            if entry.field._name == name:
                value = entry.field.get()
                if len(value) > entry.length and entry.entry_field != None:
                    value = value[0:entry.length]
                    entry.entry_field.delete(ZERO, END)
                    entry.entry_field.insert(ZERO, value)
                    break
                break

        return

    def on_keypress(self, event):
        if os.name == WINDOWS_OS:
            if event.char == ENTER_KEY:
                self.cmd_click()
            elif event.keycode == UP_ARROW:
                self.cycle_commands(CYCLE_UP)
            elif event.keycode == DOWN_ARROW:
                self.cycle_commands(CYCLE_DOWN)
            elif event.keycode == ESCAPE:
                self.command_input.delete(ZERO, END)
        elif os.name == LINUX_OS:
            if event.keycode == LINUX_ENTER_KEY:
                self.cmd_click()
            elif event.keycode == LINUX_UP_ARROW:
                self.cycle_commands(CYCLE_UP)
            elif event.keycode == LINUX_DOWN_ARROW:
                self.cycle_commands(CYCLE_DOWN)
            elif event.keycode == LINUX_ESCAPE_KEY:
                self.command_input.delete(ZERO, END)
        
        return

    def cycle_commands(self, modifier: int):
        if len(self.command_list) == ZERO:
                return
        self.command_input.delete(ZERO, END)
        self.command_input.insert(ZERO, self.command_list[self.current_command_entry])
        self.current_command_entry = self.current_command_entry + modifier
        if self.current_command_entry < 0:
            self.current_command_entry = len(self.command_list) + modifier
        
        if self.current_command_entry >= len(self.command_list):
            self.current_command_entry = ZERO

        return

    def clear_frame(frame):
        for widget in frame.winfo_children():
            widget.destroy()

        return

    def cmd_click(self):
        text = self.command_input.get().strip()
        self.process_command(text)

        return

    def set_dd_values(self):
        current_dd = cobol_variable._read_file(DD_CONFIG_FILE, False)
        dd_splits = current_dd.split(NEWLINE)
        for dd_split in dd_splits:
            if dd_split == EMPTY_STRING:
                continue

            s = dd_split.split(COLON)
            os.environ[s[0]] = s[1].replace(NEWLINE, EMPTY_STRING).replace(CARRIAGE_RETURN, EMPTY_STRING)

    def process_command(self, text: str):
        self.current_command_entry = len(self.command_list) - 1
        self.message_label.config(foreground=STANDARD_TEXT_COLOR)
        self.command_input.delete(ZERO, END)
        self.message_label.config(text=EMPTY_STRING)
        if text.lower().startswith(START_COMMAND):
            self.start_module(text)
        elif text.lower().startswith(SHOW_SYSOUT):
            self.show_sysout_window()
        elif text.lower().startswith(HIDE_SYSOUT):
            self.hide_sysout_window()
        elif text.lower().startswith(PIPE_FLAG):
            self.write_to_sysout(text[len(PIPE_FLAG):] + NEWLINE)
        elif text.lower().startswith(SET_TRANSACTION):
            self.set_transaction(text)
        elif text.lower().startswith(LIST_TRANSACTIONS):
            self.list_transactions()
        elif text.lower().startswith(SET_DD):
            self.set_dd(text)
        else:
            trans = self.check_for_transaction(text)
            if trans != EMPTY_STRING:
                self.start_module(START_COMMAND + SPACE + trans)
            else:
                self.show_error_message(text)
                return

        self.command_list.append(text)

        return

    def show_error_message(self, text: str):
        self.message_label.config(foreground=ERROR_TEXT_COLOR)
        self.message_label.config(text=INVALID_COMMAND_MSG + SPACE + text)

    def list_transactions(self):
        current_transactions = cobol_variable._read_file(TRANSACTION_CONFIG_FILE)
        self.write_to_sysout(current_transactions + NEWLINE)
        return

    def set_transaction(self, text: str):
        tokens = text.split(SPACE)
        current_transactions = cobol_variable._read_file(TRANSACTION_CONFIG_FILE)
        current_transactions = current_transactions + NEWLINE + tokens[2] + COLON + tokens[3]
        cobol_variable._write_file(TRANSACTION_CONFIG_FILE, current_transactions)
        return

    def set_dd(self, text: str):
        tokens = text.split(SPACE)
        current_dd = cobol_variable._read_file(DD_CONFIG_FILE)
        value = EMPTY_STRING
        for x in range(3, len(tokens)):
            value = value + tokens[x] + SPACE
        temp = EMPTY_STRING

        dds = current_dd.split(NEWLINE)

        found = False
        for dd in dds:
            dd_info = dd.split(COLON)
            if dd_info[0] == tokens[2]:
                found = True
                temp = temp + NEWLINE + tokens[2] + COLON + value
            else:
                temp = temp + NEWLINE + dd

        if found == False:
            temp = temp + NEWLINE + tokens[2] + COLON + value

        cobol_variable._write_file(DD_CONFIG_FILE, temp)

        self.set_dd_values()
        
        return

    def check_for_transaction(self, trans: str):
        trans = trans.lower().strip()
        current_transactions = cobol_variable._read_file(TRANSACTION_CONFIG_FILE).split(NEWLINE)
        for ct in current_transactions:
            s = ct.split(COLON)
            if len(s) < 2 or s[0] == EMPTY_STRING:
                return EMPTY_STRING
            if s[0].lower().strip() == trans:
                return s[1]

        return EMPTY_STRING

    def start_module(self, text: str):
        module_name = text
        try:
            tokens = text.split(SPACE)
            module_name = tokens[1]
            module = importlib.import_module(module_name)
            module_class = getattr(module, module_name + 'Class')
            module_instance = module_class()
            module_instance.calling_module = self

            # create a StringIO object
            string_io = StringIO()

            # redirect stdout to the StringIO object
            sys.stdout = string_io

            # call the module
            module_instance.main()        

            # get the contents of the StringIO object
            output = string_io.getvalue()

            # reset stdout to the original stream
            sys.stdout = sys.__stdout__

            self.write_to_sysout(output)

            return
        except:
            self.show_error_message("unable to start, module not found: " + module_name)

    def write_to_sysout(self, output: str):
        t = self.sysout_label.cget("text")
        self.sysout_label.config(text=t + output)

        return

    def show_sysout_window(self):
        if self.show_sysout:
            return

        self.sysout.deiconify()
        self.show_sysout = True

        return

    def hide_sysout_window(self):
        if self.show_sysout == False:
            return
            
        self.sysout.withdraw()
        self.show_sysout = False

        return

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def build_map(self, info: str):
        self.clear_frame(self.main_frame)
        map = cobol_variable._read_file(info + ".txt", False)
        if map == EMPTY_STRING:
            map = cobol_variable._read_file(info + ".map", False)
            if map == EMPTY_STRING:
                map = cobol_variable._read_file("maps/" + info + ".map", False)
                if map == EMPTY_STRING:
                    map = cobol_variable._read_file("maps/" + info + ".txt", False)
                    if map == EMPTY_STRING:
                        self.show_error_message("MAP " + info + " NOT FOUND")
                        return

        lines = map.split(NEWLINE)

        field_info = EMPTY_STRING

        for x in range(0, len(lines)):
            line = lines[x].strip().replace(NEWLINE, SPACE).replace(CARRIAGE_RETURN, SPACE)
            if line.startswith(COBOL_COMMENT):
                continue
            
            field_info = field_info + line + SPACE
            if line.endswith(MAP_CONTINUATION_CHARACTER) == False:
                self.build_field(field_info)
                field_info = EMPTY_STRING

        self.build_field(field_info)

    def build_field(self, field_info: str):
        if MAP_FIELD_IDENTIFIER not in field_info:
            return ZERO

        field_type = 'none'
        field_length = 0
        field_x = 1
        field_y = 1
        field_text = EMPTY_STRING
        tokens = self.parse_tokens(field_info)
        skip_lines = 0
        var_name = tokens[0].lower()
        has_focus = False
        for token in tokens:
            skip_lines = skip_lines + 1
            if ATTRB_KEYWORD in token:
                s = token.split(OPEN_PARENS)
                attributes = s[1].replace(CLOSE_PARENS, EMPTY_STRING).split(COMMA)
                if 'PROT' in attributes or 'ASKIP' in attributes:
                    field_type = "lbl"
                elif "UNPROT" in attributes:
                    field_type = "entry"

                if "IC" in attributes:
                    has_focus = True
            elif 'POS' in token:
                s = token.split(OPEN_PARENS)
                pos = s[1].replace(CLOSE_PARENS, EMPTY_STRING).split(COMMA)
                field_y = int(pos[0].replace(COMMA, EMPTY_STRING))
                field_x = int(pos[1].replace(COMMA, EMPTY_STRING))
            elif 'LENGTH' in token:
                s = token.split(EQUALS)
                field_length = int(s[1].replace(COMMA, EMPTY_STRING))
            elif 'INITIAL' in token:
                s = token.split(EQUALS)
                field_text = s[1]
                if field_text.startswith("'"):
                    field_text = field_text[1:]
                if field_text.endswith("'"):
                    field_text = field_text[:len(field_text) - 1]
            elif 'DFHMSD' in token or 'DFHMDI' in token:
                field_type = "none"

        if field_type == "lbl":
            self.create_label(self.main_frame, field_text, var_name, field_x, field_y, LINE_SPACING)
        elif field_type == "entry":
            t = KIXEntry(name=var_name,length=field_length)
            t.field.trace('w', self.validate)
            self.map_entry_fields.append(t)
            self.create_map_entry(self.main_frame, field_text, var_name, field_x, field_y, field_length, has_focus)

        return skip_lines

    def parse_tokens(self, field_info: str):
        temp_tokens = field_info.split(SPACE)
        result = []
        for token in temp_tokens:
            if token.strip() != EMPTY_STRING:
                result.append(token)

        return result

if __name__ == '__main__':
    Kix_obj = KIX()

    Kix_obj.Launch()