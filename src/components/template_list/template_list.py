from ..base.base import BaseComponent
from os import listdir, getcwd
from os.path import isfile, join
from tkinter import Listbox, Label

TEMPLATE_IR_PATH = '{}/src/static/impulse_response_templates/'.format(getcwd())

class TemplateList(BaseComponent):
    def __init__(self, app, audioController):
        super().__init__(app)

        self.audioController = audioController
        # List configuration
        self.listLabel = Label(self.root, text='Presets', font=('Helvetica', 12, 'bold'))
        self.list = Listbox(
            self.root,
            bd=0,
            font=('Helvetica', 12, 'normal'),
            height=5
        )

        # Grid
        self.listLabel.grid(column=0, row=0, sticky='nw', pady=10, padx=5)
        self.list.grid(column=0, row=1, sticky='ew', padx=10)
        self.list.bind('<<ListboxSelect>>', self.items_selected)

        # Get list of IR responses in /lib/impulse_response_templates/
        self.templates = self.getTemplates(TEMPLATE_IR_PATH)
        self.renderTemplates()

    def getTemplates(self, path):
        templates = []
        for file in listdir(path):
            if isfile(join(path, file)): 
                templates.append(file)
        return templates
    
    def renderTemplates(self):
        for idx, t in enumerate(self.templates):
            self.list.insert(idx, t[:-4])

    # handle event
    def items_selected(self, event):
        if self.audioController.isPlayable:
            selectedIndices = self.list.curselection()
            selectedLangs = ",".join([self.list.get(i) for i in selectedIndices])
            self.audioController.onTemplateChange(selectedLangs)
