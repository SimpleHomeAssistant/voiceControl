from asyncio.log import logger
from vosk import Model, KaldiRecognizer
import logging
from threading import Thread
import config
import wave

class Recognizer:
    """
    voice command recognizer using kaldi
    """
    def __init__(self, model_path):
        self.model = Model(model_path)
        self.rec = KaldiRecognizer(self.model,config.frame_rate)
        self.logger = logging.getLogger(__name__)
        
    def recognize(self, wave_object):
        """
        recognize the voice command
        :param data: audio data frames
        :return: the recognized command
        """
        self.logger.debug("recognizing")
        try:
            wf = wave.open(wave_object, "rb")
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                self.rec.AcceptWaveform(data)
            result = self.rec.FinalResult()
            self.rec.Reset()
            self.logger.debug("recognized: %s", result)
            return result
        except Exception as e:
            self.logger.error("recognize error: %s, %s", type(e), e)
            return ""
    
    def recognize_async(self, data, callback):
        """
        recognize the voice command asynchronously
        :param data: audio data frames
        :param callback: callback function, it should take a string parameter as the recognized command
        """
        def reconize_and_callback():
            result = self.recognize(data)
            callback(result)
        th= Thread(target=reconize_and_callback)
        th.start()
