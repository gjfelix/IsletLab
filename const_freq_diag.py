# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'const_freq_diag.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_const_freq_dialog(object):
    def setupUi(self, const_freq_dialog):
        const_freq_dialog.setObjectName("const_freq_dialog")
        const_freq_dialog.resize(294, 94)
        const_freq_dialog.setMinimumSize(QtCore.QSize(294, 94))
        const_freq_dialog.setMaximumSize(QtCore.QSize(294, 94))
        self.const_freq_buttonBox = QtWidgets.QDialogButtonBox(const_freq_dialog)
        self.const_freq_buttonBox.setGeometry(QtCore.QRect(-110, 50, 341, 32))
        self.const_freq_buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.const_freq_buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.const_freq_buttonBox.setObjectName("const_freq_buttonBox")
        self.formLayoutWidget = QtWidgets.QWidget(const_freq_dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 271, 31))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.const_freq_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.const_freq_label.setObjectName("const_freq_label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.const_freq_label)
        self.const_freq_value = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.const_freq_value.setObjectName("const_freq_value")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.const_freq_value)

        self.retranslateUi(const_freq_dialog)
        self.const_freq_buttonBox.accepted.connect(const_freq_dialog.accept)
        self.const_freq_buttonBox.rejected.connect(const_freq_dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(const_freq_dialog)

    def retranslateUi(self, const_freq_dialog):
        _translate = QtCore.QCoreApplication.translate
        const_freq_dialog.setWindowTitle(_translate("const_freq_dialog", "Dialog"))
        self.const_freq_label.setText(_translate("const_freq_dialog", "Constant frequency"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    const_freq_dialog = QtWidgets.QDialog()
    ui = Ui_const_freq_dialog()
    ui.setupUi(const_freq_dialog)
    const_freq_dialog.show()
    sys.exit(app.exec_())
