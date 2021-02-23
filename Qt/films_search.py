import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QPlainTextEdit, QMessageBox, QComboBox, QLineEdit
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Поиск по фильмам")
        uic.loadUi("films_search.ui", self)
        self.con = sqlite3.connect("films_db.sqlite")
        self.cbox.addItems(["Год выпуска", "Название", "Продолжительность"])
        self.search_btn.clicked.connect(self.search)

    def search(self):
        self.id.setText("")
        self.name.setText("")
        self.year.setText("")
        self.genre.setText("")
        self.duration.setText("")
        cur = self.con.cursor()
        d = {"Год выпуска": "year", "Название": "title", "Продолжительность": "duration"}

        try:
            self.status_lbl.setText("")
            inp = self.input.text()
            result = cur.execute(f"""
                SELECT * FROM Films where {d[self.cbox.currentText()]} = ?
            """, (inp,)).fetchmany(1)

            if not result:
                self.status_lbl.setText("Ничео не найдено!")
                return

            _id, _name, _year, _genre, _duration = result[0]
            g = cur.execute("""
                            SELECT title FROM genres where id = ?
                        """, (_genre,)).fetchmany(1)[0]
            _genre = g[0]
            self.id.setText(str(_id))
            self.name.setText(_name)
            self.year.setText(str(_year))
            self.genre.setText(str(_genre))
            self.duration.setText(str(_duration))
        except:
            self.status_lbl.setText("Введите корректные данные!")

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())

# Поиск по фильмам
# # Created by Sergey Yaksanov at 15.11.2020
# Copyright © 2020 Yakser. All rights reserved.
