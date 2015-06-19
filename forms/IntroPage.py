# -*- coding: utf-8 -*-
from PySide import QtGui


class IntroPage(QtGui.QWizardPage):
    def initializePage(self, *args, **kwargs):
        self.setTitle(u"Программа Аукцион 67")
        layout = QtGui.QVBoxLayout()
        layout.setSpacing(150)
        label = QtGui.QLabel(u"""Программа предназначена для проведения аукциона на повышение цены в соответствии с требованиями приказа ФАС России от 10.02.2010 №67 "О порядке проведения конкурсов или аукционов на право заключения договоров аренды, договоров безвоздмездного пользования, договоров доверительного управления имуществом, иных договоров, предусматривающих переход прав владения и (или) пользованния в отношении государственного или муниципального имущества...".

Программа расчитает шаг аукциона, цену договора, подскажет когда и что аукионист должен объявлять участникам аукциона. Подключив компьютер к проектору, Вы сможете демонстрировать ход аукциона его участникам и членам комиссии на большом экране.""")
        label.setWordWrap(True)
        layout.addWidget(label)
        label = QtGui.QLabel(u'Нажмите кнопку "Далее" для начала работы.')
        layout.addWidget(label)
        self.setLayout(layout)

    def showEvent(self, *args, **kwargs):
        self.wizard().setOption(QtGui.QWizard.HaveCustomButton1, False)
        self.wizard().setButtonText(self.wizard().NextButton, u"Далее")

    def isCommitPage(self):
        return True
