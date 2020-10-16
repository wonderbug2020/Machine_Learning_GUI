import sys
from PyQt5.QtWidgets import (QApplication, QLabel, QMainWindow, QWidget,
                             QHBoxLayout, QVBoxLayout, QComboBox, QLineEdit,
                             QPushButton)
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

class UiLayout(QWidget):
    def __init__(self):
        super().__init__()

        #self.central_widget = QWidget()
        #self.layout1 = QHBoxLayout(self.central_widget)
        #self.dropdown_1_text = QLabel("Select the predictor column")
        #self.layout1.addWidget(self.dropdown_1_text)

        self.layout_top = QVBoxLayout()
        self.text_1 = QLabel("text goes here")
        self.layout_top.addWidget(self.text_1)

class MainWindow(QMainWindow):
    def __init__(self, ui_layout):
        super(MainWindow, self).__init__()

        #Sets the title for the main window
        self.setWindowTitle("prototype 3")

        self.setCentralWidget(ui_layout)


app = QApplication(sys.argv)
ui_layout = UiLayout()
window = MainWindow(ui_layout)
window.showMaximized()
app.exec_()
