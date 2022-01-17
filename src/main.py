import config
from controlClient import ControlClient
from recognizer import Recognizer
from voiceListener import VoiceListener
import logging


client=ControlClient(config.mqtt_broker_address,config.mqtt_broker_port)
recognizer=Recognizer(config.model_directory)
logger = logging.getLogger(__name__)

def listener_callback(data):
    logger.debug("listener_callback")
    recognizer.recognize_async(data,client.send_command)

def main():
    logger.debug("application starting")
    logging.basicConfig(level=logging.DEBUG)
    listener = VoiceListener(listener_callback)
    logger.debug("starting listener")
    listener.listen_async()
    logger.debug("listener started")

if __name__ == "__main__":
    main()