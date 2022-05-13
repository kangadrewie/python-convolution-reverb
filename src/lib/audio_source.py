import numpy as np
import sounddevice as sd
import soundfile as sf
from threading import Thread, currentThread
from .utils import Utils
class AudioSource(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.sd = sd
        self.sf = sf
        self.device = self.sd.default.device['output']
        self.file = None
        self.currentFramePosition = 0
        self.blockSize = 512
        self.stream = None
        self.volume = 0.5

    def init(self, file):
        self.file = file

        # Init stream
        # Soundfile uses a callback to request data blocks
        # This is handle via getNextAudioBlock method
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

        # Allocate next block with data
        block = self.file.data[self.currentFramePosition:nextBlockIndex]

        # The next full block of 1024 samples can be passed to stream for output
        outdata[:len(block)] = np.multiply(block, self.volume)

        # Check whether the defined block size is still able to be filled fully
        if delta < self.blockSize:
            self.currentFramePosition = 0
        else:
            # keep track of position in the stream
            self.currentFramePosition += self.blockSize

    def stop(self):
        self.stream.stop()
        self.currentFramePosition = 0

    def write(self, inputData, reverbData, path, sampleRate):
        # Combine both input and reverb
        data = np.add(inputData, reverbData)
        self.sf.write(data=Utils.normalise(data), samplerate=sampleRate, file=path)

    def getThread(self):
        return currentThread()

