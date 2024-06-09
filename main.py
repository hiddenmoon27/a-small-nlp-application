from PyQt5 import QtCore, QtGui, QtWidgets
from pro import Ui_Dialog
import sys
import p
class Ui_origin(object):

    def setupUi(self, origin):
        origin.setObjectName("origin")
        origin.resize(1079, 848)
        origin.setStyleSheet("#origin{background-image:url(:/新前缀/640.jpg);}")
        self.pushButton = QtWidgets.QPushButton(origin)
        self.pushButton.setGeometry(QtCore.QRect(510, 590, 93, 28))
        self.pushButton.setStyleSheet("background-color:transparent;")
        icon = QtGui.QIcon(":/新前缀/emoji-smile.png")
        self.pushButton.setIcon(icon)
        self.pushButton.setObjectName("pushButton")
        self.actionyes = QtWidgets.QAction(origin)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/新前缀/emoji-smile.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionyes.setIcon(icon)
        self.actionyes.setObjectName("actionyes")
        self.retranslateUi(origin)
        self.pushButton.clicked.connect(self.nextp) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(origin)
    def nextp(self):
        self.np = QtWidgets.QDialog()
        dialog_ui = Ui_Dialog()
        dialog_ui.setupUi(self.np)
        self.np.exec_()

    def retranslateUi(self, origin):
        _translate = QtCore.QCoreApplication.translate
        origin.setWindowTitle(_translate("origin", "Form"))
        self.pushButton.setText(_translate("origin", "start"))
        self.actionyes.setText(_translate("origin", "yes"))

if __name__ == '__main__':
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_origin()
        ui.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())