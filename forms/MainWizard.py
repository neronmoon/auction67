# -*- coding: utf-8 -*-


from PySide.QtGui import *
from PySide import QtGui
from forms.IntroPage import IntroPage
from forms.ChooseModePage import ChooseModePage
from forms.LotsPage import LotsPage
from forms.AuctionPage import AuctionPage
from texts import *

class MainWizard(QtGui.QWizard):
    def run(self):
        self.setWindowTitle(MAIN_TITLE)
        self.setButtonText(self.NextButton, NEXT_BUTTON)
        self.setButtonText(self.BackButton, BACK_BUTTON)
        self.setWizardStyle(QWizard.WizardStyle.ModernStyle)
        self.setFixedWidth(800)
        self.setFixedHeight(600)
        self.add_pages()

    def add_pages(self):
        # self.addPage(IntroPage())
        # self.addPage(ChooseModePage())
        # self.addPage(LotsPage())
        self.addPage(AuctionPage())
