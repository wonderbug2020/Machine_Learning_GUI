from PyQt5.QtWidgets import (QApplication, QLabel, QMainWindow, QWidget,
                             QHBoxLayout, QVBoxLayout, QComboBox, QLineEdit,
                             QPushButton, QFileDialog)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtWidgets
import sys
from pathlib import Path
import pandas as pd
import numpy
import csv

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


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self._data = pd.DataFrame()

        self.central_widget = QWidget()
        self.layout1 = QHBoxLayout(self.central_widget)

        self.model = TableModel(self._data)
        self.table = QtWidgets.QTableView()
        self.table.setModel(self.model)
        self.layout1.addWidget(self.table,80)

        self.test_btn = QPushButton()
        self.test_btn.setText("Test")
        self.test_btn.clicked.connect(self.showDialog)

        self.layout1.addWidget(self.test_btn,20)

        self.setCentralWidget(self.central_widget)

    def showDialog(self):

        fname = QFileDialog.getOpenFileName(self, "Open Data File", "",
                                            "CSV data files (*.csv)")

        self._data = pd.read_csv(fname[0])
        self.model = TableModel(self._data)
        self.table.setModel(self.model)

        """
        if fname:
            ff = open(fname[0], 'r')
            with ff:
                self._data = csv.reader(ff, delimiter=';')
            print(fname[0])
            #self.model = TableModel(self._data)
            #self.table.setModel(self.model)
        """



app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
