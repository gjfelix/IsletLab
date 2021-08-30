# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'isletlabgui_v1.0.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import re
from ProgressBar import ProgressBar
import sys, time
import subprocess
import _thread

from shape import Shape
from sphere import Sphere
from sys import platform as sys_pf
if sys_pf == 'darwin':
    import matplotlib
    matplotlib.use("Qt5Agg")
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
else:
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D


# Para progress bar
class Message(QtCore.QObject):
    finished = QtCore.pyqtSignal()


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 769)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(1024, 769))
        MainWindow.setMaximumSize(QtCore.QSize(1024, 769))
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        

        # Para agregar figuras en pestañas
        self.canvases = []
        self.figure_handles = []
        self.toolbar_handles = []
        self.tab_handles = []
        self.current_window = -1

        # Parametros default para reconstruccion
        self.inittemp = 100.
        self.tolpar = 0.005
        self.maxiter = 100
        self.maxacc = 500
        self.threads = 16
        self.contacttol = 1.0

        self.message_obj = Message()

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget_settings = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget_settings.setGeometry(QtCore.QRect(1, 1, 340, 725))
        self.tabWidget_settings.setToolTip("")
        self.tabWidget_settings.setObjectName("tabWidget_settings")
        self.reconstructing_tab = QtWidgets.QWidget()
        self.reconstructing_tab.setObjectName("reconstructing_tab")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.reconstructing_tab)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(9, 9, 321, 291))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.MainVerticalLayout_Settings = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.MainVerticalLayout_Settings.setContentsMargins(0, 0, 0, 0)
        self.MainVerticalLayout_Settings.setObjectName("MainVerticalLayout_Settings")
        
        self.config_reconstruction_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.config_reconstruction_button.setObjectName("config_reconstruction_button")
        self.MainVerticalLayout_Settings.addWidget(self.config_reconstruction_button)
        self.config_reconstruction_button.clicked.connect(self.open_reconstruction_settings)
        
        self.load_islet_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.load_islet_button.setStatusTip("")
        self.load_islet_button.setObjectName("load_islet_button")
        self.MainVerticalLayout_Settings.addWidget(self.load_islet_button)
        self.load_islet_button.clicked.connect(self.open_islet_file_button_clicked)

        #self.load_islet_button.clicked.connect(self.initial_islet_stats)
        #self.load_islet_button.clicked.connect(self.plot_initial_islet)

        self.load_islet_status_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.load_islet_status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.load_islet_status_label.setObjectName("load_islet_status_label")
        self.MainVerticalLayout_Settings.addWidget(self.load_islet_status_label)
        

        self.reconstruct_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.reconstruct_button.setObjectName("reconstruct_button")
        self.MainVerticalLayout_Settings.addWidget(self.reconstruct_button)
        self.reconstruct_button.setEnabled(False)
        self.reconstruct_button.clicked.connect(self.optimizeIslet)


        self.reconstruction_status_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.reconstruction_status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.reconstruction_status_label.setObjectName("reconstruction_status_label")
        self.reconstruction_status_label.setEnabled(False)
        self.MainVerticalLayout_Settings.addWidget(self.reconstruction_status_label)


        self.contacts_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.contacts_button.setObjectName("contacts_button")
        self.MainVerticalLayout_Settings.addWidget(self.contacts_button)
        self.contacts_button.setEnabled(False)

        self.contacts_status_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.contacts_status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.contacts_status_label.setObjectName("contacts_status_label")
        self.contacts_status_label.setEnabled(False)
        self.MainVerticalLayout_Settings.addWidget(self.contacts_status_label)

        self.network_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.network_button.setObjectName("network_button")
        self.MainVerticalLayout_Settings.addWidget(self.network_button)
        self.network_button.setEnabled(False)

        self.network_status_button = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.network_status_button.setAlignment(QtCore.Qt.AlignCenter)
        self.network_status_button.setObjectName("network_status_button")
        self.network_status_button.setEnabled(False)
        self.MainVerticalLayout_Settings.addWidget(self.network_status_button)

        self.tabWidget_islet_stats = QtWidgets.QTabWidget(self.reconstructing_tab)
        self.tabWidget_islet_stats.setGeometry(QtCore.QRect(8, 329, 321, 390))
        self.tabWidget_islet_stats.setObjectName("tabWidget_islet_stats")
        self.tab_initial_islet_stats = QtWidgets.QWidget()
        self.tab_initial_islet_stats.setObjectName("tab_initial_islet_stats")
        self.ini_ncells_label = QtWidgets.QLabel(self.tab_initial_islet_stats)
        self.ini_ncells_label.setGeometry(QtCore.QRect(10, 10, 141, 16))
        self.ini_ncells_label.setObjectName("ini_ncells_label")
        self.ini_alpha_cells_label = QtWidgets.QLabel(self.tab_initial_islet_stats)
        self.ini_alpha_cells_label.setGeometry(QtCore.QRect(10, 30, 141, 16))
        self.ini_alpha_cells_label.setObjectName("ini_alpha_cells_label")
        self.ini_beta_cells_label = QtWidgets.QLabel(self.tab_initial_islet_stats)
        self.ini_beta_cells_label.setGeometry(QtCore.QRect(10, 50, 1411, 16))
        self.ini_beta_cells_label.setObjectName("ini_beta_cells_label")
        self.ini_delta_cells_label = QtWidgets.QLabel(self.tab_initial_islet_stats)
        self.ini_delta_cells_label.setGeometry(QtCore.QRect(10, 70, 141, 16))
        self.ini_delta_cells_label.setObjectName("ini_delta_cells_label")
        self.ini_ncells_value = QtWidgets.QLabel(self.tab_initial_islet_stats)
        self.ini_ncells_value.setGeometry(QtCore.QRect(170, 10, 50, 15))
        self.ini_ncells_value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ini_ncells_value.setObjectName("ini_ncells_value")
        self.ini_alphacells_value = QtWidgets.QLabel(self.tab_initial_islet_stats)
        self.ini_alphacells_value.setGeometry(QtCore.QRect(170, 30, 50, 15))
        self.ini_alphacells_value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ini_alphacells_value.setObjectName("ini_alphacells_value")
        self.ini_betacells_value = QtWidgets.QLabel(self.tab_initial_islet_stats)
        self.ini_betacells_value.setGeometry(QtCore.QRect(170, 50, 50, 15))
        self.ini_betacells_value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ini_betacells_value.setObjectName("ini_betacells_value")
        self.ini_deltacells_value = QtWidgets.QLabel(self.tab_initial_islet_stats)
        self.ini_deltacells_value.setGeometry(QtCore.QRect(170, 70, 50, 15))
        self.ini_deltacells_value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ini_deltacells_value.setObjectName("ini_deltacells_value")
        self.ini_ncells_perc = QtWidgets.QLabel(self.tab_initial_islet_stats)
        self.ini_ncells_perc.setGeometry(QtCore.QRect(250, 10, 50, 15))
        self.ini_ncells_perc.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ini_ncells_perc.setObjectName("ini_ncells_perc")
        self.ini_alphacells_perc = QtWidgets.QLabel(self.tab_initial_islet_stats)
        self.ini_alphacells_perc.setGeometry(QtCore.QRect(250, 30, 50, 15))
        self.ini_alphacells_perc.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ini_alphacells_perc.setObjectName("ini_alphacells_perc")
        self.ini_betacells_perc = QtWidgets.QLabel(self.tab_initial_islet_stats)
        self.ini_betacells_perc.setGeometry(QtCore.QRect(250, 50, 50, 15))
        self.ini_betacells_perc.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ini_betacells_perc.setObjectName("ini_betacells_perc")
        self.ini_deltacells_perc = QtWidgets.QLabel(self.tab_initial_islet_stats)
        self.ini_deltacells_perc.setGeometry(QtCore.QRect(250, 70, 50, 15))
        self.ini_deltacells_perc.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ini_deltacells_perc.setObjectName("ini_deltacells_perc")
        self.tabWidget_islet_stats.addTab(self.tab_initial_islet_stats, "")
        self.tab_final_islet_stats = QtWidgets.QWidget()
        self.tab_final_islet_stats.setObjectName("tab_final_islet_stats")
        self.fin_deltacells_value = QtWidgets.QLabel(self.tab_final_islet_stats)
        self.fin_deltacells_value.setGeometry(QtCore.QRect(170, 70, 50, 15))
        self.fin_deltacells_value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.fin_deltacells_value.setObjectName("fin_deltacells_value")
        self.fin_ncells_value = QtWidgets.QLabel(self.tab_final_islet_stats)
        self.fin_ncells_value.setGeometry(QtCore.QRect(170, 10, 50, 15))
        self.fin_ncells_value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.fin_ncells_value.setObjectName("fin_ncells_value")
        self.fin_alphacells_perc = QtWidgets.QLabel(self.tab_final_islet_stats)
        self.fin_alphacells_perc.setGeometry(QtCore.QRect(250, 30, 50, 15))
        self.fin_alphacells_perc.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.fin_alphacells_perc.setObjectName("fin_alphacells_perc")
        self.fin_betacells_value = QtWidgets.QLabel(self.tab_final_islet_stats)
        self.fin_betacells_value.setGeometry(QtCore.QRect(170, 50, 50, 15))
        self.fin_betacells_value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.fin_betacells_value.setObjectName("fin_betacells_value")
        self.fin_betacells_perc = QtWidgets.QLabel(self.tab_final_islet_stats)
        self.fin_betacells_perc.setGeometry(QtCore.QRect(250, 50, 50, 15))
        self.fin_betacells_perc.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.fin_betacells_perc.setObjectName("fin_betacells_perc")
        self.fin_delta_cells_label = QtWidgets.QLabel(self.tab_final_islet_stats)
        self.fin_delta_cells_label.setGeometry(QtCore.QRect(10, 70, 141, 16))
        self.fin_delta_cells_label.setObjectName("fin_delta_cells_label")
        self.fin_ncells_perc = QtWidgets.QLabel(self.tab_final_islet_stats)
        self.fin_ncells_perc.setGeometry(QtCore.QRect(250, 10, 50, 15))
        self.fin_ncells_perc.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.fin_ncells_perc.setObjectName("fin_ncells_perc")
        self.fin_beta_cells_label = QtWidgets.QLabel(self.tab_final_islet_stats)
        self.fin_beta_cells_label.setGeometry(QtCore.QRect(10, 50, 1411, 16))
        self.fin_beta_cells_label.setObjectName("fin_beta_cells_label")
        self.fin_ncells_label = QtWidgets.QLabel(self.tab_final_islet_stats)
        self.fin_ncells_label.setGeometry(QtCore.QRect(10, 10, 141, 16))
        self.fin_ncells_label.setObjectName("fin_ncells_label")
        self.fin_alpha_cells_label = QtWidgets.QLabel(self.tab_final_islet_stats)
        self.fin_alpha_cells_label.setGeometry(QtCore.QRect(10, 30, 141, 16))
        self.fin_alpha_cells_label.setObjectName("fin_alpha_cells_label")
        self.fin_alphacells_value = QtWidgets.QLabel(self.tab_final_islet_stats)
        self.fin_alphacells_value.setGeometry(QtCore.QRect(170, 30, 50, 15))
        self.fin_alphacells_value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.fin_alphacells_value.setObjectName("fin_alphacells_value")
        self.fin_deltacells_perc = QtWidgets.QLabel(self.tab_final_islet_stats)
        self.fin_deltacells_perc.setGeometry(QtCore.QRect(250, 70, 50, 15))
        self.fin_deltacells_perc.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.fin_deltacells_perc.setObjectName("fin_deltacells_perc")
        self.opt_stats_groupbox = QtWidgets.QGroupBox(self.tab_final_islet_stats)
        self.opt_stats_groupbox.setGeometry(QtCore.QRect(9, 180, 301, 141))
        self.opt_stats_groupbox.setObjectName("opt_stats_groupbox")
        self.perc_of_total_label = QtWidgets.QLabel(self.opt_stats_groupbox)
        self.perc_of_total_label.setGeometry(QtCore.QRect(10, 30, 130, 16))
        self.perc_of_total_label.setObjectName("perc_of_total_label")
        self.n_overlaps_label = QtWidgets.QLabel(self.opt_stats_groupbox)
        self.n_overlaps_label.setGeometry(QtCore.QRect(10, 50, 130, 16))
        self.n_overlaps_label.setObjectName("n_overlaps_label")
        self.total_iter_label = QtWidgets.QLabel(self.opt_stats_groupbox)
        self.total_iter_label.setGeometry(QtCore.QRect(10, 70, 130, 16))
        self.total_iter_label.setObjectName("total_iter_label")
        self.acc_iter_label = QtWidgets.QLabel(self.opt_stats_groupbox)
        self.acc_iter_label.setGeometry(QtCore.QRect(10, 90, 130, 16))
        self.acc_iter_label.setObjectName("acc_iter_label")
        self.comp_time_label = QtWidgets.QLabel(self.opt_stats_groupbox)
        self.comp_time_label.setGeometry(QtCore.QRect(10, 110, 130, 16))
        self.comp_time_label.setObjectName("comp_time_label")
        self.perc_of_total_value = QtWidgets.QLabel(self.opt_stats_groupbox)
        self.perc_of_total_value.setGeometry(QtCore.QRect(180, 30, 100, 15))
        self.perc_of_total_value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.perc_of_total_value.setObjectName("perc_of_total_value")
        self.n_overlaps_value = QtWidgets.QLabel(self.opt_stats_groupbox)
        self.n_overlaps_value.setGeometry(QtCore.QRect(180, 50, 100, 15))
        self.n_overlaps_value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.n_overlaps_value.setObjectName("n_overlaps_value")
        self.total_iter_value = QtWidgets.QLabel(self.opt_stats_groupbox)
        self.total_iter_value.setGeometry(QtCore.QRect(180, 70, 100, 15))
        self.total_iter_value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.total_iter_value.setObjectName("total_iter_value")
        self.acc_iter_value = QtWidgets.QLabel(self.opt_stats_groupbox)
        self.acc_iter_value.setGeometry(QtCore.QRect(180, 90, 100, 15))
        self.acc_iter_value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.acc_iter_value.setObjectName("acc_iter_value")
        self.comp_time_value = QtWidgets.QLabel(self.opt_stats_groupbox)
        self.comp_time_value.setGeometry(QtCore.QRect(180, 110, 100, 15))
        self.comp_time_value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.comp_time_value.setObjectName("comp_time_value")
        self.fin_total_vol_label = QtWidgets.QLabel(self.tab_final_islet_stats)
        self.fin_total_vol_label.setGeometry(QtCore.QRect(10, 90, 141, 16))
        self.fin_total_vol_label.setObjectName("fin_total_vol_label")
        self.fin_total_vol_value = QtWidgets.QLabel(self.tab_final_islet_stats)
        self.fin_total_vol_value.setGeometry(QtCore.QRect(170, 90, 50, 15))
        self.fin_total_vol_value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.fin_total_vol_value.setObjectName("fin_total_vol_value")
        self.fin_total_vol_perc = QtWidgets.QLabel(self.tab_final_islet_stats)
        self.fin_total_vol_perc.setGeometry(QtCore.QRect(250, 90, 50, 15))
        self.fin_total_vol_perc.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.fin_total_vol_perc.setObjectName("fin_total_vol_perc")
        self.fin_alpha_vol_label = QtWidgets.QLabel(self.tab_final_islet_stats)
        self.fin_alpha_vol_label.setGeometry(QtCore.QRect(10, 110, 141, 16))
        self.fin_alpha_vol_label.setObjectName("fin_alpha_vol_label")
        self.fin_alpha_vol_value = QtWidgets.QLabel(self.tab_final_islet_stats)
        self.fin_alpha_vol_value.setGeometry(QtCore.QRect(170, 110, 50, 15))
        self.fin_alpha_vol_value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.fin_alpha_vol_value.setObjectName("fin_alpha_vol_value")
        self.fin_alpha_vol_perc = QtWidgets.QLabel(self.tab_final_islet_stats)
        self.fin_alpha_vol_perc.setGeometry(QtCore.QRect(250, 110, 50, 15))
        self.fin_alpha_vol_perc.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.fin_alpha_vol_perc.setObjectName("fin_alpha_vol_perc")
        self.fin_beta_vol_label = QtWidgets.QLabel(self.tab_final_islet_stats)
        self.fin_beta_vol_label.setGeometry(QtCore.QRect(10, 130, 141, 16))
        self.fin_beta_vol_label.setObjectName("fin_beta_vol_label")
        self.fin_delta_vol_label = QtWidgets.QLabel(self.tab_final_islet_stats)
        self.fin_delta_vol_label.setGeometry(QtCore.QRect(10, 150, 141, 16))
        self.fin_delta_vol_label.setObjectName("fin_delta_vol_label")
        self.fin_beta_vol_value = QtWidgets.QLabel(self.tab_final_islet_stats)
        self.fin_beta_vol_value.setGeometry(QtCore.QRect(170, 130, 50, 15))
        self.fin_beta_vol_value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.fin_beta_vol_value.setObjectName("fin_beta_vol_value")
        self.fin_delta_vol_value = QtWidgets.QLabel(self.tab_final_islet_stats)
        self.fin_delta_vol_value.setGeometry(QtCore.QRect(170, 150, 50, 15))
        self.fin_delta_vol_value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.fin_delta_vol_value.setObjectName("fin_delta_vol_value")
        self.fin_beta_vol_perc = QtWidgets.QLabel(self.tab_final_islet_stats)
        self.fin_beta_vol_perc.setGeometry(QtCore.QRect(250, 130, 50, 15))
        self.fin_beta_vol_perc.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.fin_beta_vol_perc.setObjectName("fin_beta_vol_perc")
        self.fin_delta_vol_perc = QtWidgets.QLabel(self.tab_final_islet_stats)
        self.fin_delta_vol_perc.setGeometry(QtCore.QRect(250, 150, 50, 15))
        self.fin_delta_vol_perc.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.fin_delta_vol_perc.setObjectName("fin_delta_vol_perc")
        self.tabWidget_islet_stats.addTab(self.tab_final_islet_stats, "")
        self.tab_contacts_stats = QtWidgets.QWidget()
        self.tab_contacts_stats.setObjectName("tab_contacts_stats")
        self.total_contacts_label = QtWidgets.QLabel(self.tab_contacts_stats)
        self.total_contacts_label.setGeometry(QtCore.QRect(10, 10, 91, 16))
        self.total_contacts_label.setObjectName("total_contacts_label")
        self.total_contacts_value = QtWidgets.QLabel(self.tab_contacts_stats)
        self.total_contacts_value.setGeometry(QtCore.QRect(170, 10, 57, 15))
        self.total_contacts_value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.total_contacts_value.setObjectName("total_contacts_value")
        self.total_contacts_perc = QtWidgets.QLabel(self.tab_contacts_stats)
        self.total_contacts_perc.setGeometry(QtCore.QRect(250, 10, 50, 15))
        self.total_contacts_perc.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.total_contacts_perc.setObjectName("total_contacts_perc")
        self.homotypic_contacts_label = QtWidgets.QLabel(self.tab_contacts_stats)
        self.homotypic_contacts_label.setGeometry(QtCore.QRect(10, 30, 91, 16))
        self.homotypic_contacts_label.setObjectName("homotypic_contacts_label")
        self.homotypic_contacts_value = QtWidgets.QLabel(self.tab_contacts_stats)
        self.homotypic_contacts_value.setGeometry(QtCore.QRect(170, 30, 57, 15))
        self.homotypic_contacts_value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.homotypic_contacts_value.setObjectName("homotypic_contacts_value")
        self.homotypic_contacts_perc = QtWidgets.QLabel(self.tab_contacts_stats)
        self.homotypic_contacts_perc.setGeometry(QtCore.QRect(250, 30, 50, 15))
        self.homotypic_contacts_perc.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.homotypic_contacts_perc.setObjectName("homotypic_contacts_perc")
        self.heterotypic_contacts_label = QtWidgets.QLabel(self.tab_contacts_stats)
        self.heterotypic_contacts_label.setGeometry(QtCore.QRect(10, 50, 91, 16))
        self.heterotypic_contacts_label.setObjectName("heterotypic_contacts_label")
        self.heterotypic_contacts_value = QtWidgets.QLabel(self.tab_contacts_stats)
        self.heterotypic_contacts_value.setGeometry(QtCore.QRect(170, 50, 57, 15))
        self.heterotypic_contacts_value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.heterotypic_contacts_value.setObjectName("heterotypic_contacts_value")
        self.heterotypic_contacts_perc = QtWidgets.QLabel(self.tab_contacts_stats)
        self.heterotypic_contacts_perc.setGeometry(QtCore.QRect(250, 50, 50, 15))
        self.heterotypic_contacts_perc.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.heterotypic_contacts_perc.setObjectName("heterotypic_contacts_perc")
        self.alphaalpha_contacts_label = QtWidgets.QLabel(self.tab_contacts_stats)
        self.alphaalpha_contacts_label.setGeometry(QtCore.QRect(10, 70, 91, 16))
        self.alphaalpha_contacts_label.setObjectName("alphaalpha_contacts_label")
        self.alphaalpha_contacts_value = QtWidgets.QLabel(self.tab_contacts_stats)
        self.alphaalpha_contacts_value.setGeometry(QtCore.QRect(170, 70, 57, 15))
        self.alphaalpha_contacts_value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.alphaalpha_contacts_value.setObjectName("alphaalpha_contacts_value")
        self.alphaalpha_contacts_perc = QtWidgets.QLabel(self.tab_contacts_stats)
        self.alphaalpha_contacts_perc.setGeometry(QtCore.QRect(250, 70, 50, 15))
        self.alphaalpha_contacts_perc.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.alphaalpha_contacts_perc.setObjectName("alphaalpha_contacts_perc")
        self.betabeta_contacts_label = QtWidgets.QLabel(self.tab_contacts_stats)
        self.betabeta_contacts_label.setGeometry(QtCore.QRect(10, 90, 91, 16))
        self.betabeta_contacts_label.setObjectName("betabeta_contacts_label")
        self.betabeta_contacts_value = QtWidgets.QLabel(self.tab_contacts_stats)
        self.betabeta_contacts_value.setGeometry(QtCore.QRect(170, 90, 57, 15))
        self.betabeta_contacts_value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.betabeta_contacts_value.setObjectName("betabeta_contacts_value")
        self.betabeta_contacts_perc = QtWidgets.QLabel(self.tab_contacts_stats)
        self.betabeta_contacts_perc.setGeometry(QtCore.QRect(250, 90, 50, 15))
        self.betabeta_contacts_perc.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.betabeta_contacts_perc.setObjectName("betabeta_contacts_perc")
        self.deltadelta_contacts_label = QtWidgets.QLabel(self.tab_contacts_stats)
        self.deltadelta_contacts_label.setGeometry(QtCore.QRect(10, 110, 91, 16))
        self.deltadelta_contacts_label.setObjectName("deltadelta_contacts_label")
        self.deltadelta_contacts_value = QtWidgets.QLabel(self.tab_contacts_stats)
        self.deltadelta_contacts_value.setGeometry(QtCore.QRect(170, 110, 57, 15))
        self.deltadelta_contacts_value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.deltadelta_contacts_value.setObjectName("deltadelta_contacts_value")
        self.deltadelta_contacts_perc = QtWidgets.QLabel(self.tab_contacts_stats)
        self.deltadelta_contacts_perc.setGeometry(QtCore.QRect(250, 110, 50, 15))
        self.deltadelta_contacts_perc.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.deltadelta_contacts_perc.setObjectName("deltadelta_contacts_perc")
        self.alphabeta_contacts_label = QtWidgets.QLabel(self.tab_contacts_stats)
        self.alphabeta_contacts_label.setGeometry(QtCore.QRect(10, 130, 91, 16))
        self.alphabeta_contacts_label.setObjectName("alphabeta_contacts_label")
        self.alphabeta_contacts_value = QtWidgets.QLabel(self.tab_contacts_stats)
        self.alphabeta_contacts_value.setGeometry(QtCore.QRect(170, 130, 57, 15))
        self.alphabeta_contacts_value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.alphabeta_contacts_value.setObjectName("alphabeta_contacts_value")
        self.alphabeta_contacts_perc = QtWidgets.QLabel(self.tab_contacts_stats)
        self.alphabeta_contacts_perc.setGeometry(QtCore.QRect(250, 130, 50, 15))
        self.alphabeta_contacts_perc.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.alphabeta_contacts_perc.setObjectName("alphabeta_contacts_perc")
        self.alphadelta_contacts_label = QtWidgets.QLabel(self.tab_contacts_stats)
        self.alphadelta_contacts_label.setGeometry(QtCore.QRect(10, 150, 91, 16))
        self.alphadelta_contacts_label.setObjectName("alphadelta_contacts_label")
        self.alphadelta_contacts_value = QtWidgets.QLabel(self.tab_contacts_stats)
        self.alphadelta_contacts_value.setGeometry(QtCore.QRect(170, 150, 57, 15))
        self.alphadelta_contacts_value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.alphadelta_contacts_value.setObjectName("alphadelta_contacts_value")
        self.alphadelta_contacts_perc = QtWidgets.QLabel(self.tab_contacts_stats)
        self.alphadelta_contacts_perc.setGeometry(QtCore.QRect(250, 150, 50, 15))
        self.alphadelta_contacts_perc.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.alphadelta_contacts_perc.setObjectName("alphadelta_contacts_perc")
        self.betadelta_contacts_label = QtWidgets.QLabel(self.tab_contacts_stats)
        self.betadelta_contacts_label.setGeometry(QtCore.QRect(10, 170, 91, 16))
        self.betadelta_contacts_label.setObjectName("betadelta_contacts_label")
        self.betadelta_contacts_value = QtWidgets.QLabel(self.tab_contacts_stats)
        self.betadelta_contacts_value.setGeometry(QtCore.QRect(170, 170, 57, 15))
        self.betadelta_contacts_value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.betadelta_contacts_value.setObjectName("betadelta_contacts_value")
        self.betadelta_contacts_perc = QtWidgets.QLabel(self.tab_contacts_stats)
        self.betadelta_contacts_perc.setGeometry(QtCore.QRect(250, 170, 50, 15))
        self.betadelta_contacts_perc.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.betadelta_contacts_perc.setObjectName("betadelta_contacts_perc")
        self.tabWidget_islet_stats.addTab(self.tab_contacts_stats, "")
        self.tab_network_stats = QtWidgets.QWidget()
        self.tab_network_stats.setObjectName("tab_network_stats")
        self.degree_label = QtWidgets.QLabel(self.tab_network_stats)
        self.degree_label.setGeometry(QtCore.QRect(10, 10, 100, 15))
        self.degree_label.setObjectName("degree_label")
        self.density_label = QtWidgets.QLabel(self.tab_network_stats)
        self.density_label.setGeometry(QtCore.QRect(10, 30, 100, 15))
        self.density_label.setObjectName("density_label")
        self.clustering_label = QtWidgets.QLabel(self.tab_network_stats)
        self.clustering_label.setGeometry(QtCore.QRect(10, 50, 100, 15))
        self.clustering_label.setObjectName("clustering_label")
        self.diameter_label = QtWidgets.QLabel(self.tab_network_stats)
        self.diameter_label.setGeometry(QtCore.QRect(10, 70, 100, 15))
        self.diameter_label.setObjectName("diameter_label")
        self.efficiency_label = QtWidgets.QLabel(self.tab_network_stats)
        self.efficiency_label.setGeometry(QtCore.QRect(10, 90, 100, 15))
        self.efficiency_label.setObjectName("efficiency_label")
        self.degree_value = QtWidgets.QLabel(self.tab_network_stats)
        self.degree_value.setGeometry(QtCore.QRect(170, 10, 100, 15))
        self.degree_value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.degree_value.setObjectName("degree_value")
        self.density_value = QtWidgets.QLabel(self.tab_network_stats)
        self.density_value.setGeometry(QtCore.QRect(170, 30, 100, 15))
        self.density_value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.density_value.setObjectName("density_value")
        self.clustering_value = QtWidgets.QLabel(self.tab_network_stats)
        self.clustering_value.setGeometry(QtCore.QRect(170, 50, 100, 15))
        self.clustering_value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.clustering_value.setObjectName("clustering_value")
        self.diameter_value = QtWidgets.QLabel(self.tab_network_stats)
        self.diameter_value.setGeometry(QtCore.QRect(170, 70, 100, 15))
        self.diameter_value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.diameter_value.setObjectName("diameter_value")
        self.efficiency_value = QtWidgets.QLabel(self.tab_network_stats)
        self.efficiency_value.setGeometry(QtCore.QRect(170, 90, 100, 15))
        self.efficiency_value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.efficiency_value.setObjectName("efficiency_value")
        self.tabWidget_islet_stats.addTab(self.tab_network_stats, "")
        self.tabWidget_settings.addTab(self.reconstructing_tab, "")
        self.tab_plots = QtWidgets.QWidget()
        self.tab_plots.setObjectName("tab_plots")
        self.opt_plot_groupbox = QtWidgets.QGroupBox(self.tab_plots)
        self.opt_plot_groupbox.setGeometry(QtCore.QRect(10, 5, 321, 61))
        self.opt_plot_groupbox.setObjectName("opt_plot_groupbox")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.opt_plot_groupbox)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(9, 20, 301, 41))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.plot_convergence_button = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.plot_convergence_button.setObjectName("plot_convergence_button")
        self.verticalLayout.addWidget(self.plot_convergence_button)
        self.arch_plots_groupbox = QtWidgets.QGroupBox(self.tab_plots)
        self.arch_plots_groupbox.setGeometry(QtCore.QRect(10, 75, 321, 141))
        self.arch_plots_groupbox.setObjectName("arch_plots_groupbox")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.arch_plots_groupbox)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(9, 20, 301, 121))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.cell_number_plot_button = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.cell_number_plot_button.setObjectName("cell_number_plot_button")
        self.verticalLayout_2.addWidget(self.cell_number_plot_button)
        self.radii_plot_button = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.radii_plot_button.setObjectName("radii_plot_button")
        self.verticalLayout_2.addWidget(self.radii_plot_button)
        self.islet_volume_plot_button = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.islet_volume_plot_button.setObjectName("islet_volume_plot_button")
        self.verticalLayout_2.addWidget(self.islet_volume_plot_button)
        self.connectivity_plots_groupbox = QtWidgets.QGroupBox(self.tab_plots)
        self.connectivity_plots_groupbox.setGeometry(QtCore.QRect(9, 230, 321, 61))
        self.connectivity_plots_groupbox.setObjectName("connectivity_plots_groupbox")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.connectivity_plots_groupbox)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(9, 19, 301, 41))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.contacts_plot_button = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.contacts_plot_button.setObjectName("contacts_plot_button")
        self.verticalLayout_3.addWidget(self.contacts_plot_button)
        self.network_plots_groupbox = QtWidgets.QGroupBox(self.tab_plots)
        self.network_plots_groupbox.setGeometry(QtCore.QRect(10, 300, 321, 80))
        self.network_plots_groupbox.setObjectName("network_plots_groupbox")
        self.verticalLayoutWidget_5 = QtWidgets.QWidget(self.network_plots_groupbox)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(9, 20, 301, 61))
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.network_metrics_plots_butthon = QtWidgets.QPushButton(self.verticalLayoutWidget_5)
        self.network_metrics_plots_butthon.setObjectName("network_metrics_plots_butthon")
        self.verticalLayout_5.addWidget(self.network_metrics_plots_butthon)
        self.tabWidget_settings.addTab(self.tab_plots, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.intrinsicfreq_groupbox = QtWidgets.QGroupBox(self.tab_2)
        self.intrinsicfreq_groupbox.setGeometry(QtCore.QRect(10, 10, 321, 111))
        self.intrinsicfreq_groupbox.setObjectName("intrinsicfreq_groupbox")
        self.verticalLayoutWidget_6 = QtWidgets.QWidget(self.intrinsicfreq_groupbox)
        self.verticalLayoutWidget_6.setGeometry(QtCore.QRect(9, 19, 301, 91))
        self.verticalLayoutWidget_6.setObjectName("verticalLayoutWidget_6")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_6)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.intrinsicfreq_constant_radio = QtWidgets.QRadioButton(self.verticalLayoutWidget_6)
        self.intrinsicfreq_constant_radio.setObjectName("intrinsicfreq_constant_radio")
        self.verticalLayout_6.addWidget(self.intrinsicfreq_constant_radio)
        self.intrinsicfreq_random_radio = QtWidgets.QRadioButton(self.verticalLayoutWidget_6)
        self.intrinsicfreq_random_radio.setObjectName("intrinsicfreq_random_radio")
        self.verticalLayout_6.addWidget(self.intrinsicfreq_random_radio)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.intrinsicfreq_file_radio = QtWidgets.QRadioButton(self.verticalLayoutWidget_6)
        self.intrinsicfreq_file_radio.setObjectName("intrinsicfreq_file_radio")
        self.horizontalLayout.addWidget(self.intrinsicfreq_file_radio)
        self.intrinsicfreq_file_button = QtWidgets.QPushButton(self.verticalLayoutWidget_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.intrinsicfreq_file_button.sizePolicy().hasHeightForWidth())
        self.intrinsicfreq_file_button.setSizePolicy(sizePolicy)
        self.intrinsicfreq_file_button.setObjectName("intrinsicfreq_file_button")
        self.horizontalLayout.addWidget(self.intrinsicfreq_file_button)
        self.verticalLayout_6.addLayout(self.horizontalLayout)
        self.intitialphase_groupbox = QtWidgets.QGroupBox(self.tab_2)
        self.intitialphase_groupbox.setGeometry(QtCore.QRect(10, 130, 321, 111))
        self.intitialphase_groupbox.setObjectName("intitialphase_groupbox")
        self.verticalLayoutWidget_7 = QtWidgets.QWidget(self.intitialphase_groupbox)
        self.verticalLayoutWidget_7.setGeometry(QtCore.QRect(9, 19, 301, 91))
        self.verticalLayoutWidget_7.setObjectName("verticalLayoutWidget_7")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_7)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.initialphase_constant_radio = QtWidgets.QRadioButton(self.verticalLayoutWidget_7)
        self.initialphase_constant_radio.setObjectName("initialphase_constant_radio")
        self.verticalLayout_7.addWidget(self.initialphase_constant_radio)
        self.initialphase_random_radio = QtWidgets.QRadioButton(self.verticalLayoutWidget_7)
        self.initialphase_random_radio.setObjectName("initialphase_random_radio")
        self.verticalLayout_7.addWidget(self.initialphase_random_radio)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.intitialphase_file_radio = QtWidgets.QRadioButton(self.verticalLayoutWidget_7)
        self.intitialphase_file_radio.setObjectName("intitialphase_file_radio")
        self.horizontalLayout_2.addWidget(self.intitialphase_file_radio)
        self.intitialphase_file_button = QtWidgets.QPushButton(self.verticalLayoutWidget_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.intitialphase_file_button.sizePolicy().hasHeightForWidth())
        self.intitialphase_file_button.setSizePolicy(sizePolicy)
        self.intitialphase_file_button.setObjectName("intitialphase_file_button")
        self.horizontalLayout_2.addWidget(self.intitialphase_file_button)
        self.verticalLayout_7.addLayout(self.horizontalLayout_2)
        self.interaction_strength_groupbox = QtWidgets.QGroupBox(self.tab_2)
        self.interaction_strength_groupbox.setGeometry(QtCore.QRect(10, 250, 311, 111))
        self.interaction_strength_groupbox.setObjectName("interaction_strength_groupbox")
        self.verticalLayoutWidget_8 = QtWidgets.QWidget(self.interaction_strength_groupbox)
        self.verticalLayoutWidget_8.setGeometry(QtCore.QRect(9, 19, 301, 91))
        self.verticalLayoutWidget_8.setObjectName("verticalLayoutWidget_8")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_8)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.constant_strength_constant_radio = QtWidgets.QRadioButton(self.verticalLayoutWidget_8)
        self.constant_strength_constant_radio.setObjectName("constant_strength_constant_radio")
        self.verticalLayout_8.addWidget(self.constant_strength_constant_radio)
        self.interaction_strength_random_radio = QtWidgets.QRadioButton(self.verticalLayoutWidget_8)
        self.interaction_strength_random_radio.setObjectName("interaction_strength_random_radio")
        self.verticalLayout_8.addWidget(self.interaction_strength_random_radio)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.interaction_strength_file_label = QtWidgets.QRadioButton(self.verticalLayoutWidget_8)
        self.interaction_strength_file_label.setObjectName("interaction_strength_file_label")
        self.horizontalLayout_3.addWidget(self.interaction_strength_file_label)
        self.interaction_strength_file_button = QtWidgets.QPushButton(self.verticalLayoutWidget_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.interaction_strength_file_button.sizePolicy().hasHeightForWidth())
        self.interaction_strength_file_button.setSizePolicy(sizePolicy)
        self.interaction_strength_file_button.setObjectName("interaction_strength_file_button")
        self.horizontalLayout_3.addWidget(self.interaction_strength_file_button)
        self.verticalLayout_8.addLayout(self.horizontalLayout_3)
        self.sim_settings_groupbox = QtWidgets.QGroupBox(self.tab_2)
        self.sim_settings_groupbox.setGeometry(QtCore.QRect(10, 370, 321, 101))
        self.sim_settings_groupbox.setObjectName("sim_settings_groupbox")
        self.formLayoutWidget = QtWidgets.QWidget(self.sim_settings_groupbox)
        self.formLayoutWidget.setGeometry(QtCore.QRect(9, 29, 301, 61))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.sim_total_time_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.sim_total_time_label.setObjectName("sim_total_time_label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.sim_total_time_label)
        self.total_time_lineedit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.total_time_lineedit.setMaximumSize(QtCore.QSize(500, 16777215))
        self.total_time_lineedit.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.total_time_lineedit.setObjectName("total_time_lineedit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.total_time_lineedit)
        self.sim_timestep_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.sim_timestep_label.setObjectName("sim_timestep_label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.sim_timestep_label)
        self.timestep_lineedit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.timestep_lineedit.setObjectName("timestep_lineedit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.timestep_lineedit)
        self.run_simulation_button = QtWidgets.QPushButton(self.tab_2)
        self.run_simulation_button.setGeometry(QtCore.QRect(10, 490, 321, 81))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.run_simulation_button.sizePolicy().hasHeightForWidth())
        self.run_simulation_button.setSizePolicy(sizePolicy)
        self.run_simulation_button.setObjectName("run_simulation_button")
        self.tabWidget_settings.addTab(self.tab_2, "")
        self.tabWidget_Plots = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget_Plots.setGeometry(QtCore.QRect(342, 1, 681, 725))
        self.tabWidget_Plots.setObjectName("tabWidget_Plots")
        self.initial_islet_plot_tab = QtWidgets.QWidget()
        self.initial_islet_plot_tab.setObjectName("initial_islet_plot_tab")
        self.tabWidget_Plots.addTab(self.initial_islet_plot_tab, "")
        self.final_islet_plot_tab = QtWidgets.QWidget()
        self.final_islet_plot_tab.setObjectName("final_islet_plot_tab")
        self.tabWidget_Plots.addTab(self.final_islet_plot_tab, "")
        self.contacts_plot_tab = QtWidgets.QWidget()
        self.contacts_plot_tab.setObjectName("contacts_plot_tab")
        self.tabWidget_Plots.addTab(self.contacts_plot_tab, "")
        self.networks_plot_tab = QtWidgets.QWidget()
        self.networks_plot_tab.setObjectName("networks_plot_tab")
        self.tabWidget_Plots.addTab(self.networks_plot_tab, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1024, 20))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionExport_data = QtWidgets.QAction(MainWindow)
        self.actionExport_data.setObjectName("actionExport_data")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionDocumentation = QtWidgets.QAction(MainWindow)
        self.actionDocumentation.setObjectName("actionDocumentation")
        
        self.actionReconstruction = QtWidgets.QAction(MainWindow)
        self.actionReconstruction.setObjectName("actionReconstruction")
        self.actionReconstruction.triggered.connect(self.open_reconstruction_settings)

        self.actionContacts = QtWidgets.QAction(MainWindow)
        self.actionContacts.setObjectName("actionContacts")
        self.actionLoad_data = QtWidgets.QAction(MainWindow)
        self.actionLoad_data.setWhatsThis("")
        self.actionLoad_data.setObjectName("actionLoad_data")
        self.actionRestart = QtWidgets.QAction(MainWindow)
        self.actionRestart.setWhatsThis("")
        self.actionRestart.triggered.connect(self.restart)
        self.actionLoad_data.setObjectName("actionRestart")
        self.actionSimulation = QtWidgets.QAction(MainWindow)
        self.actionSimulation.setObjectName("actionSimulation")
        self.actionGraphs = QtWidgets.QAction(MainWindow)
        self.actionGraphs.setObjectName("actionGraphs")
        self.menuFile.addAction(self.actionExport_data)
        self.menuFile.addAction(self.actionLoad_data)
        self.menuFile.addAction(self.actionRestart)
        self.menuSettings.addAction(self.actionReconstruction)
        self.menuSettings.addAction(self.actionSimulation)
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionDocumentation)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        #self.tabWidget_settings.setCurrentIndex(0)
        self.tabWidget_settings.setTabEnabled(1, False)
        self.tabWidget_settings.setTabEnabled(2, False)
        self.tabWidget_settings.setTabEnabled(3, False)


        #self.tabWidget_islet_stats.setCurrentIndex(0)
        self.tabWidget_islet_stats.setTabEnabled(0, False)
        self.tabWidget_islet_stats.setTabEnabled(1, False)
        self.tabWidget_islet_stats.setTabEnabled(2, False)
        self.tabWidget_islet_stats.setTabEnabled(3, False)
        
        
        #self.tabWidget_Plots.setCurrentIndex(0)
        self.tabWidget_Plots.setTabEnabled(0, False)
        self.tabWidget_Plots.setTabEnabled(1, False)
        self.tabWidget_Plots.setTabEnabled(2, False)
        self.tabWidget_Plots.setTabEnabled(3, False)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "IsletLab"))
        self.config_reconstruction_button.setWhatsThis(_translate("MainWindow", "whatsthis"))
        self.config_reconstruction_button.setText(_translate("MainWindow", "Reconstruction settings"))
        self.load_islet_button.setText(_translate("MainWindow", "Load initial islet"))
        self.load_islet_status_label.setText(_translate("MainWindow", "Initial islet not loaded"))
        self.reconstruct_button.setText(_translate("MainWindow", "Reconstruct islet"))
        self.reconstruction_status_label.setText(_translate("MainWindow", "Islet not reconstructed"))
        self.contacts_button.setText(_translate("MainWindow", "Cell-to-cell contacts"))
        self.contacts_status_label.setText(_translate("MainWindow", "Contacts not identified"))
        self.network_button.setText(_translate("MainWindow", "Build Network"))
        self.network_status_button.setText(_translate("MainWindow", "Network not generated"))
        self.ini_ncells_label.setText(_translate("MainWindow", "Number of cells"))
        self.ini_alpha_cells_label.setText(_translate("MainWindow", "Number of alpha cells"))
        self.ini_beta_cells_label.setText(_translate("MainWindow", "Number of beta cells"))
        self.ini_delta_cells_label.setText(_translate("MainWindow", "Number of delta cells"))
        self.ini_ncells_value.setText(_translate("MainWindow", "0"))
        self.ini_alphacells_value.setText(_translate("MainWindow", "0"))
        self.ini_betacells_value.setText(_translate("MainWindow", "0"))
        self.ini_deltacells_value.setText(_translate("MainWindow", "0"))
        self.ini_ncells_perc.setText(_translate("MainWindow", "0"))
        self.ini_alphacells_perc.setText(_translate("MainWindow", "0"))
        self.ini_betacells_perc.setText(_translate("MainWindow", "0"))
        self.ini_deltacells_perc.setText(_translate("MainWindow", "0"))
        self.tabWidget_islet_stats.setTabText(self.tabWidget_islet_stats.indexOf(self.tab_initial_islet_stats), _translate("MainWindow", "Initial islet"))
        self.fin_deltacells_value.setText(_translate("MainWindow", "0"))
        self.fin_ncells_value.setText(_translate("MainWindow", "0"))
        self.fin_alphacells_perc.setText(_translate("MainWindow", "0"))
        self.fin_betacells_value.setText(_translate("MainWindow", "0"))
        self.fin_betacells_perc.setText(_translate("MainWindow", "0"))
        self.fin_delta_cells_label.setText(_translate("MainWindow", "Number of delta cells"))
        self.fin_ncells_perc.setText(_translate("MainWindow", "0"))
        self.fin_beta_cells_label.setText(_translate("MainWindow", "Number of beta cells"))
        self.fin_ncells_label.setText(_translate("MainWindow", "Number of cells"))
        self.fin_alpha_cells_label.setText(_translate("MainWindow", "Number of alpha cells"))
        self.fin_alphacells_value.setText(_translate("MainWindow", "0"))
        self.fin_deltacells_perc.setText(_translate("MainWindow", "0"))
        self.opt_stats_groupbox.setTitle(_translate("MainWindow", "Optimization "))
        self.perc_of_total_label.setText(_translate("MainWindow", "% of experimental"))
        self.n_overlaps_label.setText(_translate("MainWindow", "Number of overlaps"))
        self.total_iter_label.setText(_translate("MainWindow", "Total iterations"))
        self.acc_iter_label.setText(_translate("MainWindow", "Accepted iterations"))
        self.comp_time_label.setText(_translate("MainWindow", "Computing time"))
        self.perc_of_total_value.setText(_translate("MainWindow", "0"))
        self.n_overlaps_value.setText(_translate("MainWindow", "0"))
        self.total_iter_value.setText(_translate("MainWindow", "0"))
        self.acc_iter_value.setText(_translate("MainWindow", "0"))
        self.comp_time_value.setText(_translate("MainWindow", "0"))
        self.fin_total_vol_label.setText(_translate("MainWindow", "Total cell volume"))
        self.fin_total_vol_value.setText(_translate("MainWindow", "0"))
        self.fin_total_vol_perc.setText(_translate("MainWindow", "0"))
        self.fin_alpha_vol_label.setText(_translate("MainWindow", "Alpha cell volume"))
        self.fin_alpha_vol_value.setText(_translate("MainWindow", "0"))
        self.fin_alpha_vol_perc.setText(_translate("MainWindow", "0"))
        self.fin_beta_vol_label.setText(_translate("MainWindow", "Beta cell volume"))
        self.fin_delta_vol_label.setText(_translate("MainWindow", "Delta cell volume"))
        self.fin_beta_vol_value.setText(_translate("MainWindow", "0"))
        self.fin_delta_vol_value.setText(_translate("MainWindow", "0"))
        self.fin_beta_vol_perc.setText(_translate("MainWindow", "0"))
        self.fin_delta_vol_perc.setText(_translate("MainWindow", "0"))
        self.tabWidget_islet_stats.setTabText(self.tabWidget_islet_stats.indexOf(self.tab_final_islet_stats), _translate("MainWindow", "Final islet"))
        self.total_contacts_label.setText(_translate("MainWindow", "Total contacts"))
        self.total_contacts_value.setText(_translate("MainWindow", "0"))
        self.total_contacts_perc.setText(_translate("MainWindow", "0"))
        self.homotypic_contacts_label.setText(_translate("MainWindow", "Homotypic"))
        self.homotypic_contacts_value.setText(_translate("MainWindow", "0"))
        self.homotypic_contacts_perc.setText(_translate("MainWindow", "0"))
        self.heterotypic_contacts_label.setText(_translate("MainWindow", "Heterotypic"))
        self.heterotypic_contacts_value.setText(_translate("MainWindow", "0"))
        self.heterotypic_contacts_perc.setText(_translate("MainWindow", "0"))
        self.alphaalpha_contacts_label.setText(_translate("MainWindow", "alpha - alpha"))
        self.alphaalpha_contacts_value.setText(_translate("MainWindow", "0"))
        self.alphaalpha_contacts_perc.setText(_translate("MainWindow", "0"))
        self.betabeta_contacts_label.setText(_translate("MainWindow", "beta - beta"))
        self.betabeta_contacts_value.setText(_translate("MainWindow", "0"))
        self.betabeta_contacts_perc.setText(_translate("MainWindow", "0"))
        self.deltadelta_contacts_label.setText(_translate("MainWindow", "delta - delta"))
        self.deltadelta_contacts_value.setText(_translate("MainWindow", "0"))
        self.deltadelta_contacts_perc.setText(_translate("MainWindow", "0"))
        self.alphabeta_contacts_label.setText(_translate("MainWindow", "alpha - beta"))
        self.alphabeta_contacts_value.setText(_translate("MainWindow", "0"))
        self.alphabeta_contacts_perc.setText(_translate("MainWindow", "0"))
        self.alphadelta_contacts_label.setText(_translate("MainWindow", "alpha - delta"))
        self.alphadelta_contacts_value.setText(_translate("MainWindow", "0"))
        self.alphadelta_contacts_perc.setText(_translate("MainWindow", "0"))
        self.betadelta_contacts_label.setText(_translate("MainWindow", "beta - delta"))
        self.betadelta_contacts_value.setText(_translate("MainWindow", "0"))
        self.betadelta_contacts_perc.setText(_translate("MainWindow", "0"))
        self.tabWidget_islet_stats.setTabText(self.tabWidget_islet_stats.indexOf(self.tab_contacts_stats), _translate("MainWindow", "Contacts"))
        self.degree_label.setText(_translate("MainWindow", "Degree"))
        self.density_label.setText(_translate("MainWindow", "Density"))
        self.clustering_label.setText(_translate("MainWindow", "Clustering"))
        self.diameter_label.setText(_translate("MainWindow", "Diameter"))
        self.efficiency_label.setText(_translate("MainWindow", "Efficiency"))
        self.degree_value.setText(_translate("MainWindow", "0"))
        self.density_value.setText(_translate("MainWindow", "0"))
        self.clustering_value.setText(_translate("MainWindow", "0"))
        self.diameter_value.setText(_translate("MainWindow", "0"))
        self.efficiency_value.setText(_translate("MainWindow", "0"))
        self.tabWidget_islet_stats.setTabText(self.tabWidget_islet_stats.indexOf(self.tab_network_stats), _translate("MainWindow", "Network"))
        self.tabWidget_settings.setTabText(self.tabWidget_settings.indexOf(self.reconstructing_tab), _translate("MainWindow", "Reconstruction"))
        self.opt_plot_groupbox.setTitle(_translate("MainWindow", "Optimization"))
        self.plot_convergence_button.setText(_translate("MainWindow", "Convergence"))
        self.arch_plots_groupbox.setTitle(_translate("MainWindow", "Architecture"))
        self.cell_number_plot_button.setText(_translate("MainWindow", "Number of cells"))
        self.radii_plot_button.setText(_translate("MainWindow", "Cells radii"))
        self.islet_volume_plot_button.setText(_translate("MainWindow", "Islet volume"))
        self.connectivity_plots_groupbox.setTitle(_translate("MainWindow", "Connectivity"))
        self.contacts_plot_button.setText(_translate("MainWindow", "Cell-to-cell contacts"))
        self.network_plots_groupbox.setTitle(_translate("MainWindow", "Network"))
        self.network_metrics_plots_butthon.setText(_translate("MainWindow", "Metrics"))
        self.tabWidget_settings.setTabText(self.tabWidget_settings.indexOf(self.tab_plots), _translate("MainWindow", "Graphs"))
        self.intrinsicfreq_groupbox.setTitle(_translate("MainWindow", "Intrinsic frequency"))
        self.intrinsicfreq_constant_radio.setText(_translate("MainWindow", "Constant"))
        self.intrinsicfreq_random_radio.setText(_translate("MainWindow", "Random"))
        self.intrinsicfreq_file_radio.setText(_translate("MainWindow", "From file"))
        self.intrinsicfreq_file_button.setText(_translate("MainWindow", "Open"))
        self.intitialphase_groupbox.setTitle(_translate("MainWindow", "Initial phase"))
        self.initialphase_constant_radio.setText(_translate("MainWindow", "Constant"))
        self.initialphase_random_radio.setText(_translate("MainWindow", "Random"))
        self.intitialphase_file_radio.setText(_translate("MainWindow", "From file"))
        self.intitialphase_file_button.setText(_translate("MainWindow", "Open"))
        self.interaction_strength_groupbox.setTitle(_translate("MainWindow", "Interaction strenght"))
        self.constant_strength_constant_radio.setText(_translate("MainWindow", "Constant"))
        self.interaction_strength_random_radio.setText(_translate("MainWindow", "Random"))
        self.interaction_strength_file_label.setText(_translate("MainWindow", "From file"))
        self.interaction_strength_file_button.setText(_translate("MainWindow", "Open"))
        self.sim_settings_groupbox.setTitle(_translate("MainWindow", "Simulation settings"))
        self.sim_total_time_label.setText(_translate("MainWindow", "Total time"))
        self.sim_timestep_label.setText(_translate("MainWindow", "Time step"))
        self.run_simulation_button.setText(_translate("MainWindow", "Run Simulation"))
        self.tabWidget_settings.setTabText(self.tabWidget_settings.indexOf(self.tab_2), _translate("MainWindow", "Simulation"))
        self.tabWidget_Plots.setTabText(self.tabWidget_Plots.indexOf(self.initial_islet_plot_tab), _translate("MainWindow", "Initial Islet"))
        self.tabWidget_Plots.setTabText(self.tabWidget_Plots.indexOf(self.final_islet_plot_tab), _translate("MainWindow", "Final Islet"))
        self.tabWidget_Plots.setTabText(self.tabWidget_Plots.indexOf(self.contacts_plot_tab), _translate("MainWindow", "Contacts"))
        self.tabWidget_Plots.setTabText(self.tabWidget_Plots.indexOf(self.networks_plot_tab), _translate("MainWindow", "Network"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionExport_data.setText(_translate("MainWindow", "Export data"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionDocumentation.setText(_translate("MainWindow", "Documentation"))
        self.actionReconstruction.setText(_translate("MainWindow", "Reconstruction"))
        self.actionContacts.setText(_translate("MainWindow", "Contacts"))
        self.actionLoad_data.setText(_translate("MainWindow", "Load data"))
        self.actionRestart.setText(_translate("MainWindow", "Restart"))
        self.actionSimulation.setText(_translate("MainWindow", "Simulation"))
        self.actionGraphs.setText(_translate("MainWindow", "Graphs"))

    def open_islet_file_button_clicked(self, s):
        #print("click", s)
        dlg = QtWidgets.QFileDialog()
        filename = dlg.getOpenFileName()
        #dlg.setWindowTitle("Hello")
        if filename[0]:
            try:
                self.exp_islet_data = np.loadtxt(filename[0])
                self.current_islet_file = filename[0]
                # abrevio nombre para mostrar en GUI

                self.abbv_filename = re.search("(/.*/)(.*)", self.current_islet_file)[2]
                #print(self.abbv_filename)
                #print(self.exp_islet_data[:,0])
                #print(self.current_islet_file)
                self.load_islet_status_label.setText(self.abbv_filename + " loaded succesfully")
                self.load_islet_status_label.setStyleSheet("color: Green")

                # se grafica
                self.plot_initial_islet()
                # se genera la estadistica
                self.initial_islet_stats()
                self.load_islet_button.setEnabled(False)
                self.reconstruction_status_label.setEnabled(True)
                self.reconstruct_button.setEnabled(True)
                self.tabWidget_islet_stats.setTabEnabled(0, True)
                self.tabWidget_Plots.setTabEnabled(0, True)
            except: 
                self.load_islet_status_label.setText("Error loading islet file")
                self.load_islet_status_label.setStyleSheet("color: Red")
                

    ## funcion que grafica islote inicial
    def plot_initial_islet(self):
        #new_tab = QWidget()
        layout = QtWidgets.QVBoxLayout()
        self.initial_islet_plot_tab.setLayout(layout)

        figure = plt.figure()
        figure.subplots_adjust(left=0.1, right=0.99, bottom=0.05, top=1.0, wspace=0.2, hspace=0.2)
        new_canvas = FigureCanvas(figure)
        new_canvas.setFocusPolicy(QtCore.Qt.StrongFocus)
        new_canvas.setFocus()
        
        ax = Axes3D(figure)
        ax.view_init(elev = -80., azim = 90)
        plt.xlabel('x')
        plt.ylabel('y')
        #ax.set_xlim(-10, 10)
        #ax.set_ylim(-10, 10)
        #ax.set_zlim(-10, 10)
        #ax.set_zlabel('z')
        #ax.set_zticks([])
        for cell in self.exp_islet_data:
            x_coord = cell[1]
            y_coord = cell[2]
            z_coord = cell[3]
            # si no hay columna de radio
            #r_cell = cell[0]
            r_cell = 8.
            cell_type = cell[0]
            if cell_type == 12.:
                cell_color = "g"
            elif cell_type == 11.:
                cell_color = "r"
            elif cell_type == 13:
                cell_color = "b"
            else:
                cell_color = "k"
            s = Sphere(ax, x = x_coord, y = y_coord, z = z_coord, radius = r_cell, detail_level = 10, rstride = 2, cstride = 2, color = cell_color)
            #s.modify_x(2)
        ax.mouse_init()


        new_toolbar = NavigationToolbar(new_canvas, self.initial_islet_plot_tab)
        unwanted_buttons = ["Subplots", "Zoom"]
        for x in new_toolbar.actions():
            if x.text() in unwanted_buttons:
                new_toolbar.removeAction(x)

        layout.addWidget(new_canvas)
        layout.addWidget(new_toolbar)
        #self.tabWidget_stats.addTab(new_tab, "txt")
        self.toolbar_handles.append(new_toolbar)
        self.canvases.append(new_canvas)
        self.figure_handles.append(figure)
        self.tab_handles.append(self.initial_islet_plot_tab)

    # funcion que saca estadística de islote inicial
    def initial_islet_stats(self):
        
        #stats islote
        ncells = np.shape(self.exp_islet_data)[0]
        self.ini_ncells_value.setText(str(ncells))
        self.ini_ncells_perc.setText(str(100.00) + " %")
        
        #stats alfas
        nalphas = np.count_nonzero(self.exp_islet_data[:,0] == 11.)
        perc_alphas = np.round(nalphas/ncells*100, 2)
        self.ini_alphacells_value.setText(str(nalphas))
        self.ini_alphacells_perc.setText(str(perc_alphas) + " %")

        nbetas = np.count_nonzero(self.exp_islet_data[:,0] == 12.)
        perc_betas = np.round(nbetas/ncells * 100, 2)
        self.ini_betacells_value.setText(str(nbetas))
        self.ini_betacells_perc.setText(str(perc_betas)+ " %")

        ndeltas  = np.count_nonzero(self.exp_islet_data[:,0] == 13.)
        perc_deltas = np.round(ndeltas * 100.  / ncells,2)
        self.ini_deltacells_value.setText(str(ndeltas))
        self.ini_deltacells_perc.setText(str(perc_deltas)+ " %")
        #print("nalfas = " + str(nalphas) +" "+ str(perc_alphas))
        #print("nbetas = " + str(nbetas) +" "+ str(perc_betas))
        #print("ndeltas = " + str(ndeltas) +" "+ str(perc_deltas))


    def open_reconstruction_settings(self):
        recpars = [self.inittemp, self.tolpar, self.maxiter, self.maxacc, self.threads, self.contacttol]
        reconstruction_settings_diag = QtWidgets.QDialog()
        ui = Ui_reconstruction_settings_diag()
        ui.setupUi(reconstruction_settings_diag, recpars)
        reconstruction_settings_diag.exec_()
        
        # preventing empty form
        if ui.rec_settings_initemp_value.text() == "":
            self.inittemp = recpars[0]
        else:
            self.inittemp = float(ui.rec_settings_initemp_value.text())

        if ui.rec_settings_tolpar_value.text() == "":
            self.tolpar = recpars[1]
        else:
            self.tolpar = float(ui.rec_settings_tolpar_value.text())

        if ui.rec_settings_maxiter_value.text() == "":
            self.maxiter = recpars[2]
        else:
            self.maxiter = int(float(ui.rec_settings_maxiter_value.text()))

        if ui.rec_settings_maxacc_value.text() == "":
            self.maxacc = recpars[3]
        else:
            self.maxacc = int(float(ui.rec_settings_maxacc_value.text()))

        if ui.rec_settings_threads_value.text() == "":
            self.threads = recpars[4]
        else:
            self.threads = int(float(ui.rec_settings_threads_value.text()))

        if ui.rec_settings_contacttol_value.text() == "":
            self.contacttol = recpars[5]
        else:
            self.contacttol = float(ui.rec_settings_contacttol_value.text())

    def optimizeIslet(self):
        ### Generate C code using initial islet
        
        
        # ini_islet_file is the path to the exp file
        try:
            # abro archivo a modificar 
            fsource = open("SA_Islote.c", "r")
            # nombre de archivo de salida
            fout = self.current_islet_file[:-4] + "_opt.c"
            # abro archivo de salida
            fsalida = open(fout, "w")

            # leo archivo original
            lines = fsource.readlines()
            lines[21] = "#define numCells " + str(self.ini_ncells_value.text()) +"\n"
            lines[22] = "#define NUMHILOS " + str(self.threads) +"\n" 
            lines[67] = 'fp = fopen("'+self.current_islet_file+'", "r");\n'

            reconstructed_islet_file = self.current_islet_file[:-4] + "_reconstructed.txt"
            lines[273] = 'FILE *archivoSalida = fopen("'+ reconstructed_islet_file + '", "w");\n'

            initial_islet_file = self.current_islet_file[:-4] + "_initial.txt"
            lines[287] = 'FILE *archivoSalida = fopen("'+ initial_islet_file + '", "w");\n'

            lines[373] = "int MaxTrialN = numCells * " + str(self.maxiter) +";\n"
            lines[374] = "int MaxAcceptN = numCells * " + str(self.maxacc) +";\n"
            lines[375] = "double StopTolerance = " + str(self.tolpar) + ";\n"

            process_log_file = self.current_islet_file[:-4] + "_process_log.txt"
            lines[386] = 'FILE *archivoLog = fopen("'+ process_log_file + '", "w");\n'

            lines[505] = "temp = " + str(self.inittemp) +";\n"

            #escribo archivo de salida
            for line in lines:
                fsalida.write(line)
            
            fsalida.close()
            fsource.close()

            self.reconstruction_status_label.setText("Optimization was configured succesfully")
            self.reconstruction_status_label.setStyleSheet("color: Green")
            self.reconstruction_status_label.setEnabled(True)
            
        except:

            self.reconstruction_status_label.setText("Error during the optimization configuration")
            self.reconstruction_status_label.setStyleSheet("color: Red")

        #time.sleep(1)
        

        try:
            subprocess.run(["gcc", fout , "-o", fout[:-2], "-lm", "-fopenmp"])
            self.reconstruction_status_label.setText("Compilation success")
            self.reconstruction_status_label.setStyleSheet("color: Green")
        except:
            self.reconstruction_status_label.setText("Compilation failed 1")
            self.reconstruction_status_label.setStyleSheet("color: Red")

        #time.sleep(1)

        try:
            # self.progress_indicator = QtWidgets.QProgressDialog()
            # self.progress_indicator.setWindowModality(QtCore.Qt.WindowModal)
            # self.progress_indicator.setRange(0, 0)
            # self.progress_indicator.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            # self.message_obj.finished.connect(self.progress_indicator.close, QtCore.Qt.QueuedConnection)
            # self.progress_indicator.show()
            #_thread.start_new_thread(self.run_code, (self.message_obj, fout))

            subprocess.run([fout[:-2]])
            progressbar = ProgressBar(n, title = "Copying files...")
            #if progressbar.wasCanceled():
            #    break

            self.reconstruction_status_label.setText("Optimization completed")
            self.reconstruction_status_label.setStyleSheet("color: Green")
            self.reconstruct_button.setEnabled(False)
            self.contacts_button.setEnabled(True)
            self.contacts_status_label.setEnabled(True)
            self.tabWidget_settings.setTabEnabled(1, False)
            

            #self.tabWidget_islet_stats.setCurrentIndex(0)
            self.tabWidget_islet_stats.setTabEnabled(1, True)
            
            
            
            
            self.tabWidget_Plots.setTabEnabled(1, True)
            
        except Exception as e:
            #print(fout[:-2])
            print(e)
            self.reconstruction_status_label.setText("Failed")
            self.reconstruction_status_label.setStyleSheet("color: Red")


            #pb = ProgressBar()
            #for i in range(0, 100):
            #    time.sleep(0.05)
            #    pb.setValue(((i + 1) / 100) * 100)
            #    QtWidgets.QApplication.processEvents()

            #pb.close()
        
    
    def run_code(self, obj, fout):
        subprocess.run([fout[:-2]])
        obj.finished.emit()

    def restart(self):
        QtCore.QCoreApplication.quit()
        status = QtCore.QProcess.startDetached(sys.executable, sys.argv)
        print(status)


class ProgressBar(QtWidgets.QProgressDialog):
    def __init__(self, max, title):
        super().__init__()
        self.setMinimumDuration(0) # Sets how long the loop should last before progress bar is shown (in miliseconds)
        self.setWindowTitle(title)
        self.setModal(True)

        self.setValue(0)
        self.setMinimum(0)
        self.setMaximum(max)

        self.show()



class Ui_reconstruction_settings_diag(object):

            # reconstruction settings

    def setupUi(self, reconstruction_settings_diag, recpars):

        # para guardar parametros en el dialogo
        self.diaginitTemp = recpars[0]
        self.diagtolpar = recpars[1]
        self.diagmaxiter = recpars[2]
        self.diagmaxacc = recpars[3]
        self.diagthreads = recpars[4]
        self.diagcontacttol = recpars[5]

        # para validacion de entradas solo numeros
        reg_ex_numeros = QtCore.QRegExp("[+]?[0-9]*\.?[0-9]+")


        reconstruction_settings_diag.setObjectName("reconstruction_settings_diag")
        reconstruction_settings_diag.resize(313, 238)
        reconstruction_settings_diag.setMinimumSize(QtCore.QSize(313, 238))
        reconstruction_settings_diag.setMaximumSize(QtCore.QSize(313, 238))
        self.recconstruction_settings_buttonbox = QtWidgets.QDialogButtonBox(reconstruction_settings_diag)
        self.recconstruction_settings_buttonbox.setGeometry(QtCore.QRect(118, 200, 171, 32))
        self.recconstruction_settings_buttonbox.setOrientation(QtCore.Qt.Horizontal)
        self.recconstruction_settings_buttonbox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        #self.recconstruction_settings_buttonbox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
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
        
        # initemp 
        self.rec_settings_initemp_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.rec_settings_initemp_label.setObjectName("rec_settings_initemp_label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.rec_settings_initemp_label)
        self.rec_settings_initemp_value = QtWidgets.QLineEdit(self.formLayoutWidget)
        initemp_validator = QtGui.QRegExpValidator(reg_ex_numeros, self.rec_settings_initemp_value)
        self.rec_settings_initemp_value.setValidator(initemp_validator)
        self.rec_settings_initemp_value.setFrame(True)
        self.rec_settings_initemp_value.setAlignment(QtCore.Qt.AlignCenter)
        self.rec_settings_initemp_value.setObjectName("rec_settings_initemp_value")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.rec_settings_initemp_value)

        # tolpar
        self.rec_settings_tolpar_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.rec_settings_tolpar_label.setObjectName("rec_settings_tolpar_label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.rec_settings_tolpar_label)
        self.rec_settings_tolpar_value = QtWidgets.QLineEdit(self.formLayoutWidget)
        tolpar_validator = QtGui.QRegExpValidator(reg_ex_numeros, self.rec_settings_tolpar_value)
        self.rec_settings_tolpar_value.setValidator(tolpar_validator)
        self.rec_settings_tolpar_value.setAlignment(QtCore.Qt.AlignCenter)
        self.rec_settings_tolpar_value.setObjectName("rec_settings_tolpar_value")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.rec_settings_tolpar_value)

        # maxiter
        self.rec_settings_maxiter_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.rec_settings_maxiter_label.setObjectName("rec_settings_maxiter_label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.rec_settings_maxiter_label)
        self.rec_settings_maxiter_value = QtWidgets.QLineEdit(self.formLayoutWidget)
        maxiter_validator = QtGui.QRegExpValidator(reg_ex_numeros, self.rec_settings_maxiter_value)
        self.rec_settings_maxiter_value.setValidator(maxiter_validator)
        self.rec_settings_maxiter_value.setAlignment(QtCore.Qt.AlignCenter)
        self.rec_settings_maxiter_value.setObjectName("rec_settings_maxiter_value")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.rec_settings_maxiter_value)

        # maxacc
        self.rec_settings_maxacc_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.rec_settings_maxacc_label.setObjectName("rec_settings_maxacc_label")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.rec_settings_maxacc_label)
        self.rec_settings_maxacc_value = QtWidgets.QLineEdit(self.formLayoutWidget)
        maxacc_validator = QtGui.QRegExpValidator(reg_ex_numeros, self.rec_settings_maxacc_value)
        self.rec_settings_maxacc_value.setValidator(maxacc_validator)
        self.rec_settings_maxacc_value.setAlignment(QtCore.Qt.AlignCenter)
        self.rec_settings_maxacc_value.setObjectName("rec_settings_maxacc_value")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.rec_settings_maxacc_value)

        # threads
        self.rec_settings_threads_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.rec_settings_threads_label.setObjectName("rec_settings_threads_label")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.rec_settings_threads_label)
        self.rec_settings_threads_value = QtWidgets.QLineEdit(self.formLayoutWidget)
        threads_validator = QtGui.QRegExpValidator(reg_ex_numeros, self.rec_settings_threads_value)
        self.rec_settings_threads_value.setValidator(tolpar_validator)
        self.rec_settings_threads_value.setAlignment(QtCore.Qt.AlignCenter)
        self.rec_settings_threads_value.setObjectName("rec_settings_threads_value")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.rec_settings_threads_value)

        # contacttol
        self.rec_settings_contacttol_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.rec_settings_contacttol_label.setObjectName("rec_settings_contacttol_label")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.rec_settings_contacttol_label)
        self.rec_settings_contacttol_value = QtWidgets.QLineEdit(self.formLayoutWidget)
        contacttol_validator = QtGui.QRegExpValidator(reg_ex_numeros, self.rec_settings_contacttol_value)
        self.rec_settings_contacttol_value.setValidator(tolpar_validator)
        self.rec_settings_contacttol_value.setAlignment(QtCore.Qt.AlignCenter)
        self.rec_settings_contacttol_value.setObjectName("rec_settings_contacttol_value")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.rec_settings_contacttol_value)

        self.retranslateUi(reconstruction_settings_diag)
        self.recconstruction_settings_buttonbox.accepted.connect(reconstruction_settings_diag.accept)
        #self.recconstruction_settings_buttonbox.rejected.connect(reconstruction_settings_diag.reject)
        QtCore.QMetaObject.connectSlotsByName(reconstruction_settings_diag)


    def retranslateUi(self, reconstruction_settings_diag):
        _translate = QtCore.QCoreApplication.translate
        reconstruction_settings_diag.setWindowTitle(_translate("reconstruction_settings_diag", "Reconstruction settings"))
        self.rec_settings_initemp_label.setText(_translate("reconstruction_settings_diag", "Initial temperature"))
        self.rec_settings_initemp_value.setText(_translate("reconstruction_settings_diag", str(self.diaginitTemp)))
        self.rec_settings_tolpar_label.setText(_translate("reconstruction_settings_diag", "Tolerance parameter"))
        self.rec_settings_tolpar_value.setText(_translate("reconstruction_settings_diag", str(self.diagtolpar)))
        self.rec_settings_maxiter_label.setText(_translate("reconstruction_settings_diag", "Iterations multiplier"))
        self.rec_settings_maxiter_value.setText(_translate("reconstruction_settings_diag", str(self.diagmaxiter)))
        self.rec_settings_maxacc_label.setText(_translate("reconstruction_settings_diag", "Acceptance multiplier"))
        self.rec_settings_maxacc_value.setText(_translate("reconstruction_settings_diag", str(self.diagmaxacc)))
        self.rec_settings_threads_label.setText(_translate("reconstruction_settings_diag", "Threads"))
        self.rec_settings_threads_value.setText(_translate("reconstruction_settings_diag", str(self.diagthreads)))
        self.rec_settings_contacttol_label.setText(_translate("reconstruction_settings_diag", "Contact tolerance"))
        self.rec_settings_contacttol_value.setText(_translate("reconstruction_settings_diag", str(self.diagcontacttol)))






if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

