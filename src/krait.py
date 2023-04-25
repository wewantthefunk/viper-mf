from tkinter import *
from tkinter import font
from tkinter import ttk
from io import StringIO
from os.path import exists
import importlib, sys, os, random
import cobol_variable, string
import krait_region, krait_util

class KRAIT:     
    def __init__(self):
        self.queues = []

        self.window = Tk()
        self.window.bind("<Key>", self.main_on_keypress)
        self.window.title(krait_util.WINDOW_TITLE)
        self.window.geometry(krait_util.WINDOW_SIZE)
        self.window.configure(bg=krait_util.STANDARD_BACKGROUND_COLOR)
        self.window.resizable(width=False, height=False)
        self.command_input = None
        self.message_label = None
        self.sysout_label = None
        self.main_frame = None
        self.transaction_module = None
        self.character_height = krait_util.STANDARD_FONT_SIZE
        self.character_width = 10
        self.map_entry_fields = []
        self.last_known_trans_id = krait_util.GENERIC_TRANS_ID

        self.is_in_transaction = False
        self.map_key_pressed = BooleanVar()

        self.command_list = []
        self.current_command_entry = len(self.command_list)

        self.sysout = Toplevel()
        self.sysout.protocol("WM_DELETE_WINDOW", self.hide_sysout_window)
        self.show_sysout = False

        cobol_variable.initialize()

        if exists(krait_util.TERMINAL_CONFIG) == False:
            cobol_variable._write_file(krait_util.TERMINAL_CONFIG, self.create_terminal_id())

        self.terminal_id = cobol_variable._read_file(krait_util.TERMINAL_CONFIG, True)
        self.transaction_id = krait_util.EMPTY_STRING
        self.transaction_label = None
        self.region_label = None

        self.set_dd_values()

        self.variables_list = []
        self.eib_variables = []
        self.variables_list.append(self.eib_variables)
        self.EIBMemory = krait_util.EMPTY_STRING

        result = cobol_variable.Add_Variable(self.EIBMemory,self.eib_variables,'EIB-FIELDS', 0, 'X','EIB-FIELDS','',0,0,'','01')
        self.eib_variables = result[0]
        self.EIBMemory = result[1]
        result = cobol_variable.Add_Variable(self.EIBMemory,self.eib_variables,'EIBAID', 1, 'X','EIB-FIELDS','',0,0,'','05')
        self.eib_variables = result[0]
        self.EIBMemory = result[1]
        result = cobol_variable.Add_Variable(self.EIBMemory,self.eib_variables,'EIBCALEN', 4, 'S9','EIB-FIELDS','',0,0,'COMP','05')
        self.eib_variables = result[0]
        self.EIBMemory = result[1]
        result = cobol_variable.Add_Variable(self.EIBMemory,self.eib_variables,'EIBDATE', 7, 'S9','EIB-FIELDS','',0,0,'COMP-3','05')
        self.eib_variables = result[0]
        self.EIBMemory = result[1]
        result = cobol_variable.Add_Variable(self.EIBMemory,self.eib_variables,'IEBRCODE', 6, 'X','EIB-FIELDS','',0,0,'','05')
        self.eib_variables = result[0]
        self.EIBMemory = result[1]
        result = cobol_variable.Add_Variable(self.EIBMemory,self.eib_variables,'EIBTASKN', 7, 'S9','EIB-FIELDS','',0,0,'COMP-3','05')
        self.eib_variables = result[0]
        self.EIBMemory = result[1]
        result = cobol_variable.Add_Variable(self.EIBMemory,self.eib_variables,'EIBTIME', 7, 'S9','EIB-FIELDS','',0,0,'COMP-3','05')
        self.eib_variables = result[0]
        self.EIBMemory = result[1]
        result = cobol_variable.Add_Variable(self.EIBMemory,self.eib_variables,'EIBTRMID', 4, 'X','EIB-FIELDS','',0,0,'','05')
        self.eib_variables = result[0]
        self.EIBMemory = result[1]
        result = cobol_variable.Add_Variable(self.EIBMemory,self.eib_variables,'EIBTRNID', 4, 'X','EIB-FIELDS','',0,0,'','05')
        self.eib_variables = result[0]
        self.EIBMemory = result[1]

        result = cobol_variable.Allocate_Memory(self.eib_variables, self.EIBMemory)
        self.eib_variables = result[0]
        self.EIBMemory = result[1]

        return

    def Launch(self):
        lbl = Label(self.window, text=krait_util.COMMAND_PROMPT_PREFIX, font=(krait_util.STANDARD_FONT, krait_util.STANDARD_FONT_SIZE),background=krait_util.STANDARD_BACKGROUND_COLOR,foreground=krait_util.STANDARD_TEXT_COLOR)
        lbl.place(x=5,y=4,in_=self.window)

        txt = Entry(self.window,width=127,font=(krait_util.STANDARD_FONT, krait_util.STANDARD_FONT_SIZE),background=krait_util.ENTRY_BOX_BACKGROUND,foreground=krait_util.ENTRY_BOX_TEXT_COLOR)
        txt.place(x=25,y=4,in_=self.window)
        txt.bind("<Key>", self.on_keypress)
        txt.config(insertwidth=krait_util.STANDARD_CURSOR_SIZE)
        txt.config(insertbackground=krait_util.ENTRY_CURSOR_COLOR)
        txt.focus_set()
        self.command_input = txt

        cmd_btn = Button(self.window,width=7,font=(krait_util.STANDARD_FONT, krait_util.STANDARD_FONT_SIZE), text="Submit",command=self.cmd_click)
        cmd_btn.place(x=1430,y=1,in_=self.window)

        f1 = Frame(self.window,background=krait_util.STANDARD_BACKGROUND_COLOR)
        f1.pack(padx=0,pady=30,fill=krait_util.BOTH_OPTION, expand=True)
        self.main_frame = f1

        temp_lbl = Label(self.window, text=krait_util.EMPTY_STRING, font=(krait_util.STANDARD_FONT, krait_util.STANDARD_FONT_SIZE),name="message_label",background=krait_util.STANDARD_BACKGROUND_COLOR,foreground=krait_util.STANDARD_TEXT_COLOR)
        temp_lbl.place(x=5,y=740)
        self.message_label = temp_lbl

        term_lbl1 = Label(self.window, text="TERM ID:", font=(krait_util.STANDARD_FONT, krait_util.STANDARD_FONT_SIZE),name="terminal_id_lbl",background=krait_util.STANDARD_BACKGROUND_COLOR,foreground=krait_util.STANDARD_TEXT_COLOR)
        term_lbl1.place(x=1,y=30)

        region_lbl1 = Label(self.window, text="REGION:", font=(krait_util.STANDARD_FONT, krait_util.STANDARD_FONT_SIZE),name="region_id_lbl",background=krait_util.STANDARD_BACKGROUND_COLOR,foreground=krait_util.STANDARD_TEXT_COLOR)
        region_lbl1.place(x=150,y=30)

        region_lbl = Label(self.window, text=krait_util.EMPTY_STRING, font=(krait_util.STANDARD_FONT, krait_util.STANDARD_FONT_SIZE),name="region_id",background=krait_util.STANDARD_BACKGROUND_COLOR,foreground=krait_util.STANDARD_INFO_TEXT_COLOR)
        region_lbl.place(x=230,y=30)
        self.region_label = region_lbl

        tran_lbl1 = Label(self.window, text="TRAN ID:", font=(krait_util.STANDARD_FONT, krait_util.STANDARD_FONT_SIZE),name="transaction_id_lbl",background=krait_util.STANDARD_BACKGROUND_COLOR,foreground=krait_util.STANDARD_TEXT_COLOR)
        tran_lbl1.place(x=370,y=30)

        term_lbl = Label(self.window, text=self.terminal_id, font=(krait_util.STANDARD_FONT, krait_util.STANDARD_FONT_SIZE),name="terminal_id",background=krait_util.STANDARD_BACKGROUND_COLOR,foreground=krait_util.STANDARD_INFO_TEXT_COLOR)
        term_lbl.place(x=95,y=30)

        tran_lbl = Label(self.window, text=krait_util.EMPTY_STRING, font=(krait_util.STANDARD_FONT, krait_util.STANDARD_FONT_SIZE),name="transaction_id",background=krait_util.STANDARD_BACKGROUND_COLOR,foreground=krait_util.STANDARD_INFO_TEXT_COLOR)
        tran_lbl.place(x=460,y=30)
        self.transaction_label = tran_lbl

        self.sysout_label = self.create_label(self.sysout, krait_util.EMPTY_STRING, "sysout_label", 5, 5)
        self.sysout.geometry(krait_util.SYSOUT_WINDOW_SIZE)
        self.sysout.title(krait_util.SYSOUT_TITLE)
        self.sysout.configure(bg=krait_util.STANDARD_BACKGROUND_COLOR)

        self.sysout.withdraw()

        self.write_to_sysout(krait_util.OS_LABEL + os.name + krait_util.NEWLINE)

        f = font.Font(size=krait_util.STANDARD_FONT_SIZE, family=krait_util.STANDARD_BACKGROUND_COLOR)
        self.character_width = f.measure('W')
        self.character_height = f.metrics("linespace")
        self.window.mainloop()

        return

    def create_label(self, widget, text: str, name: str, place_x:int, place_y: int, spacing = 0):
        label = Label(widget, text=text, name=name, background=krait_util.STANDARD_BACKGROUND_COLOR, foreground=krait_util.STANDARD_TEXT_COLOR, justify=LEFT, font=(krait_util.STANDARD_FONT, krait_util.STANDARD_FONT_SIZE))
        label.place(x=(place_x - 1) * self.character_width, y=place_y * (self.character_height + spacing))
        return label

    def create_map_entry(self, widget, text: str, name: str, place_x:int, place_y: int, length: int, has_cursor: bool):
        t = StringVar()
        found = False
        if len(self.map_entry_fields) > krait_util.ZERO:
            t = self.map_entry_fields[len(self.map_entry_fields) - 1].field
            found = True
        entry_field = Entry(widget, text=text, name=name, background=krait_util.ENTRY_BOX_BACKGROUND, foreground=krait_util.ENTRY_BOX_TEXT_COLOR, justify=LEFT, font=(krait_util.STANDARD_FONT, krait_util.STANDARD_FONT_SIZE), width=length, textvariable=t)
        entry_field.place(x=place_x * self.character_width, y=place_y * (self.character_height +krait_util. LINE_SPACING))
        entry_field.config(insertbackground=krait_util.ENTRY_CURSOR_COLOR)
        entry_field.config(insertwidth=krait_util.STANDARD_CURSOR_SIZE)
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
                    entry.entry_field.delete(krait_util.ZERO, END)
                    entry.entry_field.insert(krait_util.ZERO, value)
                    break
                break

        return
    
    def main_on_keypress(self, event):
        if self.is_in_transaction:
            if event.keycode in krait_util.ATTENTION_KEYS:
                should_return_control = self.transaction_module.process_key(event.keycode)
                self.map_key_pressed.set(True)
        else:
            #print(event)
            pass

    def on_keypress(self, event):
        if self.is_in_transaction:
            return
        
        if os.name == krait_util.WINDOWS_OS:
            if event.keycode == krait_util.ENTER_KEY:
                self.cmd_click()
            elif event.keycode == krait_util.UP_ARROW:
                self.cycle_commands(krait_util.CYCLE_UP)
            elif event.keycode == krait_util.DOWN_ARROW:
                self.cycle_commands(krait_util.CYCLE_DOWN)
            elif event.keycode == krait_util.ESCAPE:
                self.command_input.delete(krait_util.ZERO, END)
        elif os.name == krait_util.LINUX_OS:
            if event.keycode == krait_util.LINUX_ENTER_KEY:
                self.cmd_click()
            elif event.keycode == krait_util.LINUX_UP_ARROW:
                self.cycle_commands(krait_util.CYCLE_UP)
            elif event.keycode == krait_util.LINUX_DOWN_ARROW:
                self.cycle_commands(krait_util.CYCLE_DOWN)
            elif event.keycode == krait_util.LINUX_ESCAPE_KEY:
                self.command_input.delete(krait_util.ZERO, END)
        
        return

    def cycle_commands(self, modifier: int):
        if len(self.command_list) == krait_util.ZERO:
                return
        self.command_input.delete(krait_util.ZERO, END)
        self.command_input.insert(krait_util.ZERO, self.command_list[self.current_command_entry])
        self.current_command_entry = self.current_command_entry + modifier
        if self.current_command_entry < 0:
            self.current_command_entry = len(self.command_list) + modifier
        
        if self.current_command_entry >= len(self.command_list):
            self.current_command_entry = krait_util.ZERO

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
        current_dd = cobol_variable._read_file(krait_util.DD_CONFIG_FILE, False)
        dd_splits = current_dd.split(krait_util.NEWLINE)
        for dd_split in dd_splits:
            if dd_split == krait_util.EMPTY_STRING:
                continue

            s = dd_split.split(krait_util.COLON)
            os.environ[s[0]] = s[1].replace(krait_util.NEWLINE, krait_util.EMPTY_STRING).replace(krait_util.CARRIAGE_RETURN, krait_util.EMPTY_STRING)
        return

    def process_command(self, text: str):
        self.current_command_entry = len(self.command_list) - 1
        self.message_label.config(foreground=krait_util.STANDARD_TEXT_COLOR)
        self.command_input.delete(krait_util.ZERO, END)
        self.message_label.config(text=krait_util.EMPTY_STRING)
        if text.lower().startswith(krait_util.START_COMMAND):
            self.start_module(text)
        elif text.lower().startswith(krait_util.SHOW_SYSOUT):
            self.show_sysout_window()
        elif text.lower().startswith(krait_util.HIDE_SYSOUT):
            self.hide_sysout_window()
        elif text.lower().startswith(krait_util.PIPE_FLAG):
            self.write_to_sysout(text[len(krait_util.PIPE_FLAG):] + krait_util.NEWLINE)
        elif text.lower().startswith(krait_util.SET_TRANSACTION):
            self.set_transaction(text)
        elif text.lower().startswith(krait_util.LIST_TRANSACTIONS):
            self.list_transactions()
        elif text.lower().startswith(krait_util.SET_DD):
            self.set_dd(text)
        elif text.lower().startswith(krait_util.CREATE_REGION):
            self.create_region(text)
        elif text.lower().startswith(krait_util.SWITCH_REGION):
            self.switch_region(text)
        elif text.lower().startswith(krait_util.HELP):
            self.show_help()
        else:
            trans = self.check_for_transaction(text)
            if trans != krait_util.EMPTY_STRING:
                self.set_current_transaction(trans)
                self.start_module(krait_util.START_COMMAND + krait_util.SPACE + trans)
            else:
                self.show_error_message(text)
                return

        self.command_list.append(text)

        return

    def set_current_transaction(self, trans_id: str):
        self.transaction_id = trans_id.upper()
        if self.transaction_label != None:
            self.transaction_label.config(text=self.transaction_id)

    def show_error_message(self, text: str):
        self.message_label.config(foreground=krait_util.ERROR_TEXT_COLOR)
        self.message_label.config(text=krait_util.INVALID_COMMAND_MSG + krait_util.SPACE + text)
        return

    def list_transactions(self):
        current_transactions = cobol_variable._read_file(krait_util.TRANSACTION_CONFIG_FILE, False)
        self.write_to_sysout(current_transactions + krait_util.NEWLINE)
        return

    def set_transaction(self, text: str):
        tokens = text.split(krait_util.SPACE)
        current_transactions = cobol_variable._read_file(krait_util.TRANSACTION_CONFIG_FILE)
        current_transactions = current_transactions + krait_util.NEWLINE + tokens[2] + krait_util.COLON + tokens[3]
        cobol_variable._write_file(krait_util.TRANSACTION_CONFIG_FILE, current_transactions)
        return

    def show_help(self):
        self.show_sysout_window()
        
        string_io = StringIO()
        sys.stdout = string_io

        for c in krait_util.COMMAND_LIST:
            print(c[0] + krait_util.COLON + krait_util.SPACE + c[1])

        self.handle_sysout_messages(string_io)

        return

    def set_dd(self, text: str):
        if not self.check_region():
            return

        tokens = text.split(krait_util.SPACE)
        current_dd = cobol_variable._read_file(krait_util.DD_CONFIG_FILE)
        value = krait_util.EMPTY_STRING
        for x in range(3, len(tokens)):
            value = value + tokens[x] + krait_util.SPACE
        temp = krait_util.EMPTY_STRING

        dds = current_dd.split(krait_util.NEWLINE)

        found = False
        for dd in dds:
            dd_info = dd.split(krait_util.COLON)
            if dd_info[0] == tokens[2]:
                found = True
                temp = temp + krait_util.NEWLINE + tokens[2] + krait_util.COLON + value
            else:
                temp = temp + krait_util.NEWLINE + dd

        if found == False:
            temp = temp + krait_util.NEWLINE + tokens[2] + krait_util.COLON + value

        cobol_variable._write_file(krait_util.DD_CONFIG_FILE, temp)

        self.set_dd_values()
        
        return
    
    def create_region(self, text: str):
        tokens = text.split(krait_util.SPACE)
        value = cobol_variable._read_file(tokens[2] + krait_util.REGION_FILE_EXT)
        if value == krait_util.EMPTY_STRING:
            cobol_variable._write_file(tokens[2] + krait_util.REGION_FILE_EXT, krait_util.REGION_FILE_EXT)
        
        return
    
    def switch_region(self, text: str):
        tokens = text.split(krait_util.SPACE)

        if cobol_variable._file_exists(tokens[2] + krait_util.REGION_FILE_EXT):
            self.region_label.config(text=tokens[2])
        else:
            self.show_error_message("Region '" + tokens[2] + "' does not exist")

        return

    def check_for_transaction(self, trans: str):
        trans = trans.lower().strip()
        current_transactions = cobol_variable._read_file(krait_util.TRANSACTION_CONFIG_FILE, False).split(krait_util.NEWLINE)
        for ct in current_transactions:
            if ct == krait_util.EMPTY_STRING:
                continue
            s = ct.split(krait_util.COLON)
            if len(s) < 2 or s[0] == krait_util.EMPTY_STRING:
                return krait_util.EMPTY_STRING
            if s[0].lower().strip() == trans:
                self.last_known_trans_id = trans.upper()
                return s[1]

        return krait_util.EMPTY_STRING

    def start_module(self, text: str):
        module_name = text
        try:
            # create a StringIO object
            string_io = StringIO()            
            tokens = text.split(krait_util.SPACE)
            module_name = tokens[1]
            cobol_variable.Build_Comm_Area(module_name, krait_util.EMPTY_STRING, [], krait_util.EMPTY_STRING)             
            module = importlib.import_module(module_name)
            module_class = getattr(module, module_name + 'Class')
            module_instance = module_class()
            module_instance.calling_module = self

            self.transaction_module = module_instance

            self.EIBMemory = cobol_variable.Build_Comm_Area(module_name, krait_util.EMPTY_STRING, self.variables_list, self.EIBMemory, self.terminal_id, self.last_known_trans_id)

            # redirect stdout to the StringIO object
            sys.stdout = string_io

            # call the module
            self.is_in_transaction = True
            module_instance.main(self)  
     
        except Exception as e:
            self.show_error_message("unable to start, module not found: " + module_name)
        except SystemExit as e:
            x = 0
        finally:
            self.handle_sysout_messages(string_io)
            return

    def handle_sysout_messages(self, string_io: StringIO):
        # get the contents of the StringIO object
        output = string_io.getvalue()

        # reset stdout to the original stream
        sys.stdout = sys.__stdout__

        self.write_to_sysout(output)

        return

    def receive_control(self, final_control = False):
        self.transaction_label.config(text=krait_util.EMPTY_STRING)
        self.is_in_transaction = not final_control
        if self.is_in_transaction and not final_control:
            # Wait for a key to be pressed
            self.window.wait_variable(self.map_key_pressed)
        elif final_control:
            self.is_in_transaction = False
        return

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

        return

    def build_map(self, map_name: str, data: str, map_only: bool, data_only: bool):
        map_name = map_name.strip()
        self.clear_frame(self.main_frame)
        map = cobol_variable._read_file(map_name + ".txt", False)
        if map == krait_util.EMPTY_STRING:
            map = cobol_variable._read_file(map_name + ".map", False)
            if map == krait_util.EMPTY_STRING:
                map = cobol_variable._read_file("maps/" + map_name + ".map", False)
                if map == krait_util.EMPTY_STRING:
                    map = cobol_variable._read_file("maps/" + map_name + ".txt", False)
                    if map == krait_util.EMPTY_STRING:
                        self.show_error_message("MAP " + map_name + " NOT FOUND")
                        return

        lines = map.split(krait_util.NEWLINE)

        field_info = krait_util.EMPTY_STRING

        for x in range(0, len(lines)):
            line = lines[x].strip().replace(krait_util.NEWLINE, krait_util.SPACE).replace(krait_util.CARRIAGE_RETURN, krait_util.SPACE)
            if line.startswith(krait_util.COBOL_COMMENT):
                continue
            
            field_info = field_info + line +krait_util. SPACE
            if line.endswith(krait_util.MAP_CONTINUATION_CHARACTER) == False:
                self.build_field(field_info, data, map_only, data_only)
                field_info = krait_util.EMPTY_STRING

        self.build_field(field_info, data, map_only, data_only)

        return

    def build_field(self, field_info: str, data: str, map_only: bool, data_only: bool):
        if krait_util.MAP_FIELD_IDENTIFIER not in field_info:
            return krait_util.ZERO

        field_type = 'none'
        field_length = 0
        field_x = 1
        field_y = 1
        field_text = krait_util.EMPTY_STRING
        tokens = self.parse_tokens(field_info)
        if tokens[0] == krait_util.MAP_FIELD_IDENTIFIER:
            tokens.insert(0, ''.join(random.choices(string.ascii_uppercase + string.digits, k=8)))
        skip_lines = 0
        var_name = tokens[0].lower()
        has_focus = False
        in_literal = False
        for token in tokens:
            skip_lines = skip_lines + 1
            if krait_util.ATTRB_KEYWORD in token:
                s = token.split(krait_util.OPEN_PARENS)
                attributes = s[1].replace(krait_util.CLOSE_PARENS, krait_util.EMPTY_STRING).split(krait_util.COMMA)
                if 'PROT' in attributes or 'ASKIP' in attributes:
                    field_type = "lbl"
                elif "UNPROT" in attributes:
                    field_type = "entry"

                if "IC" in attributes:
                    has_focus = True
            elif 'POS' in token:
                s = token.split(krait_util.OPEN_PARENS)
                pos = s[1].replace(krait_util.CLOSE_PARENS, krait_util.EMPTY_STRING).split(krait_util.COMMA)
                field_y = int(pos[0].replace(krait_util.COMMA, krait_util.EMPTY_STRING))
                field_x = int(pos[1].replace(krait_util.COMMA, krait_util.EMPTY_STRING))
                if field_y == 2:
                    x1 = 0
            elif 'LENGTH' in token:
                s = token.split(krait_util.EQUALS)
                field_length = int(s[1].replace(krait_util.COMMA, krait_util.EMPTY_STRING))
            elif 'INITIAL' in token or in_literal:
                s = token.split(krait_util.EQUALS)
                if len(s) > 1:
                    temp_field_text = s[1]
                else:
                    temp_field_text = s[0]
                if temp_field_text.startswith(krait_util.SINGLE_QUOTE):
                    temp_field_text = temp_field_text[1:]
                    in_literal = True

                if temp_field_text.endswith(krait_util.SINGLE_QUOTE):
                    if field_text == temp_field_text[:len(field_text) - 1]:
                        field_text = field_text[:len(field_text) - 1]
                    else:
                        field_text = field_text + krait_util.SPACE + temp_field_text[:len(temp_field_text) - 1]
                    in_literal = False
                else:
                    field_text = field_text + krait_util.SPACE + temp_field_text
            elif 'DFHMSD' in token or 'DFHMDI' in token:
                field_type = "none"

        if field_type == "lbl":
            self.create_label(self.main_frame, field_text, var_name, field_x, field_y, krait_util.LINE_SPACING)
        elif field_type == "entry":
            t = krait_util.KRAITEntry(name=var_name,length=field_length)
            t.field.trace('w', self.validate)
            self.map_entry_fields.append(t)
            self.create_map_entry(self.main_frame, field_text, var_name, field_x, field_y, field_length, has_focus)

        return skip_lines

    def parse_tokens(self, field_info: str):
        temp_tokens = field_info.split(krait_util.SPACE)
        result = []
        for token in temp_tokens:
            if token.strip() != krait_util.EMPTY_STRING:
                result.append(token)

        return result

    def create_terminal_id(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    
    def check_region(self):
        result = True
        if self.region_label == None:
            self.show_error_message("You must switch to a CICS Region")
            result = False
        else:
            value = self.region_label.cget("text")
            if value.strip() == krait_util.EMPTY_STRING:
                self.show_error_message("You must switch to a CICS Region")
                result = False

        return result
    
    def writeq(self, name: str, item: str):
        index = -1
        for q in self.queues:
            index = index + 1
            if q.name == name:
                break

        if index < 0:
            self.queues.append(krait_util.KRAITQueue(name))
            index = len(self.queues) - 1

        self.queues[index].append(item)

        return [index, len(self.queues[index]) - 1]
    
    def readq(self, name: str):
        index = -1
        for q in self.queues:
            index = index + 1
            if q.name == name:
                break

        if index >= 0:
            queue = self.queues[index]
            if len(queue) > 0:
                return queue.pop(0)
            
        return krait_util.EMPTY_STRING

if __name__ == '__main__':
    Krait_obj = KRAIT()

    Krait_obj.Launch()