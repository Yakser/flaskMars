import sys
from PyQt5.QtWidgets import QApplication, QWidget, \
    QMainWindow, QLineEdit, QPushButton, QLabel, QLCDNumber, \
    QCheckBox
from PyQt5 import uic  # Импортируем uic


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('calc.ui', self)

        for i in range(10):
            eval(f"self.btn{i}.clicked.connect(self.num)")

        self.btn_clear.clicked.connect(self.clear)
        self.btn_eq.clicked.connect(self.eq)

        self.btn_plus.clicked.connect(self.plus)
        self.btn_minus.clicked.connect(self.minus)
        self.btn_mult.clicked.connect(self.multiply)
        self.btn_div.clicked.connect(self.division)
        self.btn_dot.clicked.connect(self.dot)
        self.ext = ""
        self.eq_pressed = False
        self.display_num = ""

    def num(self):
        self.if_eq_pressed()
        self.clear_ans()
        self.ext += f"{self.sender().text()}"
        self.display_num += str(self.sender().text())
        self.table.display(self.display_num)

    def plus(self):

        self.if_eq_pressed()
        self.clear_ans()
        try:
            self.table.display(self.display_num)
            self.display_num = ""
            self.ext += "+"
        except:
            self.clear_ext()
            self.table.display("Error!")

    def minus(self):

        self.if_eq_pressed()
        self.clear_ans()
        try:
            self.table.display(self.display_num)
            self.display_num = ""
            self.ext += '-'
        except:
            self.clear_ext()
            self.table.display("Error!")

    def multiply(self):

        self.if_eq_pressed()
        self.clear_ans()
        try:
            self.table.display(self.display_num)
            self.display_num = ""
            self.ext += "*"
        except:
            self.clear_ext()
            self.table.display("Error!")

    def division(self):

        self.if_eq_pressed()
        self.clear_ans()
        try:
            self.table.display(self.display_num)
            self.display_num = ""
            self.ext += '/'
        except:
            self.clear_ext()
            self.table.display("Error!")

    def eq(self):
        self.display_num = ""
        self.if_eq_pressed()
        try:
            self.display_num = str(eval(self.ext))
            self.table.display(eval(self.ext))
            self.eq_pressed = True
        except:
            self.table.display("Error!")
        self.clear_ext()

    def reverse(self):

        self.if_eq_pressed()
        self.clear_ans()
        try:
            self.display_num = str(-eval(self.ext))
            self.table.display(self.display_num)
            self.ext = str(-eval(self.ext))
        except:
            self.clear_ext()
            self.table.display("Error!")

    def dot(self):

        self.if_eq_pressed()
        self.clear_ans()
        try:
            self.display_num += '.'
            self.ext += "."
        except:
            self.clear_ext()
            self.table.display("Error!")

    def create_btn(self, name, x, y):
        btn = QPushButton(name, self)
        btn.resize(50, 50)
        btn.move(x, y)
        return btn

    def clear(self):
        self.clear_ans()
        self.clear_ext()

    def delete(self):
        self.ext = str(self.ans.value())[:-1]
        self.clear_ans()

    def clear_ans(self):
        self.table.display("")

    def clear_ext(self):
        self.ext = ""

    def if_eq_pressed(self):
        if self.eq_pressed:
            self.eq_pressed = False
            self.ext = str(self.table.value())


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
