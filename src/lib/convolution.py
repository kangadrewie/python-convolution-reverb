from os import getcwd, listdir
from os.path import isfile, join
from .audio_source import AudioSource
from .utils import Utils

import soundfile as sf
import numpy as np

TEMPLATE_IR_PATH = '{}/src/static/impulse_response_templates/'.format(getcwd())

# This class can inherit AudioSource as it will do the same job only modifying the data stream
utils = Utils()

class Convolution(AudioSource):
    B = []
    def __init__(self):
        # Init parent audiosource
        super().__init__()
        self.ir = {}
        self.sf = sf
        self.volume = 0.5
        self.overlap_data_left = []
        self.overlap_data_right = []
        self.irTemplate = 'Highly Damped Large Room'

        # Read and load IR responses into memory
        for file in listdir(TEMPLATE_IR_PATH):
            if isfile(join(TEMPLATE_IR_PATH, file)):
                ir_data, ir_sr = self.sf.read(join(TEMPLATE_IR_PATH, file), always_2d=True)
                self.ir[file[:-4]] = ir_data

    def next_power_of_2(self, n):
        return 1 << (int(np.log2(n - 1)) + 1)

    def pad_zeros_to(self, x, new_length):
        """Append new_length - x.shape[0] zeros to x's end via copy."""
        output = np.zeros((new_length,))
        output[:x.shape[0]] = x
        return output

    def convolution(self, x, h, K=None):
        Nx = x[:,0].shape[0]
        Nh = h[:,0].shape[0]
        Ny = Nx + Nh - 1 # output length
        if K is None:
            K = self.next_power_of_2(Ny)
        X_1 = np.fft.fft(self.pad_zeros_to(x[:, 0], K))
        X_2 = np.fft.fft(self.pad_zeros_to(x[:, 1], K))
        H_1 = np.fft.fft(self.pad_zeros_to(h[:, 0], K))
        H_2 = np.fft.fft(self.pad_zeros_to(h[:, 1], K))
        Y_1 = np.multiply(X_1, H_1)
        Y_2 = np.multiply(X_2, H_2)
        y1 = np.real(np.fft.ifft(Y_1))
        y2 = np.real(np.fft.ifft(Y_2))
        return y1[:Nx], y2[:Nx], y1[Nx:], y2[Nx:] 

    def getNextAudioBlock(self, outdata, frames, time, status):
        # Calculate current position and total data size delta
        delta = self.file.numOfSamples - self.currentFramePosition

        # Calculate the next block index
        nextBlockIndex = self.currentFramePosition + self.blockSize

        # Get RIR
        h = np.array(self.ir[self.irTemplate])
        Y = None

        # Get next block
        block = self.file.data[self.currentFramePosition:nextBlockIndex]

        # convolve block
        newBlockLeftChannel, newBlockRightChannel, overlapLeftChannel, overlapRightChannel = self.convolution(block, h[:self.blockSize])

        if len(self.overlap_data_left) > 0:
            Y_1 = np.add(self.overlap_data_left[:len(newBlockLeftChannel)], newBlockLeftChannel)
            Y_2 = np.add(self.overlap_data_right[:len(newBlockRightChannel)], newBlockRightChannel)
        else:
            Y_1 = newBlockLeftChannel
            Y_2 = newBlockRightChannel


        self.overlap_data_left = overlapLeftChannel
        self.overlap_data_right = overlapRightChannel

        output = np.empty([len(block), 2])
        for n in range(len(block)):
            output[n] = [Y_1[n], Y_2[n]]

        outdata[:len(block)] = np.multiply(np.add(output, np.multiply(block, -1)), self.volume)

        # Check whether the defined block size is still able to be filled fully
        if delta < self.blockSize:
            self.currentFramePosition = 0
        else:
            self.currentFramePosition += self.blockSize
