# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'reconstruction_settings.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_reconstruction_settings_diag(object):
    def setupUi(self, reconstruction_settings_diag):
        reconstruction_settings_diag.setObjectName("reconstruction_settings_diag")
        reconstruction_settings_diag.resize(313, 238)
        reconstruction_settings_diag.setMinimumSize(QtCore.QSize(313, 238))
        reconstruction_settings_diag.setMaximumSize(QtCore.QSize(313, 238))
        self.recconstruction_settings_buttonbox = QtWidgets.QDialogButtonBox(reconstruction_settings_diag)
        self.recconstruction_settings_buttonbox.setGeometry(QtCore.QRect(70, 200, 171, 32))
        self.recconstruction_settings_buttonbox.setOrientation(QtCore.Qt.Horizontal)
        self.recconstruction_settings_buttonbox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.recconstruction_settings_buttonbox.setObjectName("recconstruction_settings_buttonbox")
        self.opt_settings_dialog_groupbox = QtWidgets.QWidget(reconstruction_settings_diag)
        self.opt_settings_dialog_groupbox.setGeometry(QtCore.QRect(9, 9, 291, 191))
        self.opt_settings_dialog_groupbox.setObjectName("opt_settings_dialog_groupbox")
        self.formLayoutWidget = QtWidgets.QWidget(self.opt_settings_dialog_groupbox)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 271, 181))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.rec_settings_initemp_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.rec_settings_initemp_label.setObjectName("rec_settings_initemp_label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.rec_settings_initemp_label)
        self.rec_settings_initemp_value = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.rec_settings_initemp_value.setFrame(True)
        self.rec_settings_initemp_value.setAlignment(QtCore.Qt.AlignCenter)
        self.rec_settings_initemp_value.setObjectName("rec_settings_initemp_value")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.rec_settings_initemp_value)
        self.rec_settings_tolpar_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.rec_settings_tolpar_label.setObjectName("rec_settings_tolpar_label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.rec_settings_tolpar_label)
        self.rec_settings_tolpar_value = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.rec_settings_tolpar_value.setAlignment(QtCore.Qt.AlignCenter)
        self.rec_settings_tolpar_value.setObjectName("rec_settings_tolpar_value")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.rec_settings_tolpar_value)
        self.rec_settings_maxiter_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.rec_settings_maxiter_label.setObjectName("rec_settings_maxiter_label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.rec_settings_maxiter_label)
        self.rec_settings_maxiter_value = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.rec_settings_maxiter_value.setAlignment(QtCore.Qt.AlignCenter)
        self.rec_settings_maxiter_value.setObjectName("rec_settings_maxiter_value")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.rec_settings_maxiter_value)
        self.rec_settings_maxacc_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.rec_settings_maxacc_label.setObjectName("rec_settings_maxacc_label")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.rec_settings_maxacc_label)
        self.rec_settings_maxacc_value = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.rec_settings_maxacc_value.setAlignment(QtCore.Qt.AlignCenter)
        self.rec_settings_maxacc_value.setObjectName("rec_settings_maxacc_value")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.rec_settings_maxacc_value)
        self.rec_settings_threads_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.rec_settings_threads_label.setObjectName("rec_settings_threads_label")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.rec_settings_threads_label)
        self.rec_settings_threads_value = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.rec_settings_threads_value.setAlignment(QtCore.Qt.AlignCenter)
        self.rec_settings_threads_value.setObjectName("rec_settings_threads_value")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.rec_settings_threads_value)
        self.rec_settings_contacttol_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.rec_settings_contacttol_label.setObjectName("rec_settings_contacttol_label")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.rec_settings_contacttol_label)
        self.rec_settings_contacttol_value = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.rec_settings_contacttol_value.setAlignment(QtCore.Qt.AlignCenter)
        self.rec_settings_contacttol_value.setObjectName("rec_settings_contacttol_value")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.rec_settings_contacttol_value)

        self.retranslateUi(reconstruction_settings_diag)
        self.recconstruction_settings_buttonbox.accepted.connect(reconstruction_settings_diag.accept)
        self.recconstruction_settings_buttonbox.rejected.connect(reconstruction_settings_diag.reject)
        QtCore.QMetaObject.connectSlotsByName(reconstruction_settings_diag)

    def retranslateUi(self, reconstruction_settings_diag):
        _translate = QtCore.QCoreApplication.translate
        reconstruction_settings_diag.setWindowTitle(_translate("reconstruction_settings_diag", "Reconstruction settings"))
        self.rec_settings_initemp_label.setText(_translate("reconstruction_settings_diag", "Initial temperature"))
        self.rec_settings_initemp_value.setText(_translate("reconstruction_settings_diag", "50"))
        self.rec_settings_tolpar_label.setText(_translate("reconstruction_settings_diag", "Tolerance parameter"))
        self.rec_settings_tolpar_value.setText(_translate("reconstruction_settings_diag", "0.005"))
        self.rec_settings_maxiter_label.setText(_translate("reconstruction_settings_diag", "Max. iterations"))
        self.rec_settings_maxiter_value.setText(_translate("reconstruction_settings_diag", "1E6"))
        self.rec_settings_maxacc_label.setText(_translate("reconstruction_settings_diag", "Max. accepted"))
        self.rec_settings_maxacc_value.setText(_translate("reconstruction_settings_diag", "5E5"))
        self.rec_settings_threads_label.setText(_translate("reconstruction_settings_diag", "Threads"))
        self.rec_settings_threads_value.setText(_translate("reconstruction_settings_diag", "4"))
        self.rec_settings_contacttol_label.setText(_translate("reconstruction_settings_diag", "Contact tolerance"))
        self.rec_settings_contacttol_value.setText(_translate("reconstruction_settings_diag", "1"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    reconstruction_settings_diag = QtWidgets.QDialog()
    ui = Ui_reconstruction_settings_diag()
    ui.setupUi(reconstruction_settings_diag)
    reconstruction_settings_diag.show()
    sys.exit(app.exec_())

