import requests
import logging

class ControlClient:
    """
    control client is used for sending command to the control center via http
    """
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.logger = logging.getLogger(__name__)
        self.logger.info("ControlClient initialized")
    
    def send_command(self, command):
        """
        send command to the control center
        :param command: command to be sent
        """
        self.logger.debug("sending command: %s", command)
        url = "http://" + self.host + ":" + str(self.port) + "/command/" + command
        try:
            response = requests.get(url)
            self.logger.debug("response: %s", response.text)
        except Exception as e:
            self.logger.error("send command error: %s", e)
            return False
        return True