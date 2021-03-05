import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui_st2_1.ui', self)
        self.pushButton.clicked.connect(self.run)

    def run(self):
        self.label.setText('TEect')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
