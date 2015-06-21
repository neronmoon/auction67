# -*- coding: utf-8 -*-
from PySide import QtGui
from texts import *


class IntroPage(QtGui.QWizardPage):
    def initializePage(self, *args, **kwargs):
        self.setTitle(INTRO_TITLE)
        layout = QtGui.QVBoxLayout()
        layout.setSpacing(150)
        label = QtGui.QLabel(INTRO_TEXT)
        label.setWordWrap(True)
        layout.addWidget(label)
        label = QtGui.QLabel(PRESS_NEXT_FOR_BEGIN)
        layout.addWidget(label)
        self.setLayout(layout)

    def showEvent(self, *args, **kwargs):
        self.wizard().setOption(QtGui.QWizard.HaveCustomButton1, False)
        self.wizard().setButtonText(self.wizard().NextButton, NEXT_BUTTON)
        self.wizard().setFixedWidth(800)
        self.wizard().setFixedHeight(600)

    def isCommitPage(self):
        return True
