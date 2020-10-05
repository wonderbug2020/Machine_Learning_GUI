import sys
from PyQt5.QtWidgets import (QApplication, QLabel, QMainWindow, QWidget,
                             QHBoxLayout, QVBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from PyQt5 import QtCore, QtWidgets
import pandas as pd


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row()][index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("prototype 2")


        data = pd.read_csv('data/HTRU_2.csv')

        central_widget = QWidget()
        layout1 = QHBoxLayout(central_widget)
        #layout1 = QHBoxLayout()
        layout2 = QVBoxLayout()

        self.model = TableModel(data)
        self.table = QtWidgets.QTableView()
        self.table.setModel(self.model)

        layout1.addWidget(self.table)
        layout1.addLayout(layout2)

        self.setCentralWidget(central_widget)
        #self.setCentralWidget(layout1)



app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
