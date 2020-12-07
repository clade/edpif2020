import threading
from time import time, sleep

import numpy as np

from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.widgets.MatplotlibWidget import MatplotlibWidget

from scope import TektronixScope
from fake_scope import FakeSCPITektronix
instr = FakeSCPITektronix()
scope = TektronixScope(instr)

class MyThread(threading.Thread):
    def __init__(self, cbk, delay=0.07):
        super().__init__()
        self.callback = cbk
        self.delay = delay
        self.want_to_terminate = False
    
    def run(self):
        t0 = time()
        while not self.want_to_terminate:
            self.callback(time() - t0)
            sleep(self.delay)


class StopWatchWindows(QtGui.QWidget):

    def __init__(self, args):
        super().__init__()

        self.main_layout = main_layout = QtGui.QVBoxLayout()
        self.setLayout(main_layout)
                

        self.startstop_button = QtGui.QPushButton('Start', self)
        self.save_button = QtGui.QPushButton('Save', self)
        self.label = QtGui.QLabel(self)
        self.display_time(0)

        self.plot_widget = MatplotlibWidget()

        main_layout.addWidget(self.startstop_button)
        main_layout.addWidget(self.label)
        main_layout.addWidget(self.plot_widget)
        main_layout.addWidget(self.save_button)

        self.startstop_button.clicked.connect(self.on_startstop_clicked)
        self.save_button.clicked.connect(self.save_to_file)

    def on_startstop_clicked(self):
        if self.startstop_button.text()=='Start':
            self.thread = MyThread(self.display_time)
            self.thread.start()
            self.thread_scope = MyThread(self.update_graph, delay=0.2)
            self.thread_scope.start()

            self.startstop_button.setText('Stop') 
        else:
            self.startstop_button.setText('Start')
            self.thread.want_to_terminate = True
            self.thread_scope.want_to_terminate = True

    def display_time(self, val):
        dec = val%1
        int_part = int(val-dec)
        seconds = int_part%60
        minutes = int_part//60
        val = f"{minutes:02d}:{seconds:02d}:{int(100*dec):02d}"
        self.label.setText(val)

    def update_graph(self, val):
        fig = self.plot_widget.getFigure()
        fig.clf()
        ax = fig.subplots(1, 1)
        x, y = scope.get_waveform()
        ax.plot(x, y)
        self.data = np.array([x, y]).T
        fig.canvas.draw()

    def save_to_file(self):
        file_name, _ = QtGui.QFileDialog.getSaveFileName(self.save_button, 'Save file', 
                                "", "Data file (*.txt)")
        np.savetxt(file_name, self.data)

if __name__ == "__main__":
    app = QtGui.QApplication([])
    main = StopWatchWindows([])
    main.show()
    exit(app.exec_())


# !pip install pyqtgraph
