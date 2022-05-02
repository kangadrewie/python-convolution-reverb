from ..base.base import BaseComponent
from tkinter import ttk, Label, Frame

class FunctionalControls(BaseComponent):
    def __init__(self, app):
        super().__init__(app)
        
        self.frame = Frame(self.root)
        self.frame.columnconfigure(1, weight=1, uniform='column')
        self.frame.rowconfigure(1, weight=0, uniform='row')
        self.volume = self.renderControlWidget('Volume', 0, 1, self.onVolumeChange)
        self.predelay = self.renderControlWidget('Predelay', 0, 1, self.onPredelayChange)
        self.density = self.renderControlWidget('Density', 0, 1, self.onDensityChange)

        self.volume.grid(column=1, row=1, padx=25, pady=15, sticky='ew')
        self.predelay.grid(column=1, row=2, padx=25, pady=15, sticky='ew')
        self.density.grid(column=1, row=3, padx=25, pady=15, sticky='ew')

        # global layout
        self.frame.grid(column=1, row=0, sticky='ew', rowspan=4)

    def renderControlWidget(self, label, minValue, maxValue, onChangeFunction):
        localFrame = Frame(self.frame)
        localFrame.columnconfigure(1, weight=1)
        label = Label(localFrame, text=label, font=('Helvetica, 16'))
        slider = ttk.Scale(
            localFrame,
            from_=minValue,
            to=maxValue,
            orient='horizontal',
            variable=0,
            command=onChangeFunction
        )
        label.grid(column=1, row=0, sticky='w', pady=10)
        slider.grid(column=1, row=1, sticky='ew')
        return localFrame
    
    def onVolumeChange(self, event):
        print(event)

    def onPredelayChange(self, event):
        print(event)

    def onDensityChange(self, event):
        print(event)


