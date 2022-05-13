from os import getcwd, listdir
from os.path import isfile, join
from .audio_source import AudioSource
from .utils import Utils

import soundfile as sf
import numpy as np
import math

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

    def nextBestPowerOf2(self, n):
        # Funtion to help find the best length of our padded array
        # FFT performs best when the array size if a power of 2
        # ref - https://www.mathworks.com/help/matlab/ref/fft.html
        return 1 if n == 0 else 2**math.ceil(math.log2(n))

    def padWithZeros(self, x, new_length):
        output = np.zeros((new_length,))
        output[:x.shape[0]] = x
        return output

    def convolution(self, x, h):
        # This article helped influence alot of this code - https://thewolfsound.com/fast-convolution-fft-based-overlap-add-overlap-save-partitioned/
        # With a blockSize of 512, after applying convolution, we will have a length of X+H-1

        # N = Input, H = RIR

        # We get the length of both input and RIR blocks
        # We only need to use one channel here
        X = x[:,0].shape[0]
        H = h[:,0].shape[0]
        Y = X + H - 1 # output length

        # Get closet power of 2 to new output length
        # If X+H-1 = 2030, the next power of 2 would be 2048
        K = self.nextBestPowerOf2(Y)

        # We want to run an fft on both our input data and room impulse response
        # Each channel is fft'd independently since they will have different data
        X_1 = np.fft.fft(self.padWithZeros(x[:, 0], K))
        X_2 = np.fft.fft(self.padWithZeros(x[:, 1], K))
        H_1 = np.fft.fft(self.padWithZeros(h[:, 0], K))
        H_2 = np.fft.fft(self.padWithZeros(h[:, 1], K))

        # We then multiply our input with our rir data
        # This is the equivalent to convolution in the time domain
        Y_1 = np.multiply(X_1, H_1)
        Y_2 = np.multiply(X_2, H_2)

        # Once we have our convolved data in the frequency domain
        # We used an IFFT to get back to the time domain and be able to output our convolved signal 
        y1 = np.real(np.fft.ifft(Y_1))
        y2 = np.real(np.fft.ifft(Y_2))

        # We are returning several different arrays of data here
        # First our outputs left and right channels
        # Notice that we are only taking our original blockSize of 512, since convolution will double our array size
        # We are passing the remaining 512 samples separately to store for the next block
        # This is known as the overlap-add method and is useful for processing large audio files.
        # We can split up our data into smaller blocks and process them in real time
        # Rather than needing to load data buffer to memory, which is impractical for large files
        return y1[:X], y2[:X], y1[X:], y2[X:] 

    def getNextAudioBlock(self, outdata, frames, time, status):
        # Calculate current position and total data size delta
        delta = self.file.numOfSamples - self.currentFramePosition

        # Calculate the next block index
        nextBlockIndex = self.currentFramePosition + self.blockSize

        # Get RIR data
        h = np.array(self.ir[self.irTemplate])
        Y = None

        # Get next block
        block = self.file.data[self.currentFramePosition:nextBlockIndex]

        # convolve blocks
        newBlockLeftChannel, newBlockRightChannel, overlapLeftChannel, overlapRightChannel = self.convolution(block, h[:self.blockSize])

        # Overlap-add the previous 512 samples from the last convolution
        # Previous convolved block is sumed with current block, unless it is first pass of convolution.
        # Then there is nothing to sum and can be passed to the stream as is.
        if len(self.overlap_data_left) > 0:
            Y_1 = np.add(self.overlap_data_left[:len(newBlockLeftChannel)], newBlockLeftChannel)
            Y_2 = np.add(self.overlap_data_right[:len(newBlockRightChannel)], newBlockRightChannel)
        else:
            Y_1 = newBlockLeftChannel
            Y_2 = newBlockRightChannel

        # we then store the next 512 samples that will be added to the next block
        self.overlap_data_left = overlapLeftChannel
        self.overlap_data_right = overlapRightChannel

        # Add our independent channels together in the shape of (1024, 2)
        # which is expected by our OutputStream
        output = Utils.combineChannels(Y_1, Y_2)

        # Before passing the block to the output stream, we apply the selected gain to our data
        # This is probably not the best place for this 
        outdata[:len(block)] = np.multiply(output, self.volume)

        # Once block has been passed to stream, we check whether the defined block size is still able to be filled fully
        # If not, start frame position to 0.
        if delta < self.blockSize:
            self.currentFramePosition = 0
        else:
            self.currentFramePosition += self.blockSize
