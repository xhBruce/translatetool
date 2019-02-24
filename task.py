# -*- coding: utf-8 -*-

from PyQt5.QtCore import QThread
from PyQt5 import QtCore

from googletrans import Translator
import traceback

translator = Translator(service_urls=[
    'translate.google.cn',
])


class TranslateTask(QThread):
    done = QtCore.pyqtSignal(str)

    def set_attr(self, src, dst, text=''):
        self.src = src
        self.dst = dst
        self.text = text

    def run(self):
        try:
            msg = translator.translate(self.text, dest=self.dst, src=self.src)
        except:
            traceback.print_exc()
            msg = '\t<b>Google翻译异常，请稍后再试</b>'
            print(msg)
            return
        self.done.emit(msg.text)
