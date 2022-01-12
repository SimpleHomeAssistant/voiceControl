import numpy as np

class ActivityDetector:
    def __init__(self, threshold=0.1):
        self.threshold = threshold

    def detectActivity(self, data):
        activity = []
        for i in range(len(self.data)):
            if self.data[i] > self.threshold:
                activity.append(1)
            else:
                activity.append(0)
        return activity

    def getActivity(self):
        return self.activity