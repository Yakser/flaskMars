import sqlite3
import sys

from PyQt5 import QtCore
from PyQt5 import uic, QtMultimedia
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap, QIcon, QColor
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget, QInputDialog, \
    QGraphicsDropShadowEffect, QMessageBox, QListWidgetItem

from Main_styles import *


class MenuWidget(QWidget):  # Виджет окна с выбором плейлистов
    def __init__(self):
        super().__init__()
        uic.loadUi('menuUI.ui', self)
        # Добавление в список плейлистов, существующих по умолчанию
        self.playlists.addItem("Все треки")
        self.playlists.addItem("Понравившиеся")
        self.playlists.itemAt(0, 0).setSelected(True)  # Первый плейлист выбран по умолчанию

        self.playlists.setStyleSheet(PLAYLISTS_STYLES)
        self.setStyleSheet(PLAYLISTS_STYLES)

        self.close_menu_btn.setIcon(QIcon(QPixmap("icons/back.png")))
        self.close_menu_btn.setIconSize(QSize(25, 25))

        self.cur_playlist = "Все треки"


class TracksSelectionWidget(QWidget):  # Виджет для добавления треков в плейлисты
    def __init__(self):
        super().__init__()
        uic.loadUi('tracks-selectionUI.ui', self)
        self.setWindowTitle("Добавление аудио в плейлист")
        self.setStyleSheet(TRACKS_SELECTION_STYLES)
        self.tracks_list.setStyleSheet(TRACKS_SELECTION_LIST_STYLES)


class Main(QMainWindow):  # Основное окно
    def __init__(self):
        super().__init__()
        uic.loadUi('mainUI.ui', self)
        self.setWindowTitle('Я.Музычка')
        self.setWindowIcon(QIcon('icons/app-ico.png'))
        self.setup_player()  # Настройка QtMultimedia.QMediaPlayer()

        self.IS_PLAY = False
        self.menu_isopen = False
        self.DB_NAME = "Tracks.db"
        self.cur_ind = 0

        # установка обработчика событий на кнопки нижнего меню
        self.like_btn.installEventFilter(self)
        self.menu_btn.installEventFilter(self)
        self.add_new_track_btn.installEventFilter(self)
        self.delete_cur_track_btn.installEventFilter(self)

        # подключение функций к кнопка нижнего меню
        self.play_btn.clicked.connect(self.play_track)  # воспроизведение текущего трека
        self.next_btn.clicked.connect(self.next_track)  # переключение на следующий трек
        self.prev_btn.clicked.connect(self.prev_track)  # переключение на предыдущий трек
        self.like_btn.clicked.connect(self.like_track)

        self.add_new_track_btn.clicked.connect(self.add_new_track)  # add new track
        self.delete_cur_track_btn.clicked.connect(self.delete_cur_track)  # delete current track

        # настройка слайдера для регулировки громкости
        self.volume_slider.valueChanged.connect(self.change_volume)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setValue(10)  # установка громкости по умолчанию

        self.menu = MenuWidget()
        self.menu.close_menu_btn.clicked.connect(self.close_menu)  # функция открытия и закрытия меню с плейлистами

        self.stackedWidget.addWidget(self.menu)
        self.menu_btn.clicked.connect(self.open_menu)

        self.menu.close_menu_btn.installEventFilter(self)  # обработчик событий для отображения стилей при наведении
        self.menu.create_playlist_btn.clicked.connect(self.create_playlist)  # ф-я создания плейлистов
        self.cur_playlist = self.menu.cur_playlist
        self.menu.playlists.currentItemChanged.connect(self.change_playlist)  # ф-я переключения плейлистов

        self.tracks_selection = TracksSelectionWidget()
        self.tracks_selection.add_btn.clicked.connect(self.add_track_to_playlist)  # ф-я добавления треков в плейлист

        # словарь с названиями плейлистов и их именами в БД
        self.playlists = {
            "Все треки": "Tracks",
            "Понравившиеся": "Liked"
        }

        #  Получение имен таблиц БД и добавление их в список плейлистов self.menu.playlists
        con = sqlite3.connect(self.DB_NAME)
        cur = con.cursor()
        pl_names = cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()[3:]
        con.close()

        for playlist_name in pl_names:
            playlist_name = playlist_name[0]
            if playlist_name not in self.playlists:
                self.menu.playlists.addItem(playlist_name)
                self.playlists[playlist_name] = playlist_name

        self.apply_styles()  # Применение стилей
        self.connect_db()  # Подключение БД
        self.update_ui()  # Обновление интерфейса

    # настройка  QtMultimedia.QMediaPlayer для воспроизведения аудио
    def setup_player(self):
        self.mediaPlayer = QtMultimedia.QMediaPlayer(self)
        self._buffer = QtCore.QBuffer()
        self._buffer.close()
        self.mediaPlayer.setVolume(10)
        self.mediaPlayer.stateChanged.connect(self.is_media_ended)
        self.mediaPlayer: QMediaPlayer
        self.mediaPlayer.audioRoleChanged.connect(self.is_media_ended)

    #  Подключение БД
    def connect_db(self):
        con = sqlite3.connect(self.DB_NAME)
        cur = con.cursor()
        #  Список атрибутов всех треков текущего плейлиста (id, название трека, имя артиста..)
        self.tracks = cur.execute(f"""
            SELECT *
            FROM Tracks
            WHERE id in (SELECT id from {self.playlists[self.cur_playlist]} )
        """).fetchall()
        #  Список треков плейлиста 'Понравившиеся'
        self.liked_tracks = cur.execute("""
                            SELECT id
                            FROM Liked
                        """).fetchall()

        #  Список треков, не добавленных в текущий плейлист
        not_added_tracks = cur.execute(f"""
            SELECT *
            FROM Tracks
            WHERE id NOT in (SELECT id from {self.playlists[self.cur_playlist]})
            """).fetchall()
        con.close()
        # очистка списка не добавленных треков и обновление списка
        self.tracks_selection.tracks_list.clear()
        for id, artist, name, *args in not_added_tracks:
            item = self.create_checkbox_item()
            item.setText(artist + " - " + name)
            self.tracks_selection.tracks_list.addItem(item)

    # Обновление интерфейса
    def update_ui(self):

        if self.tracks:  # Если текущий плейлист не пустой

            self.cur_id, self.cur_artist_name, self.cur_track_name, \
            self.cur_song_avatar, self.cur_track = self.tracks[self.cur_ind]

            # Обновление надписей
            self.track_name.setText(self.cur_track_name)
            self.artist_name.setText(self.cur_artist_name)
            # Обновление кнопки лайка
            if (self.tracks[self.cur_ind][0],) in self.liked_tracks:
                self.like_btn.setIcon(QIcon(QPixmap("icons/liked.png")))
            else:
                self.like_btn.setIcon(QIcon(QPixmap("icons/unliked.png")))

            temp = open("temp", "wb")
            temp.write(self.cur_track)
            temp = open("temp", "rb")

            self._buffer.close()
            self._buffer.setData(temp.read())
            if self._buffer.open(QtCore.QIODevice.ReadOnly):
                self.mediaPlayer.setMedia(
                    QtMultimedia.QMediaContent(), self._buffer)

            self.song_avatar.setText("")
            # TODO обложка трека
            # self.song_avatar.setPixmap(QPixmap(self.cur_song_avatar))

        else:  # Если плейлист пуст
            self.setup_player()  # сброс медиа объекта в медиа плеере
            self.track_name.setText("Плейлист пуст :(")
            self.artist_name.setText("")
            self.like_btn.setIcon(QIcon(QPixmap("icons/unliked.png")))

    def is_media_ended(self):  # Если трек кончился или был переключен
        if self.IS_PLAY and self.mediaPlayer.state() == 0 and self.mediaPlayer.mediaStatus() == 7:
             self.next_track()  # переключение на следующий трек

    #  Применение стилей
    def apply_styles(self):
        self.setStyleSheet(MAIN_WINDOW_STYLES)
        # стили кнопок нижнего меню
        self.play_btn.setStyleSheet(DEFAULT_BTN_STYLES)
        self.next_btn.setStyleSheet(DEFAULT_BTN_STYLES)
        self.prev_btn.setStyleSheet(DEFAULT_BTN_STYLES)
        self.like_btn.setStyleSheet(LIKE_BTN_STYLES)
        self.volume_slider.setStyleSheet(DEFAULT_SLIDER_STYLES)

        # self.song_avatar.setStyleSheet(SONG_AVATAR_STYLES)
        # стили названия трека и имени артиста
        self.artist_name.setStyleSheet(ARTIST_NAME_STYLES)
        self.track_name.setStyleSheet(TRACK_NAME_STYLES)

        # Установка иконок
        self.like_btn.setIcon(QIcon(QPixmap("icons/unliked.png")))  # иконка не лайкнутого сердечка
        self.like_btn.setIconSize(QSize(40, 40))

        self.add_new_track_btn.setIcon(QIcon(QPixmap("icons/add.png")))  # иконка добавления трека
        self.add_new_track_btn.setIconSize(QSize(30, 30))

        self.delete_cur_track_btn.setIcon(QIcon(QPixmap("icons/delete.png")))  # иконка удаления трека
        self.delete_cur_track_btn.setIconSize(QSize(30, 30))

        self.menu_btn.setIcon(QIcon(QPixmap("icons/menu.png")))  # иконка меню
        self.menu_btn.setIconSize(QSize(40, 40))

        self.stackedWidget.setStyleSheet(STACKED_WIDGET_STYLES)
        self.page_3.setStyleSheet("""background:transparent""")  # прозрачный фон для StackedWidget в вернем меню

        # добавление теней
        shadow = [self.create_shadow() for _ in range(7)]

        self.add_new_track_btn.setGraphicsEffect(shadow[0])
        self.like_btn.setGraphicsEffect(shadow[1])
        self.play_btn.setGraphicsEffect(shadow[2])
        self.next_btn.setGraphicsEffect(shadow[3])
        self.prev_btn.setGraphicsEffect(shadow[4])
        self.menu_btn.setGraphicsEffect(shadow[5])
        self.delete_cur_track_btn.setGraphicsEffect(shadow[6])

    # Создание эффекта тени
    def create_shadow(self):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(4, 2)
        c = QColor(0, 0, 0)
        c.setAlpha(100)
        shadow.setColor(c)
        return shadow

    # Функция добавления новых треков
    def add_new_track(self):
        if self.cur_playlist == "Все треки":  # Добавление нового трека в БД
            fname = QFileDialog.getOpenFileName(self, 'Выбрать трек', '')[0]

            with open(fname, "rb") as track_bytes:
                track_bytes = track_bytes.read()
                artist_name = fname.split("/")[-1].split('.mp3')[0].split("-")[0]
                track_name = fname.split("/")[-1].split('.mp3')[0].split("-")[1]

                con = sqlite3.connect(self.DB_NAME)
                cur = con.cursor()
                args = (artist_name, track_name, track_bytes)

                cur.execute("""
                            INSERT INTO Tracks(artist_name, track_name, track)
                            VALUES(?,
                                ?,
                                ?)
                        """, args).fetchall()
                con.commit()
                con.close()

                self.connect_db()
        else:
            self.tracks_selection.show()  # Открытие меню для добавления треков в текущий плейлист

    #  Ф-я удалеения текущего трека из текущего плейлиста
    def delete_cur_track(self):
        con = sqlite3.connect(self.DB_NAME)
        cur = con.cursor()
        cur.execute(f"""
            DELETE FROM {self.playlists[self.cur_playlist]}
            where id = ?
         """, (self.cur_id,)).fetchall()
        con.commit()
        con.close()
        self.cur_ind = 0
        self.connect_db()
        self.update_ui()

    # Ф-я воспроизведения / паузы
    def play_track(self):

        if self.IS_PLAY:
            self.play_btn.setText("▶")
            self.IS_PLAY = False

            self.mediaPlayer.pause()
        else:
            self.play_btn.setText("| |")
            self.IS_PLAY = True
            self.mediaPlayer.play()

    # Переключение на следующий трек
    def next_track(self):

        self.cur_ind += 1
        if self.cur_ind >= len(self.tracks):
            self.cur_ind = 0

        self.update_ui()
        if self.IS_PLAY:
            self.mediaPlayer.play()

    # Переключение на предыдущий трек
    def prev_track(self):
        self.prev = True
        self.next = False
        self.cur_ind -= 1
        if self.cur_ind < 0:
            self.cur_ind = len(self.tracks) - 1
        self.update_ui()
        if self.IS_PLAY:
            self.mediaPlayer.play()

    # Лайк (добавление/удаление в плейлист "Понравившиеся")
    def like_track(self):
        con = sqlite3.connect(self.DB_NAME)
        cur = con.cursor()

        if (self.cur_id,) in self.liked_tracks:
            cur.execute("""
            DELETE from Liked
            where id = ?
            """, (self.cur_id,))
        else:
            cur.execute("""
                INSERT INTO Liked VALUES(?)
            """, (self.cur_id,))
        con.commit()

        self.liked_tracks = cur.execute("""
                            SELECT id
                            FROM Liked
                        """).fetchall()
        con.close()

        # Замена иконок
        if (self.cur_id,) in self.liked_tracks:
            self.like_btn.setIcon(QIcon(QPixmap("icons/liked.png")))
        else:
            self.like_btn.setIcon(QIcon(QPixmap("icons/unliked.png")))

        self.connect_db()
        

    # Обработчик событий для кнопок
    def eventFilter(self, obj, event):
        if obj is self.like_btn:  # Кнопка лайка

            if event.type() == QtCore.QEvent.HoverEnter:
                if (self.cur_id,) in self.liked_tracks:
                    self.like_btn.setIcon(QIcon(QPixmap("icons/H-liked.png")))
                else:
                    self.like_btn.setIcon(QIcon(QPixmap("icons/H-unliked.png")))

            elif event.type() == QtCore.QEvent.HoverLeave:
                if (self.cur_id,) in self.liked_tracks:
                    self.like_btn.setIcon(QIcon(QPixmap("icons/liked.png")))
                else:
                    self.like_btn.setIcon(QIcon(QPixmap("icons/unliked.png")))

        elif obj is self.add_new_track_btn:  # Кнопка добавления трека

            if event.type() == QtCore.QEvent.HoverEnter:
                self.add_new_track_btn.setIcon(QIcon(QPixmap("icons/H-add.png")))
            elif event.type() == QtCore.QEvent.HoverLeave:
                self.add_new_track_btn.setIcon(QIcon(QPixmap("icons/add.png")))

        elif obj is self.delete_cur_track_btn:  # Кнопка удаления трека

            if event.type() == QtCore.QEvent.HoverEnter:
                self.delete_cur_track_btn.setIcon(QIcon(QPixmap("icons/H-delete.png")))
            elif event.type() == QtCore.QEvent.HoverLeave:
                self.delete_cur_track_btn.setIcon(QIcon(QPixmap("icons/delete.png")))

        elif obj is self.menu_btn:  # Кнопка открытия меню

            if event.type() == QtCore.QEvent.HoverEnter:
                self.menu_btn.setIcon(QIcon(QPixmap("icons/H-menu.png")))
            elif event.type() == QtCore.QEvent.HoverLeave:
                self.menu_btn.setIcon(QIcon(QPixmap("icons/menu.png")))

        elif obj is self.menu.close_menu_btn:  # Кнопка закрытия меню
            if event.type() == QtCore.QEvent.HoverEnter:
                self.menu.close_menu_btn.setIcon(QIcon(QPixmap("icons/H-back.png")))
            elif event.type() == QtCore.QEvent.HoverLeave:
                self.menu.close_menu_btn.setIcon(QIcon(QPixmap("icons/back.png")))

        return super().eventFilter(obj, event)

    # Регулировка громкости
    def change_volume(self):
        self.mediaPlayer.setVolume(self.volume_slider.value())

    # Ф-я открывающая меню
    def open_menu(self):
        self.menu_isopen = True
        self.stackedWidget.setCurrentIndex(2)

    # Ф-я закрывающая меню
    def close_menu(self):
        self.menu_isopen = False
        self.stackedWidget.setCurrentIndex(0)

    # Переключение плейлиста
    def change_playlist(self):

        self.cur_ind = 0
        self.cur_playlist = self.menu.playlists.currentItem().text()
        self.play_btn.setText("▶")
        self.IS_PLAY = False  # Остановка воспроизведения

        self.connect_db()
        self.update_ui()

    # Создание нового плейлиста
    def create_playlist(self):
        playlist_name, ok_pressed = QInputDialog.getText(self, "Создание нового плейлиста",
                                                         "Введите название плейлиста:")
        if ok_pressed:
            # Преобразование названия плейлиста
            t = ""
            cap = 0
            for i in playlist_name:
                if i.isalpha():
                    t += i if cap else i.upper()
                    cap = 1
                else:
                    cap = 0
            playlist_name = "".join(t)

            if not playlist_name:
                QMessageBox.warning(self, "Внимание!", "Некорректное название плейлиста!")
            elif playlist_name in self.playlists:
                QMessageBox.warning(self, "Внимание!", "Плейлист с таким названием уже существует!")
            else:
                con = sqlite3.connect(self.DB_NAME)
                cur = con.cursor()
                cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS {playlist_name} (
                        id integer NOT NULL,
                        FOREIGN KEY (id) REFERENCES Tracks (id)
                );
                """)
                con.commit()
                con.close()
                self.menu.playlists.addItem(playlist_name)
                self.playlists[playlist_name] = playlist_name

    # Ф-я добавления треков в текущий плейлист
    def add_track_to_playlist(self):
        con = sqlite3.connect(self.DB_NAME)
        cur = con.cursor()

        # Не добавленные треки
        not_added_tracks = cur.execute(f"""
                    SELECT *
                    FROM Tracks
                    WHERE id NOT in (SELECT id from {self.playlists[self.cur_playlist]})
                    """).fetchall()

        # Треки, которые нужно добавить
        need_to_add = []
        for row in range(len(not_added_tracks)):
            it = self.tracks_selection.tracks_list.item(row)
            if it.checkState() == 2:
                artist, name = it.text().split(' - ')
                need_to_add.append((artist, name))

        # Добавление id треков в плейлист
        for id, artist, name, *args in not_added_tracks:
            if (artist, name) in need_to_add:
                cur.execute(f"""
                            INSERT INTO {self.playlists[self.cur_playlist]}(id)
                            VALUES(?)
                        """, (id,)).fetchall()
        con.commit()
        con.close()
        self.connect_db()
        self.update_ui()
        self.tracks_selection.hide()

    # Обработчик нажатий
    # Удаление текущего плейлиста
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete and self.menu_isopen:
            if self.menu.playlists.currentItem().text() in ["Все треки", "Понравившиеся"]:
                QMessageBox.warning(self, "Внимание!", "Нельзя удалить этот плейлист!")
            else:
                ok_pressed = QMessageBox.question(self, "Внимание!", "Вы точно хотите удалить плейлист?")
                if ok_pressed == QMessageBox.Yes:

                    if self.IS_PLAY:  # ставим на паузу перед удалением
                        self.play_track()

                    pl_name = self.menu.playlists.currentItem().text()
                    con = sqlite3.connect(self.DB_NAME)
                    cur = con.cursor()
                    cur.execute(f"""
                                DROP TABLE IF EXISTS {pl_name}
                             """).fetchall()
                    con.commit()
                    con.close()
                    self.menu.playlists.takeItem(self.menu.playlists.currentRow())
                    self.connect_db()
                    self.update_ui()

    # Создание чекбокса для списка плейлистов
    def create_checkbox_item(self):
        item = QListWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        item.setCheckState(QtCore.Qt.Unchecked)
        return item


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())

# "Я.Музычка"
# # Created by Sergey Yaksanov at 28.10.2020
# Copyright © 2020 Yakser. All rights reserved.
