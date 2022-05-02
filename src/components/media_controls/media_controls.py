from distutils import ccompiler
from os import getcwd
from ..base.base import BaseComponent
from ...lib.file import File

from tkinter import Frame, ttk, filedialog, Label

class MediaControls(BaseComponent):
    currentTimestamp = '00:00:00'
    def __init__(self, app):
        super().__init__(app)
        self.frame = Frame(self.root)
        self.frame.columnconfigure(0, weight=1, uniform='column')
        self.frame.columnconfigure(1, weight=1, uniform='column')
        self.frame.columnconfigure(2, weight=1, uniform='column')
        self.frame.columnconfigure(3, weight=1, uniform='column')

        self.openFile = ttk.Button(self.frame, text='Open', command=self.fileBrowser)
        self.playButton = ttk.Button(self.frame, text='Play')
        self.stopButton = ttk.Button(self.frame, text='Stop')
        self.exportButton = ttk.Button(self.frame, text='Export')
        self.fileInformationFrame = None

        self.openFile.grid(row=0, column=0, sticky='ew', padx=2)
        self.playButton.grid(row=0, column=1, sticky='ew', padx=2)
        self.stopButton.grid(row=0, column=2, sticky='ew', padx=2)
        self.exportButton.grid(row=0, column=3, sticky='ew', padx=2)

        self.fileInformation(None)

        self.frame.grid(column=0, row=3, sticky='ew')

    def validFileOpened(self, file):
        # Enable timestamp label
        self.fileInformation(file)

    def fileBrowser(self):
        fileToOpen = filedialog.askopenfilename(initialdir='{}'.format(getcwd()), title='Select a .wav file', filetypes=(('Audio Files', '.wav'), ('All Files', '*.*')))
        file = File(fileToOpen)

        if file:
            self.validFileOpened(file)

    def fileInformation(self, file):
        fileInfoFrame = Frame(self.frame)
        fileInfoFrame.columnconfigure(0, weight=1)
        fileInfoFrame.columnconfigure(4, weight=1)

        _filename = Label(fileInfoFrame, text='File Name:')
        _samplerate = Label(fileInfoFrame, text='Sample Rate:')
        _bitdepth = Label(fileInfoFrame, text='Bit Depth:')
        _filetype = Label(fileInfoFrame, text='File Type:')
        _timestamp = Label(fileInfoFrame, text='Timestamp:')

        _filename.grid(column=0, row=0, sticky='w')
        _samplerate.grid(column=0, row=1, sticky='w')
        _bitdepth.grid(column=0, row=2, sticky='w')
        _filetype.grid(column=0, row=3, sticky='w')
        _timestamp.grid(column=0, row=4, sticky='w')

        if file:
            filename = Label(fileInfoFrame, text='105_AnalogueDrums_97_21_SP')
            samplerate = Label(fileInfoFrame, text='44.1 kHz')
            bitdepth = Label(fileInfoFrame, text='24')
            filetype = Label(fileInfoFrame, text='.wav')
            timestamp = Label(fileInfoFrame, text=self.currentTimestamp)

            filename.grid(column=3, row=0, sticky='e', columnspan=2)
            samplerate.grid(column=3, row=1, sticky='e', columnspan=2)
            bitdepth.grid(column=3, row=2, sticky='e', columnspan=2)
            filetype.grid(column=3, row=3, sticky='e', columnspan=2)
            timestamp.grid(column=3, row=4, sticky='e', columnspan=2)

        self.fileInformationFrame = fileInfoFrame
        self.fileInformationFrame.grid(row=4, column=0, columnspan=4, sticky='ew', pady=10)

