import numpy as np
import sounddevice as sd

class AudioSource():
    def __init__(self):
        self.sd = sd
        self.file = None

    def init(self, file):
        self.file = file

    def process(self):
        fs = self.file.sampleRate
        data = self.file.frequencyDomain
        self.sd.play(data, fs)

    def stop(self):
        self.sd.stop()

    def write(self):
        print('write to file')