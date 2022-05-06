import scipy.signal as sps
import numpy as np

class Utils():
    def downsample(newSampleRate, oldSampleRate, data):
        numOfSamples = round(len(data) * float(newSampleRate) / oldSampleRate)
        return sps.resample(data, numOfSamples)

    def combineChannels(x, y):
        output = np.empty([len(x), 2])
        for n in range(len(x)):
            output[n] = [x[n], y[n]]
        return output

    def normalise(a):
        b = np.interp(a, (a.min(), a.max()), (-1, +1))
        return b