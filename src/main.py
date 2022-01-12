import pyaudio
from vosk import Model, KaldiRecognizer
from threading import Thread
import time

def test():
    thread1 = Thread(target=fun, args=(10,20))
    thread2= Thread(target=fun, args=(20,30))
    thread1.start()
    thread2.start()


def fun(start:int, end:int):
    for i in range(start, end):
        print(i)
        time.sleep(1)
        

if __name__ == "__main__":
    test()