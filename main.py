# Lib Imports
from tkinter import Tk, Label
from turtle import bgcolor

# Component Imports
from src.components.template_list.template_list import TemplateList
from src.components.media_controls.media_controls import MediaControls
from src.components.functional_controls.functional_controls import FunctionalControls

# Theme used - credit - https://github.com/rdbende/Sun-Valley-ttk-theme

class Application():
    def __init__(self, title, width, height, padding):
        self.root = Tk()
        self.title = self.root.title(title)
        self.root.geometry('{}x{}'.format(width, height))
        self.root.resizable(0, 0)
        self.setTheme()

        # Layout
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=2)

        self.templateList = TemplateList(self)
        self.mediaControls = MediaControls(self)
        self.functionalControls = FunctionalControls(self)

    def setTheme(self):
        self.root.tk.call("source", "sun-valley.tcl")
        self.root.tk.call("set_theme", "dark")

    def run(self):
        return self.root.mainloop()

    def init(self):
        # Default template list to be first item. Must be changed before app.run()
        self.templateList.list.selection_set(first=0)


if __name__ == '__main__':
    app = Application('Convolution Reverb', 550, 300, 5)
    app.init()
    app.run()