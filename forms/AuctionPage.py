# -*- coding: utf-8 -*-
from PySide import QtGui, QtCore
from Application import *
from Auction import Auction
import cPickle as pickle
from elements.Slider import Slider
from texts import *
from State import State
from behaviours.AbstractAuctionPage import AbstractAuctionPage


class AuctionPage(AbstractAuctionPage):
    def __init__(self, *args, **kwargs):
        self.slider = None
        self.history = {}
        super(AuctionPage, self).__init__(*args, **kwargs)

    def debug(self):
        app.set_auction(Auction(pickle.load(open("/Users/vkrasnoperov/Envs/auction/test.auc", "r"))['lots']))

    def showEvent(self, *args, **kwargs):
        self.wizard().setOption(QtGui.QWizard.HaveCustomButton1, False)
        self.wizard().setButtonText(self.wizard().FinishButton, EXIT_BUTTON)
        self.wizard().setFixedWidth(1300)
        self.wizard().setFixedHeight(768)

    def isFinalPage(self, *args, **kwargs):
        return True

    def initializePage(self, *args, **kwargs):
        self.debug()
        slides = []
        for i, lot in enumerate(app.auction.lots):
            self.history[i] = []
            slide = QtGui.QVBoxLayout()
            slide.setObjectName("slide%s" % i)
            slide.addStretch(0)
            slide.addLayout(self.get_badge(LOT_NUM % (i + 1), lot.title, "title%s" % i))
            slide.addLayout(self.get_badge(LOT_STEPS_UP, LOT_STEPS_UP_VALUE))
            row = QtGui.QHBoxLayout()
            row.addLayout(self.get_badge(LOT_START_PRICE_SHORT, lot.start_price_formated()))
            row.addLayout(self.get_badge(STEP, value=1, name="current_step%s" % i))
            row.addLayout(self.get_badge(LOT_STEP_UP, "5.0% " + lot.get_start_price_step(), "current_price_step%s" % i))
            slide.addLayout(row)
            slide.addLayout(self.get_badge(OFFER_PRICE,
                                           lot.format_price(lot.get_start_price_step(False) + float(lot.start_price)),
                                           "current_price%s" % i, big=True))
            slide.addLayout(self.members_field(lot.members, i, self.next_step))
            slide.addLayout(self.offer_field(LOT_LAST_OFFER, "last_offer_%s" % i))
            slide.addLayout(self.offer_field(LOT_PRELAST_OFFER, "prelast_offer_%s" % i))
            bottom_layout = QtGui.QHBoxLayout()
            bottom_layout.addWidget(self.advice_field(lot, i))
            backstep_btn = QtGui.QPushButton(AUCTION_BACK_STEP_TITLE)
            backstep_btn.setDisabled(True)
            backstep_btn.clicked.connect(self.back_step)
            backstep_btn.setObjectName("backstep%s" % i)
            backstep_btn.setFixedWidth(160)
            bottom_layout.addWidget(backstep_btn)
            slide.addLayout(bottom_layout)
            slides.append(slide)
        self.setLayout(Slider(slides, show_pagination=(len(app.auction.lots) > 1)))

    def get_state(self, i):
        price_step = self.get_value("current_price_step%s" % i).split("%")
        return State(
            step=self.get_value("current_step%s" % i, type=int),
            price_step=[float(price_step[0]), self.parse_price(price_step[1].strip())],
            price=self.get_value("current_price%s" % i, type=float),
            last_offer=[
                self.get_value("last_offer_%s_card" % i, type=int),
                self.get_value("last_offer_%s_name" % i),
                self.get_value("last_offer_%s_offer" % i, type=float)
            ] if self.get_value("last_offer_%s_name" % i) != u"-" else None,
            prelast_offer=[
                self.get_value("prelast_offer_%s_card" % i, type=int),
                self.get_value("prelast_offer_%s_name" % i),
                self.get_value("prelast_offer_%s_offer" % i, type=float)
            ] if self.get_value("prelast_offer_%s_name" % i) != u"-" else None,
            advice=self.get_value("advice%s" % i),
        )

    def apply_state(self, i, state):
        self.findChild(QtGui.QPushButton, "backstep%s" % i).setDisabled(len(self.history[i]) == 0)
        price_step = unicode(state.price_step[0]) + u"% " + self.format_price(state.price_step[1])
        self.set_value("current_step%s" % i, state.step)
        self.set_value("current_price_step%s" % i, price_step)
        self.set_value("current_price%s" % i, self.format_price(state.price))
        self.set_value("advice%s" % i, state.advice)
        self.set_value("last_offer_%s_card" % i, state.last_offer[0] if state.last_offer is not None else "-")
        self.set_value("last_offer_%s_name" % i, state.last_offer[1] if state.last_offer is not None else "-")
        self.set_value("last_offer_%s_offer" % i,
                       self.format_price(state.last_offer[2]) if state.last_offer is not None else "-")
        self.set_value("prelast_offer_%s_card" % i, state.prelast_offer[0] if state.prelast_offer is not None else "-")
        self.set_value("prelast_offer_%s_name" % i, state.prelast_offer[1] if state.prelast_offer is not None else "-")
        self.set_value("prelast_offer_%s_offer" % i,
                       self.format_price(state.prelast_offer[2]) if state.prelast_offer is not None else "-")

    def end_lot(self, i, success=True):
        slide = self.findChild(QtGui.QVBoxLayout, "slide%s" % i)
        state = self.get_state(i)
        self.clear_layout(slide)
        if success:
            badge_text = AUCTION_LOT_OK_RESULT_TEXT if state.prelast_offer is None else (
                AUCTION_LOT_OK_RESULT_TEXT + AUCTION_LOT_OK_RESULT_PRELAST_OFFER_TEXT)
            badge_params = {
                "last_offer_card": state.last_offer[0],
                "last_offer_price": self.format_price(state.last_offer[2]),
            }
            advice_text = AUCTION_LOT_OK_RESULT_ADVICE if state.prelast_offer is None else (
                AUCTION_LOT_OK_RESULT_ADVICE + AUCTION_LOT_OK_RESULT_PRELAST_OFFER_ADVICE)
            advice_params = {
                "last_offer_card": state.last_offer[0],
                "last_offer_name": state.last_offer[1],
                "last_offer_price": self.format_price(state.last_offer[2]),

            }
            if state.prelast_offer is not None:
                badge_params.update({
                    "prelast_offer_card": state.prelast_offer[0],
                    "prelast_offer_price": self.format_price(state.prelast_offer[2])
                })
                advice_params.update({
                    "prelast_offer_card": state.prelast_offer[0],
                    "prelast_offer_name": state.prelast_offer[1],
                    "prelast_offer_price": self.format_price(state.prelast_offer[2]),
                })
        v_layout = QtGui.QVBoxLayout()
        v_layout.addLayout(self.get_badge(
            AUCTION_LOT_RESULT_TITLE,
            badge_text.format(**badge_params) if success else AUCTION_LOT_FAIL_RESULT_TEXT
        ))
        advice_label = QtGui.QLabel(advice_text.format(**advice_params) if success else AUCTION_LOT_FAIL_RESULT_ADVICE)
        advice_label.setWordWrap(True)
        advice_label.setObjectName("advice%s" % i)
        advice_label.setAlignment(QtCore.Qt.AlignLeft)
        v_layout.addWidget(advice_label)
        slide.addLayout(v_layout)

    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clear_layout(item.layout())

    def back_step(self):
        i = int(self.sender().objectName().replace("backstep", ""))
        if len(self.history[i]) > 0:
            reply = QtGui.QMessageBox.question(self, AUCTION_BACK_STEP_TITLE, AUCTION_BACK_STEP_TEXT,
                                               QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
                state = self.history[i].pop()
                self.apply_state(i, state)

    def next_step(self):
        data = self.sender().objectName().split("member")
        member_id = data[0]
        i = int(data[1])
        start_price = app.auction.lots[i].start_price
        self.history[i].append(self.get_state(i))
        state = self.get_state(i)
        member = None if member_id == "no" else app.auction.lots[i].members[int(member_id)]

        state.step += 1
        last_price = state.price
        if member is not None:
            state.add_offer([member["card"], member["name"], last_price])
            state.price += state.price_step[1]
            state.advice = ADVICE_AUCTION_MEMBER_CLICK.format(
                member_card=member["card"],
                last_price=self.format_price(last_price),
                current_price=self.format_price(state.price),
                current_price_step_value=self.format_price(state.price_step[1]),
            )
        else:
            last_price = state.price - state.price_step[1]
            new_price_step_percent = state.price_step[0] - 0.5
            if new_price_step_percent < 0.5:
                self.end_lot(i, success=(len(self.history[i]) > 10))
                return
            new_price_step_value = (float(start_price) * new_price_step_percent) / 100
            state.price = last_price + new_price_step_value
            state.price_step = [new_price_step_percent, new_price_step_value]
            state.advice = ADVICE_AUCTION_NO_MEMBER.format(
                current_price=self.format_price(state.price),
                current_price_step_percent=new_price_step_percent,
                current_price_step_value=self.format_price(new_price_step_value),
            )
        self.apply_state(i, state)
