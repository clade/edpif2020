import threading
import time

from pyqtgraph.Qt import QtCore, QtGui

class MyThread(threading.Thread):
    def __init__(self, callback):   
        threading.Thread.__init__(self)
        self.running = True
        self.callback = callback

    def run(self):
        t0 = time.time()
        while self.running:
            t = time.time() - t0
            self.callback(t)
            time.sleep(0.08) 

    def stop(self):
        self.running = False

class StopWatchWindows(QtGui.QWidget):

    def __init__(self, args):
        super().__init__()

        self.main_layout = main_layout = QtGui.QVBoxLayout()
        self.setLayout(main_layout)
        
        self.startstop = QtGui.QPushButton('Start', self)
        self.label = QtGui.QLabel(self)


        main_layout.addWidget(self.startstop)   # button goes in upper-left
        main_layout.addWidget(self.label)

        self.startstop.clicked.connect(self.on_startstop_clicked)

        self.display_label(0)
    
    @QtCore.pyqtSlot()
    def on_startstop_clicked(self):
        if self.startstop.text()=='Start':
            self.startstop.setText('Stop')
            self.thread = MyThread(self.display_label)
            self.thread.start()
        elif self.startstop.text()=='Stop':
            self.startstop.setText('Start')
            self.thread.stop()
    
    def display_label(self, val):
        dec = val%1
        int_part = int(val - dec)
        seconde = int_part%60
        minutes = int_part//60
        self.label.setText('{:02d}:{:02d}:{:02d}'.format(minutes, seconde, int(100*dec)))


if __name__ == "__main__":
    app = QtGui.QApplication([])
    main = StopWatchWindows([])
    main.show()
    exit(app.exec_())
