# -*- coding: utf-8 -*-

from PySide import QtGui
from PySide import QtCore
from texts import MEMBER, OWNER


class MembersTable(QtGui.QTableWidget):
    def __init__(self, *args, **kwargs):
        super(MembersTable, self).__init__(*args, **kwargs)
        self.member_count = 20
        self.setRowCount(self.member_count)
        # self.setColumnCount(2)
        self.setColumnCount(1)
        self.setColumnWidth(0, 640)
        # self.setColumnWidth(0, 570)
        # self.setColumnWidth(1, 70)
        # self.setHorizontalHeaderLabels([MEMBER, OWNER])
        self.setHorizontalHeaderLabels([MEMBER])
        # for i in range(0, self.member_count):
        #     self.drawCheckbox(i)

    def drawCheckbox(self, i):
        widget = self.cellWidget(i, 1)
        paintCheckbox = False
        if widget is not None:
            prevWidgets = widget.findChildren(QtGui.QCheckBox)
            if len(prevWidgets) < 1:
                paintCheckbox = True
        else:
            paintCheckbox = True
        if paintCheckbox:
            widget = QtGui.QWidget()
            checkbox = QtGui.QCheckBox(self)
            layout = QtGui.QHBoxLayout(widget)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setAlignment(QtCore.Qt.AlignCenter)
            layout.addWidget(checkbox)
            widget.setLayout(layout)
            self.setCellWidget(i, 1, widget)

    def getMembers(self):
        members = []
        for i in range(0, self.member_count):
            item = self.item(i, 0)
            if item is not None:
                memberName = item.text().strip()
                # memberIsOwner = self.cellWidget(i, 1).findChildren(QtGui.QCheckBox)[0].isChecked()
                if memberName != "":
                    members.append({
                        "card": i+1,
                        "name": memberName,
                        # "isOwner": memberIsOwner
                    })
        return members

    def setMembers(self, members):
        for i, member in enumerate(members):
            self.setItem(i, 0, QtGui.QTableWidgetItem(member['name']))
            # self.drawCheckbox(i)
            # self.cellWidget(i, 1).findChildren(QtGui.QCheckBox)[0].setChecked(member['isOwner'])