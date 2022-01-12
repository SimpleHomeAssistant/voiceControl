# VoiceListener keeps listening the microphone and save the data in a cache.
# it also tries to identify the voice, when a possible active voice is detected, it will
# call a callback function and send the raw data to the callback function via the parameter.

import pyaudio
import config

class VoiceListener:
    def __init__(self, callback):
        self.callback = callback
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=config.format, channels=config.channels, rate=config.rate, input=True, frames_per_buffer=config.chunk)
        self.is_listening = False
        self.is_stopped = False
        self.is_paused = False

    def listen(self):
        self.is_listening = True
        while self.is_listening:
            data = self.stream.read(config.chunk)
            self.callback(data)
    
    def stop(self):
        self.is_listening = False
        self.is_stopped = True
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
