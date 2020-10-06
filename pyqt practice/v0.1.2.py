import sys
from PyQt5.QtWidgets import (QApplication, QLabel, QMainWindow, QWidget,
                             QHBoxLayout, QVBoxLayout, QComboBox, QSlider)
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

        #Sets the title for the main window
        self.setWindowTitle("prototype 2")

        #Loads the data into a df to be used elsewhere
        data = pd.read_csv('data/HTRU_2.csv')
        #makes a list of all the column headers
        col_headers = data.columns.tolist()
        #makes a list of the ML models to used
        model_lst = ['Logistic regression']

        #Sets up the layouts that will be used
        self.central_widget = QWidget()
        self.layout1 = QHBoxLayout(self.central_widget)
        self.layout2 = QVBoxLayout()

        #Left side table
        self.model = TableModel(data)
        self.table = QtWidgets.QTableView()
        self.table.setModel(self.model)
        self.layout1.addWidget(self.table,80)

        #Right side UI
        #Dropdown list to choose the column
        self.dropdown_1_text = QLabel("Select the predictor column")
        self.dropdown_1 = QComboBox()
        self.dropdown_1.addItems(col_headers)
        #Dropdown list to choose the model
        self.dropdown_2_text = QLabel("Select the Model you would like to use")
        self.dropdown_2 = QComboBox()
        self.dropdown_2.addItems(model_lst)
        #Slider bar to set train/test split
        self.train_split_text = QLabel("Select the train test split you would like to use")
        self.train_split_slider = QSlider(Qt.Horizontal)
        #self.train_split_slider.setMinimum(0)
        #self.train_split_slider.setMaximum(100)
        self.train_split_slider.setRange(0,100)
        self.train_split_slider.setSingleStep(5)
        #self.train_split_slider.value()
        self.train_split_slider.setTickInterval(5)
        self.train_split_slider.setTickPosition(QSlider.TicksBelow)
        #adding the widgets to the layout
        self.layout2.addWidget(self.dropdown_1_text)
        self.layout2.addWidget(self.dropdown_1)
        self.layout2.addWidget(self.dropdown_2_text)
        self.layout2.addWidget(self.dropdown_2)
        self.layout2.addWidget(self.train_split_text)
        self.layout2.addWidget(self.train_split_slider)
        #adding the rightside ui to the main layout
        self.layout2.setAlignment(Qt.AlignTop)

        self.layout1.addLayout(self.layout2, 20)

        self.setCentralWidget(self.central_widget)
        #self.setCentralWidget(layout1)



app = QApplication(sys.argv)
window = MainWindow()
window.showMaximized()
app.exec_()
