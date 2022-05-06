from os import getcwd
from turtle import bgcolor
from ..base.base import BaseComponent
from tkinter import Frame, ttk, filedialog, Label

class MediaControls(BaseComponent):
    currentTimestamp = '00:00:00'
    def __init__(self, app, audioController):
        super().__init__(app)
        self.frame = Frame(self.root)
        self.frame.columnconfigure(0, weight=1, uniform='column')
        self.frame.columnconfigure(1, weight=1, uniform='column')
        self.frame.columnconfigure(2, weight=1, uniform='column')
        self.frame.columnconfigure(3, weight=1, uniform='column')

        self.audioController = audioController

        self.openFile = ttk.Button(self.frame, text='Open', command=self.fileBrowser)
        self.playButton = ttk.Button(self.frame, text='Play', command=self.onPressPlay, state='disabled')
        self.stopButton = ttk.Button(self.frame, text='Stop', command=self.onPressStop, state='disabled')
        self.exportButton = ttk.Button(self.frame, text='Export', command=self.audioController.onPressExport, state='disabled')
        self.fileInformationFrame = None

        self.openFile.grid(row=0, column=0, sticky='ew', padx=2)
        self.playButton.grid(row=0, column=1, sticky='ew', padx=2)
        self.stopButton.grid(row=0, column=2, sticky='ew', padx=2)
        self.exportButton.grid(row=0, column=3, sticky='ew', padx=2)

        self.fileInformation(None)

        self.frame.grid(column=0, row=3, sticky='ew')

    def validFileOpened(self, file):
        # Enable media controls
        self.playButton.config(state='normal')
        self.stopButton.config(state='normal')
        self.exportButton.config(state='normal')

        # Enable timestamp label
        self.fileInformation(file)

    def fileBrowser(self):
        fileToOpen = filedialog.askopenfilename(initialdir='{}'.format(getcwd()), title='Select a .wav file', filetypes=(('Audio Files', '.wav'), ('All Files', '*.*')))
        if fileToOpen:
            isLoaded = self.audioController.load(fileToOpen)
            if isLoaded:
                self.validFileOpened(fileToOpen)

    def fileInformation(self, file):
        fileInfoFrame = Frame(self.frame)
        fileInfoFrame.columnconfigure(0, weight=1)
        fileInfoFrame.columnconfigure(4, weight=1)

        _filename = Label(fileInfoFrame, text='File Name:')
        _samplerate = Label(fileInfoFrame, text='Sample Rate:')
        _bitdepth = Label(fileInfoFrame, text='Duration:')
        _filetype = Label(fileInfoFrame, text='File Type:')
        _timestamp = Label(fileInfoFrame, text='Timestamp:')

        _filename.grid(column=0, row=0, sticky='w')
        _samplerate.grid(column=0, row=1, sticky='w')
        _bitdepth.grid(column=0, row=2, sticky='w')
        _filetype.grid(column=0, row=3, sticky='w')
        _timestamp.grid(column=0, row=4, sticky='w')

        if file:
            filename = Label(fileInfoFrame, text=self.audioController.file.filename)
            samplerate = Label(fileInfoFrame, text='{} kHz'.format(self.audioController.file.sampleRate))
            bitdepth = Label(fileInfoFrame, text=self.audioController.file.duration)
            filetype = Label(fileInfoFrame, text=self.audioController.file.filetype)
            timestamp = Label(fileInfoFrame, text=self.currentTimestamp)

            filename.grid(column=3, row=0, sticky='e', columnspan=2)
            samplerate.grid(column=3, row=1, sticky='e', columnspan=2)
            bitdepth.grid(column=3, row=2, sticky='e', columnspan=2)
            filetype.grid(column=3, row=3, sticky='e', columnspan=2)
            timestamp.grid(column=3, row=4, sticky='e', columnspan=2)

        self.fileInformationFrame = fileInfoFrame
        self.fileInformationFrame.grid(row=4, column=0, columnspan=4, sticky='ew', pady=10)

    def updateTimestamp(self, time):
        print(time)

    def onPressPlay(self):
        play = ttk.Style()
        stop = ttk.Style()
        play.configure('MCPlay.TButton', foreground='green')
        stop.configure('MCStop.TButton', foreground='red')
        self.playButton.configure(style='MCPlay.TButton')
        self.stopButton.configure(style='MCStop.TButton')
        self.audioController.onPressPlay()

    def onPressStop(self):
        self.playButton.configure(style='TButton')
        self.stopButton.configure(style='TButton')
        self.audioController.onPressStop()
