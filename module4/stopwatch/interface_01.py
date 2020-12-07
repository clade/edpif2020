import threading
import time

from pyqtgraph.Qt import QtCore, QtGui

class StopWatchWindows(QtGui.QWidget):

    def __init__(self, args):
        super().__init__()

        self.main_layout = main_layout = QtGui.QVBoxLayout()
        self.setLayout(main_layout)
        
        self.startstop = QtGui.QPushButton('Start', self)
        self.label = QtGui.QLabel(self)
        self.label.setText('Bonjour') 

        main_layout.addWidget(self.startstop)
        main_layout.addWidget(self.label)

        self.startstop.clicked.connect(self.on_startstop_clicked)

   

    @QtCore.pyqtSlot()
    def on_startstop_clicked(self):
        if self.startstop.text()=='Start':
            self.startstop.setText('Stop')
            print('START')
        elif self.startstop.text()=='Stop':
            self.startstop.setText('Start')
            print('STOP')

if __name__ == "__main__":
    app = QtGui.QApplication([])
    main = StopWatchWindows([])
    main.show()
    exit(app.exec_())
