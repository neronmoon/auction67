# -*- coding: utf-8 -*-
from PySide import QtGui
from PySide import QtCore
from elements.MembersTable import MembersTable
from Application import *
from elements.Slider import Slider
from Lot import Lot
from Auction import Auction
import cPickle as pickle


class LotsPage(QtGui.QWizardPage):
    def __init__(self, *args, **kwargs):
        self.title = []
        self.price = []
        self.members = []
        self.slider = None
        super(LotsPage, self).__init__(*args, **kwargs)

    @staticmethod
    def load_file():
        dialog = QtGui.QFileDialog()
        filename = dialog.getOpenFileName()[0]
        if ".auc" not in filename:
            filename += ".auc"
        try:
            file = open(filename, "r")
        except Exception:
            QtGui.QMessageBox.critical(None, u"Ошибка", u"Файл не может быть открыт")
            return False
        loaded = pickle.load(file)
        auction = Auction(loaded['lots'])
        app.set_auction(auction)

    def initializePage(self, *args, **kwargs):
        if app.mode == Application.LoadMode:
            self.load_file()
            app.set_mode(Application.PrepareMode)
        self.setTitle(u"Регистрация участников аукциона по лотам")
        self.setSubTitle(u"""Заполните начальную информацию о лотах.
Нажмите кнопку \"Далее\" для начала торгов.""")
        self.wizard().setButtonText(self.wizard().NextButton, u"Начать торги")

        slides = []
        for i in range(0, 20):
            # TODO first item padding
            slide = QtGui.QVBoxLayout()
            slide.addWidget(QtGui.QLabel(u"Наименование лота #%s" % (i + 1)))
            title = QtGui.QTextEdit()
            title.setFixedHeight(70)
            title.setObjectName("title%s" % i)
            slide.addWidget(title)
            slide.addWidget(QtGui.QLabel(u"Начальная цена лота в рублях"))
            price = QtGui.QLineEdit()
            price.setObjectName("price%s" % i)
            slide.addWidget(price)
            slide.addWidget(QtGui.QLabel(u"Участники аукциона"))
            members = MembersTable()
            members.setObjectName("members%s" % i)
            slide.addWidget(members)
            slides.append(slide)
        self.slider = Slider(slides)
        self.setLayout(self.slider)

        self.setWindowModality(QtCore.Qt.NonModal)
        self.wizard().setButtonText(QtGui.QWizard.CustomButton1, u"Сохранить аукцион")
        self.wizard().setOption(QtGui.QWizard.HaveCustomButton1, True)
        self.connect(self.wizard(), QtCore.SIGNAL("customButtonClicked(int)"), self, QtCore.SLOT("save_auction()"))
        if app.auction is not None:
            self.load_auction(app.auction)

    def load_auction(self, auction):
        for i, lot in enumerate(auction.lots):
            self.findChild(QtGui.QTextEdit, "title%s" % i).setText(lot.title)
            self.findChild(QtGui.QLineEdit, "price%s" % i).setText(unicode(lot.startPrice))
            self.findChild(MembersTable, "members%s" % i).setMembers(lot.members)

    def get_lots(self):
        lots = []
        for i in range(0, 20):
            title = self.findChild(QtGui.QTextEdit, "title%s" % i).toPlainText().strip()
            start_price = self.findChild(QtGui.QLineEdit, "price%s" % i).text().strip()
            members = self.findChild(MembersTable, "members%s" % i).getMembers()
            lots.append(Lot(title, start_price, members))
        return lots

    def validatePage(self):
        lots = self.get_lots()
        for i, lot in enumerate(lots):
            if len(lot.title) == 0:
                continue
            if 5 > len(lot.title) > 0:
                self.slider.goto(i)
                QtGui.QMessageBox.critical(None, u"Ошибка", u"Название лота должно содержать как минимум 5 символов")
                return False
            try:
                float(lot.startPrice)
            except ValueError:
                self.slider.goto(i)
                QtGui.QMessageBox.critical(None, u"Ошибка", u"Поле начальной цены введено неверно")
                return False
            if len(lot.members) < 1:
                self.slider.goto(i)
                QtGui.QMessageBox.critical(None, u"Ошибка", u"Введите как минимум одного участника аукциона")
                return False
            app.set_auction(Auction(lots))
        return True

    def save_auction(self):
        if not self.validatePage():
            return False
        dialog = QtGui.QFileDialog()
        filename = dialog.getSaveFileName()[0]
        if ".auc" not in filename:
            filename += ".auc"
        if pickle.dump({"lots": self.get_lots()}, open(filename, "w")):
            QtGui.QMessageBox.information(self, u'Сохраниение', u"Аукцион успешно сохранен")
        return True
