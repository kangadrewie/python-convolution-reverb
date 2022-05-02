from .file import File
from .audio_source import AudioSource
from .convolution import Convolution

class AudioController():
    def __init__(self):
        self.file = None
        self.audioSource = AudioSource()
        self.convolution = Convolution()

    def onPressPlay(self):
        self.audioSource.init(self.file)
        self.audioSource.process()

    def onPressStop(self):
        self.audioSource.stop()

    def onPressExport(self):
        print('Export')
    
    def onVolumeChange(self, event):
        return event

    def onDelayChange(self, event):
        return event

    def onDecayChange(self, event):
        return event

    def load(self, file):
        try:
            self.file = None # destroy pointer to old File instance if reloading new file
            self.file = File(file)
            return True
        except:
            return False
