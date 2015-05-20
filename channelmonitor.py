# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QSpacerItem
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont


class ChannelMonitor(QGroupBox):

    def __init__(self, parent=None, name="Термостат 1"):
        super(ChannelMonitor, self).__init__(parent)
        self.setTitle(name)
        self.setMinimumHeight(50)
        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(10, 0, 10, 0)
        #
        # Bold Font
        #
        font = QFont()
        font.setBold(True)
        font.setWeight(75)

        #
        #Label Вход
        #
        self.labelInput = QLabel(self)
        self.labelInput.setText("Вход")
        self.labelInput.setMaximumHeight(20)
        self.labelInput.setFont(font)
        self.layout.addWidget(self.labelInput)

        self.spacer1 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.layout.addItem(self.spacer1)

        #
        # Edit Вход
        #
        self.editInput = QLineEdit(self)
        # sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.labelInput.sizePolicy().hasHeightForWidth())
        # self.editInput.setSizePolicy(sizePolicy)
        self.editInput.setMaximumSize(QSize(50, 16777215))
        self.editInput.setMaximumHeight(20)
        self.editInput.setReadOnly(True)
        self.setAlignment(0)
        self.layout.addWidget(self.editInput)

        self.spacer2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.layout.addItem(self.spacer2)

        #
        #Label Измерване
        #

        self.measurementLabel = QLabel(self)
        self.measurementLabel.setMaximumHeight(20)
        self.measurementLabel.setText("Темпрература")
        self.measurementLabel.setFont(font)
        self.layout.addWidget(self.measurementLabel)

        self.spacer3 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.layout.addItem(self.spacer3)

        #
        #Edit Измерване + label градуси
        #

        self.editMeasurement = QLineEdit(self)
        self.editMeasurement.setMaximumHeight(20)
        self.editMeasurement.setMaximumSize(QSize(50, 16777215))
        self.editMeasurement.setReadOnly(True)
        self.layout.addWidget(self.editMeasurement)

        self.spacer3 = QSpacerItem(5, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.layout.addItem(self.spacer3)

        self.labelTc = QLabel(self)
        self.labelTc.setText("t/ºC")
        self.layout.addWidget(self.labelTc)

        self.spacer4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.layout.addItem(self.spacer4)

        #
        #Label Тригер
        #

        self.triggerLabel = QLabel(self)
        self.triggerLabel.setMaximumHeight(20)
        self.triggerLabel.setText("Тригер")
        self.triggerLabel.setFont(font)
        self.layout.addWidget(self.triggerLabel)

        self.spacer10 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.layout.addItem(self.spacer10)

        #
        #Edit Тригер + label градуси
        #

        self.editTrigger = QLineEdit(self)
        self.editTrigger.setMaximumHeight(20)
        self.editTrigger.setMaximumSize(QSize(50, 16777215))
        self.editTrigger.setReadOnly(True)
        self.layout.addWidget(self.editTrigger)

        self.spacer11 = QSpacerItem(5, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.layout.addItem(self.spacer11)

        self.labelTc1 = QLabel(self)
        self.labelTc1.setText("t/ºC")
        self.layout.addWidget(self.labelTc1)

        self.spacer12 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.layout.addItem(self.spacer12)

        #
        #Labels Изход
        #

        self.labelOutTitle = QLabel(self)
        self.labelOutTitle.setFont(font)
        self.labelOutTitle.setText("Изход")
        self.layout.addWidget(self.labelOutTitle)

        self.spacer5 = QSpacerItem(5, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.layout.addItem(self.spacer5)

        self.labelOut = QLabel(self)
        self.labelOut.setMaximumHeight(20)
        self.labelOut.setFrameShape(QFrame.Box)
        self.labelOut.setFrameShadow(QFrame.Plain)
        self.labelOut.setStyleSheet("color: rgb(255, 0, 0);")
        self.labelOut.setText("Изключен")
        self.labelOut.setFont(font)
        self.layout.addWidget(self.labelOut)

        self.spacer6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.layout.addItem(self.spacer6)

        #
        # Labels Разрешен
        #

        self.labelЕnabledTitle = QLabel(self)
        self.labelЕnabledTitle.setFont(font)
        self.labelЕnabledTitle.setText("Разрешен")
        self.layout.addWidget(self.labelЕnabledTitle)

        self.spacer7 = QSpacerItem(5, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.layout.addItem(self.spacer7)

        self.labelЕnabled = QLabel(self)
        self.labelЕnabled.setMaximumHeight(20)
        self.labelЕnabled.setFrameShape(QFrame.Box)
        self.labelЕnabled.setFrameShadow(QFrame.Plain)
        self.labelЕnabled.setStyleSheet("color: rgb(78, 66, 255);")
        self.labelЕnabled.setText("Да")
        self.labelЕnabled.setFont(font)
        self.layout.addWidget(self.labelЕnabled)

        self.spacer8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.layout.addItem(self.spacer8)

        #
        #Button Настройки
        #

        self.buttonChanSettings = QPushButton(self)
        self.buttonChanSettings.setText("Настройка ...")
        self.layout.addWidget(self.buttonChanSettings)

    def setValues(self, state):
        self.editInput.setText("T("+ state.input + ")")
        self.editMeasurement.setText(state.measurment)
        self.editTrigger.setText(state.trigger)

        if state.outputOn == "0":
            self.labelOut.setText("Изключен")
            self.labelOut.setStyleSheet("color: rgb(255, 0, 0);")
        else:
            self.labelOut.setText("Включен")
            self.labelOut.setStyleSheet("color: rgb(78, 66, 255);")

        if state.enabled == "Off":
            self.labelЕnabled.setText("Не")
            self.labelЕnabled.setStyleSheet("color: rgb(255, 0, 0);")
        else:
            self.labelЕnabled.setText("Да")
            self.labelЕnabled.setStyleSheet("color: rgb(78, 66, 255);")