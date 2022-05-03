from os import getcwd, listdir
from os.path import isfile, join
from .audio_source import AudioSource
from .utils import Utils

import soundfile as sf
import numpy as np
from scipy import signal

TEMPLATE_IR_PATH = '{}/static/impulse_response_templates/'.format(getcwd())

# This class can inherit AudioSource as it will do the same job only modifying the data stream
utils = Utils()


class Convolution(AudioSource):
    def __init__(self):
        # Init parent audiosource
        super().__init__()
        self.ir = {}
        self.sf = sf
        self.volume = 0.5
        # Read and load IR responses into memory
        for file in listdir(TEMPLATE_IR_PATH):
            if isfile(join(TEMPLATE_IR_PATH, file)):
                ir_data, ir_sr = self.sf.read(join(TEMPLATE_IR_PATH, file))
                # Soundfile always returns two channels despite IR files being mono.
                # The null channel is dropped and the mono data is normalised to -1 to 1
                # self.ir[file] = { 'sr': ir_sr, 'data': Utils.normalise(ir_data[0]) }
                # self.ir[file] = {'sr': ir_sr, 'data': ir_data}
                self.ir[file] = Utils.downsample(44100, 96000, ir_data)

        # print(self.ir)

        return None

    def getNextAudioBlock(self, outdata, frames, time, status):
        # Calculate current position and total data size delta
        delta = self.file.numOfSamples - self.currentFramePosition

        # Calculate the next block index
        nextBlockIndex = self.currentFramePosition + self.blockSize

        IR = np.array(self.ir['ir_centre_hall.wav'])

        # Check whether the defined block size is still able to be filled fully
        if self.blockSize < delta:
            # The next full block of 2048 samples can be passed to stream for output

            block = self.file.data[self.currentFramePosition:nextBlockIndex]
            # y(n) = (h*x)(n) = SIGMA n,m=0 = h(m)x(n-m)
            # for each sample in audio data
            # mulitple by h(n)
            y = np.zeros((self.blockSize, 2), dtype=np.float64)
            x = block
            h = IR
            h.reshape(220468, 2)
            x.reshape(self.blockSize, 2)
            for n in range(0, len(block)):
                y[n][0] = h[n][0] * x[n, :1][0]
                y[n][1] = h[n][1] * x[n, :1][0]
                # y[n][0] = x[n, :1][0]
                # y[n][1] = x[n, :1][0]


            print('Block', block.shape)
            print('Y', y.shape)


            # Apply gain to convolution
            # block = np.array(y) * self.volume

            # Process new block with gain
            outdata[:self.blockSize] = y

            # keep track of position in the stream
            self.currentFramePosition += self.blockSize
        else:
            # Block Size is too large for remaining data. Pass what is left to stream and restart from zero
            outdata = self.file.data[self.currentFramePosition:]
            self.currentFramePosition = 0
