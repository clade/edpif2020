import threading
import time

from pyqtgraph.Qt import QtCore, QtGui


class StopWatchWindows(QtGui.QWidget):

    def __init__(self, args):
        super().__init__()

        self.main_layout = main_layout = QtGui.QVBoxLayout()
        self.setLayout(main_layout)
                

if __name__ == "__main__":
    app = QtGui.QApplication([])
    main = StopWatchWindows([])
    main.show()
    exit(app.exec_())


# !pip install pyqtgraph
