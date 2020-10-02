import sys
import pandas as pd
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt

pulsar_data = pd.read_csv('data/HTRU_2.csv')

class DataInteractionForm(QWidget, QAbstractTableModel):
    def __init__(self,data):
        #super().__init__()
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self):
        return self._data.shape[0]

    def columnCount(self):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Gotta Start Somewhere')
        self.resize(1200,600)

        data = pulsar_data
        #print(data.iloc[index.row(),index.column()])

        self.menuBar = self.menuBar()
        self.fileMenu = self.menuBar.addMenu('File')
        self.modelMenu = self.menuBar.addMenu('Model')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
