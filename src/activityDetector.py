import numpy as np

class ActivityDetector:
    def __init__(self, threshold=0.1):
        self.threshold = threshold

    def detectActivity(self, data:list):
        """	
        this function tries to detect activity in the given data
        :param data: a list of data frames from the microphone
        :return: true if activity is detected and false otherwise
        """
        activity = []
        for i in range(len(self.data)):
            if self.data[i] > self.threshold:
                activity.append(1)
            else:
                activity.append(0)
        return activity

    def getActivity(self):
        return self.activity