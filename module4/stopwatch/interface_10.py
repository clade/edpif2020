import threading
import time

import numpy as np

from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.widgets.MatplotlibWidget import MatplotlibWidget

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


class ScopeWindows(QtGui.QWidget):

    def __init__(self, args):
        super().__init__()
        self.setObjectName('I')

        self.main_layout = main_layout = QtGui.QVBoxLayout()
        self.setLayout(main_layout)

        self.plot_widget = MatplotlibWidget()
        
        btn_layout = QtGui.QHBoxLayout()

        self.startstop = QtGui.QPushButton(self)
        self.startstop.setText('Start')
        self.label = QtGui.QLabel(self)
        self.display_label(0)
        self.save_btn = QtGui.QPushButton('Save', self)

        btn_layout.addWidget(self.startstop)
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.label)

        main_layout.addWidget(self.plot_widget)
        main_layout.addLayout(btn_layout)

        self.startstop.clicked.connect(self.on_startstop_clicked)
        self.save_btn.clicked.connect(self.save_to_file)

    
        print('INIT')

    @QtCore.pyqtSlot()
    def on_startstop_clicked(self):
        if self.startstop.text()=='Start':
            self.startstop.setText('Stop')
            self.thread = MyThread(self.display_label)
            self.thread.start()
        elif self.startstop.text()=='Stop':
            self.startstop.setText('Start')
            self.thread.running = False
    
    @QtCore.pyqtSlot()
    def save_to_file(self):
        # See https://doc.qt.io/qtforpython/PySide2/QtWidgets/QFileDialog.html#PySide2.QtWidgets.PySide2.QtWidgets.QFileDialog.getSaveFileName
        file_name = QtGui.QFileDialog.getSaveFileName(self.save_btn, 'Save file', 
                                "", "Data file (*.txt)")
        print(file_name)

    def plot(self, param=0):
        fig = self.plot_widget.getFigure()
        fig.clf()
        x = np.linspace(0, 1, 1001)
        y = np.sin(2*np.pi*x*param)
        ax = fig.subplots()
        ax.plot(x, y)
        ax.set_ylim(-1, 1)
        fig.canvas.draw()

    def display_label(self, val):
        self.plot(val)
        dec = val%1
        int_part = int(val - dec)
        seconde = int_part%60
        minutes = int_part//60
        self.label.setText('{:02d}:{:02d}:{:02d}'.format(minutes, seconde, int(100*dec)))


if __name__ == "__main__":
    app = QtGui.QApplication([])
    main = ScopeWindows([])
    main.show()
    exit(app.exec_())
