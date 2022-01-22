from asyncio.log import logger
from vosk import Model, KaldiRecognizer
import logging
import threading
from threading import Thread
import config
import wave
import json

class Recognizer:
    """
    voice command recognizer using kaldi
    """
    def __init__(self, model_path):
        self.model = Model(model_path)
        self.rec = KaldiRecognizer(self.model,config.frame_rate)
        self.logger = logging.getLogger(__name__)
        self.lock = threading.Lock()
        
    def recognize(self, wave_object):
        """
        recognize the voice command
        :param data: audio data frames
        :return: the recognized command
        """
        
        self.lock.acquire()
        self.logger.debug("recognizing")
        recognized_text= None
        try:
            wf = wave.open(wave_object, "rb")
            count=0
            while True:
                count+=1
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                self.rec.AcceptWaveform(data)
            result = self.rec.FinalResult()
            self.rec.Reset()
            self.logger.debug("recognized: %s, %d times frame read", result,count)
            obj = json.loads(result)
            recognized_text = obj["text"]
        except Exception as e:
            self.logger.error("recognize error: %s, %s", type(e), e)
        finally:
            self.lock.release()
        
        return recognized_text
    
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
