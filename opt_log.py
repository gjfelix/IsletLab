# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'opt_log.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(650, 400)
        Dialog.setMinimumSize(QtCore.QSize(650, 400))
        Dialog.setMaximumSize(QtCore.QSize(650, 400))
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(10, 10, 630, 350))
        self.textEdit.setObjectName("textEdit")
        self.runopt_pushButton = QtWidgets.QPushButton(Dialog)
        self.runopt_pushButton.setGeometry(QtCore.QRect(180, 370, 131, 23))
        self.runopt_pushButton.setObjectName("runopt_pushButton")
        self.abortopt_pushbutton = QtWidgets.QPushButton(Dialog)
        self.abortopt_pushbutton.setGeometry(QtCore.QRect(340, 370, 131, 23))
        self.abortopt_pushbutton.setObjectName("abortopt_pushbutton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Optimization log"))
        self.runopt_pushButton.setText(_translate("Dialog", "Run"))
        self.abortopt_pushbutton.setText(_translate("Dialog", "Abort"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

