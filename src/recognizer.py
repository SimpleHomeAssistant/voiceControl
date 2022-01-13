from asyncio.log import logger
from vosk import Model, KaldiRecognizer
import logging
from threading import Thread
import config

class Recognizer:
    """
    voice command recognizer using kaldi
    """
    def __init__(self, model_path):
        self.model = Model(model_path)
        self.rec = KaldiRecognizer(self.model,config.frame_rate)
        self.logger = logging.getLogger(__name__)
        
    def recognize(self, data):
        """
        recognize the voice command
        :param data: audio data frames
        :return: the recognized command
        """
        self.logger.debug("recognizing")
        self.logger.debug("data count: %d", len(data))
        try:
            for frame in data:
                self.rec.AcceptWaveform(frame)
            result = self.rec.FinalResult()
            self.logger.debug("recognized result: %s", result)
            return result
        except Exception as e:
            self.logger.error("recognize error: %s", e)
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
