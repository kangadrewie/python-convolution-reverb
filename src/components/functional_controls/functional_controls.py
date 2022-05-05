from concurrent.futures.process import _system_limits_checked
from ..base.base import BaseComponent
from tkinter import ttk, Label, Frame

class FunctionalControls(BaseComponent):
    # Slider variables, must be unique values for some reason.
    s0, s1, s2 = 1, 99.9, 100
    defaultVolume, defaultDelay, defaultDecay = 0.5, 0, 0
    currentVolume, currentDelay, currentDecay = None, None, None

    def __init__(self, app, audioController):
        super().__init__(app)
        self.audioController = audioController
        
        self.frame = Frame(self.root)
        self.frame.columnconfigure(1, weight=1, uniform='column')
        self.frame.rowconfigure(1, weight=0, uniform='row')

        self.volume, self.currentVolume = self.renderControlWidget('Level', 0, 1, self.s0, self.defaultVolume, self.onVolumeChange)

        self.volume.grid(column=1, row=1, padx=25, pady=5, sticky='ew')

        # global layout
        self.frame.grid(column=1, row=0, sticky='ew', rowspan=4)

    def renderControlWidget(self, label, minValue, maxValue, var, defaultValue, onChangeFunction):
        localFrame = Frame(self.frame)
        localFrame.columnconfigure(1, weight=1)
        label = Label(localFrame, text=label, font=('Helvetica, 16'))
        valueLabel = Label(localFrame, text=defaultValue)
        slider = ttk.Scale(
            localFrame,
            from_=minValue,
            to=maxValue,
            orient='horizontal',
            variable=var,
            command=onChangeFunction
        )
        slider.set(defaultValue)
        label.grid(column=1, row=0, sticky='w', pady=10)
        slider.grid(column=1, row=1, sticky='ew')
        valueLabel.grid(column=1, row=2, sticky='ne')
        return localFrame, valueLabel
    
    def onVolumeChange(self, event):
        if not self.currentVolume == None:
            self.currentVolume.configure(text=event[0:4])
            self.audioController.onVolumeChange(event)
