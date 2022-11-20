import sys
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtMultimedia
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QInputDialog
import re
import time


class BadSymbol(Exception):
    pass


class LenError(Exception):
    pass


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Piano.ui', self)
        self.notes = {'ДО': 0, 'РЕ': 1, 'МИ': 2, 'ФА': 3,
                      'СОЛЬ': 4, 'ЛЯ': 5, 'СИ': 6, 'ДО*': 7} #словать для определения строки для записи конкретной ноты
        self.isprint = True #проверка на возможность записи
        self.long = False #отвечает за длительность ноты: True - длинная, False - короткая
        self.column = 1 #номер столбца в котором ведётся запись нот
        self.quite_max = 10 #максимальное количество столбцов без нот при воспроизведении
        self.speed = 0.5 #скорсть воспроизведения
        #подключение всего интерфейса программы
        self.noteEdit.appendPlainText(((('-' * 104) + '\n') * 8)) #первичное заполнение поля с нотами
        self.Button_1.clicked.connect(self.load_1)
        self.Button_2.clicked.connect(self.load_2)
        self.Button_3.clicked.connect(self.load_3)
        self.Button_4.clicked.connect(self.load_4)
        self.Button_5.clicked.connect(self.load_5)
        self.Button_6.clicked.connect(self.load_6)
        self.Button_7.clicked.connect(self.load_7)
        self.Button_8.clicked.connect(self.load_8)
        self.pedal.pressed.connect(self.pressed)
        self.pedal.released.connect(self.released)
        self.ButtonRecording.clicked.connect(self.recording)
        self.ButtonDeliteNote.clicked.connect(self.delitenote)
        self.ButtonClear.clicked.connect(self.clean)
        self.ButtonPlaying.clicked.connect(self.playing)
        self.NextColumn.clicked.connect(self.next)
        self.PreviousColumn.clicked.connect(self.previous)
        self.ButtonOpen.clicked.connect(self.open)
        self.ButtonSave.clicked.connect(self.save)
        self.ButtonLongEnd.clicked.connect(self.quite)
        self.ButtonSpeed.clicked.connect(self.speeds)
        self.pixmap = QPixmap('info.png')
        self.InfoLabel.setPixmap(self.pixmap)
        self.ColumnNumber.setText(str(1))
        self.noteEdit.setReadOnly(True)

    #8 клавишь фортепиано
    def load_1(self):
        if self.long: #проверка на длительность ноты
            media1 = QtCore.QUrl.fromLocalFile(f'long_note\do.mp3') #подключение файла с мелодией
            content1 = QtMultimedia.QMediaContent(media1)
            if self.isprint: #проверка на возможность записи
                self.writing('ДО', True)
        else:
            media1 = QtCore.QUrl.fromLocalFile(f'note\do.mp3')
            content1 = QtMultimedia.QMediaContent(media1)
            if self.isprint:
                self.writing('ДО', False)
        self.player1 = QtMultimedia.QMediaPlayer()
        self.player1.setMedia(content1)
        self.player1.play() #воспроизведение ноты

    def load_2(self):
        if self.long:
            media2 = QtCore.QUrl.fromLocalFile(f'long_note\pe.mp3')
            content2 = QtMultimedia.QMediaContent(media2)
            if self.isprint:
                self.writing('РЕ', True)
        else:
            media2 = QtCore.QUrl.fromLocalFile(f'note\pe.mp3')
            content2 = QtMultimedia.QMediaContent(media2)
            if self.isprint:
                self.writing('РЕ', False)
        self.player2 = QtMultimedia.QMediaPlayer()
        self.player2.setMedia(content2)
        self.player2.play()

    def load_3(self):
        if self.long:
            media3 = QtCore.QUrl.fromLocalFile(f'long_note\mi.mp3')
            content3 = QtMultimedia.QMediaContent(media3)
            if self.isprint:
                self.writing('МИ', True)
        else:
            media3 = QtCore.QUrl.fromLocalFile(f'note\mi.mp3')
            content3 = QtMultimedia.QMediaContent(media3)
            if self.isprint:
                self.writing('МИ', False)
        self.player3 = QtMultimedia.QMediaPlayer()
        self.player3.setMedia(content3)
        self.player3.play()

    def load_4(self):
        if self.long:
            media4 = QtCore.QUrl.fromLocalFile(f'long_note\Fa.mp3')
            content4 = QtMultimedia.QMediaContent(media4)
            if self.isprint:
                self.writing('ФА', True)
        else:
            media4 = QtCore.QUrl.fromLocalFile(f'note\Fa.mp3')
            content4 = QtMultimedia.QMediaContent(media4)
            if self.isprint:
                self.writing('ФА', False)
        self.player4 = QtMultimedia.QMediaPlayer()
        self.player4.setMedia(content4)
        self.player4.play()

    def load_5(self):
        if self.long:
            media5 = QtCore.QUrl.fromLocalFile(f'long_note\sol.mp3')
            content5 = QtMultimedia.QMediaContent(media5)
            if self.isprint:
                self.writing('СОЛЬ', True)
        else:
            media5 = QtCore.QUrl.fromLocalFile(f'note\sol.mp3')
            content5 = QtMultimedia.QMediaContent(media5)
            if self.isprint:
                self.writing('СОЛЬ', False)
        self.player5 = QtMultimedia.QMediaPlayer()
        self.player5.setMedia(content5)
        self.player5.play()

    def load_6(self):
        if self.long:
            media6 = QtCore.QUrl.fromLocalFile(f'long_note\la.mp3')
            content6 = QtMultimedia.QMediaContent(media6)
            if self.isprint:
                self.writing('ЛЯ', True)
        else:
            media6 = QtCore.QUrl.fromLocalFile(f'note\la.mp3')
            content6 = QtMultimedia.QMediaContent(media6)
            if self.isprint:
                self.writing('ЛЯ', False)
        self.player6 = QtMultimedia.QMediaPlayer()
        self.player6.setMedia(content6)
        self.player6.play()

    def load_7(self):
        if self.long:
            media7 = QtCore.QUrl.fromLocalFile(f'long_note\si.mp3')
            content7 = QtMultimedia.QMediaContent(media7)
            if self.isprint:
                self.writing('СИ', True)
        else:
            media7 = QtCore.QUrl.fromLocalFile(f'note\si.mp3')
            content7 = QtMultimedia.QMediaContent(media7)
            if self.isprint:
                self.writing('СИ', False)
        self.player7 = QtMultimedia.QMediaPlayer()
        self.player7.setMedia(content7)
        self.player7.play()

    def load_8(self):
        if self.long:
            media8 = QtCore.QUrl.fromLocalFile(f'long_note\do2.mp3')
            content8 = QtMultimedia.QMediaContent(media8)
            if self.isprint:
                self.writing('ДО*', True)
        else:
            media8 = QtCore.QUrl.fromLocalFile(f'note\do2.mp3')
            content8 = QtMultimedia.QMediaContent(media8)
            if self.isprint:
                self.writing('ДО*', False)
        self.player8 = QtMultimedia.QMediaPlayer()
        self.player8.setMedia(content8)
        self.player8.play()

    #отслеживание нажатий клавиатуры
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_E:
            self.load_1()
        if event.key() == Qt.Key_R:
            self.load_2()
        if event.key() == Qt.Key_T:
            self.load_3()
        if event.key() == Qt.Key_Y:
            self.load_4()
        if event.key() == Qt.Key_U:
            self.load_5()
        if event.key() == Qt.Key_I:
            self.load_6()
        if event.key() == Qt.Key_O:
            self.load_7()
        if event.key() == Qt.Key_P:
            self.load_8()
        if event.key() == Qt.Key_Z:
            self.pressed()
        if event.key() == Qt.Key_N:
            self.next()
        if event.key() == Qt.Key_B:
            self.previous()

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Z:
            self.released()

    #удаление одной ноты
    def delitenote(self):
        name, ok_pressed = QInputDialog.getText(self, "Удаление ноты",
                                                f"Какую ноту в столбце {self.column} вы хотите удалить?")
        if ok_pressed:
            notes_edit = self.noteEdit.toPlainText().split('\n') #загружаем список нот
            clear_note = list(notes_edit[self.notes[name.upper()]]) #через словарь определяем в какой строке находится нужная нота
            clear_note[self.column - 1] = '-' #заменяем ноту на -
            notes_edit[self.notes[name.upper()]] = ''.join(clear_note)
            self.noteEdit.clear()
            for i in range(8): #выгружаем ноты обратно
                self.noteEdit.appendPlainText(notes_edit[i])

    #очистка поля для записи нот
    def clean(self):
        valid = QMessageBox.question(self, 'Clean', "Вы уверены? Весть несохранённый прогресс будет потерян.",
                                     QMessageBox.Yes, QMessageBox.No) #диалоговое окно с подтверждением
        if valid == QMessageBox.Yes:
            self.noteEdit.clear()
            self.noteEdit.appendPlainText(((('-' * 104) + '\n') * 8))

    #включение/выключение записи нот
    def recording(self):
        if self.isprint:
            self.isprint = False
        else:
            self.isprint = True
        self.ButtonRecording.setText(f'Запись {"включена" if self.isprint else "выключена"}')

    #следующие 2 функции отвечают за длительность нот
    def pressed(self):
        self.long = True

    def released(self):
        self.long = False

    #следующие 2 функции отвечают за выбор столбца для записи нот
    def next(self):
        if self.column < 104:
            self.column += 1
            self.ColumnNumber.setText(str(self.column))

    def previous(self):
        if self.column != 1:
            self.column -= 1
            self.ColumnNumber.setText(str(self.column))

    #установка скорости воспроизведения
    def speeds(self):
        speed, ok_pressed = QInputDialog.getInt(self, "Скорость воспроизведения", "Укажите скорость воспроизведения",
                                                int(self.speed * 10), 1, 25, 1) #т.к. нельзя float * 10
        if ok_pressed:
            self.speed = speed / 10

    #функция для установки предела тишины
    def quite(self):
        value, ok_pressed = QInputDialog.getInt(self, "Предел тишины", "Укажите предел тишины",
                                                self.quite_max, 5, 103, 1)
        if ok_pressed:
            self.quite_max = value

    #функция для записи нот
    def writing(self, who, is_long):
        #в переменную who передаётся имя ноты, которую нужно записать, а в is_long - является ли нота длинной
        which_note = self.notes[who] #через словать определяем нужную строку для записи ноты по её значению
        notes_edit = self.noteEdit.toPlainText().split('\n') #список строчек с нотами
        new_note = list(notes_edit[which_note])
        if is_long: #в зависимости от длительности ноты в поле с нотами записывается ! или |
            new_note[self.column - 1] = '|'
        else:
            new_note[self.column - 1] = '!'
        notes_edit[which_note] = ''.join(new_note)
        self.noteEdit.clear()
        for i in range(8):
            self.noteEdit.appendPlainText(notes_edit[i])

    #функция для открытия файла
    def open(self):
        try:
            with open(self.Filename.text()) as f:
                file = f.readlines()
                right_string = "^[|!-]+$" #допустимые символы
                pattern = re.compile(right_string)
                if len(file) != 8: #проверка на длинну текста
                    raise LenError
                for i in file:
                    if pattern.search(i) == None: #проверка на допустимые символы
                        raise BadSymbol
                    if len(i.replace('\n', '')) > 104:
                        raise LenError
                self.noteEdit.clear()
                for i in file: #выгрузка текста если все условия выполнены
                    #если длина строки меньше 104, то недостающие - добавятся автоматически
                    self.noteEdit.appendPlainText(i.replace('\n', '') + '-' * (104 - len(i.replace('\n', ''))))
        #исключения с диалоговыми окнами
        except BadSymbol:
            QMessageBox.question(self, 'Неверный формат',
                                 "Файл содержит недопустимые символы(Файл должен содержать только |, ! и -).")
        except LenError:
            QMessageBox.question(self, 'Неверный формат',
                                 "Файл содержит недопустимое кол-во строк или длина одной из строк > 104")
        except:
            QMessageBox.question(self, 'Файл не найден',
                                 "Неверное имя или формат файла(.txt).")

    #функция для сохранения нот в файл
    def save(self):
        try:
            if self.Filename.text() == '': #проверка на пустоту строки с именем файла
                raise BadSymbol
            if self.Filename.text()[-4:] != '.txt': #проверка на наличие расширения
                raise TypeError
            else:
                with open(self.Filename.text(), mode='w') as save:
                    for i in self.noteEdit.toPlainText().split('\n'):
                        if i != '':
                            save.write(i + '\n')
        except TypeError: #ошибка наличия расширения файла
            type_error = QMessageBox.question(self, 'TypeError', 'У файла отсутствует расширение .txt. Поставить его?',
                                         QMessageBox.Yes, QMessageBox.No)
            if type_error == QMessageBox.Yes: #если пользователь согласится, то расширение поставится автоматически
                with open(f'{self.Filename.text()}.txt', mode='w') as save:
                    for i in self.noteEdit.toPlainText().split('\n'):
                        if i != '':
                            save.write(i + '\n')
        except BadSymbol:
            QMessageBox.question(self, 'Неверное имя', "Введите имя файла")

    #функция для проигрывания мелодии
    def playing(self):
        try:
            melody = self.noteEdit.toPlainText().split('\n') #получает список нот
            long_end = 0 #кол-во пустых столбцов
            if melody[-1] == '' or melody[-1] == '\n':
                melody.pop(-1)
            if self.isprint: #отключаем запись нот (вызываем функцию т.к. иначе надпись на кнопке не изменится)
                self.recording()
            for i in range(104):
                # проверка и отслеживание предела тишины
                if long_end == self.quite_max:
                    raise BadSymbol
                elif melody[0][i] == melody[1][i] == melody[2][i] == melody[3][i] == melody[4][i] and\
                        melody[4][i] == melody[5][i] == melody[6][i] == melody[7][i]:
                    long_end += 1
                else:
                    long_end = 0
                #воспроизведение нот
                for j in range(8):
                    if melody[j][i] != '-':
                        if melody[j][i] == '|':
                            self.pressed()
                        if j == 0:
                            self.load_1()
                        if j == 1:
                            self.load_2()
                        if j == 2:
                            self.load_3()
                        if j == 3:
                            self.load_4()
                        if j == 4:
                            self.load_5()
                        if j == 5:
                            self.load_6()
                        if j == 6:
                            self.load_7()
                        if j == 7:
                            self.load_8()
                        self.released()
                time.sleep(self.speed) #время ожидания между нотами
        except BadSymbol: #превышение лимита тишины
            QMessageBox.question(self, 'Конец', "Воспроизведение завершилось т.к. тишина была слишком долгой)")


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
