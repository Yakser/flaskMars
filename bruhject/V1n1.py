from tkinter import Tk, Canvas
from math import cos, sin, pi, radians


def mnog(xa, ya, r, n):
    # рисуем правильный многоугольник с центром в xa, ya , r - радиус описанной окружности
    s = [[xa + r * cos(0), ya + r * sin(0)]]
    for i in range(4):
        xa1 = xa + r * cos(2 * pi / 4 * i)
        ya1 = ya + r * sin(2 * pi / 4 * i)
        cnv.create_line((xa1, ya1, *s[-1]))
        s.append([xa1, ya1])
        # cnv.create_oval(xa1 - 10, ya1 - 10, xa1 + 10, ya1 + 10)
    cnv.create_line((*s[0], *s[-1]))

    # cnv.create_polygon(s, fill='red', outline='black')
    cnv.update()
    if n > 0:
        r1 = 1.2 * r
        r = r * 0.8
        xa1 = xa + r1 * cos(2 * pi / 4 * 0)
        ya1 = ya + r1 * sin(2 * pi / 4 * 0)
        mnog(xa1, ya1, r, n - 1)


root = Tk()
cnv = Canvas(master=root, width=800, height=800, bg='white')
cnv.pack()
x1, y1 = 400, 400
mnog(x1, y1, 50, 2)
root.mainloop()
