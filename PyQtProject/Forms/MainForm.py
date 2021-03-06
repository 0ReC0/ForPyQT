from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QTabWidget, QGridLayout, QTableWidget, \
    QTableWidgetItem, QPushButton
from PyQtProject.UIs.MainUI_ui import Ui_MainWindow
import sqlite3
import magic


class MainForm(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainForm, self).__init__()
        self.setupUi(self)

        self.db_name = None
        self.db_connection = None
        self.tables_tab_widget = None
        self.modified_data_in_tables = {}
        self.connect_toolbar_with_functions()

    def connect_toolbar_with_functions(self):
        self.open_db_action.triggered.connect(self.open_db)
        self.delete_selected_elements_action.triggered.connect(self.delete_elem)
        self.save_current_table_action.triggered.connect(self.save_current_table_changes)
        self.save_all_tables_action.triggered.connect(self.save_all_tables_changes)
        self.save_db_as_action.triggered.connect(self.save_db_as)

    def open_db(self):
        try:
            self.db_name = QFileDialog.getOpenFileName(self, "Выберите базу данных sqlite", '', "*.sqlite")[0]
            self.db_connection = sqlite3.connect(self.db_name)

            cur = self.db_connection.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables_names = [el[0] for el in cur.fetchall()]
            if not tables_names:
                raise Exception("Нет таблиц в базе данных")

            self.notLoadDbLabel.deleteLater()
            self.tables_tab_widget = QTabWidget(self)
            self.gridLayout.addWidget(self.tables_tab_widget)

            for name in tables_names:
                self.modified_data_in_tables[name] = {}
                table_widget = QTableWidget()
                self.tables_tab_widget.addTab(table_widget, name)
                self.init_table_widget_for_db_table(table_widget, name)

        except sqlite3.Error as e:
            self.statusBar().showMessage(f'Ошибка с бд: {e.args[0]}')
        except Exception as e:
            self.statusBar().showMessage(f'Ошибка: {e.args[0]}')

    def save_db_as(self):
        db_name = QFileDialog.getSaveFileName(self, "Сохранить базу данных sqlite как", '', "*.sqlite")[0]
        with open(self.db_name, mode='rb') as db_cur:
            with open(db_name, mode='wb') as out_file:
                out_file.write(db_cur.read())

    def init_table_widget_for_db_table(self, table_widget, name):
        try:
            # Получим результат запроса,
            cursor = self.db_connection.cursor()
            res = cursor.execute(f"SELECT * FROM {name}").fetchall()

            # Если запись не нашлась, то не будем ничего делать
            if not res:
                self.statusBar().showMessage('Ничего не нашлось')
                return
            # Заполнили размеры таблицы
            table_widget.setRowCount(len(res))
            table_widget.setColumnCount(len(res[0]))
            # Устанавливаем заголовки таблицы
            titles = [description[0] for description in cursor.description]
            table_widget.setHorizontalHeaderLabels(titles)
            # Заполнили таблицу полученными элементами
            for i, elem in enumerate(res):
                for j, val in enumerate(elem):
                    str_val = str(val)
                    if str_val.startswith("b'"):
                        button = QPushButton('Открыть файл')
                        file_type = magic.from_buffer(val)
                        # TODO: Add opening image and txt file
                        table_widget.setCellWidget(i, j, button)
                    else:
                        table_widget.setItem(i, j, QTableWidgetItem(str_val))

            table_widget.resizeColumnsToContents()

            table_widget.itemChanged.connect(self.item_changed)

        except sqlite3.Error as e:
            self.statusBar().showMessage(f'Ошибка с бд: {e.args[0]}')
        except Exception as e:
            self.statusBar().showMessage(f'Ошибка: {e.args[0]}')

    def get_current_table_name(self):
        current_table_name = self.tables_tab_widget \
            .tabText(self.tables_tab_widget.currentIndex())

        # clear table name of modified state
        if current_table_name[-1] == "*":
            current_table_name = current_table_name[:-1]

        return current_table_name

    def get_id_of_element_at_row_and_column(self, item_row, item_column):
        table_widget = self.tables_tab_widget.currentWidget()
        column_id = -1
        for column_i in range(table_widget.columnCount()):
            column_text = table_widget.horizontalHeaderItem(column_i).text()
            if column_text == "id":
                column_id = column_i
                break
        if column_id == -1:
            raise Exception("Поля id не существует в таблице")

        return int(table_widget.item(item_row, column_id).text())

    def item_changed(self, item):
        try:
            current_table_name = self.get_current_table_name()
            # Если значение в ячейке было изменено,
            # то в словарь записывается пара: название поля, новое значение
            table_widget = self.tables_tab_widget.currentWidget()
            prop = table_widget.horizontalHeaderItem(item.column()).text()

            id = self.get_id_of_element_at_row_and_column(item.row(), item.column())

            modified_data = {"property": prop, "text": item.text()}
            current_modif_table = self.modified_data_in_tables.get(current_table_name)
            if not current_modif_table.get(id, False):
                current_modif_table[id] = [modified_data]
            else:
                current_modif_table[id].append(modified_data)

            self.tables_tab_widget.setTabText(
                self.tables_tab_widget.currentIndex(), f"{current_table_name}*")
        except Exception as e:
            self.statusBar().showMessage(f'Ошибка: {e.args[0]}')

    def save_all_tables_changes(self):
        if self.modified_data_in_tables:
            indx_of_table = 0
            for table_name, value in self.modified_data_in_tables.items():
                if value:
                    cur = self.db_connection.cursor()
                    for id, changed_props in self.modified_data_in_tables[table_name].items():
                        que = f"UPDATE {table_name} SET\n"
                        que += ", ".join([f"{props['property']}='{props['text']}'" for props in changed_props])
                        que += f" WHERE id = {id}"
                        cur.execute(que)

                    self.db_connection.commit()
                    self.modified_data_in_tables[table_name].clear()
                self.tables_tab_widget.setTabText(
                        indx_of_table, table_name)
                indx_of_table += 1

    def save_current_table_changes(self):
        current_table_name = self.get_current_table_name()
        if self.modified_data_in_tables[current_table_name]:
            cur = self.db_connection.cursor()
            for id, changed_props in self.modified_data_in_tables[current_table_name].items():
                que = f"UPDATE {current_table_name} SET\n"
                que += ", ".join([f"'{props['property']}'='{props['text']}'" for props in changed_props])
                que += f" WHERE id = '{id}'"
                print(que)
                cur.execute(que)

            self.db_connection.commit()
            self.modified_data_in_tables[current_table_name].clear()
            self.tables_tab_widget.setTabText(
                    self.tables_tab_widget.currentIndex(), current_table_name)

    def delete_elem(self):
        try:
            # Получаем список элементов без повторов
            table_widget = self.tables_tab_widget.currentWidget()
            rows = list(set([i.row() for i in table_widget.selectedItems()]))
            if not rows:
                raise Exception('Не выделены никакие строки')
            ids = [table_widget.item(i, 0).text() for i in rows]
            # Спрашиваем у пользователя подтверждение на удаление элементов
            valid = QMessageBox.question(
                self, '', "Действительно удалить элементы с id " + ",".join(ids),
                QMessageBox.Yes, QMessageBox.No)
            # Если пользователь ответил утвердительно, удаляем элементы.
            # Не забываем зафиксировать изменения
            if valid == QMessageBox.Yes:
                cur = self.db_connection.cursor()
                current_table_name = self.get_current_table_name()

                cur.execute(f"DELETE FROM {current_table_name} WHERE id IN (" + ", ".join(
                    '?' * len(ids)) + ")", ids)
                self.db_connection.commit()

                for id in ids:
                    self.modified_data_in_tables[current_table_name].pop(int(id), None)

                self.init_table_widget_for_db_table(table_widget, current_table_name)

                self.modified_data_in_tables[current_table_name].clear()
                self.tables_tab_widget.setTabText(
                    self.tables_tab_widget.currentIndex(), current_table_name)
        except sqlite3.Error as e:
            self.statusBar().showMessage(f'Ошибка с бд: {e.args[0]}')
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
