# VoiceListener keeps listening the microphone and save the data in a cache.
# it also tries to identify the voice, when a possible active voice is detected, it will
# call a callback function and send the raw data to the callback function via the parameter.

import pyaudio
import config
from activityDetector import ActivityDetector
import logging

class VoiceListener:
    def __init__(self, callback):
        self.callback = callback
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=config.format, channels=config.channels, rate=config.rate, input=True, frames_per_buffer=config.chunk)
        self.is_listening = False
        self.is_stopped = False
        self.is_paused = False
        self.cache = []
        self.voiceIdleTime = config.voiceIdleTime
        self.detector = ActivityDetector(config.activityDetectionThreshold)
        self.max_inactivity_count = config.voiceIdleTime * (config.rate / config.chunk)
        self.voice_inactivity_counter = 0
        self.logger = logging.getLogger(__name__)
        self.logger.info("VoiceListener initialized")

    def listen(self):
        self.logger.debug("start listening")
        self.is_listening = True
        while self.is_listening:
            # read 0.5 seconds of data each time
            chunk = config.chunk
            data = self.stream.read(config.chunk, exception_on_overflow = False)
            self.cache.append(data)
            is_active = self.detector.detectActivity(data)
            if is_active:
                self.voice_inactivity_counter = 0
            else:
                self.voice_inactivity_counter += 1
            if self.voice_inactivity_counter > self.max_inactivity_count:
                self.callback(self.cache)
                self.cache = []
                self.voice_inactivity_counter = 0


    def stop(self):
        self.is_listening = False
        self.is_stopped = True
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
