# -*- coding: utf-8 -*-

from PySide import QtGui


class Slider(QtGui.QVBoxLayout):
    def __init__(self, slides, *args, **kwargs):
        super(Slider, self).__init__(*args, **kwargs)
        self.current_slide = 0
        self.slides = slides
        button_layout = QtGui.QHBoxLayout()
        self.back = QtGui.QPushButton(u"< Предыдущий лот")
        self.back.setDisabled(True)
        self.back.clicked.connect(self.back_click)
        button_layout.addWidget(self.back)
        self.next = QtGui.QPushButton(u"Следующий лот >")
        self.next.clicked.connect(self.next_click)
        button_layout.addWidget(self.next)

        self.slides_box = QtGui.QStackedLayout()
        for slide in slides:
            w = QtGui.QWidget()
            w.setLayout(slide)
            self.slides_box.addWidget(w)
        self.addLayout(button_layout)
        self.addLayout(self.slides_box)

    def next_click(self):
        if self.current_slide < len(self.slides):
            self.current_slide += 1
            self.slides_box.setCurrentIndex(self.current_slide)
        self.buttons_check()

    def buttons_check(self):
        if self.current_slide > 0:
            self.back.setDisabled(False)
        else:
            self.back.setDisabled(True)
        if self.current_slide == (len(self.slides) - 1):
            self.next.setDisabled(True)
        else:
            self.next.setDisabled(False)

    def back_click(self):
        if self.current_slide > 0:
            self.current_slide -= 1
            self.slides_box.setCurrentIndex(self.current_slide)
        self.buttons_check()

    def goto(self, i):
        if 0 <= i < len(self.slides):
            self.current_slide = i
            self.slides_box.setCurrentIndex(self.current_slide)
            return True
        return False