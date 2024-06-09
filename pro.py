from PyQt5 import QtCore, QtGui, QtWidgets
import n2
import p
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1041, 733)
        Dialog.setStyleSheet("#Dialog{background-image: url(:/新前缀/尼娅.png);margin-left:-300;}")
        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser.setGeometry(QtCore.QRect(665, 230, 241, 192))
        self.textBrowser.setStyleSheet("background-color:rgba(255, 255, 255, 100);")
        self.textBrowser.setObjectName("textBrowser")
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(190, 230, 211, 201))
        self.textEdit.setStyleSheet("background-color:rgba(255, 255, 255, 100);")
        self.textEdit.setObjectName("textEdit")
        self.commandLinkButton = QtWidgets.QCommandLinkButton(Dialog)
        self.commandLinkButton.setGeometry(QtCore.QRect(440, 290, 171, 61))
        self.commandLinkButton.setStyleSheet("color:rgba(196, 236, 255, 100);\n"
"font: 75 16pt \"微软雅黑\";\n"
"")
        self.commandLinkButton.setObjectName("commandLinkButton")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(240, 170, 181, 41))
        self.label.setStyleSheet("color:rgb(16, 16, 16);\n"
"font: 16pt \"黑体\";\n"
"")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(740, 180, 101, 41))
        self.label_2.setStyleSheet("color:rgb(16, 16, 16);\n"
"font: 16pt \"黑体\";\n"
"")
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Dialog)
        self.textEdit.textChanged.connect(self.slot1) # type: ignore
        self.commandLinkButton.clicked.connect(self.slot2) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    def slot1(self):
        self.textBrowser.setText(self.textEdit.toPlainText())
    def slot2(self):
        self.textBrowser.setText(n2.convert(self.textEdit.toPlainText()))
        print("convert successfully")
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.commandLinkButton.setText(_translate("Dialog", "Convert"))
        self.label.setText(_translate("Dialog", "input"))
        self.label_2.setText(_translate("Dialog", "output"))

