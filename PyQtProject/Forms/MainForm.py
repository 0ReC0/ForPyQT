from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QTabWidget, QGridLayout, QTableWidget
from PyQtProject.UIs.MainUI_ui import Ui_MainWindow
import sqlite3


class MainForm(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainForm, self).__init__()
        self.setupUi(self)
        self.layout = QGridLayout()

        self.db_connection = None
        self.tables_tab_widget = None

        self.connect_toolbar_with_functions()

    def connect_toolbar_with_functions(self):
        self.open_db_action.triggered.connect(self.open_db)
        # self.save_db_action.triggered.connect()

    def open_db(self):
        try:
            table_name = QFileDialog.getOpenFileName(self, "Выберите базу данных sqlite", '', "*.sqlite")[0]
            self.db_connection = sqlite3.connect(table_name)

            cur = self.db_connection.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables_names = [el[0] for el in cur.fetchall()]
            if not tables_names:
                raise Exception("Нет таблиц в базе данных")

            self.notLoadDbLabel.deleteLater()
            self.tables_tab_widget = QTabWidget()

            for name in tables_names:
                table_widget = QTableWidget(self)
                table_widget.layout = QGridLayout(self.tables_tab_widget)
                self.tables_tab_widget.addTab(table_widget, name)

        except sqlite3.Error as e:
            self.statusBar().showMessage(f'Ошибка: {e.args[0]}')
        except Exception as e:
            self.statusBar().showMessage(f'Ошибка: {e.args[0]}')

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Закрытие окна', 'Вы уверены, что хотите закрыть приложение?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            if self.db_connection:
                self.db_connection.close()
            event.accept()
        else:
            event.ignore()