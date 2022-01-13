# here are some configuration variables

import pyaudio

format= pyaudio.paInt16 # if you change this, you will have to change the numpy dtype in activityDetector.py
channels = 1
rate = 44100
chunk = 1024

voiceIdleTime = 1 # seconds
activityDetectionThreshold = 1300 # this value is tested in my room, it may still need adjustment
