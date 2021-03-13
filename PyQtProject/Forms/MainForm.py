from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QTabWidget, QGridLayout, QTableWidget, \
    QTableWidgetItem, QPushButton

from PyQtProject.Forms.ImageReplaceForm import ImageReplaceForm
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
            name = QFileDialog.getOpenFileName(self, "Выберите базу данных sqlite", '', "*.sqlite")[0]
            if name:
                self.db_name = name
                if self.db_connection:
                    self.db_connection.close()
                self.db_connection = sqlite3.connect(self.db_name)

                cur = self.db_connection.cursor()
                cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables_names = [el[0] for el in cur.fetchall()]
                if not tables_names:
                    raise Exception("Нет таблиц в базе данных")

                if self.notLoadDbLabel:
                    self.notLoadDbLabel.deleteLater()
                    self.notLoadDbLabel = None

                if not self.tables_tab_widget:
                    self.tables_tab_widget = QTabWidget(self)
                    self.gridLayout.addWidget(self.tables_tab_widget)
                else:
                    self.tables_tab_widget.clear()

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
        try:
            db_name = QFileDialog.getSaveFileName(self, "Сохранить базу данных sqlite как", '', "*.sqlite")[0]
            with open(self.db_name, mode='rb') as db_cur:
                with open(db_name, mode='wb') as out_file:
                    out_file.write(db_cur.read())
        except Exception as e:
            self.statusBar().showMessage(f'Ошибка: {e.args[0]}')

    def init_table_widget_for_db_table(self, table_widget, name):
        try:
            # Получим результат запроса
            cursor = self.db_connection.cursor()
            res = cursor.execute(f"SELECT * FROM {name}").fetchall()

            # Если запись не нашлась, то не будем ничего делать
            if not res:
                self.statusBar().showMessage('Ничего не нашлось')
                return
            table_widget.clear()
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
                    if str_val.startswith("b'") and type(val) is bytes:
                        button = QPushButton('Открыть файл')
                        file_type = magic.from_buffer(val).split()[0].lower()
                        image_file_types = ['jpeg', 'jpg']
                        if file_type in image_file_types:
                            button.imageBytes = val
                            id_el = self.get_id_of_element_at_row_and_column(i, j)
                            prop = titles[j]

                            button.clicked.connect(self.open_image_edit_form(id_el, prop,
                                                                             button.imageBytes, button))
                            table_widget.setCellWidget(i, j, button)
                    else:
                        table_widget.setItem(i, j, QTableWidgetItem(str_val))

            table_widget.resizeColumnsToContents()

            table_widget.itemChanged.connect(self.item_changed)

        except sqlite3.Error as e:
            self.statusBar().showMessage(f'Ошибка с бд: {e.args[0]}')
        except Exception as e:
            self.statusBar().showMessage(f'Ошибка: {e.args[0]}')

    def open_image_edit_form(self, id_el, prop, image_data, button):
        def callback():
            try:
                self.imageEditForm = ImageReplaceForm(id_el, prop, image_data)
                self.imageEditForm.show()
                self.imageEditForm.replaceImageButton.clicked.connect(lambda: self.save_image(button))
            except Exception as e:
                self.statusBar().showMessage(f'Ошибка: {e.args[0]}')

        return callback

    def save_image(self, button):
        try:
            if not self.imageEditForm.new_image_name:
                raise Exception("Не отключена кнопка сохранения картинки")
            with open(self.imageEditForm.new_image_name, mode='rb') as new_image:
                blob_data = new_image.read()
                element_id = self.imageEditForm.element_id
                element_property = self.imageEditForm.element_property
                self.imageEditForm.close()

                current_table_name = self.get_current_table_name()
                cur = self.db_connection.cursor()
                cur.execute(f"""UPDATE {current_table_name} 
                        SET '{element_property}'= ? WHERE id = {element_id}""", (blob_data,)).fetchone()

                self.db_connection.commit()
                button.imageBytes = blob_data
                button.clicked.connect(self.open_image_edit_form(element_id, element_property,
                                                                 button.imageBytes, button))

        except Exception as e:
            self.statusBar().showMessage(f'Ошибка: {e.args[0]}')

    def get_current_table_name(self):
        try:
            current_table_name = self.tables_tab_widget \
                .tabText(self.tables_tab_widget.currentIndex())

            # clear table name of modified state
            if current_table_name[-1] == "*":
                current_table_name = current_table_name[:-1]

            return current_table_name
        except Exception as e:
            self.statusBar().showMessage(f'Ошибка: {e.args[0]}')

    def get_id_of_element_at_row_and_column(self, item_row, item_column):
        try:
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
        except Exception as e:
            self.statusBar().showMessage(f'Ошибка: {e.args[0]}')

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
        try:
            if self.modified_data_in_tables and self.tables_tab_widget:
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
            else:
                raise Exception('Нет таблицы')
        except Exception as e:
            self.statusBar().showMessage(f'Ошибка: {e.args[0]}')

    def save_current_table_changes(self):
        try:
            if self.modified_data_in_tables and self.tables_tab_widget:
                current_table_name = self.get_current_table_name()
                if current_table_name and self.modified_data_in_tables[current_table_name]:
                    cur = self.db_connection.cursor()
                    for id, changed_props in self.modified_data_in_tables[current_table_name].items():
                        que = f"UPDATE {current_table_name} SET\n"
                        que += ", ".join([f"'{props['property']}'='{props['text']}'" for props in changed_props])
                        que += f" WHERE id = '{id}'"
                        cur.execute(que)

                    self.db_connection.commit()
                    self.modified_data_in_tables[current_table_name].clear()
                    self.tables_tab_widget.setTabText(
                        self.tables_tab_widget.currentIndex(), current_table_name)
            else:
                raise Exception('Нет таблицы')
        except Exception as e:
            self.statusBar().showMessage(f'Ошибка: {e.args[0]}')

    def delete_elem(self):
        try:
            if self.tables_tab_widget:
                table_widget = self.tables_tab_widget.currentWidget()
                rows = list(set([i.row() for i in table_widget.selectedItems()]))
                if not rows:
                    raise Exception('Не выделены никакие строки')
                ids = [table_widget.item(i, 0).text() for i in rows]

                valid = QMessageBox.question(
                    self, '', "Действительно удалить элементы с id " + ",".join(ids),
                    QMessageBox.Yes, QMessageBox.No)

                if valid == QMessageBox.Yes:
                    cur = self.db_connection.cursor()
                    current_table_name = self.get_current_table_name()

                    cur.execute(f"DELETE FROM {current_table_name} WHERE id IN (" + ", ".join(
                        '?' * len(ids)) + ")", ids)
                    self.db_connection.commit()

                    self.init_table_widget_for_db_table(table_widget, current_table_name)

                    self.modified_data_in_tables[current_table_name].clear()
                    self.tables_tab_widget.setTabText(
                        self.tables_tab_widget.currentIndex(), current_table_name)
            else:
                raise Exception('Нет таблицы')
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
