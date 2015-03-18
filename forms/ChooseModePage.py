# -*- coding: utf-8 -*-
from PySide import QtGui
from Application import *
import cPickle as pickle
from Auction import Auction


class ChooseModePage(QtGui.QWizardPage):
    def __init__(self, *args, **kwargs):
        self.modes = {}
        super(ChooseModePage, self).__init__(*args, **kwargs)

    def initializePage(self, *args, **kwargs):
        self.setTitle(u"Начало работы")
        self.setSubTitle(u"Выберите нужное действие и нажмите кнопку \"Далее\"")
        layout = QtGui.QVBoxLayout()
        layout.setSpacing(15)
        oneLotRadio = QtGui.QRadioButton(u"Провести или подготовить однолотовый аукцион")
        oneLotRadio.setChecked(True)
        self.modes[Application.OneLotMode] = oneLotRadio
        self.modes[Application.MultiLotMode] = QtGui.QRadioButton(u"Провести или подготовить многолотовый аукцион")
        self.modes[Application.MultiLotMode].setDisabled(True)
        self.modes[Application.LoadMode] = QtGui.QRadioButton(u"Загрузить из файла ранее сохраненный аукцион")
        for k, radio in self.modes.iteritems():
            layout.addWidget(radio)
        self.setLayout(layout)

        super(ChooseModePage, self).initializePage(*args, **kwargs)

    def isFinalPage(self, *args, **kwargs):
        return False


    def nextButton(self):
        pass

    def backButton(self):
        pass

    def finishButton(self):
        pass

    def onNext(self):
        for k, radio in enumerate(self.findChildren(QtGui.QRadioButton)):
            if radio.isChecked():
                if k == 2:
                    openDialog = QtGui.QFileDialog()
                    filename = openDialog.getOpenFileName()[0]
                    if ".auc" not in filename:
                        filename += ".auc"
                    try:
                        file = open(filename, "r")
                    except Exception:
                        QtGui.QMessageBox.critical(None, u"Ошибка", u"Файл не может быть открыт")
                        return False
                    loaded = pickle.load(file)
                    auction = Auction(loaded['lots'], loaded['members'])
                    app.setAuction(auction)
                    app.setMode(loaded['applicationMode'])
                    self.wizard().page(app.getLotPageId()).cleanupPage()
                else:
                    app.setMode(k)
                return app.getLotPageId()
        return False