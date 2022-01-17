import logging
from time import sleep
import paho.mqtt.client as mqtt

class ControlClient:
    """
    control client is used for publish MQTT message to the broker
    """
    def __init__(self, broker_address, port):
        """
        initialize control client
        """
        self.logger = logging.getLogger(__name__)
        # init paho mqtt client
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(host =broker_address, port = port, keepalive = 60)
        self.client.loop_start()
        self.client.subscribe("$SYS/#")

    
    def on_connect(self, client, userdata, flags, rc):
        """
        callback for mqtt client on_connect
        """
        self.logger.info("Connected with result code "+str(rc))
        # client.subscribe("test")
    
    def on_message(self, client, userdata, msg):
        """
        callback for mqtt client on_message
        """
        self.logger.info(msg.topic+" "+str(msg.payload))


    def send_command(self, command):
        """
        send command to the broker
        """
        topic = "test"
        self.logger.debug("send command %s to topic %s" % (command, topic))
        self.client.publish(topic, command)

