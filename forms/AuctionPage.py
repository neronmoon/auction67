# -*- coding: utf-8 -*-
from PySide import QtGui
from Application import *

class AuctionPage(QtGui.QWizardPage):
    def __init__(self, *args, **kwargs):
        self.modes = {}
        super(AuctionPage, self).__init__(*args, **kwargs)

    def initializePage(self, *args, **kwargs):
        self.setTitle(u"Начало работы")
        self.setSubTitle(u"Выберите нужное действие и нажмите кнопку \"Далее\"")
        layout = QtGui.QVBoxLayout()
        layout.setSpacing(15)
        oneLotRadio = QtGui.QRadioButton(u"Провести однолотовый аукцион")
        oneLotRadio.setChecked(True)
        self.modes[Application.OneLotMode] = oneLotRadio
        self.modes[Application.MultiLotMode] = QtGui.QRadioButton(u"Провести или подготовить многолотовый аукцион")
        self.modes[Application.MultiLotMode].setDisabled(True)
        self.modes[Application.LoadMode] = QtGui.QRadioButton(u"Загрузить из файла ранее сохраненный аукцион")
        for k, radio in self.modes.iteritems():
            layout.addWidget(radio)
        self.setLayout(layout)

        super(AuctionPage, self).initializePage(*args, **kwargs)

    def isFullScreen(self, *args, **kwargs):
        return True
    
    def onNext(self):
        for k, radio in self.modes.iteritems():
            if radio.isChecked():
                app.setMode(k)
                return app.getLotPageId()
        return False