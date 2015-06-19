# -*- coding: utf-8 -*-


from PySide.QtCore import *
from PySide.QtGui import *
from PySide import QtGui
from forms.IntroPage import IntroPage
from forms.ChooseModePage import ChooseModePage
from forms.LotsPage import LotsPage
# from forms.AuctionPage import AuctionPage


class MainWizard(QtGui.QWizard):
    def run(self):
        self.setButtonText(self.NextButton, u"Далее")
        self.setButtonText(self.FinishButton, u"Начать торги")
        self.setButtonText(self.BackButton, u"Назад")
        self.setWizardStyle(QWizard.WizardStyle.ModernStyle)
        self.setFixedWidth(800)
        self.setFixedHeight(600)
        self.setModal(False)
        self.setWindowModality(Qt.NonModal)
        self.add_pages()

        self.setWindowTitle(u"Аукцион 67")

    def add_pages(self):
        self.addPage(IntroPage())
        self.addPage(ChooseModePage())
        self.addPage(LotsPage())
        # self.addPage(AuctionPage())
