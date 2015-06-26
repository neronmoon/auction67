# -*- coding: utf-8 -*-

from PySide import QtGui
from PySide import QtCore
from texts import *


class AbstractAuctionPage(QtGui.QWizardPage):
    @staticmethod
    def offer_field(title, name):
        offer_vlayout = QtGui.QVBoxLayout()
        offer_vlayout.addStretch(0)
        offer_label = QtGui.QLabel(unicode(title))
        offer_label.setAlignment(QtCore.Qt.AlignCenter)
        offer_vlayout.addWidget(offer_label)
        row = QtGui.QHBoxLayout()
        for d in [["card", QtCore.Qt.AlignLeft], ["name", QtCore.Qt.AlignCenter], ["offer", QtCore.Qt.AlignRight]]:
            label = QtGui.QLabel("-")
            label.setObjectName("%s_%s" % (name, d[0]))
            label.setStyleSheet("font-size: 16px;")
            label.setAlignment(d[1])
            row.addWidget(label)
        offer_vlayout.addLayout(row)
        return offer_vlayout

    @staticmethod
    def members_field(members, i, callback):
        members_vlayout = QtGui.QVBoxLayout()
        members_label = QtGui.QLabel(MEMBERS_CARDS)
        members_label.setAlignment(QtCore.Qt.AlignCenter)
        members_vlayout.addWidget(members_label)
        row = QtGui.QHBoxLayout()
        nomember_btn = QtGui.QPushButton(NO_MEMBER_CARD)
        nomember_btn.clicked.connect(callback)
        nomember_btn.setObjectName("nomember%s" % i)
        nomember_btn.setFixedWidth(160)
        row.addWidget(nomember_btn)
        for m, member in enumerate(members):
            member_btn = QtGui.QPushButton(unicode(member["card"]))
            member_btn.setFixedWidth(60)
            member_btn.clicked.connect(callback)
            member_btn.setMinimumHeight(18)
            member_btn.setObjectName("%smember%s" % (m, i))
            row.addWidget(member_btn)
        members_vlayout.addLayout(row, 0)
        return members_vlayout

    def advice_field(self, lot, i):
        help_label = QtGui.QLabel(ADVICE_AUCTION_BEGIN.format(
            title=lot.title,
            starting_price=lot.start_price_formated(),
            current_price_step=lot.get_start_price_step(),
            # AUCTION_BEGIN_OWNER=ADVICE_AUCTION_BEGIN_OWNER.format(
            #     owner_card=unicode(lot.get_owner()["card"])) if lot.has_owner() else u""
        ))
        help_label.setWordWrap(True)
        help_label.setObjectName("advice%s" % i)
        help_label.setAlignment(QtCore.Qt.AlignLeft)
        help_label.setStyleSheet("font-style: italic;")
        help_label.setMinimumHeight(100)
        return help_label

    @staticmethod
    def get_badge(label, value=None, name=None, big=False):
        v_layout = QtGui.QVBoxLayout()
        v_layout.addStretch(0)
        label_w = QtGui.QLabel(unicode(label))
        label_w.setAlignment(QtCore.Qt.AlignHCenter)
        label_w.setMinimumHeight(16)
        v_layout.addWidget(label_w, 0, QtCore.Qt.AlignTop)
        value_w = QtGui.QLabel(unicode(value))
        if name is not None:
            value_w.setObjectName(name)
        value_w.setAlignment(QtCore.Qt.AlignHCenter)
        value_w.setStyleSheet("font-size: 32px;") if big else value_w.setStyleSheet("font-size: 16px;")
        value_w.setMinimumHeight(16)
        value_w.setMaximumHeight(160)
        value_w.setWordWrap(True)
        v_layout.addWidget(value_w, 0, QtCore.Qt.AlignTop)
        return v_layout

    def get_value(self, name, type=unicode):
        val = self.findChild(QtGui.QLabel, name).text().strip()
        if type is int:
            return int(val)
        elif type is float:
            return self.parse_price(val)
        return val

    @staticmethod
    def parse_price(val):
        return float(val[:-3].replace(",", ""))

    @staticmethod
    def format_price(price):
        return u'{:20,.2f} р.'.format(float(price)).strip()

    def set_value(self, name, value):
        return self.findChild(QtGui.QLabel, name).setText(unicode(value))

    @staticmethod
    def word_wrap(string, width=80, ind1=0, ind2=0, prefix=''):
        """ word wrapping function.
            string: the string to wrap
            width: the column number to wrap at
            prefix: prefix each line with this string (goes before any indentation)
            ind1: number of characters to indent the first line
            ind2: number of characters to indent the rest of the lines
        """
        string = prefix + ind1 * " " + string
        newstring = ""
        while len(string) > width:
            # find position of nearest whitespace char to the left of "width"
            marker = width - 1
            while not string[marker].isspace():
                marker = marker - 1

            # remove line from original string and add it to the new string
            newline = string[0:marker] + "\n"
            newstring = newstring + newline
            string = prefix + ind2 * " " + string[marker + 1:]

        return newstring + string
