import scipy.signal as sps
import numpy as np

class Utils():
    def downsample(newSampleRate, oldSampleRate, data):
        numOfSamples = round(len(data) * float(newSampleRate) / oldSampleRate)
        return sps.resample(data, numOfSamples)

    def normalise(data):
        norm = np.linalg.norm(data)
        return  data / norm