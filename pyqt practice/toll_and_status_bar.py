import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QToolBar,
                             QAction, QStatusBar, QCheckBox)
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Some good ol practice")

        label = QLabel("This is a PyQt5 window!")
        label.setAlignment(Qt.AlignCenter)

        self.setCentralWidget(label)

        toolbar = QToolBar("My main toolbar")
        self.addToolBar(toolbar)

        button_action = QAction("Your button", self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.onMyToolBarButtonClick)
        button_action.setCheckable(True)
        toolbar.addAction(button_action)

        toolbar.addSeparator()

        button_action_2 = QAction("Your button2", self)
        button_action_2.setStatusTip("This is your button2")
        button_action_2.triggered.connect(self.onMyToolBarButtonClick)
        button_action_2.setCheckable(True)
        toolbar.addAction(button_action_2)

        toolbar.addWidget(QLabel("Hello"))
        toolbar.addWidget(QCheckBox())

        self.setStatusBar(QStatusBar(self))

    def onMyToolBarButtonClick(self,s):
        print("click", s)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()
