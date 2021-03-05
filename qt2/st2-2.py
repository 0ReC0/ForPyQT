import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from ui_st2_1 import Ui_MainWindow


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyWidget, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.run)

    def run(self):
        self.label.setText("From py loaded ui")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = MyWidget()
    wnd.show()
    sys.exit(app.exec_())