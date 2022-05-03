# Class to handle all file related operations
# Is useful to include some getters to easily receive file information through app.
import librosa
import soundfile as sf
import datetime
from .utils import Utils
class File():
    file = ''
    path = ''
    filename = ''
    filetype = ''
    sampleRate = 0
    numOfSamples = 0
    duration = 0
    data = []

    def __init__(self, file):
        self.file = file # Set file

        # Carry out file related operations, set above attributes for easy access
        self.filename()
        self.filetype()
        self.getData()
        self.duration()

    def reset(self):
        self.file = ''
        self.path = ''
        self.filename = ''
        self.filetype = ''
        self.sampleRate = 0
        self.numOfSamples = 0
        self.duration = 0
        self.data = []

    def get(self):
        return self.file

    def filename(self):
        filename = None
        filename = self.file.rsplit('/', 1)[-1].split('.', 1)[0]
        if len(filename) > 26:
            self.filename = filename[0:22]+'...'
        else:
            self.filename = filename

    def filetype(self):
        self.filetype = self.file.rsplit('.', 1)[-1]
        return '.'+self.filetype

    def getData(self):
        y, sr = sf.read(self.file) # sf returns a numpy array [frames x channels], along with files SR

        # Normalise data
        # self.data = [Utils.normalise(i) for i in y.shape()]
        self.data = y
        self.sampleRate = sr
        self.numOfSamples = len(y)

    def duration(self):
        duration = self.numOfSamples / self.sampleRate
        self.duration = str(datetime.timedelta(seconds=int(str(duration).split('.', 1)[0])))
