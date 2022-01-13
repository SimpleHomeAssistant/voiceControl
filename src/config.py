# here are some configuration variables

import pyaudio
import os

format= pyaudio.paInt16 # if you change this, you will have to change the numpy dtype in activityDetector.py
channels = 1
frame_rate = 44100
chunk = 1024

voiceIdleTime = 1 # seconds
activity_detection_threshold = 1300 # this value is tested in my room, it may still need adjustment
model_directory = os.path.join(os.path.dirname(__file__), "model")

control_server_ip = "127.0.0.1"	
control_server_port = 2133