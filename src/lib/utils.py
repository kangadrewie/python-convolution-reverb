import scipy.signal as sps
import numpy as np

class Utils():
    def downsample(newSampleRate, oldSampleRate, data):
        numOfSamples = round(len(data) * float(newSampleRate) / oldSampleRate)
        return sps.resample(data, numOfSamples)

    def normalise(a):
        # b = np.interp(a, (a.min(), a.max()), (-10, +10))
        return a