from .file import File
from .audio_source import AudioSource
from .convolution import Convolution

class AudioController():
    def __init__(self):
        self.file = None
        self.audioSource = None
        self.convolution = Convolution()
        self.audioThreads = []

    def onPressPlay(self):
        # Simple flow to keep track of audioSource threads.
        # If thread has not started/does not exist, then start and track in self.audioThreads
        # Threads are destroyed when new file is added
        thread = self.audioSource.init(self.file)
        if thread in self.audioThreads:
            self.audioSource.run()
        else:
            self.audioThreads.append(thread)
            self.audioSource.start()

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
            # Destroy old pointers to file/audioSource instances before load/reloading new file
            self.file = None
            self.audioSource = None 
            self.audioThreads = []

            # Create new instances of both
            self.file = File(file)
            self.audioSource = AudioSource()
            return True
        except:
            return False
