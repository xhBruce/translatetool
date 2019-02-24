# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5.QtGui import QIcon

import googletrans
from image import images_rc

import task


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.initUi()
        self.show()

    def initUi(self):
        icon = QIcon(':/icon.png')
        self.setWindowIcon(icon)
        self.resize(800, 600)

        mainLayout = QWidget()

        label = QtWidgets.QLabel("文字翻译")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        label.setFont(font)

        languages = googletrans.LANGUAGES.copy()
        languages['zh-cn'] = '中文(简体)'
        languages['zh-tw'] = '中文(繁体)'
        self.langcodes = dict(map(reversed, languages.items()))
        self.langlist = [k.capitalize() for k in self.langcodes.keys()]

        horizontalLayout = QtWidgets.QHBoxLayout()
        self.srcComboBox = self.createComboBox('English')
        self.swapButton = QtWidgets.QPushButton()
        self.swapButton.setStyleSheet("QPushButton{border-image: url(:/swap.png);width:40px;height:40px}")
        self.swapButton.clicked.connect(self.swapCombBox)
        self.dstComboBox = self.createComboBox('中文(简体)')
        horizontalLayout.addWidget(self.srcComboBox)
        horizontalLayout.addWidget(self.swapButton)
        horizontalLayout.addWidget(self.dstComboBox)

        self.fanyiButton = QtWidgets.QPushButton("&翻译")
        self.fanyiButton.clicked.connect(self.translate)

        self.textEdit = QtWidgets.QTextEdit()
        self.textEdit_2 = QtWidgets.QTextEdit()
        self.textEdit_2.setReadOnly(True)

        gridLayout = QtWidgets.QGridLayout()
        gridLayout.addWidget(label, 0, 0, 1, 1)
        gridLayout.addLayout(horizontalLayout, 1, 0, 1, 3)
        gridLayout.addWidget(self.fanyiButton, 1, 3, 1, 1)
        gridLayout.addWidget(self.textEdit, 2, 0, 1, 2)
        gridLayout.addWidget(self.textEdit_2, 2, 2, 1, 2)

        mainLayout.setLayout(gridLayout)
        self.setCentralWidget(mainLayout)
        self.statusBar().showMessage("启动完成")

        # translate
        self.translateTask = task.TranslateTask()
        self.translateTask.done.connect(self.result)

    def createComboBox(self, index=''):
        comboBox = QtWidgets.QComboBox(self)
        comboBox.setEditable(True)
        comboBox.addItems(self.langlist)
        comboBox.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                               QtWidgets.QSizePolicy.Preferred)
        comboBox.setCurrentIndex(self.langlist.index(index))
        return comboBox


    def swapCombBox(self):
        language_src = self.srcComboBox.currentText()
        language_dst = self.dstComboBox.currentText()
        self.srcComboBox.setCurrentIndex(self.langlist.index(language_dst))
        self.dstComboBox.setCurrentIndex(self.langlist.index(language_src))

    def translate(self):
        if self.textEdit.toPlainText():
            language_src = self.srcComboBox.currentText()
            language_dst = self.dstComboBox.currentText()
            lang_src = self.langcodes.get(language_src.lower())
            lang_dst = self.langcodes.get(language_dst.lower())
            self.translateTask.set_attr(lang_src, lang_dst, self.textEdit.toPlainText())
            self.translateTask.start()

    def result(self, msg):
        self.textEdit_2.setText(msg)


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui_window = Ui_MainWindow()
    sys.exit(app.exec_())
