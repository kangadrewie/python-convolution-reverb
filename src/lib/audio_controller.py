from .file import File
from .audio_source import AudioSource
from .convolution import Convolution

class AudioController():
    def __init__(self):
        self.file = None
        self.isPlayable = False
        self.audioSource = None
        self.convolution = None
        self.audioThreads = []

    def onPressPlay(self):
        # Simple flow to keep track of audioSource threads.
        # If thread has not started/does not exist, then start and track in self.audioThreads[]
        # Threads are destroyed when new file is loaded
        dryThread = self.audioSource.getThread()
        wetThread = self.convolution.getThread()
        if dryThread and wetThread in self.audioThreads:
            self.audioSource.run()
            self.convolution.run()
        else:
            self.audioThreads.append(dryThread)
            self.audioThreads.append(wetThread)
            self.audioSource.start()
            self.convolution.start()

    def onPressStop(self):
        self.audioSource.stop()
        self.convolution.stop()

    def onPressExport(self):
        print('Export')
    
    def onVolumeChange(self, event):
        self.convolution.volume = float(event) / 100 # Scale Volume to be 0-1
        self.audioSource.volume = 1 - (float(event) / 100) # adjust original source volume to keep overall gain the same, but change the mix

    def onTemplateChange(self, event):
        self.convolution.irTemplate = event

    def load(self, file):
        # Load audio File into memory
        try:
            # Destroy any old pointers to file/audioSource instances before load/reloading new file
            self.file = None
            self.audioSource = None 
            self.audioThreads = []

            # Create new instances of both
            self.file = File(file)
            self.convolution = Convolution()
            self.audioSource = AudioSource()
            self.convolution.init(self.file)  # init audioSource
            self.audioSource.init(self.file) # init audioSource
            self.isPlayable = True # var to tell gui that file is able to be played
            return True
        except Exception as e:
            print(e)
            return False
