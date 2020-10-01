import sys
import pandas
from PyQt5.QtWidgets import QMainWindow, QApplication



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Gotta Start Somewhere')
        self.resize(1200,600)

        self.menuBar = self.menuBar()
        self.fileMenu = self.menuBar.addMenu('File')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
