import csv

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
import sys


class SaveToCSVWidget(QMainWindow):
    def __init__(self):
        super(SaveToCSVWidget, self).__init__()
        uic.loadUi("UI2.ui", self)
        self.pushButton.clicked.connect(self.save_2_csv)

    def save_2_csv(self):
        with open('results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(
                csvfile, delimiter=';', quotechar='"',
                quoting=csv.QUOTE_MINIMAL)
            # Получение списка заголовков
            writer.writerow(
                [self.tableWidget.horizontalHeaderItem(i).text()
                 for i in range(self.tableWidget.columnCount())])
            for i in range(self.tableWidget.rowCount()):
                row = []
                for j in range(self.tableWidget.columnCount()):
                    item = self.tableWidget.item(i, j)
                    if item is not None:
                        row.append(item.text())
                writer.writerow(row)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = SaveToCSVWidget()
    wnd.show()
    sys.exit(app.exec())
