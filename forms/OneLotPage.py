# -*- coding: utf-8 -*-
from PySide import QtGui
from PySide import QtCore
from elements.MembersTable import MembersTable
from Application import *
from Lot import Lot
from Auction import Auction
import cPickle as pickle


class OneLotPage(QtGui.QWizardPage):
    def __init__(self, *args, **kwargs):
        self.title = None
        self.price = None
        self.members = None
        super(OneLotPage, self).__init__(*args, **kwargs)

    def initializePage(self, *args, **kwargs):
        self.setTitle(u"Регистрация участников аукциона по лоту")
        self.setSubTitle(u"""Заполните начальную информацию о лоте.
Нажмите кнопку \"Далее\" для начала торгов.""")
        self.wizard().setButtonText(self.wizard().NextButton, u"Сохранить аукцион")

        self.setFinalPage(True)
        layout = QtGui.QVBoxLayout()
        label = QtGui.QLabel(u"Наименование лота")
        layout.addWidget(label)
        self.title = QtGui.QTextEdit()
        self.title.setFixedHeight(70)
        layout.addWidget(self.title)
        label = QtGui.QLabel(u"Начальная цена лота в рублях")
        layout.addWidget(label)
        self.price = QtGui.QLineEdit()
        layout.addWidget(self.price)
        label = QtGui.QLabel(u"Участники аукциона")
        layout.addWidget(label)
        self.members = MembersTable()
        layout.addWidget(self.members)
        self.setLayout(layout)
        self.setWindowModality(QtCore.Qt.NonModal)
        super(OneLotPage, self).initializePage(*args, **kwargs)
        self.wizard().button(self.wizard().NextButton).clicked.disconnect(self.wizard().next)
        self.wizard().button(self.wizard().NextButton).clicked.connect(self.nextButton)
        self.wizard().button(self.wizard().BackButton).clicked.connect(self.backButton)
        if app.auction is not None:
            self.loadAuction(app.auction)

    def isFinalPage(self, *args, **kwargs):
        return True

    def loadAuction(self, auction):
        self.findChild(MembersTable).setMembers(auction.members)
        lot = auction.lots[0]
        self.findChild(QtGui.QTextEdit).setText(lot.title)
        self.findChild(QtGui.QLineEdit).setText(unicode(lot.startPrice))

    def validate(self):
        result = True
        title = self.findChild(QtGui.QTextEdit).toPlainText().strip()
        if len(title) < 5:
            QtGui.QMessageBox.critical(None, u"Ошибка", u"Название лота должно содержать как минимум 5 символов")
            return False, "", 0, []
        price = self.findChild(QtGui.QLineEdit).text().strip()
        try:
            float(price)
        except ValueError:
            QtGui.QMessageBox.critical(None, u"Ошибка", u"Поле начальной цены введено неверно")
            return False, "", 0, []

        members = self.findChild(MembersTable).getMembers()
        if len(members) < 1:
            QtGui.QMessageBox.critical(None, u"Ошибка", u"Введите как минимум одного участника аукциона")
            return False, "", 0, []

        return result, title, price, members

    def onNext(self):
        result, title, price, members = self.validate()
        if not result:
            return False
        lots = [
            Lot(title, price)
        ]

        msg = u"Начать торги по лоту \"%s\"?" % title
        reply = QtGui.QMessageBox.question(self, u'Начать торги?', msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            auction = Auction(lots, members)
            app.setAuction(auction)
            return -1
        else:
            return False


    def nextButton(self):
        result, title, price, members = self.validate()
        if not result:
            return False

        lots = [
            Lot(title, price)
        ]
        object = {
            "applicationMode": app.mode,
            "lots": lots,
            "members": members
        }
        saveDialog = QtGui.QFileDialog()
        filename = saveDialog.getSaveFileName()[0]
        if ".auc" not in filename:
            filename += ".auc"
        file = open(filename, "w")
        pickle.dump(object, file)
        QtGui.QMessageBox.information(self, u'Сохраниение', u"Аукцион успешно сохранен")
        return True

    def backButton(self):
        self.cleanupPage()
        self.wizard().button(self.wizard().NextButton).clicked.disconnect(self.nextButton)
        self.wizard().button(self.wizard().NextButton).clicked.connect(self.wizard().next)
        self.wizard().setButtonText(self.wizard().NextButton, u"Далее")

