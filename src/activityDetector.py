import numpy as np
import logging

class ActivityDetector:
    def __init__(self, threshold=0.1):
        self.threshold = threshold
        self.logger = logging.getLogger(__name__)

    def detectActivity(self, data:list):
        """	
        this function tries to detect activity in the given data
        :param data: a list of data frames from the microphone
        :return: true if activity is detected and false otherwise
        """
        # merge the data frames into a single array
        data = np.fromstring(b''.join(data), dtype=np.int16)
        # get spectrum of the data
        spectrum = np.fft.fft(data)
        # get the absolute value of the spectrum
        spectrum = np.abs(spectrum)
        # get the average of the spectrum
        avg = np.mean(spectrum)
        # check if the average is above the threshold
        if avg > self.threshold:
            self.logger.debug("activity detected, avg = %f", avg)
            return True
        return False
