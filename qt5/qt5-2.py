import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton
from PyQt5.QtWidgets import QInputDialog


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 150, 150)
        self.setWindowTitle('Диалоговые окна')

        self.button_1 = QPushButton(self)
        self.button_1.move(20, 40)
        self.button_1.setText("Кнопка")
        self.button_1.clicked.connect(self.run)

    def run(self):
        name, ok_pressed = QInputDialog.getText(self, "Введите имя",
                                                "Как тебя зовут?")
        age, ok_pressed = QInputDialog.getInt(
            self, "Введите возраст", "Сколько тебе лет?",
            20, 18, 27, 1)

        country, ok_pressed = QInputDialog.getItem(
            self, "Выберите вашу страну", "Откуда ты?",
            ("Россия", "Германия", "США"), 1, False)

        if ok_pressed:
            self.button_1.setText(name)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())