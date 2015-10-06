#!/usr/bin/python

import sys
import numpy as np
import pyaudio
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

class Plom(QtCore.QObject):
    
    toc = QtCore.pyqtSignal()
    t = 0
    
    def __init__(self,mw):
        super(QtCore.QObject, self).__init__()
        self.mw = mw
        self.music_proc = MusicProcessor()
        self.music_proc.toc.connect(self.handle_toc)
        self.music_proc.start()
    
    def handle_toc(self):
        if self.t == 0:
            self.mw.setStyleSheet("background-color: rgb(0,200,0);")
            self.t = 1
        else:
            self.mw.setStyleSheet("background-color: rgb(200,0,0);")
            self.t = 0


class MusicProcessor(QtCore.QObject):
    
    drum = 0
    toc = QtCore.pyqtSignal()
    
    def __init__(self):
        super(QtCore.QObject, self).__init__()
    
    def process_data(self, in_data, frame_count, time_info, flag):
        audio_data = np.fromstring(in_data, dtype=np.int32)
        if max(np.diff(np.diff(np.diff((audio_data))))) > 1e9:
            if self.drum == 0:
                self.toc.emit()
                self.drum = 1
        else:
            self.drum = 0
        return (audio_data, pyaudio.paContinue)
    
    def start(self):
        pa = pyaudio.PyAudio()
        rate = 44100
        chunk_duration = 0.05
        chunk_size = int(rate * chunk_duration)
        stream = pa.open(   format = pyaudio.paInt16,
                            channels = 2,
                            rate = 44100, 
                            input = True,
                            frames_per_buffer = chunk_size,
                            stream_callback = self.process_data
                        )
        stream.start_stream()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mw = QtWidgets.QMainWindow()
    mw.resize(500,500)
    mw.show()
    p = Plom(mw)
    sys.exit(app.exec_())
