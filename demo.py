import sys
import array
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QLabel, QTextEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
#from record import Recorder

from SpeechModel251 import ModelSpeech
from LanguageModel2 import ModelLanguage
import os

import pyaudio
import wave
import threading
import time

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = "output.wav"

os.environ['KMP_DUPLICATE_LIB_OK']='True'

class Recorder(object):
    def __init__(self):

        self.p = pyaudio.PyAudio()
        

    def start(self):
        threading._start_new_thread(self._record, ())

    def stop(self):
        self._running = False

    def _record(self):
        self._running = True
        self._frames = []
        stream = self.p.open(format=pyaudio.paInt16,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

        while(self._running):
            self._frames.append(stream.read(CHUNK))
 
        #self.stream.stop_stream()
        #self.stream.close()
        #self.p.terminate()

    def save(self, filename='output.wav'):
        wf = wave.open(filename, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(self._frames))
        wf.close()

# Subclass QMainWindow to customise your application's main window
class App(QWidget):

    def __init__(self):
        super(App, self).__init__()
        self.record_name = 'saved_record.wav'
        self.ms = ModelSpeech('dataset')
        self.ms.LoadModel('model_speech/speech_model251_e_0_step_12000.model')
        self.ml = ModelLanguage('model_language')
        self.ml.LoadModel()
        self.title = 'ASR demo'
        self.left = 10
        self.top = 10
        self.width = 420
        self.height = 400
        self.rec = Recorder()
        #self.rec.start_thread()
        self.initUI()
        self.rec.start()



        
        #self.setWindowTitle("ASR demo")

        
        
            

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        button = QPushButton('Record', self)
        button.setToolTip('Press to start recording')
        button.move(100,70)
        button.clicked.connect(self.start_record)
        
        button = QPushButton('To Transcript', self)
        button.setToolTip('Press to convert to transcript')
        button.move(200,70)
        button.clicked.connect(self.stop_record)

        button = QPushButton('Clear', self)
        button.setToolTip('Press to clear transcripts')
        button.move(100,100)
        button.clicked.connect(self.clear)

        self.text_edit = QTextEdit("What you said: ",self)
        self.text_edit.setReadOnly(True)
        self.text_edit.move(100,140)

        #self.results=QLabel(self)
        #self.results.move(100,140)

        self.show()

    @pyqtSlot()
    def clear(self):
        self.text_edit.clear()
        self.text_edit.append("What you said: ")

    @pyqtSlot()
    def start_record(self):
        self.rec.start()
        
        #print('PyQt5 button click')
        #self.rec.start()

    @pyqtSlot()
    def stop_record(self):
        print(len(self.rec._frames))
        #print('PyQt5 button click')
        self.rec.stop()
        self.rec.save(self.record_name)
        r = self.ms.RecognizeSpeech_FromFile(self.record_name)
        self.w = self.ml.SpeechToText(r)
        print('语音转文字结果：\n',self.w)
        self.text_edit.append(self.w)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
