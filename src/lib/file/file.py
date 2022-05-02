# Class to handle all file related operations
# Is useful to include some getters to easily receive file information through app.

class File():
    path = ''
    filename = ''
    filetype = ''
    sampleRate = 0
    numOfSamples = 0
    duration = 0
    timeDomain = []
    frequencyDomain = []

    def __init__(self, file):
        self.file = file
    
    def get(self):
        return self.file

    def path(self):
        return self.file

    def sampleRate(self):
        return self.file

    def filetype(self):
        return self.file

    def duration(self):
        return self.file

    def timeDomain(self):
        return self.file

    def frequencyDomain(self):
        return self.file
