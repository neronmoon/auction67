# -*- coding: utf-8 -*-
from PySide import QtGui
from PySide import QtCore
from elements.MembersTable import MembersTable
from Application import *
from elements.Slider import Slider
from Lot import Lot
from Auction import Auction
import cPickle as pickle
from texts import *


class LotsPage(QtGui.QWizardPage):
    def __init__(self, *args, **kwargs):
        self.title = []
        self.price = []
        self.members = []
        self.slider = None
        super(LotsPage, self).__init__(*args, **kwargs)

    def showEvent(self, *args, **kwargs):
        self.wizard().setFixedWidth(800)
        self.wizard().setFixedHeight(600)
        self.wizard().setButtonText(self.wizard().NextButton, START_AUCTION)
        self.wizard().setButtonText(QtGui.QWizard.CustomButton1, SAVE_AUCTION)
        self.wizard().setOption(QtGui.QWizard.HaveCustomButton1, True)
        self.disconnect(self.wizard(), QtCore.SIGNAL("customButtonClicked(int)"), self, QtCore.SLOT("save_auction()"))
        self.connect(self.wizard(), QtCore.SIGNAL("customButtonClicked(int)"), self, QtCore.SLOT("save_auction()"))

    @staticmethod
    def load_file():
        dialog = QtGui.QFileDialog()
        filename = dialog.getOpenFileName()[0]
        if ".auc" not in filename:
            filename += ".auc"
        try:
            return Auction(pickle.load(open(filename, "r"))['lots'])
        except:
            QtGui.QMessageBox.critical(None, ERROR, FILE_CANNOT_OPEN)
            return False

    def fill_forms(self, auction):
        for i, lot in enumerate(auction.lots):
            self.findChild(QtGui.QTextEdit, "title%s" % i).setText(lot.title)
            self.findChild(QtGui.QLineEdit, "price%s" % i).setText(unicode(lot.start_price))
            self.findChild(MembersTable, "members%s" % i).setMembers(lot.members)

    def initializePage(self, *args, **kwargs):
        self.setTitle(LOTS_TITLE)
        self.setSubTitle(LOTS_SUBTITLE)
        slides = []
        for i in range(0, 20):
            slide = self.create_lot_slide(i)
            slides.append(slide)
        self.slider = Slider(slides)
        self.setLayout(self.slider)
        if app.mode == Application.LoadMode:
            auction = self.load_file()
            if auction is not False:
                self.fill_forms(auction)
                app.set_auction(auction)
                app.set_mode(Application.PrepareMode)

    @staticmethod
    def create_lot_slide(i):
        # TODO first item padding
        slide = QtGui.QVBoxLayout()
        slide.addWidget(QtGui.QLabel(LOTS_LOTNAME % (i + 1)))
        title = QtGui.QTextEdit()
        title.setFixedHeight(70)
        title.setObjectName("title%s" % i)
        slide.addWidget(title)
        slide.addWidget(QtGui.QLabel(LOT_START_PRICE))
        price = QtGui.QLineEdit()
        price.setObjectName("price%s" % i)
        slide.addWidget(price)
        slide.addWidget(QtGui.QLabel(MEMBERS))
        members = MembersTable()
        members.setObjectName("members%s" % i)
        slide.addWidget(members)
        return slide

    def get_lots(self, convert=False):
        lots = []
        for i in range(0, 20):
            title = self.findChild(QtGui.QTextEdit, "title%s" % i).toPlainText().strip()
            if len(title) == 0:
                continue
            start_price = self.findChild(QtGui.QLineEdit, "price%s" % i).text().replace(" ", "").replace(",", ".").strip()
            if convert:
                start_price = float(start_price)
            members = self.findChild(MembersTable, "members%s" % i).getMembers()
            lots.append(Lot(title, start_price, members))
        return lots

    def validatePage(self, question=True):
        lots = self.get_lots()
        if len(lots) < 1:
            QtGui.QMessageBox.critical(None, ERROR, LOTS_FULL_AUCTION)
            return False
        for i, lot in enumerate(lots):
            if 5 > len(lot.title) > 0:
                self.slider.goto(i)
                QtGui.QMessageBox.critical(None, ERROR, LOTS_TITLE_INCORRECT)
                return False
            try:
                float(lot.start_price)
            except ValueError:
                self.slider.goto(i)
                QtGui.QMessageBox.critical(None, ERROR, )
                return False
            if len(lot.members) < 1:
                self.slider.goto(i)
                QtGui.QMessageBox.critical(None, ERROR, LOTS_MEMBERS_EMPTY)
                return False
        app.set_auction(Auction(lots))
        if question:
            reply = QtGui.QMessageBox.question(self, START_AUCTION_QUESTION, START_AUCTION_QUESTION, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            return reply == QtGui.QMessageBox.Yes
        else:
            return True

    def save_auction(self):
        if self.validatePage(question=False):
            dialog = QtGui.QFileDialog()
            filename = dialog.getSaveFileName()[0]
            if ".auc" not in filename:
                filename += ".auc"
            if pickle.dump({"lots": self.get_lots(convert=True)}, open(filename, "w")):
                QtGui.QMessageBox.information(self, SAVING, AUCTION_SAVED)
        return True
