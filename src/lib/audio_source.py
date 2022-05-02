import numpy as np
import sounddevice as sd
from threading import Thread, currentThread

class AudioSource(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.sd = sd
        self.file = None

    def init(self, file):
        self.file = file
        return currentThread()

    def run(self):
        fs = self.file.sampleRate
        data = self.file.frequencyDomain
        self.sd.play(data, fs)

    def stop(self):
        self.sd.stop()

    def write(self):
        print('write to file')