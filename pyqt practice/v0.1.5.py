import sys
from PyQt5.QtWidgets import (QApplication, QLabel, QMainWindow, QWidget,
                             QHBoxLayout, QVBoxLayout, QComboBox, QLineEdit,
                             QPushButton)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from PyQt5 import QtCore, QtWidgets
import pandas as pd
import numpy


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

    def build_model(self, predictor, model_select, tts):
        #print(f"The predictor is {predictor} and the model is {model_select}")
        X,y = self.get_X_y(predictor)
        X_train, X_test, y_train, y_test = self.get_train_test_split(X,y,float(tts))
        x_train, X_test = self.get_scaled_data(X_train, X_test)
        if model_select == 'Logistic regression':
            y_pred = self.logistic_regression_model(X_train, y_train, X_test)
        elif model_select == 'Random Forest':
            y_pred = self.random_forest_model(X_train, y_train, X_test)
        cm, ac = self.get_metrics(y_test, y_pred)
        #print(f"{cm} and {ac}")
        print(cm)
        print(ac)

    def get_X_y(self, predictor):
        y=self._data[predictor].to_numpy()
        X=self._data.drop(labels=[predictor],axis=1).to_numpy()
        return X, y

    def get_train_test_split(self, X, y, split):
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=split, random_state=101)
        return X_train, X_test, y_train, y_test

    def get_scaled_data(self, X_train, X_test):
        from sklearn.preprocessing import StandardScaler
        sc = StandardScaler()
        X_train = sc.fit_transform(X_train)
        X_test = sc.transform(X_test)
        return X_train, X_test

    def logistic_regression_model(self, X_train, y_train, X_test):
        from sklearn.linear_model import LogisticRegression
        log_cla = LogisticRegression(random_state = 0)
        log_cla.fit(X_train, y_train)
        y_pred = log_cla.predict(X_test)
        return(y_pred)

    def random_forest_model(self, X_train, y_train, X_test):
        from sklearn.ensemble import RandomForestClassifier
        rfc = RandomForestClassifier(n_estimators=10, criterion = 'entropy', random_state = 0)
        rfc.fit(X_train,y_train)
        y_pred = rfc.predict(X_test)
        return(y_pred)

    def get_metrics(self, y_test, y_pred):
        from sklearn.metrics import confusion_matrix, accuracy_score
        cm = confusion_matrix(y_test, y_pred)
        #print(cm)
        ac = accuracy_score(y_test, y_pred)
        #print(ac)
        return cm, ac

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
        model_lst = ['Logistic regression','Random Forest']

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

        self.model_btn.clicked.connect(lambda: self.model.build_model(
                                               self.dropdown_1.currentText(),
                                               self.dropdown_2.currentText(),
                                               self.train_split_input.text()))

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
