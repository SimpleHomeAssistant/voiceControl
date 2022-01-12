# here are some configuration variables

import pyaudio

format= pyaudio.paInt16
channels = 1
rate = 44100
chunk = 1024

voiceIdleTime = 2 # seconds
activityDetectionThreshold = 0.1 
