# -*- coding: utf-8 -*-


from PySide.QtCore import *
from PySide.QtGui import *
from PySide import QtGui
from forms.IntroPage import IntroPage
from forms.ChooseModePage import ChooseModePage
from forms.OneLotPage import OneLotPage
from forms.AuctionPage import AuctionPage


class MainWizard(QtGui.QWizard):
    def __init__(self, *args, **kwargs):
        self.nextPage = 1

        super(MainWizard, self).__init__(*args, **kwargs)

    def run(self):
        self.setButtonText(self.NextButton, u"Далее")
        self.setButtonText(self.FinishButton, u"Начать торги")
        self.setButtonText(self.BackButton, u"Назад")
        self.setWizardStyle(QWizard.WizardStyle.ModernStyle)
        self.setFixedWidth(800)
        self.setFixedHeight(600)
        self.setModal(False)
        self.setWindowModality(Qt.NonModal)
        self.addPage(IntroPage())
        self.addPage(ChooseModePage())
        self.addPage(OneLotPage())
        self.addPage(AuctionPage())
        self.setWindowTitle(u"Аукцион 67")

    def validateCurrentPage(self, *args, **kwargs):
        super(MainWizard, self).validateCurrentPage(*args, **kwargs)
        self.nextPage = self.currentPage().onNext()
        return self.nextPage is not False

    def finished(self, *args, **kwargs):
        super(MainWizard, self).finished(*args, **kwargs)

    def nextId(self, *args, **kwargs):
        return self.nextPage
