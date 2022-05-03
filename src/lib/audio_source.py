import numpy as np
import sounddevice as sd
from threading import Thread, currentThread


class AudioSource(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.sd = sd
        self.device = self.sd.default.device['output']
        self.file = None
        self.currentFramePosition = 0
        self.blockSize = 2048
        self.stream = None

    def init(self, file):
        self.file = file

        # Init stream
        self.stream = sd.OutputStream(
            samplerate=self.file.sampleRate,
            device=self.device,
            blocksize=self.blockSize,
            channels=self.file.data.shape[1],
            callback=self.getNextAudioBlock
        )

    def run(self):
        self.stream.start()

    def getNextAudioBlock(self, outdata, frames, time, status):
        # Calculate current position and total data size delta
        delta = self.file.numOfSamples - self.currentFramePosition

        # Calculate the next block index
        nextBlockIndex = self.currentFramePosition + self.blockSize

        # Check whether the defined block size is still able to be filled fully
        if self.blockSize < delta:
            # The next full block of 1024 samples can be passed to stream for output
            outdata[:self.blockSize] = self.file.data[self.currentFramePosition:nextBlockIndex]

            # keep track of position in the stream
            self.currentFramePosition += self.blockSize
        else:
            # Block Size is too large for remaining data. Pass what is left to stream and restart from zero
            outdata = self.file.data[self.currentFramePosition:]
            self.currentFramePosition = 0

    def stop(self):
        self.stream.stop()
        self.currentFramePosition = 0

    def write(self):
        print('write to file')

    def getThread(self):
        return currentThread()

