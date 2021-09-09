# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'random_freq_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_random_freq_dialog(object):
    def setupUi(self, random_freq_dialog):
        random_freq_dialog.setObjectName("random_freq_dialog")
        random_freq_dialog.resize(192, 120)
        self.buttonBox = QtWidgets.QDialogButtonBox(random_freq_dialog)
        self.buttonBox.setGeometry(QtCore.QRect(-160, 80, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayoutWidget = QtWidgets.QWidget(random_freq_dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 171, 61))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.mean_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.mean_label.setObjectName("mean_label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.mean_label)
        self.mean_value = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.mean_value.setObjectName("mean_value")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.mean_value)
        self.sd_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.sd_label.setObjectName("sd_label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.sd_label)
        self.sd_value = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.sd_value.setObjectName("sd_value")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.sd_value)

        self.retranslateUi(random_freq_dialog)
        self.buttonBox.accepted.connect(random_freq_dialog.accept)
        self.buttonBox.rejected.connect(random_freq_dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(random_freq_dialog)

    def retranslateUi(self, random_freq_dialog):
        _translate = QtCore.QCoreApplication.translate
        random_freq_dialog.setWindowTitle(_translate("random_freq_dialog", "Random frequency"))
        self.mean_label.setText(_translate("random_freq_dialog", "Mean"))
        self.sd_label.setText(_translate("random_freq_dialog", "SD"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    random_freq_dialog = QtWidgets.QDialog()
    ui = Ui_random_freq_dialog()
    ui.setupUi(random_freq_dialog)
    random_freq_dialog.show()
    sys.exit(app.exec_())
