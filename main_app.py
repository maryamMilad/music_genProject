from colab_notebook import *
from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui, QtWidgets
from functools import partial
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QTextCursor
import json


def write_list_to_file(my_list, filename):
    with open(filename, 'w') as f:
        json.dump(my_list, f)


# Define a custom output stream that writes to the QTextEdit widget
class OutputWrapper:
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        cursor = self.widget.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.widget.ensureCursorVisible()
        QApplication.processEvents()

    def flush(self):
        pass


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('GUI_Music.ui', self)

        # editing all event handlers for all buttons
        self.browse_buttons = []
        self.file_path_views = []

        self.clear_buttons = []
        self.train_buttons = []
        self.gen_buttons = []
        self.logs = []

        for i in range(1, 4):
            browse_button = self.findChild(QPushButton, f'browse_btn_{i}')
            line_edit = self.findChild(QLineEdit, f'file_path_view_{i}')

            clear_button = self.findChild(QPushButton, f'clear_btn_{i}')
            train_button = self.findChild(QPushButton, f'train_btn_{i}')
            gen_button = self.findChild(QPushButton, f'gen_btn_{i}')
            log_screen = self.findChild(QTextEdit, f'logs_{i}')

            self.browse_buttons.append(browse_button)
            self.file_path_views.append(line_edit)

            self.clear_buttons.append(clear_button)
            self.train_buttons.append(train_button)
            self.gen_buttons.append(gen_button)
            self.logs.append(log_screen)

            self.browse_buttons[i-1].clicked.connect(partial(self.select_directory, i))
            self.gen_buttons[i - 1].clicked.connect(partial(self.gen_music, i))
            self.train_buttons[i - 1].clicked.connect(partial(self.train_music, i))
            self.clear_buttons[i-1].clicked.connect(self.clear_func)

        # show the window
        self.show()

    def select_directory(self, i):
        directory = QFileDialog.getExistingDirectory(self, 'Select Directory')

        if directory:
            print(directory)
            self.file_path_views[i-1].setText(f'{directory}')

        # Redirect output to the QTextEdit widget
        sys.stdout = OutputWrapper(self.logs[i-1])

    def gen_music(self, i):
        directory = self.file_path_views[i-1].text()
        print("Starting......")
        # sys.stdout.flush()
        if i == 1:
            generate_music(num_to_gen=100, music_path=directory, file_name="piano_generated_music", tool='piano')
            print("#### DONE Generating Music ####")
        elif i == 2:
            generate_music(num_to_gen=100, music_path=directory, file_name="drums_generated_music", tool='drums')
            print("#### DONE Generating Music ####")
        elif i == 3:
            generate_music(num_to_gen=100, music_path=directory, file_name="guitar_generated_music", tool='guitar')
            print("#### DONE Generating Music ####")
        else:
            print('Unknown Instrument!')

    def train_music(self, i):
        directory = self.file_path_views[i-1].text()
        print("Starting......")
        # sys.stdout.flush()
        if i == 1:
            loss_list = train_music_generator(directory, 'piano')
            write_list_to_file(loss_list, 'piano_loss_list.txt')
            print("#### DONE TRAINING ####")
        elif i == 2:
            loss_list = train_music_generator(directory, 'drums')
            write_list_to_file(loss_list, 'drums_loss_list.txt')
            print("#### DONE TRAINING ####")
        elif i == 3:
            loss_list = train_music_generator(directory, 'guitar')
            write_list_to_file(loss_list, 'guitar_loss_list.txt')
            print("#### DONE TRAINING ####")
        else:
            print('Unknown Instrument!')

    def clear_func(self):
        for i in range(len(self.file_path_views)):
            self.file_path_views[i - 1].clear()
            self.logs[i - 1].clear()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    app.exec_()