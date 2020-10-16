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



    def get_predictor(self, predictor):
        #print(self._data[y])
        y_df = self._data[predictor]
        x_df = self._data.drop(labels=[predictor],axis=1)

        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(x_df, y_df, test_size=0.25, random_state=101)

        from sklearn.preprocessing import StandardScaler
        sc = StandardScaler()
        X_train = sc.fit_transform(X_train)
        X_test = sc.transform(X_test)

        from sklearn.linear_model import LogisticRegression
        log_cla = LogisticRegression(random_state = 0)
        log_cla.fit(X_train, y_train)
        y_pred = log_cla.predict(X_test)

        from sklearn.metrics import confusion_matrix, accuracy_score
        cm = confusion_matrix(y_test, y_pred)
        print(cm)
        ac = accuracy_score(y_test, y_pred)
        print(ac)






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

        #Input box to set train/test split
        self.train_split_text = QLabel("Select the train test split you would like to use")
        self.train_split_input = QLineEdit()
        self.train_split_input.setMaxLength(3)

        #Button to build the model
        self.model_btn_text = QLabel("Push here once you have choosen all your options")
        self.model_btn = QPushButton()
        self.model_btn.setText("Run Model")

        self.model_btn.clicked.connect(lambda: self.model.get_predictor(self.dropdown_1.currentText()))

        #Label to display the results
        self.output_text = QLabel()

        #adding the widgets to the layout
        self.layout2.addWidget(self.dropdown_1_text)
        self.layout2.addWidget(self.dropdown_1)
        self.layout2.addWidget(self.dropdown_2_text)
        self.layout2.addWidget(self.dropdown_2)
        self.layout2.addWidget(self.train_split_text)
        self.layout2.addWidget(self.train_split_input)
        self.layout2.addWidget(self.model_btn_text)
        self.layout2.addWidget(self.model_btn)
        self.layout2.addWidget(self.output_text)
        #adding the rightside ui to the main layout
        self.layout2.setAlignment(Qt.AlignTop)

        self.layout1.addLayout(self.layout2, 20)

        self.setCentralWidget(self.central_widget)

    #def test_func(self):
        #self.output_text.setText("Clicked")


app = QApplication(sys.argv)
window = MainWindow()
window.showMaximized()
app.exec_()
