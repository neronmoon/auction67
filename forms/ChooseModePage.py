# -*- coding: utf-8 -*-
from PySide import QtGui
from Application import *


class ChooseModePage(QtGui.QWizardPage):
    def __init__(self, *args, **kwargs):
        self.modes = {}
        super(ChooseModePage, self).__init__(*args, **kwargs)

    def showEvent(self, *args, **kwargs):
        self.wizard().setOption(QtGui.QWizard.HaveCustomButton1, False)
        self.wizard().setButtonText(self.wizard().NextButton, u"Далее")

    def initializePage(self, *args, **kwargs):

        self.setTitle(u"Начало работы")
        self.setSubTitle(u"Выберите нужное действие и нажмите кнопку \"Далее\"")
        layout = QtGui.QVBoxLayout()
        layout.setSpacing(15)
        self.modes[Application.PrepareMode] = QtGui.QRadioButton(u"Провести или подготовить аукцион")
        self.modes[Application.LoadMode] = QtGui.QRadioButton(u"Загрузить из файла ранее сохраненный аукцион")
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
        QtGui.QMessageBox.warning(self, u'', u"Выберите режим работы")
        return False
