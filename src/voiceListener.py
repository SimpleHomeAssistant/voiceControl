# VoiceListener keeps listening the microphone and save the data in a cache.
# it also tries to identify the voice, when a possible active voice is detected, it will
# call a callback function and send the raw data to the callback function via the parameter.

from threading import Thread
import pyaudio
import config
from activityDetector import ActivityDetector
import logging
import wave
import io

class VoiceListener:
    def __init__(self, callback):
        self.callback = callback
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=config.format, channels=config.channels, rate=config.frame_rate, input=True, frames_per_buffer=config.chunk)
        self.is_listening = False
        self.is_stopped = False
        self.is_paused = False
        self.wave_stream= None # the steam from the wave file
        self.wave_file = None # the io.BytesIO of the wave file
        self.has_data = False # if there is data in the wave file
        self.detector = ActivityDetector(config.activity_detection_threshold)
        self.max_inactivity_count = config.voiceIdleTime / 0.5 # 0.5 seconds per count
        self.voice_inactivity_counter = 0
        self.logger = logging.getLogger(__name__)
        self.logger.info("VoiceListener initialized")

    def reset_wave(self):
        self.wave_file = io.BytesIO()
        self.wave_stream = wave.open(self.wave_file, 'wb')
        self.wave_stream.setnchannels(config.channels)
        self.wave_stream.setsampwidth(self.p.get_sample_size(config.format))
        self.wave_stream.setframerate(config.frame_rate)
        self.has_data = False


    def listen(self):
        self.logger.debug("start listening")
        self.is_listening = True
        self.reset_wave()
        while self.is_listening:
            # read 0.5 seconds of data each time
            chunk = config.chunk
            frames = []
            for i in range(0, int(config.frame_rate / config.chunk * 0.5)):
                data = self.stream.read(chunk, exception_on_overflow = False)
                frames.append(data)
                self.wave_stream.writeframes(data)
            
            is_active = self.detector.detectActivity(frames)
            if is_active:
                self.voice_inactivity_counter = 0
                self.has_data = True
            else:
                self.voice_inactivity_counter += 1
            if self.voice_inactivity_counter > self.max_inactivity_count and self.has_data:
                self.logger.info("activity detected, sending data for recognition")	
                self.wave_stream.close()
                self.wave_file.seek(0)
                self.callback(self.wave_file)
                    
                self.reset_wave()
                self.voice_inactivity_counter = 0

    def listen_async(self):
        th = Thread(target=self.listen)
        th.start()

    def stop(self):
        self.is_listening = False
        self.is_stopped = True
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
