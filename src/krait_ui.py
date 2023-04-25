import string
from tkinter import *

class KRAITEntry:
    def __init__(self, name: str, length: int) -> None:
        self.name = name
        self.length = length
        self.field = StringVar()
        self.entry_field = None

        return