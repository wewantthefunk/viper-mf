from tkinter import *
import importlib

EMPTY_STRING = ""
ENTER_KEY = "\r"
ERROR_TEXT_COLOR = "red"
INVALID_COMMAND_MSG = "INVALID COMMAND:"
SPACE = " "
STANDARD_BACKGROUND_COLOR = "black"
STANDARD_CURSOR_SIZE = 10
STANDARD_FONT = "Courier"
STANDARD_FONT_SIZE = 12
STANDARD_TEXT_COLOR = "white"
START_COMMAND = "start"
WINDOW_TITLE = "Kix CICS Emulator"
WINDOW_SIZE = '1280x768'

class Kix:     
    def __init__(self):
        self.window = Tk()

        self.window.title(WINDOW_TITLE)
        self.window.geometry(WINDOW_SIZE)
        self.window.configure(bg=STANDARD_BACKGROUND_COLOR)
        self.command_input = None
        self.message_label = None

    def Launch(self):
        lbl = Label(self.window, text="> ", font=(STANDARD_FONT, 12),background=STANDARD_BACKGROUND_COLOR,foreground=STANDARD_TEXT_COLOR)
        lbl.place(x=5,y=4,in_=self.window)

        txt = Entry(self.window,width=110,font=(STANDARD_FONT, 12),background=STANDARD_BACKGROUND_COLOR,foreground=STANDARD_TEXT_COLOR)
        txt.place(x=20,y=4,in_=self.window)
        txt.bind("<Key>", self.on_keypress)
        txt.config(insertbackground=STANDARD_TEXT_COLOR)
        txt.config(insertwidth=STANDARD_CURSOR_SIZE)
        txt.focus_set()
        self.command_input = txt

        cmd_btn = Button(self.window,width=7,font=(STANDARD_FONT, 12), text="Submit",command=self.cmd_click)
        cmd_btn.place(x=1150,y=1,in_=self.window)

        f1 = Frame(self.window,background=STANDARD_BACKGROUND_COLOR)
        f1.pack(padx=20,pady=30,fill="both", expand=True)

        temp_lbl = Label(self.window, text="-", font=(STANDARD_FONT, 12),name="message_label",background=STANDARD_BACKGROUND_COLOR,foreground=STANDARD_TEXT_COLOR)
        temp_lbl.place(x=5,y=740)
        self.message_label = temp_lbl

        self.window.mainloop()

    def on_keypress(self, event):
        if event.char == ENTER_KEY:
            self.cmd_click()

    def cmd_click(self):
        text = self.command_input.get().strip()
        self.process_command(text)

    def process_command(self, text):
        self.message_label.config(foreground=STANDARD_TEXT_COLOR)
        self.command_input.delete(0, END)
        self.message_label.config(text=EMPTY_STRING)
        if text.lower().startswith(START_COMMAND):
            self.start_module(text)
        else:
            self.message_label.config(foreground=ERROR_TEXT_COLOR)
            self.message_label.config(text=INVALID_COMMAND_MSG + SPACE + text)

    def start_module(self, text):
        tokens = text.split(SPACE)
        module_name = tokens[1]
        module = importlib.import_module(module_name)
        module_class = getattr(module, module_name + 'Class')
        module_instance = module_class()
        module_instance.main()

if __name__ == '__main__':
    Kix_obj = Kix()

    Kix_obj.Launch()