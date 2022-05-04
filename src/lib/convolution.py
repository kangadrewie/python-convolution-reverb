from inspect import currentframe
from os import getcwd, listdir
from os.path import isfile, join
from .audio_source import AudioSource
from .utils import Utils

import soundfile as sf
import numpy as np
import numpy.fft as fft
from scipy import signal

TEMPLATE_IR_PATH = '{}/static/impulse_response_templates/'.format(getcwd())

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
        self.overlap_data = np.array([])
        self.overlap_index = 0
        self.x = None
        # Read and load IR responses into memory
        for file in listdir(TEMPLATE_IR_PATH):
            if isfile(join(TEMPLATE_IR_PATH, file)):
                ir_data, ir_sr = self.sf.read(join(TEMPLATE_IR_PATH, file), always_2d=True)
                self.ir[file] = ir_data

        # print(self.ir)

        return None

    def next_power_of_2(self, n):
        return 1 << (int(np.log2(n - 1)) + 1)

    def pad_zeros_to(self, x, new_length):
        """Append new_length - x.shape[0] zeros to x's end via copy."""
        output = np.zeros((new_length,))
        output[:x.shape[0]] = x
        return output

    def fft_convolution(self, x, h, K=None):
        Nx = x[:,0].shape[0]
        Nh = h[:,0].shape[0]
        Ny = Nx + Nh # output length

        # Make K smallest optimal
        if K is None:
            K = self.next_power_of_2(Ny)

        # Calculate the fast Fourier transforms 
        # of the time-domain signals
        X_1 = np.fft.fft(self.pad_zeros_to(x[:, 0], K))
        X_2 = np.fft.fft(self.pad_zeros_to(x[:, 1], K))

        H_1 = np.fft.fft(self.pad_zeros_to(h[:, 0], K))
        H_2 = np.fft.fft(self.pad_zeros_to(h[:, 1], K))

        # Perform circular convolution in the frequency domain
        Y_1 = np.multiply(X_1, H_1)
        Y_2 = np.multiply(X_2, H_2)

        # Go back to time domain
        y_1 = np.real(np.fft.ifft(Y_1))
        y_2 = np.real(np.fft.ifft(Y_2))

        output = np.empty([Ny, 2])
        for n in range(Ny):
            output[n] = [y_1[n], y_2[n]]

        # Trim the signal to the expected length
        # return first half of convolved block
        # return second half for next block overlap
        return output[:Nx], output[Nx:]

    def getNextAudioBlock(self, outdata, frames, time, status):
        # Calculate current position and total data size delta
        delta = self.file.numOfSamples - self.currentFramePosition

        # Calculate the next block index
        nextBlockIndex = self.currentFramePosition + self.blockSize

        h = np.array(self.ir['Large Wide Echo Hall.wav'])
        block = self.file.data[self.currentFramePosition:nextBlockIndex]

        # Check whether the defined block size is still able to be filled fully
        if self.blockSize > delta:
            block = self.file.data[self.currentFramePosition:]

        # Receive output of convolution
        if self.currentFramePosition < self.blockSize:
            self.x = block
        else:
            print('OVERLLAPING FROM {} to {}'.format(self.overlap_index, self.blockSize))
            print('half of previous block', self.overlap_data[:self.blockSize//2].shape, 'half of new block', self.x[:self.blockSize//2].shape)
            self.x = np.concatenate((self.overlap_data[:self.blockSize//2], self.x[:self.blockSize//2]))

        y, next_y = self.fft_convolution(self.x, h[:self.blockSize])
        print(y.shape, '<<< Y')
        self.overlap_data = next_y
        print(next_y.shape, '<<< NEXT Y')
        self.overlap_index += self.blockSize // 2

        outdata[:self.blockSize] = y
        # keep track of position in the stream
        self.currentFramePosition += self.blockSize
