# -*- coding: utf-8 -*-
from PySide import QtGui
from PySide import QtCore
from elements.MembersTable import MembersTable
from Application import *
from Lot import Lot
from Auction import Auction


class MultiLotPage(QtGui.QWizardPage):
    def __init__(self, *args, **kwargs):
        self.title = None
        self.price = None
        self.members = None
        super(MultiLotPage, self).__init__(*args, **kwargs)

    def initializePage(self, *args, **kwargs):
        self.setTitle(u"Регистрация участников аукциона по лоту")
        self.setSubTitle(u"""Заполните начальную информацию о лоте.
Нажмите кнопку \"Далее\" для начала торгов.""")
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
        super(MultiLotPage, self).initializePage(*args, **kwargs)

    def isFinalPage(self, *args, **kwargs):
        return True


    def onNext(self):
        title = self.title.toPlainText().strip()
        if len(title) < 5:
            QtGui.QMessageBox.critical(None, u"Ошибка", u"Название лога должно содержать как минимум 5 символов")
            return False
        
        price = self.price.text()
        try:
            price = float(price)
        except ValueError:
            QtGui.QMessageBox.critical(None, u"Ошибка", u"Поле начальной цены введено неверно")
            return False

        members = self.members.getMembers()
        if len(members) < 1:
            QtGui.QMessageBox.critical(None, u"Ошибка", u"Введите как минимум одного участника аукциона")
            return False
        
        lots = [
            Lot(title, price)
        ]

        msg = u"Начать торги по лоту \"%s\"?" % title
        reply = QtGui.QMessageBox.question(self, u'Начать торги?', msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            auction = Auction(lots, members)
            app.setAuction(auction)
            return True        
        else:
            return False
