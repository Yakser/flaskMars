import sys
from PyQt5.QtWidgets import QApplication, QWidget, \
    QMainWindow, QLineEdit, QPushButton, QLabel, QLCDNumber, \
    QCheckBox, QDoubleSpinBox, QListWidget
from PyQt5 import uic  # Импортируем uic


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('shuffle.ui', self)
        self.setWindowTitle("Перемешивание")
        self.load_btn.clicked.connect(self.load_strings)

    def load_strings(self):

        try:
            with open("input.txt", encoding="utf-8") as f:
                text = f.read().split('\n')
                self.output_list.clear()
                [self.output_list.addItem(i) for i in text[::2]]
                [self.output_list.addItem(i) for i in text[1::2]]
                with open("input.txt", "w", encoding="utf-8") as wf:
                    wf.write("\n".join(text[::2]) + "\n" + "\n".join(text[1::2]))

        except FileNotFoundError:
            pass


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())


# shuffle
# # Created by Sergey Yaksanov at 27.10.2020
# Copyright © 2020 Yakser. All rights reserved.


