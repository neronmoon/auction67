# -*- coding: utf-8 -*-
from PySide import QtGui
from Application import *
from texts import *


class ChooseModePage(QtGui.QWizardPage):
    def __init__(self, *args, **kwargs):
        self.modes = {}
        super(ChooseModePage, self).__init__(*args, **kwargs)

    def showEvent(self, *args, **kwargs):
        self.wizard().setOption(QtGui.QWizard.HaveCustomButton1, False)
        self.wizard().setButtonText(self.wizard().NextButton, NEXT_BUTTON)
        self.wizard().setFixedWidth(800)
        self.wizard().setFixedHeight(600)

    def initializePage(self, *args, **kwargs):

        self.setTitle(CMP_TITLE)
        self.setSubTitle(CMP_SUBTITLE)
        layout = QtGui.QVBoxLayout()
        layout.setSpacing(15)
        self.modes[Application.PrepareMode] = QtGui.QRadioButton(CMP_PREPARE_MODE)
        self.modes[Application.LoadMode] = QtGui.QRadioButton(CMP_LOAD_MODE)
        for k, radio in self.modes.iteritems():
            layout.addWidget(radio)
        self.setLayout(layout)

    def isFinalPage(self, *args, **kwargs):
        return False

    def validatePage(self, *args, **kwargs):
        for k, radio in enumerate(self.findChildren(QtGui.QRadioButton)):
            if radio.isChecked():
                app.set_mode(k)
                return True
        QtGui.QMessageBox.warning(self, u'', CMP_MODE)
        return False
