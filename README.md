# voiceControl

This project listens to the microphone and recognizes the voice commands.It also send the raw recognized texts to mqtt broker.


## Installation (tested in Raspberry Pi OS) 
install the following packages:
```
sudo apt-get install python3-pyaudio
sudo pip3 install vosk numpy paho-mqtt
```
vosk model files is not included in this repository, you may download them from [here](https://alphacephei.com/vosk/models)


## Todo
* optimize the recognition speed

## License
MIT License