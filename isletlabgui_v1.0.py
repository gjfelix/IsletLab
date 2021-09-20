# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'isletlabgui_v1.0.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import re
import sys, time
import subprocess
#import _thread
#import threading
from decimal import Decimal

from shape import Shape
from sphere import Sphere
from sys import platform as sys_pf

from matplotlib.dates import date2num
from matplotlib.ticker import ScalarFormatter, FormatStrFormatter
from datetime import datetime

import networkx as nx
import glob
from zipfile import ZipFile
import os

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
        #MainWindow.show()
        
        reg_ex_numeros = QtCore.QRegExp("[+]?[0-9]*\.?[0-9]+")

        
        app.aboutToQuit.connect(self.closeEvent)

        # Para agregar figuras en pestañas
        self.canvases = []
        self.figure_handles = []
        self.toolbar_handles = []
        self.tab_handles = []
        self.current_window = -1

        # Parametros default para reconstruccion
        self.inittemp = 1.
        self.tolpar = 0.005
        self.maxiter = 1
        self.maxacc = 1
        self.threads = 6
        self.contacttol = 1.0
        self.optstatus = 0

        # diccionario de contactos
        self.contacts_islet = {}

        # parametros default de simulacion
        self.constfreq = 0.1/60. # periodo = 10 min, freq = 1/10 [min^-1] = 0.1/60 [s^-1]
        self.constphase = 0.
        self.initialphase_type = "Constant"
        self.intrinsicfreq_type = "Constant"
        self.meanfreq = 0.1/60.
        self.sdfreq = self.meanfreq/10.
        self.meanphase = 0.
        self.sdphase = self.meanphase/10.
        self.totaltimesim = 20000.0
        self.dtsim = 0.1
        self.saveMultiple = 500

        # interaction strength parameters (kuramoto oscilators)
        self.Kaa = 1.0
        self.Kba = 0.1
        self.Kda = 1.0
        self.Kab = -10.0
        self.Kbb = 1.0
        self.Kdb = 1.0
        self.Kad = -1.0
        self.Kbd = -1.0
        self.Kdd = 0.0

        # Simulation settings (CUDA settings)
        self.nblocks = 30
        self.ncudathreads = 64
        self.maxVecinos = 10

        #self.message_obj = Message()

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
        self.contacts_button.clicked.connect(self.contactos)
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
        self.network_button.clicked.connect(self.build_network)

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
        self.clustering_label.setGeometry(QtCore.QRect(10, 50, 200, 15))
        self.clustering_label.setObjectName("clustering_label")
        
        self.diameter_label = QtWidgets.QLabel(self.tab_network_stats)
        self.diameter_label.setGeometry(QtCore.QRect(10, 70, 100, 15))
        self.diameter_label.setObjectName("diameter_label")
        
        self.efficiency_label = QtWidgets.QLabel(self.tab_network_stats)
        self.efficiency_label.setGeometry(QtCore.QRect(10, 90, 100, 15))
        self.efficiency_label.setObjectName("efficiency_label")
        
        self.degree_value = QtWidgets.QLabel(self.tab_network_stats)
        self.degree_value.setGeometry(QtCore.QRect(200, 10, 100, 15))
        self.degree_value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.degree_value.setObjectName("degree_value")
        
        self.density_value = QtWidgets.QLabel(self.tab_network_stats)
        self.density_value.setGeometry(QtCore.QRect(200, 30, 100, 15))
        self.density_value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.density_value.setObjectName("density_value")
        
        self.clustering_value = QtWidgets.QLabel(self.tab_network_stats)
        self.clustering_value.setGeometry(QtCore.QRect(200, 50, 100, 15))
        self.clustering_value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.clustering_value.setObjectName("clustering_value")
        
        self.diameter_value = QtWidgets.QLabel(self.tab_network_stats)
        self.diameter_value.setGeometry(QtCore.QRect(200, 70, 100, 15))
        self.diameter_value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.diameter_value.setObjectName("diameter_value")
        
        self.efficiency_value = QtWidgets.QLabel(self.tab_network_stats)
        self.efficiency_value.setGeometry(QtCore.QRect(200, 90, 100, 15))
        self.efficiency_value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.efficiency_value.setObjectName("efficiency_value")
        
        self.tabWidget_islet_stats.addTab(self.tab_network_stats, "")
        self.tabWidget_settings.addTab(self.reconstructing_tab, "")
        #self.tab_plots = QtWidgets.QWidget()
        #self.tab_plots.setObjectName("tab_plots")
        #self.opt_plot_groupbox = QtWidgets.QGroupBox(self.tab_plots)
        #self.opt_plot_groupbox.setGeometry(QtCore.QRect(10, 5, 321, 61))
        #self.opt_plot_groupbox.setObjectName("opt_plot_groupbox")
        #self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.opt_plot_groupbox)
        #self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(9, 20, 301, 41))
        #self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        #self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        #self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        #self.verticalLayout.setObjectName("verticalLayout")
        
        #self.plot_convergence_button = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        #self.plot_convergence_button.setObjectName("plot_convergence_button")
        #self.plot_convergence_button.clicked.connect(self.plotOptConvergence)
        #self.verticalLayout.addWidget(self.plot_convergence_button)
        

        # self.arch_plots_groupbox = QtWidgets.QGroupBox(self.tab_plots)
        # self.arch_plots_groupbox.setGeometry(QtCore.QRect(10, 75, 321, 141))
        # self.arch_plots_groupbox.setObjectName("arch_plots_groupbox")
        # self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.arch_plots_groupbox)
        # self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(9, 20, 301, 121))
        # self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        # self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        # self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        # self.verticalLayout_2.setObjectName("verticalLayout_2")
        # self.cell_number_plot_button = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        # self.cell_number_plot_button.setObjectName("cell_number_plot_button")
        # self.verticalLayout_2.addWidget(self.cell_number_plot_button)
        # self.radii_plot_button = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        # self.radii_plot_button.setObjectName("radii_plot_button")
        # self.verticalLayout_2.addWidget(self.radii_plot_button)
        # self.islet_volume_plot_button = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        # self.islet_volume_plot_button.setObjectName("islet_volume_plot_button")
        # self.verticalLayout_2.addWidget(self.islet_volume_plot_button)
        # self.connectivity_plots_groupbox = QtWidgets.QGroupBox(self.tab_plots)
        # self.connectivity_plots_groupbox.setGeometry(QtCore.QRect(9, 230, 321, 61))
        # self.connectivity_plots_groupbox.setObjectName("connectivity_plots_groupbox")
        # self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.connectivity_plots_groupbox)
        # self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(9, 19, 301, 41))
        # self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        # self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        # self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        # self.verticalLayout_3.setObjectName("verticalLayout_3")
        # self.contacts_plot_button = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        # self.contacts_plot_button.setObjectName("contacts_plot_button")
        # self.verticalLayout_3.addWidget(self.contacts_plot_button)
        # self.network_plots_groupbox = QtWidgets.QGroupBox(self.tab_plots)
        # self.network_plots_groupbox.setGeometry(QtCore.QRect(10, 300, 321, 80))
        # self.network_plots_groupbox.setObjectName("network_plots_groupbox")
        # self.verticalLayoutWidget_5 = QtWidgets.QWidget(self.network_plots_groupbox)
        # self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(9, 20, 301, 61))
        # self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        # self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
        # self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        # self.verticalLayout_5.setObjectName("verticalLayout_5")
        # self.network_metrics_plots_butthon = QtWidgets.QPushButton(self.verticalLayoutWidget_5)
        # self.network_metrics_plots_butthon.setObjectName("network_metrics_plots_butthon")
        # self.verticalLayout_5.addWidget(self.network_metrics_plots_butthon)
        #self.tabWidget_settings.addTab(self.tab_plots, "")
        self.simulation_tab = QtWidgets.QWidget()
        self.simulation_tab.setObjectName("simulation_tab")
        self.intrinsicfreq_groupbox = QtWidgets.QGroupBox(self.simulation_tab)
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
        self.intrinsicfreq_constant_radio.setChecked(True)
        self.intrinsicfreq_random_radio = QtWidgets.QRadioButton(self.verticalLayoutWidget_6)
        self.intrinsicfreq_random_radio.setObjectName("intrinsicfreq_random_radio")
        self.verticalLayout_6.addWidget(self.intrinsicfreq_random_radio)
        self.intrinsicfreq_config_button = QtWidgets.QPushButton(self.verticalLayoutWidget_6)
        self.intrinsicfreq_config_button.setObjectName("intrinsicfreq_config_button")
        self.intrinsicfreq_config_button.clicked.connect(self.selectIntrinsicFreqConfig)
        self.verticalLayout_6.addWidget(self.intrinsicfreq_config_button)
        #self.horizontalLayout = QtWidgets.QHBoxLayout()
        #self.horizontalLayout.setSpacing(6)
        #self.horizontalLayout.setObjectName("horizontalLayout")
        #self.intrinsicfreq_file_radio = QtWidgets.QRadioButton(self.verticalLayoutWidget_6)
        #self.intrinsicfreq_file_radio.setObjectName("intrinsicfreq_file_radio")
        #self.intrinsicfreq_file_radio.clicked.connect(self.open_int_freq_file)
        #self.horizontalLayout.addWidget(self.intrinsicfreq_file_radio)
        #self.intrinsicfreq_file_button = QtWidgets.QPushButton(self.verticalLayoutWidget_6)
        #sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        #sizePolicy.setHorizontalStretch(0)
        #sizePolicy.setVerticalStretch(0)
        #sizePolicy.setHeightForWidth(self.intrinsicfreq_file_button.sizePolicy().hasHeightForWidth())
        #self.intrinsicfreq_file_button.setSizePolicy(sizePolicy)
        #self.intrinsicfreq_file_button.setObjectName("intrinsicfreq_file_button")
        #self.horizontalLayout.addWidget(self.intrinsicfreq_file_button)
        #self.verticalLayout_6.addLayout(self.horizontalLayout)
        self.intitialphase_groupbox = QtWidgets.QGroupBox(self.simulation_tab)
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
        self.initialphase_random_radio.setChecked(True)
        self.verticalLayout_7.addWidget(self.initialphase_random_radio)
        self.initialphase_random_radio.toggled.connect(lambda:self.disable_random_phase_config_button(self.initialphase_random_radio))
        
        self.initialphase_config_button = QtWidgets.QPushButton(self.verticalLayoutWidget_7)
        self.initialphase_config_button.setObjectName("initialphase_config_button")
        self.initialphase_config_button.clicked.connect(self.selectInitialPhaseConfig)
        self.initialphase_config_button.setEnabled(False)
        self.verticalLayout_7.addWidget(self.initialphase_config_button)

        #self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        #self.horizontalLayout_2.setSpacing(6)
        #self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        #self.intitialphase_file_radio = QtWidgets.QRadioButton(self.verticalLayoutWidget_7)
        #self.intitialphase_file_radio.setObjectName("intitialphase_file_radio")
        #self.horizontalLayout_2.addWidget(self.intitialphase_file_radio)
        #self.intitialphase_file_button = QtWidgets.QPushButton(self.verticalLayoutWidget_7)
        #sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        #sizePolicy.setHorizontalStretch(0)
        #sizePolicy.setVerticalStretch(0)
        #sizePolicy.setHeightForWidth(self.intitialphase_file_button.sizePolicy().hasHeightForWidth())
        #self.intitialphase_file_button.setSizePolicy(sizePolicy)
        #self.intitialphase_file_button.setObjectName("intitialphase_file_button")
        #self.horizontalLayout_2.addWidget(self.intitialphase_file_button)
        #self.verticalLayout_7.addLayout(self.horizontalLayout_2)
        self.interaction_strength_groupbox = QtWidgets.QGroupBox(self.simulation_tab)
        self.interaction_strength_groupbox.setGeometry(QtCore.QRect(10, 250, 311, 111))
        self.interaction_strength_groupbox.setObjectName("interaction_strength_groupbox")
        self.verticalLayoutWidget_8 = QtWidgets.QWidget(self.interaction_strength_groupbox)
        self.verticalLayoutWidget_8.setGeometry(QtCore.QRect(9, 19, 301, 91))
        self.verticalLayoutWidget_8.setObjectName("verticalLayoutWidget_8")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_8)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        #self.constant_strength_constant_radio = QtWidgets.QRadioButton(self.verticalLayoutWidget_8)
        #self.constant_strength_constant_radio.setObjectName("constant_strength_constant_radio")
        #self.verticalLayout_8.addWidget(self.constant_strength_constant_radio)
        #self.interaction_strength_random_radio = QtWidgets.QRadioButton(self.verticalLayoutWidget_8)
        #self.interaction_strength_random_radio.setObjectName("interaction_strength_random_radio")
        #self.verticalLayout_8.addWidget(self.interaction_strength_random_radio)
        

        #self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        #self.horizontalLayout_3.setSpacing(6)
        #self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        #self.interaction_strength_file_radio = QtWidgets.QRadioButton(self.verticalLayoutWidget_8)
        #self.interaction_strength_file_radio.setObjectName("interaction_strength_file_radio")
        #self.interaction_strength_file_radio.toggled.connect(self.activate_interaction_strength_file_button)
        #self.horizontalLayout_3.addWidget(self.interaction_strength_file_radio)
        self.interaction_strength_file_button = QtWidgets.QPushButton(self.verticalLayoutWidget_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.interaction_strength_file_button.sizePolicy().hasHeightForWidth())
        self.interaction_strength_file_button.setSizePolicy(sizePolicy)
        self.interaction_strength_file_button.setObjectName("interaction_strength_file_button")
        self.interaction_strength_file_button.clicked.connect(self.open_interaction_strength_dialog)
        


        self.verticalLayout_8.addWidget(self.interaction_strength_file_button)
        #self.verticalLayout_8.addLayout(self.horizontalLayout_3)
        self.sim_settings_groupbox = QtWidgets.QGroupBox(self.simulation_tab)
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
        self.total_time_lineedit.setText(str(self.totaltimesim))
        total_time_validator = QtGui.QRegExpValidator(reg_ex_numeros, self.total_time_lineedit)
        self.total_time_lineedit.setValidator(total_time_validator)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.total_time_lineedit)
        
        self.sim_timestep_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.sim_timestep_label.setObjectName("sim_timestep_label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.sim_timestep_label)
        self.timestep_lineedit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.timestep_lineedit.setObjectName("timestep_lineedit")
        self.timestep_lineedit.setText(str(self.dtsim))
        # para validacion de entradas solo numeros
        timestep_validator = QtGui.QRegExpValidator(reg_ex_numeros, self.timestep_lineedit)
        self.timestep_lineedit.setValidator(timestep_validator)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.timestep_lineedit)
        
        self.save_mult_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.save_mult_label.setObjectName("save_mult_label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.save_mult_label)
        self.save_mult_lineedit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.save_mult_lineedit.setObjectName("timestep_lineedit")
        self.save_mult_lineedit.setText(str(self.saveMultiple))
        # para validacion de entradas solo numeros
        save_mult_validator = QtGui.QRegExpValidator(reg_ex_numeros, self.save_mult_lineedit)
        self.save_mult_lineedit.setValidator(save_mult_validator)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.save_mult_lineedit)


        self.cuda_settings_groupbox = QtWidgets.QGroupBox(self.simulation_tab)
        self.cuda_settings_groupbox.setGeometry(QtCore.QRect(10, 480, 321, 101))
        self.cuda_settings_groupbox.setObjectName("sim_settings_groupbox")
        self.formLayoutWidgetcuda = QtWidgets.QWidget(self.cuda_settings_groupbox)
        self.formLayoutWidgetcuda.setGeometry(QtCore.QRect(9, 29, 301, 61))
        self.formLayoutWidgetcuda.setObjectName("formLayoutWidget")
        self.formLayoutcuda = QtWidgets.QFormLayout(self.formLayoutWidgetcuda)
        self.formLayoutcuda.setContentsMargins(0, 0, 0, 0)
        self.formLayoutcuda.setObjectName("formLayout")
        self.nblocks_label = QtWidgets.QLabel(self.formLayoutWidgetcuda)
        self.nblocks_label.setObjectName("nblocks_label")
        self.formLayoutcuda.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.nblocks_label)
        self.nblocks_lineedit = QtWidgets.QLineEdit(self.formLayoutWidgetcuda)
        self.nblocks_lineedit.setMaximumSize(QtCore.QSize(500, 16777215))
        self.nblocks_lineedit.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.nblocks_lineedit.setObjectName("total_time_lineedit")
        self.nblocks_lineedit.setText(str(self.nblocks))
        nblocks_validator = QtGui.QRegExpValidator(reg_ex_numeros, self.nblocks_lineedit)
        self.nblocks_lineedit.setValidator(nblocks_validator)
        self.formLayoutcuda.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.nblocks_lineedit)
        
        self.ncudathreads_label = QtWidgets.QLabel(self.formLayoutWidgetcuda)
        self.ncudathreads_label.setObjectName("nthreads_label")
        self.formLayoutcuda.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.ncudathreads_label)
        self.ncudathreads_lineedit = QtWidgets.QLineEdit(self.formLayoutWidgetcuda)
        self.ncudathreads_lineedit.setObjectName("timestep_lineedit")
        self.ncudathreads_lineedit.setText(str(self.ncudathreads))
        # para validacion de entradas solo numeros
        ncudathreads_validator = QtGui.QRegExpValidator(reg_ex_numeros, self.ncudathreads_lineedit)
        self.ncudathreads_lineedit.setValidator(ncudathreads_validator)
        self.formLayoutcuda.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.ncudathreads_lineedit)

        self.run_simulation_button = QtWidgets.QPushButton(self.simulation_tab)
        self.run_simulation_button.setGeometry(QtCore.QRect(10, 590, 321, 61))
        self.run_simulation_button.clicked.connect(self.run_kuramoto_simulation)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.run_simulation_button.sizePolicy().hasHeightForWidth())
        self.run_simulation_button.setSizePolicy(sizePolicy)
        self.run_simulation_button.setObjectName("run_simulation_button")


        self.sim_status_label = QtWidgets.QLabel(self.simulation_tab)
        self.sim_status_label.setObjectName("save_mult_label")
        self.sim_status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.sim_status_label.setEnabled(True)
        self.sim_status_label.setGeometry(QtCore.QRect(10, 665, 321, 16))
        #self.sim_status_label.setText("Test Label")

        self.tabWidget_settings.addTab(self.simulation_tab, "")
        self.tabWidget_Plots = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget_Plots.setGeometry(QtCore.QRect(342, 1, 681, 725))
        self.tabWidget_Plots.setObjectName("tabWidget_Plots")
        self.tabWidget_Plots.setTabsClosable(False)
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
        #self.menuSettings = QtWidgets.QMenu(self.menubar)
        #self.menuSettings.setObjectName("menuSettings")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionExport_data = QtWidgets.QAction(MainWindow)
        self.actionExport_data.setObjectName("actionExport_data")
        self.actionExport_data.triggered.connect(self.save_project)
        self.actionExport_data.setEnabled(False)
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout.triggered.connect(self.about_isletlab)
        self.actionDocumentation = QtWidgets.QAction(MainWindow)
        self.actionDocumentation.setObjectName("actionDocumentation")
        
        self.actionReconstruction = QtWidgets.QAction(MainWindow)
        self.actionReconstruction.setObjectName("actionReconstruction")
        self.actionReconstruction.triggered.connect(self.open_reconstruction_settings)

        #self.actionContacts = QtWidgets.QAction(MainWindow)
        #self.actionContacts.setObjectName("actionContacts")
        self.actionLoad_data = QtWidgets.QAction(MainWindow)
        self.actionLoad_data.setWhatsThis("")
        self.actionLoad_data.setObjectName("actionLoad_data")
        self.actionLoad_data.triggered.connect(self.load_project)
        self.actionRestart = QtWidgets.QAction(MainWindow)
        self.actionRestart.setWhatsThis("")
        self.actionRestart.triggered.connect(self.restart)
        self.actionLoad_data.setObjectName("actionRestart")
        #self.actionSimulation = QtWidgets.QAction(MainWindow)
        #self.actionSimulation.setObjectName("actionSimulation")
        #self.actionGraphs = QtWidgets.QAction(MainWindow)
        #self.actionGraphs.setObjectName("actionGraphs")
        self.menuFile.addAction(self.actionExport_data)
        self.menuFile.addAction(self.actionLoad_data)
        self.menuFile.addAction(self.actionRestart)
        #self.menuSettings.addAction(self.actionReconstruction)
        #self.menuSettings.addAction(self.actionSimulation)
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionDocumentation)
        self.menubar.addAction(self.menuFile.menuAction())
        #self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        #self.tabWidget_settings.setCurrentIndex(0)
        self.tabWidget_settings.setTabEnabled(1, False)
        #self.tabWidget_settings.setTabEnabled(2, False)
        #self.tabWidget_settings.setTabEnabled(3, False)


        #self.tabWidget_islet_stats.setCurrentIndex(0)
        self.tabWidget_islet_stats.setTabEnabled(0, False)
        self.tabWidget_islet_stats.setTabEnabled(1, False)
        self.tabWidget_islet_stats.setTabEnabled(2, False)
        self.tabWidget_islet_stats.setTabEnabled(3, False)
        

        self.tabWidget_Plots.setCurrentIndex(0)
        self.tabWidget_Plots.setTabEnabled(0, False)
        self.tabWidget_Plots.setTabEnabled(1, False)
        self.tabWidget_Plots.setTabEnabled(2, False)
        self.tabWidget_Plots.setTabEnabled(3, False)

        #self.contacts_plot_button.setEnabled(False)
        #self.network_metrics_plots_button.setEnabled(False)

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
        self.ini_alpha_cells_label.setText(_translate("MainWindow", "Number of \u03b1-cells"))
        self.ini_beta_cells_label.setText(_translate("MainWindow", "Number of \u03b2-cells"))
        self.ini_delta_cells_label.setText(_translate("MainWindow", "Number of \u03b4-cells"))
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
        self.fin_delta_cells_label.setText(_translate("MainWindow", "Number of \u03b4-cells"))
        self.fin_ncells_perc.setText(_translate("MainWindow", "0"))
        self.fin_beta_cells_label.setText(_translate("MainWindow", "Number of \u03b2-cells"))
        self.fin_ncells_label.setText(_translate("MainWindow", "Number of cells"))
        self.fin_alpha_cells_label.setText(_translate("MainWindow", "Number of \u03b1-cells"))
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
        self.fin_alpha_vol_label.setText(_translate("MainWindow", "\u03b1-cell volume"))
        self.fin_alpha_vol_value.setText(_translate("MainWindow", "0"))
        self.fin_alpha_vol_perc.setText(_translate("MainWindow", "0"))
        self.fin_beta_vol_label.setText(_translate("MainWindow", "\u03b2-cell volume"))
        self.fin_delta_vol_label.setText(_translate("MainWindow", "\u03b4-cell volume"))
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
        self.alphaalpha_contacts_label.setText(_translate("MainWindow", "\u03b1 - \u03b1"))
        self.alphaalpha_contacts_value.setText(_translate("MainWindow", "0"))
        self.alphaalpha_contacts_perc.setText(_translate("MainWindow", "0"))
        self.betabeta_contacts_label.setText(_translate("MainWindow", "\u03b2 - \u03b2"))
        self.betabeta_contacts_value.setText(_translate("MainWindow", "0"))
        self.betabeta_contacts_perc.setText(_translate("MainWindow", "0"))
        self.deltadelta_contacts_label.setText(_translate("MainWindow", "\u03b4 - \u03b4"))
        self.deltadelta_contacts_value.setText(_translate("MainWindow", "0"))
        self.deltadelta_contacts_perc.setText(_translate("MainWindow", "0"))
        self.alphabeta_contacts_label.setText(_translate("MainWindow", "\u03b1 - \u03b2"))
        self.alphabeta_contacts_value.setText(_translate("MainWindow", "0"))
        self.alphabeta_contacts_perc.setText(_translate("MainWindow", "0"))
        self.alphadelta_contacts_label.setText(_translate("MainWindow", "\u03b1 - \u03b4"))
        self.alphadelta_contacts_value.setText(_translate("MainWindow", "0"))
        self.alphadelta_contacts_perc.setText(_translate("MainWindow", "0"))
        self.betadelta_contacts_label.setText(_translate("MainWindow", "\u03b2 - \u03b4"))
        self.betadelta_contacts_value.setText(_translate("MainWindow", "0"))
        self.betadelta_contacts_perc.setText(_translate("MainWindow", "0"))
        self.tabWidget_islet_stats.setTabText(self.tabWidget_islet_stats.indexOf(self.tab_contacts_stats), _translate("MainWindow", "Contacts"))
        self.degree_label.setText(_translate("MainWindow", "Average degree"))
        self.density_label.setText(_translate("MainWindow", "Density"))
        self.clustering_label.setText(_translate("MainWindow", "Average clustering coefficient"))
        self.diameter_label.setText(_translate("MainWindow", "Diameter"))
        self.efficiency_label.setText(_translate("MainWindow", "Efficiency"))
        self.degree_value.setText(_translate("MainWindow", "0"))
        self.density_value.setText(_translate("MainWindow", "0"))
        self.clustering_value.setText(_translate("MainWindow", "0"))
        self.diameter_value.setText(_translate("MainWindow", "0"))
        self.efficiency_value.setText(_translate("MainWindow", "0"))
        self.tabWidget_islet_stats.setTabText(self.tabWidget_islet_stats.indexOf(self.tab_network_stats), _translate("MainWindow", "Network"))
        self.tabWidget_settings.setTabText(self.tabWidget_settings.indexOf(self.reconstructing_tab), _translate("MainWindow", "Reconstruction"))
        #self.opt_plot_groupbox.setTitle(_translate("MainWindow", "Optimization"))
        #self.plot_convergence_button.setText(_translate("MainWindow", "Convergence"))
        #self.arch_plots_groupbox.setTitle(_translate("MainWindow", "Architecture"))
        #self.cell_number_plot_button.setText(_translate("MainWindow", "Number of cells"))
        #self.radii_plot_button.setText(_translate("MainWindow", "Cells radii"))
        #self.islet_volume_plot_button.setText(_translate("MainWindow", "Islet volume"))
        #self.connectivity_plots_groupbox.setTitle(_translate("MainWindow", "Connectivity"))
        #self.contacts_plot_button.setText(_translate("MainWindow", "Cell-to-cell contacts"))
        #self.network_plots_groupbox.setTitle(_translate("MainWindow", "Network"))
        #self.network_metrics_plots_butthon.setText(_translate("MainWindow", "Metrics"))
        #self.tabWidget_settings.setTabText(self.tabWidget_settings.indexOf(self.tab_plots), _translate("MainWindow", "Graphs"))
        self.intrinsicfreq_groupbox.setTitle(_translate("MainWindow", "Intrinsic frequency"))
        self.intrinsicfreq_constant_radio.setText(_translate("MainWindow", "Constant"))
        self.intrinsicfreq_random_radio.setText(_translate("MainWindow", "Random"))
        self.intrinsicfreq_config_button.setText(_translate("MainWindow", "Configure"))
        #self.intrinsicfreq_file_radio.setText(_translate("MainWindow", "From file"))
        #self.intrinsicfreq_file_button.setText(_translate("MainWindow", "Open"))
        self.intitialphase_groupbox.setTitle(_translate("MainWindow", "Initial phase"))
        self.initialphase_constant_radio.setText(_translate("MainWindow", "Constant"))
        self.initialphase_random_radio.setText(_translate("MainWindow", "Random"))
        self.initialphase_config_button.setText(_translate("MainWindow", "Configure"))
        #self.intitialphase_file_radio.setText(_translate("MainWindow", "From file"))
        #self.intitialphase_file_button.setText(_translate("MainWindow", "Open"))
        
        self.interaction_strength_groupbox.setTitle(_translate("MainWindow", "Interaction strenght"))
        #self.constant_strength_constant_radio.setText(_translate("MainWindow", "Constant"))
        #self.interaction_strength_random_radio.setText(_translate("MainWindow", "Random"))
        #self.interaction_strength_file_radio.setText(_translate("MainWindow", "From file"))
        self.interaction_strength_file_button.setText(_translate("MainWindow", "Configure interactions"))
        

        self.sim_settings_groupbox.setTitle(_translate("MainWindow", "Simulation settings"))
        self.sim_total_time_label.setText(_translate("MainWindow", "Total time"))
        self.sim_timestep_label.setText(_translate("MainWindow", "Time step"))
        self.save_mult_label.setText(_translate("MainWindow", "Save step"))
        self.cuda_settings_groupbox.setTitle(_translate("MainWindow", "CUDA settings"))
        self.nblocks_label.setText(_translate("MainWindow", "Blocks"))
        self.ncudathreads_label.setText(_translate("MainWindow", "Threads"))
        self.run_simulation_button.setText(_translate("MainWindow", "Run Simulation"))
        self.tabWidget_settings.setTabText(self.tabWidget_settings.indexOf(self.simulation_tab), _translate("MainWindow", "Simulation"))
        self.tabWidget_Plots.setTabText(self.tabWidget_Plots.indexOf(self.initial_islet_plot_tab), _translate("MainWindow", "Initial Islet"))
        self.tabWidget_Plots.setTabText(self.tabWidget_Plots.indexOf(self.final_islet_plot_tab), _translate("MainWindow", "Final Islet"))
        self.tabWidget_Plots.setTabText(self.tabWidget_Plots.indexOf(self.contacts_plot_tab), _translate("MainWindow", "Contacts"))
        self.tabWidget_Plots.setTabText(self.tabWidget_Plots.indexOf(self.networks_plot_tab), _translate("MainWindow", "Network"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        #self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionExport_data.setText(_translate("MainWindow", "Export Project"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionDocumentation.setText(_translate("MainWindow", "Documentation"))
        #self.actionReconstruction.setText(_translate("MainWindow", "Reconstruction"))
        #self.actionContacts.setText(_translate("MainWindow", "Contacts"))
        self.actionLoad_data.setText(_translate("MainWindow", "Load Project"))
        self.actionRestart.setText(_translate("MainWindow", "Restart"))
        #self.actionSimulation.setText(_translate("MainWindow", "Simulation"))
        #self.actionGraphs.setText(_translate("MainWindow", "Graphs"))


    def closeEvent(self):
        if self.optstatus == 2:
            self.filespath = re.search(".+/", self.current_islet_file)[0]
            self.filemainname = re.search("(.+)\.(.+)",self.abbv_filename)[1]
            txtfiles =glob.glob(self.filespath+self.filemainname+'_*.txt') 
            datafiles = glob.glob(self.filespath+self.filemainname+'*.data')
            cudafiles = glob.glob(self.filespath+self.filemainname+'*.cu')
            cudaexecfiles = []
            if len(cudafiles) != 0:
                for file in cudafiles:
                    cudaexecfiles.append(file[:-3])
            cfiles = glob.glob(self.filespath+self.filemainname+'*.c')
            cexecfiles = []
            if len(cfiles) != 0:
                for file in cfiles:
                    cexecfiles.append(file[:-2])
            filestoclean = txtfiles + datafiles + cudafiles + cudaexecfiles + cfiles + cexecfiles
            #print(filestoclean)
            #print(len(filestoclean))
            for file in filestoclean:
                os.remove(file)
        else:
            pass
            

    def about_isletlab(self):
        QtWidgets.QMessageBox.about(None, "About IsletLab", "Version: 1.0 \nDeveloped by Gerardo J. Félix-Martínez \nContact: gjfelix2005@gmail.com")

    def save_project(self):

        self.filespath = re.search(".+/", self.current_islet_file)[0]
        self.filemainname = re.search("(.+)\.(.+)",self.abbv_filename)[1]
        
        #print(self.filemainname)
        #filestosave =glob.glob(self.filespath+self.filemainname+'*.txt') + glob.glob(self.filespath+self.filemainname+'*.data')
        filestosave =glob.glob(self.filespath+self.filemainname+'*.txt') + glob.glob(self.filespath+self.filemainname+'*.data')
        #print(self.filespath)
        #print(filestosave)
        
        dlg = QtWidgets.QFileDialog()
        save_directory = dlg.getExistingDirectory(None, "Select Directory")
        projectfilename = save_directory + '/'+self.filemainname + "_IsletLab_Project.zip"
        #print(projectfilename)
        
        try:
            zipProject = ZipFile(projectfilename, 'w')
            for file in filestosave:
                zipProject.write(file)
            successSave = QtWidgets.QMessageBox.information(None, "Project saved", "Your project has been saved succesfully")
        except:
            print("Error haciendo zipfile")
        

    def load_project(self):
        dlg = QtWidgets.QFileDialog()
        project_file = str(dlg.getOpenFileName()[0])
        if project_file:
            filespath = re.search(".+/", project_file)[0]
            
            with ZipFile(project_file, "r") as zip_ref:
                zip_ref.extractall(filespath)
                #print("archivo descomprimido")
            initial_islet_file_load = glob.glob(filespath+'/**/*_initial.txt', recursive = True)
            if initial_islet_file_load:
                self.exp_islet_data = np.loadtxt(initial_islet_file_load[0])
                self.tabWidget_islet_stats.setTabEnabled(0, True)
                self.tabWidget_Plots.setTabEnabled(0, True)
                self.plot_initial_islet_load()
                # se genera la estadistica
                self.initial_islet_stats_load()

            final_islet_file_load = glob.glob(filespath+'/**/*_postprocessed_islet.txt', recursive = True)
            
            process_log_file_load = glob.glob(filespath+'/**/*_process_log.txt', recursive = True)
            if final_islet_file_load:
                self.current_islet_file = initial_islet_file_load[0][:-8]
                self.post_processed_data = np.loadtxt(final_islet_file_load[0])
                self.tabWidget_islet_stats.setTabEnabled(1, True)
                self.tabWidget_Plots.setTabEnabled(1, True)
                self.plot_reconstructed_islet()
                self.contactos_load()
                self.tabWidget_islet_stats.setTabEnabled(2, True)
                self.tabWidget_Plots.setTabEnabled(2, True)
                self.build_network_load()
                self.tabWidget_islet_stats.setTabEnabled(3, True)
                self.tabWidget_Plots.setTabEnabled(3, True)
            if process_log_file_load:
                self.reconstructed_islet_stats(self.post_processed_data)

            sim_results_file_load = glob.glob(filespath+'/**/*_kuramoto_angles.data', recursive = True)
            if sim_results_file_load:
                self.sim_results_load = np.loadtxt(sim_results_file_load[0])
                self.plot_kuramoto_results_load()
            self.actionExport_data.setEnabled(False)
            self.actionReconstruction.setEnabled(False)
            self.config_reconstruction_button.setEnabled(False)
            self.load_islet_button.setEnabled(False)
            self.load_islet_status_label.setEnabled(False)

            
            
    ## funcion que grafica islote inicial
    def plot_initial_islet_load(self):
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
        ax.set_xlabel('X ('+r'$\mu m$'+')')
        ax.set_ylabel('Y ('+r'$\mu m$'+')')
        ax.set_zlabel('Z ('+r'$\mu m$'+')')
        
        #ax.set_xlim(-10, 10)
        #ax.set_ylim(-10, 10)
        #ax.set_zlim(-10, 10)

        for cell in self.exp_islet_data:
            x_coord = cell[3]
            y_coord = cell[4]
            z_coord = cell[5]
            # si no hay columna de radio
            #r_cell = cell[0]
            r_cell = 8.0
            cell_type = cell[2]
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

        center_coords = self.islet_center(self.exp_islet_data[:,3:])
        ax.scatter(center_coords[0], center_coords[1], center_coords[2], color="Red", label=r'$\alpha$'+"-cells")
        ax.scatter(center_coords[0], center_coords[1], center_coords[2], color="Green", label=r'$\beta$'+"-cells")
        ax.scatter(center_coords[0], center_coords[1], center_coords[2], color="Blue", label=r'$\delta$'+"-cells")
        ax.legend(frameon=False, loc='lower center', ncol=3)
        #ax.scatter(self.exp_islet_data[:,1], self.exp_islet_data[:,2], self.exp_islet_data[:,3],c=self.pointcolors(self.exp_islet_data[:,0]))
        #c=self.pointcolors(self.exp_islet_data[:,0]), label=self.cell_labels(self.exp_islet_data[:,0])
        
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
    def initial_islet_stats_load(self):
        
        #stats islote
        ncells = np.shape(self.exp_islet_data)[0]
        self.ini_ncells_value.setText(str(ncells))
        self.ini_ncells_perc.setText(str(100.00) + " %")
        
        #stats alfas
        nalphas = np.count_nonzero(self.exp_islet_data[:,2] == 11.)
        perc_alphas = np.round(nalphas/ncells*100, 2)
        self.ini_alphacells_value.setText(str(nalphas))
        self.ini_alphacells_perc.setText(str(perc_alphas) + " %")

        nbetas = np.count_nonzero(self.exp_islet_data[:,2] == 12.)
        perc_betas = np.round(nbetas/ncells * 100, 2)
        self.ini_betacells_value.setText(str(nbetas))
        self.ini_betacells_perc.setText(str(perc_betas)+ " %")

        ndeltas  = np.count_nonzero(self.exp_islet_data[:,2] == 13.)
        perc_deltas = np.round(ndeltas * 100.  / ncells,2)
        self.ini_deltacells_value.setText(str(ndeltas))
        self.ini_deltacells_perc.setText(str(perc_deltas)+ " %")
        #print("nalfas = " + str(nalphas) +" "+ str(perc_alphas))
        #print("nbetas = " + str(nbetas) +" "+ str(perc_betas))
        #print("ndeltas = " + str(ndeltas) +" "+ str(perc_deltas))


    def build_network_load(self):
        isletdata = self.post_processed_data
        # global connectivity
        #g_connectivity = np.loadtxt(self.current_islet_file[:-4]+"_all_contacts.txt")
        np.fill_diagonal(self.contacts_islet['all'], 0.)
        tipo_global = isletdata[:,2]
        G_global = nx.from_numpy_matrix(self.contacts_islet['all'])
        self.tabWidget_Plots.setTabEnabled(3, True)
        self.tabWidget_Plots.setCurrentIndex(3)
        self.tabWidget_islet_stats.setTabEnabled(3, True)
        self.tabWidget_islet_stats.setCurrentIndex(3)
        #self.network_status_button.setText("Network generated")
        #self.network_status_button.setStyleSheet("color: Green")
        self.plot_network(G_global, tipo_global)
        self.network_stats(G_global)
        #self.network_button.setEnabled(False)
        #self.network_metrics_plots_butthon.setEnabled(True)


    def plot_kuramoto_results_load(self):
        data = self.sim_results_load
        #print(np.shape(data))
        layout = QtWidgets.QVBoxLayout()
        self.kuramoto_results_tab = QtWidgets.QWidget()
        self.kuramoto_results_tab.setObjectName("kuramoto_results_tab")
        self.kuramoto_results_tab.setLayout(layout)

        figure, (ax1, ax2) = plt.subplots(2)
        #figure = plt.figure()
        #figure.subplots_adjust(left=0.1, right=0.99, bottom=0.05, top=1.0, wspace=0.2, hspace=0.2)
        new_canvas = FigureCanvas(figure)
        new_canvas.setFocusPolicy(QtCore.Qt.StrongFocus)
        new_canvas.setFocus()
        
        #np.linspace(0, model.T, int(model.T/model.dt)),
        ax2.plot(data[:,0],[self.phase_coherence(vec)
            for vec in data[:,self.ind_alfas]], 'o')
        ax2.get_yaxis().get_major_formatter().set_useOffset(False)
        ax2.get_yaxis().set_major_formatter(FormatStrFormatter('%.2f'))
        ax2.set_xlabel("Time (s)")
        ax2.set_ylabel("Sync index")

        #phase_coherence_alphas = self.phase_coherence(data[:, self.ind_alfas+1].T)
        #phase_coherence_betas = self.phase_coherence(data[:, self.ind_betas+1].T)
        #phase_coherence_deltas = self.phase_coherence(data[:, self.ind_deltas+1].T)
        #phase_coherence_islet = self.phase_coherence(data[:, 1:].T)
        #plt.plot(theta_data[:,0],[phase_coherence(vec) for vec in theta_data[:,1:]],'o')


        sum_osc_alphas = np.sum(np.sin(data[:, self.ind_alfas+1]), 1)
        sum_osc_betas = np.sum(np.sin(data[:, self.ind_betas+1]), 1)
        sum_osc_deltas = np.sum(np.sin(data[:,self.ind_deltas+1]), 1)
        sum_osc_islote = np.sum(np.sin(data[:, 1:]), 1)

        
        #fig.suptitle('Vertically stacked subplots')
        ax1.plot(data[:,0],sum_osc_islote, color="Black", label = "Islet")
        ax1.plot(data[:,0],sum_osc_alphas, color="Red", label = r'$\alpha$'+'-cells')
        ax1.plot(data[:,0],sum_osc_betas, color="Green", label = r'$\beta$'+'-cells')
        ax1.plot(data[:,0],sum_osc_deltas, color="Blue", label = r'$\delta$'+'-cells')
        ax1.set_xlabel("Time (s)")
        ax1.set_ylabel("Sin("+r'$\theta$'+")")
        ax1.legend(frameon=False, loc='lower center', ncol=4, bbox_to_anchor=(0.5, 1.01))
        #ax2.plot(phase_coherence_islet, color="Black")
        #ax2.plot(phase_coherence_alphas, color="Red")
        #ax2.plot(phase_coherence_betas, color="Green")
        #ax2.plot(phase_coherence_deltas, color="Blue")
        #ax.mouse_init()

        new_toolbar = NavigationToolbar(new_canvas, self.kuramoto_results_tab)
        unwanted_buttons = ["Subplots"]
        for x in new_toolbar.actions():
            if x.text() in unwanted_buttons:
                new_toolbar.removeAction(x)

        layout.addWidget(new_canvas)
        layout.addWidget(new_toolbar)
        #self.tabWidget_stats.addTab(new_tab, "txt")
        self.tabWidget_Plots.addTab(self.kuramoto_results_tab, "Simulation")
        self.toolbar_handles.append(new_toolbar)
        self.canvases.append(new_canvas)
        self.figure_handles.append(figure)
        #self.tab_handles.append(self.contacts_plot_tab)    
        self.tab_handles.append(self.kuramoto_results_tab)
        self.tabWidget_Plots.setCurrentIndex(4)

    def contactos_load(self):
        isletdata = self.post_processed_data
        # contactos de cualquier tipo
        contacts_global = 0
        # contactos alfa-alfa
        contacts_alfas = 0
        # contactos beta-beta
        contacts_betas = 0
        # contactos delta-delta
        contacts_deltas = 0
        # contactos alfa-beta
        contacts_alfas_betas = 0
        # contactos alfas-delta
        contacts_alfas_deltas = 0
        # contactos betas-deltas
        contacts_betas_deltas = 0
        # Matriz de conectividad b-b y b-d
        contact_matrix_bb_bd = []
        # Matriz de conectividad a-a
        contact_matrix_aa = []
        # Matriz de conectividad a-b
        contact_matrix_ab = []
        # Matriz de conetividad a-d
        contact_matrix_ad = []
        # Matriz de conectividad b-b
        contact_matrix_bb = []
        # Matriz de conectividad b-d 
        contact_matrix_bd = []
        # Matriz de conectividad d-d
        contact_matrix_dd = []
        # Matriz de conectividad global
        contact_matrix = []
        i = 0
        for cell1 in isletdata:
            x1 = cell1[3]
            y1 = cell1[4]
            z1 = cell1[5]
            # todos
            cell1_contact = []
            # bb-bd
            cell1_contact_bb_bd = []
            # aa
            cell1_contact_aa = []
            # ab
            cell1_contact_ab = []
            # ad
            cell1_contact_ad = []
            # bb
            cell1_contact_bb = []
            # bd 
            cell1_contact_bd = []
            # dd
            cell1_contact_dd = []
            j = 0
            for cell2 in isletdata:
                x2 = cell2[3]
                y2 = cell2[4]
                z2 = cell2[5]
                if i == j:
                    cell1_contact.append(cell1[2])
                    cell1_contact_bb_bd.append(0)
                    cell1_contact_aa.append(0)
                    cell1_contact_ab.append(0)
                    cell1_contact_ad.append(0)
                    cell1_contact_bb.append(0)
                    cell1_contact_bd.append(0)
                    cell1_contact_dd.append(0)
                    j = j + 1
                    continue
                d12 = np.sqrt( (x2 - x1)**2 + (y2 - y1)**2 + (z2 -z1)**2)
                # contacto de cualquier tipo
                if cell1[0] + cell2[0] + self.contacttol >= d12:
                    cell1_contact.append(1)
                    contacts_global +=1
                else:
                    cell1_contact.append(0)
                # betas-betas    
                if (cell1[2] == 12.0 and cell2[2] == 12.0):
                    cell1_contact_aa.append(0)
                    cell1_contact_ab.append(0)
                    cell1_contact_ad.append(0)
                    cell1_contact_bd.append(0)
                    cell1_contact_dd.append(0)
                    if cell1[0] + cell2[0] + self.contacttol >= d12:
                        cell1_contact_bb_bd.append(1)
                        cell1_contact_bb.append(1)
                        contacts_betas += 1
                    else:
                        cell1_contact_bb_bd.append(0)
                        cell1_contact_bb.append(0)
                # alfas-alfas
                elif (cell1[2] == 11.0 and cell2[2] == 11.0):
                    cell1_contact_bb_bd.append(0)
                    cell1_contact_ab.append(0)
                    cell1_contact_ad.append(0)
                    cell1_contact_bb.append(0)
                    cell1_contact_bd.append(0)
                    cell1_contact_dd.append(0)
                    if cell1[0] + cell2[0] + self.contacttol >= d12:
                        contacts_alfas += 1
                        cell1_contact_aa.append(1)
                    else:
                        cell1_contact_aa.append(0)
                # deltas-deltas
                elif (cell1[2] == 13.0 and cell2[2] == 13.0):
                    cell1_contact_bb_bd.append(0)
                    cell1_contact_aa.append(0)
                    cell1_contact_ab.append(0)
                    cell1_contact_ad.append(0)
                    cell1_contact_bd.append(0)
                    cell1_contact_bb.append(0)
                    if cell1[0] + cell2[0] + self.contacttol >= d12:
                        contacts_deltas += 1
                        cell1_contact_dd.append(1)
                    else:
                        cell1_contact_dd.append(0)
                # betas - deltas
                elif (cell1[2] == 12.0 and cell2[2] == 13.0) or (cell1[2] == 13.0 and cell2[2] == 12.0):
                    cell1_contact_aa.append(0)
                    cell1_contact_ab.append(0)
                    cell1_contact_ad.append(0)
                    cell1_contact_bb.append(0)
                    cell1_contact_dd.append(0)
                    if cell1[0] + cell2[0] + self.contacttol >= d12:
                        cell1_contact_bb_bd.append(1)
                        contacts_betas_deltas += 1
                        cell1_contact_bd.append(1)
                    else:
                        cell1_contact_bb_bd.append(0)
                        cell1_contact_bd.append(0)
                # alfas - betas
                elif (cell1[2] == 11.0 and cell2[2] == 12.0) or (cell1[2] == 12.0 and cell2[2] == 11.0):
                    cell1_contact_bb_bd.append(0)
                    cell1_contact_aa.append(0)
                    cell1_contact_ad.append(0)
                    cell1_contact_bb.append(0)
                    cell1_contact_dd.append(0)
                    cell1_contact_bd.append(0)
                    if cell1[0] + cell2[0] + self.contacttol >= d12:
                        contacts_alfas_betas += 1
                        cell1_contact_ab.append(1)
                    else:
                        cell1_contact_ab.append(0)
                elif (cell1[2] == 11.0 and cell2[2] == 13.0) or (cell1[2] == 13.0 and cell2[2] == 11.0):
                    cell1_contact_bb_bd.append(0)
                    cell1_contact_aa.append(0)
                    cell1_contact_ab.append(0)
                    cell1_contact_bd.append(0)
                    cell1_contact_bb.append(0)
                    cell1_contact_dd.append(0)
                    if cell1[0] + cell2[0] + self.contacttol >= d12:
                        contacts_alfas_deltas += 1 
                        cell1_contact_ad.append(1)
                    else:
                        cell1_contact_ad.append(0)
                else:
                    print('Caso raro')
                    #print(str(cell1[2]) + ' , ' + str(cell2[2]))
                    #cell1_contact.append(0)
                #print(np.sum(cell1_contact))
                j = j + 1
            #print(np.shape(cell1_contact))
            contact_matrix.append(np.asarray(cell1_contact))
            contact_matrix_bb_bd.append(np.asarray(cell1_contact_bb_bd))
            contact_matrix_aa.append(np.asarray(cell1_contact_aa))
            contact_matrix_ab.append(np.asarray(cell1_contact_ab))
            contact_matrix_ad.append(np.asarray(cell1_contact_ad))
            contact_matrix_bb.append(np.asarray(cell1_contact_bb))
            contact_matrix_bd.append(np.asarray(cell1_contact_bd))
            contact_matrix_dd.append(np.asarray(cell1_contact_dd))
            i = i + 1
        
        
        self.contacts_islet['all'] = np.stack(np.array(contact_matrix), axis = 0)
        #np.savetxt(self.current_islet_file[:-4]+"_all_contacts.txt", self.contacts_islet['all'], fmt='%1.0f')
        self.contacts_islet['bbbd'] = np.stack(np.array(contact_matrix_bb_bd), axis=0)
        #np.savetxt(self.current_islet_file[:-4]+"_bbbd_contacts.txt", self.contacts_islet['bbbd'], fmt='%1.0f')
        self.contacts_islet['aa'] = np.stack(np.array(contact_matrix_aa), axis=0)
        #np.savetxt(self.current_islet_file[:-4]+"_aa_contacts.txt", self.contacts_islet['aa'], fmt='%1.0f')
        self.contacts_islet['ab'] = np.stack(np.array(contact_matrix_ab), axis=0)
        #np.savetxt(self.current_islet_file[:-4]+"_ab_contacts.txt", self.contacts_islet['ab'], fmt='%1.0f')
        self.contacts_islet['ad'] = np.stack(np.array(contact_matrix_ad), axis=0)
        #np.savetxt(self.current_islet_file[:-4]+"_ad_contacts.txt", self.contacts_islet['ad'], fmt='%1.0f')
        self.contacts_islet['bb'] = np.stack(np.array(contact_matrix_bb), axis=0)
        #np.savetxt(self.current_islet_file[:-4]+"_bb_contacts.txt", self.contacts_islet['bb'], fmt='%1.0f')
        self.contacts_islet['bd'] = np.stack(np.array(contact_matrix_bd), axis=0)
        #np.savetxt(self.current_islet_file[:-4]+"_bd_contacts.txt", self.contacts_islet['bd'], fmt='%1.0f')
        self.contacts_islet['dd'] = np.stack(np.array(contact_matrix_dd), axis=0)
        #np.savetxt(self.current_islet_file[:-4]+"_dd_contacts.txt", self.contacts_islet['dd'], fmt='%1.0f')
        #contact_matrix.astype('int')
        contact_count_vec = [contacts_global/2, contacts_alfas/2, contacts_betas/2, contacts_deltas/2, contacts_alfas_betas/2, contacts_alfas_deltas/2, contacts_betas_deltas/2]
        #print(contact_count_vec)
        #return [contacts_islet, contact_count_vec]

        self.total_contacts_value.setText(str(contact_count_vec[0]))
        self.total_contacts_perc.setText("100 %")
        self.alphaalpha_contacts_value.setText(str(contact_count_vec[1]))
        self.alphaalpha_contacts_perc.setText(str(np.round(contact_count_vec[1]*100./contact_count_vec[0],2))+" %")
        self.betabeta_contacts_value.setText(str(contact_count_vec[2]))
        self.betabeta_contacts_perc.setText(str(np.round(contact_count_vec[2]*100./contact_count_vec[0],2))+" %")
        self.deltadelta_contacts_value.setText(str(contact_count_vec[3]))
        self.deltadelta_contacts_perc.setText(str(np.round(contact_count_vec[3]*100./contact_count_vec[0],2))+" %")
        self.alphabeta_contacts_value.setText(str(contact_count_vec[4]))
        self.alphabeta_contacts_perc.setText(str(np.round(contact_count_vec[4]*100./contact_count_vec[0],2))+" %")
        self.alphadelta_contacts_value.setText(str(contact_count_vec[5]))
        self.alphadelta_contacts_perc.setText(str(np.round(contact_count_vec[5]*100./contact_count_vec[0],2))+" %")
        self.betadelta_contacts_value.setText(str(contact_count_vec[6]))
        self.betadelta_contacts_perc.setText(str(np.round(contact_count_vec[6]*100./contact_count_vec[0],2))+" %")
        homotypic_contacts = np.sum(contact_count_vec[1:4])
        self.homotypic_contacts_value.setText(str(homotypic_contacts))
        self.homotypic_contacts_perc.setText(str(np.round(homotypic_contacts*100./contact_count_vec[0],2))+" %")
        heterotypic_contacts = np.sum(contact_count_vec[4:])
        self.heterotypic_contacts_value.setText(str(heterotypic_contacts))
        self.heterotypic_contacts_perc.setText(str(np.round(heterotypic_contacts*100./contact_count_vec[0],2))+" %")
        #return [contacts_islet, contact_count_vec]
        self.tabWidget_islet_stats.setTabEnabled(2, True)
        self.tabWidget_islet_stats.setCurrentIndex(2)
            
        self.tabWidget_Plots.setTabEnabled(2, True)
        self.tabWidget_Plots.setCurrentIndex(2)
        self.plot_contacts(isletdata)
        #self.contacts_button.setEnabled(False)
        #self.network_button.setEnabled(True)
        #self.contacts_status_label.setText("Contacts identified")
        #self.contacts_status_label.setStyleSheet("color: Green")
        self.tabWidget_settings.setTabEnabled(1, True)
        #self.contacts_plot_button.setEnabled(False)

    def disable_random_phase_config_button(self, radio):
        if radio.text() == "Random":
            if radio.isChecked() == True:
                self.initialphase_config_button.setEnabled(False)
            else:
                self.initialphase_config_button.setEnabled(True)

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
                

    def islet_center(self, coords_matrix):
        center_x = np.mean(coords_matrix[:,0])
        center_y = np.mean(coords_matrix[:,1])
        center_z = np.mean(coords_matrix[:,2])
        return [center_x, center_y, center_z]



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
        ax.set_xlabel('X ('+r'$\mu m$'+')')
        ax.set_ylabel('Y ('+r'$\mu m$'+')')
        ax.set_zlabel('Z ('+r'$\mu m$'+')')
        
        #ax.set_xlim(-10, 10)
        #ax.set_ylim(-10, 10)
        #ax.set_zlim(-10, 10)

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

        center_coords = self.islet_center(self.exp_islet_data[:,1:])
        ax.scatter(center_coords[0], center_coords[1], center_coords[2], color="Red", label=r'$\alpha$'+"-cells")
        ax.scatter(center_coords[0], center_coords[1], center_coords[2], color="Green", label=r'$\beta$'+"-cells")
        ax.scatter(center_coords[0], center_coords[1], center_coords[2], color="Blue", label=r'$\delta$'+"-cells")
        ax.legend(frameon=False, loc='lower center', ncol=3)
        #ax.scatter(self.exp_islet_data[:,1], self.exp_islet_data[:,2], self.exp_islet_data[:,3],c=self.pointcolors(self.exp_islet_data[:,0]))
        #c=self.pointcolors(self.exp_islet_data[:,0]), label=self.cell_labels(self.exp_islet_data[:,0])
        
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

    def cell_labels(self, celltypes):
        label=[]
        for l in celltypes:
            if l==11.:
                label.append(r'$\alpha-cells$')
            elif l==12.:
                cols.append(r'$\beta-cells$')
            else:
                cols.append(r'$\delta-cells$')
        return cols


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
        
        #opt_start_time = datetime.now()
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
            if sys_pf == 'darwin':
                subprocess.run(["gcc-10", fout , "-o", fout[:-2], "-lm", "-fopenmp"])
            else:
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

            #subprocess.run([fout[:-2]])
            #progressbar = ProgressBar(n, title = "Copying files...")
            #if progressbar.wasCanceled():
            #    break
            self.reconstruction_status_label.setText("Optimization in progress")
            self.reconstruction_status_label.setStyleSheet("color: Green")
            #print(fout)
            self.optstatus, computing_time = self.launch_opt_window(fout)
            #print("Checo estatus: " + str(optstatus))
            #t = threading.Thread(target=self.run_code, args=(fout,))
            #t.start()
            #while t.is_alive():
            #    pass
            if self.optstatus == 0:
                self.reconstruction_status_label.setText("Reconstruction aborted")
                self.reconstruction_status_label.setStyleSheet("color: Red")
            elif self.optstatus == 2:
                self.comp_time_value.setText(str(computing_time[0])+" h "+str(computing_time[1]) + " m " + str(computing_time[2]) + " s")
                self.reconstruction_status_label.setText("Optimization completed")
                self.reconstruction_status_label.setStyleSheet("color: Green")
                self.reconstruct_button.setEnabled(False)
                self.contacts_button.setEnabled(True)
                self.contacts_status_label.setEnabled(True)

                
                
                self.tabWidget_islet_stats.setTabEnabled(1, True)
                self.tabWidget_islet_stats.setCurrentIndex(1)
            
                self.tabWidget_Plots.setTabEnabled(1, True)
                self.tabWidget_Plots.setCurrentIndex(1)

                self.final_islet_data = np.loadtxt(self.current_islet_file[:-4]+'_reconstructed.txt')
                self.post_processed_data = self.postprocessIslet(self.final_islet_data)
                self.plot_reconstructed_islet()
                self.reconstructed_islet_stats(self.post_processed_data)
                self.processar_output_stats()
                self.plotOptConvergence()
                self.actionExport_data.setEnabled(True)

                
        except Exception as e:
            #print(fout[:-2])
            print(e)
            self.reconstruction_status_label.setText("Failed")
            self.reconstruction_status_label.setStyleSheet("color: Red")
        

    

    def launch_opt_window(self, fout):
        Dialog = QtWidgets.QDialog()
        ui = Ui_OptLog_Dialog()
        ui.setupUi(Dialog, fout, "Reconstruction Log")
        #isletlab_banner = pyfiglet.figlet_format("IsletLab", font="big")
        #ui.textEdit.setText()
        Dialog.exec_()
        Dialog.reject()
        return ui.optstatus, ui.computing_time_processed
        
    
    ## funcion que grafica islote inicial
    def plot_reconstructed_islet(self):
        #new_tab = QWidget()
        layout = QtWidgets.QVBoxLayout()
        self.final_islet_plot_tab.setLayout(layout)

        figure = plt.figure()
        figure.subplots_adjust(left=0.1, right=0.99, bottom=0.05, top=1.0, wspace=0.2, hspace=0.2)
        new_canvas = FigureCanvas(figure)
        new_canvas.setFocusPolicy(QtCore.Qt.StrongFocus)
        new_canvas.setFocus()
        
        ax = Axes3D(figure)
        ax.view_init(elev = -80., azim = 90)
        ax.set_xlabel('X ('+r'$\mu m$'+')')
        ax.set_ylabel('Y ('+r'$\mu m$'+')')
        ax.set_zlabel('Z ('+r'$\mu m$'+')')
        #ax.set_xlim(-10, 10)
        #ax.set_ylim(-10, 10)
        #ax.set_zlim(-10, 10)
        #ax.set_zlabel('z')
        #ax.set_zticks([])
        for cell in self.post_processed_data:
            x_coord = cell[3]
            y_coord = cell[4]
            z_coord = cell[5]
            # si no hay columna de radio
            r_cell = cell[0]
            #r_cell = 8.
            cell_type = cell[2]
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

        center_coords = self.islet_center(self.post_processed_data[:,3:])
        ax.scatter(center_coords[0], center_coords[1], center_coords[2], color="Red", label=r'$\alpha$'+"-cells")
        ax.scatter(center_coords[0], center_coords[1], center_coords[2], color="Green", label=r'$\beta$'+"-cells")
        ax.scatter(center_coords[0], center_coords[1], center_coords[2], color="Blue", label=r'$\delta$'+"-cells")
        ax.legend(frameon=False, loc='lower center', ncol=3)

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


    # funcion que saca estadística de islote final
    def reconstructed_islet_stats(self, finalisletdata):
        
        #stats islote
        ncells = np.shape(finalisletdata)[0]
        self.fin_ncells_value.setText(str(ncells))
        self.fin_ncells_perc.setText(str(100.00) + " %")
        
        #stats alfas
        nalphas = np.count_nonzero(finalisletdata[:,2] == 11.)
        perc_alphas = np.round(nalphas/ncells*100, 2)
        self.fin_alphacells_value.setText(str(nalphas))
        self.fin_alphacells_perc.setText(str(perc_alphas) + " %")

        nbetas = np.count_nonzero(finalisletdata[:,2] == 12.)
        perc_betas = np.round(nbetas/ncells * 100, 2)
        self.fin_betacells_value.setText(str(nbetas))
        self.fin_betacells_perc.setText(str(perc_betas)+ " %")

        ndeltas  = np.count_nonzero(finalisletdata[:,2] == 13.)
        perc_deltas = np.round(ndeltas * 100.  / ncells,2)
        self.fin_deltacells_value.setText(str(ndeltas))
        self.fin_deltacells_perc.setText(str(perc_deltas)+ " %")
        self.calculate_volumes(finalisletdata)
        self.calculate_opt_stats(finalisletdata)
        self.processar_output_stats()
        


    def restart(self):
        QtCore.QCoreApplication.quit()
        status = QtCore.QProcess.startDetached(sys.executable, sys.argv)
        print(status)
    

    def calculate_volumes(self, finalisletdata):
        self.ind_alfas = np.where(finalisletdata[:,2] == 11.)[0]
        self.ind_betas = np.where(finalisletdata[:,2] == 12.)[0]
        self.ind_deltas = np.where(finalisletdata[:,2] == 13.)[0]
        volcells = 4./3.*np.pi*finalisletdata[:,0]
        totalvol = np.sum(volcells)
        self.fin_total_vol_value.setText('{:.1e}'.format(Decimal(totalvol)))
        self.fin_total_vol_perc.setText('100.0 %')
        volalfas = np.sum(volcells[self.ind_alfas])
        self.fin_alpha_vol_value.setText('{:.1e}'.format(Decimal(volalfas)))
        self.fin_alpha_vol_perc.setText(str(np.round(volalfas*100./totalvol,2))+' %')
        volbetas = np.sum(volcells[self.ind_betas])
        self.fin_beta_vol_value.setText('{:.1e}'.format(Decimal(volbetas)))
        self.fin_beta_vol_perc.setText(str(np.round(volbetas*100./totalvol,2))+' %')
        voldeltas = np.sum(volcells[self.ind_deltas])
        self.fin_delta_vol_value.setText('{:.1e}'.format(Decimal(voldeltas)))
        self.fin_delta_vol_perc.setText(str(np.round(voldeltas*100./totalvol,2))+' %')


    def calculate_opt_stats(self, finalisletdata):
        ncells_opt = len(finalisletdata)
        ncells_exp = len(self.exp_islet_data)
        perc_of_exp = ncells_opt/ncells_exp * 100.
        self.perc_of_total_value.setText(str(np.round(perc_of_exp,2)))
        noverlaps = ncells_exp - ncells_opt
        self.n_overlaps_value.setText(str(noverlaps))

    def processar_output_stats(self):
        process_out_file = self.current_islet_file[:-4]+"_process_log.txt"
    
        processdata = np.loadtxt(process_out_file, skiprows=1, usecols=(0,1,2,3,4,5))
    
        self.total_iter_value.setText('{:.2e}'.format(Decimal(np.sum(processdata[:,5]))))

        self.acc_iter_value.setText('{:.2e}'.format(Decimal(np.sum(processdata[:,4]))))

    def postprocessIslet(self, finalisletdata):
        ncells = len(finalisletdata)
        overlapped_cells = []
        for i in np.arange(ncells):
            for j in np.arange(i+1, ncells):
                #print(i,j)
                sumradios = finalisletdata[i,0] + finalisletdata[j,0]
                distcenters = np.linalg.norm(finalisletdata[i,3:6]-finalisletdata[j,3:6])
                #distcenters = (sqrt((finalisletdata[i,3]-finalisletdata[j,3])^2+
                #    (finalisletdata[i,4]-finalisletdata[j,4])^2))
                #print(distcenters)
                if sumradios >= distcenters:
                    #print("suma de radios: " + str(sumradios))
                    #print("distancia: " + str(distcenters))
                    #overlapped_pair = [i,j]
                    overlapped_cells.append(np.random.choice([i,j]))
                else:
                    continue

        finished_islet = np.delete(finalisletdata, np.unique(overlapped_cells), axis=0)
        #print(overlapped_cells)
        #print(finished_islet)
        np.savetxt(self.current_islet_file[:-4]+"_overlapped_cells.txt", np.array(overlapped_cells), fmt='%1.0f')
        np.savetxt(self.current_islet_file[:-4]+"_postprocessed_islet.txt", finished_islet, fmt='%1.5f')
        return finished_islet

    def contactos(self):
        isletdata = np.loadtxt(self.current_islet_file[:-4]+"_postprocessed_islet.txt")
        # contactos de cualquier tipo
        contacts_global = 0
        # contactos alfa-alfa
        contacts_alfas = 0
        # contactos beta-beta
        contacts_betas = 0
        # contactos delta-delta
        contacts_deltas = 0
        # contactos alfa-beta
        contacts_alfas_betas = 0
        # contactos alfas-delta
        contacts_alfas_deltas = 0
        # contactos betas-deltas
        contacts_betas_deltas = 0
        # Matriz de conectividad b-b y b-d
        contact_matrix_bb_bd = []
        # Matriz de conectividad a-a
        contact_matrix_aa = []
        # Matriz de conectividad a-b
        contact_matrix_ab = []
        # Matriz de conetividad a-d
        contact_matrix_ad = []
        # Matriz de conectividad b-b
        contact_matrix_bb = []
        # Matriz de conectividad b-d 
        contact_matrix_bd = []
        # Matriz de conectividad d-d
        contact_matrix_dd = []
        # Matriz de conectividad global
        contact_matrix = []
        i = 0
        for cell1 in isletdata:
            x1 = cell1[3]
            y1 = cell1[4]
            z1 = cell1[5]
            # todos
            cell1_contact = []
            # bb-bd
            cell1_contact_bb_bd = []
            # aa
            cell1_contact_aa = []
            # ab
            cell1_contact_ab = []
            # ad
            cell1_contact_ad = []
            # bb
            cell1_contact_bb = []
            # bd 
            cell1_contact_bd = []
            # dd
            cell1_contact_dd = []
            j = 0
            for cell2 in isletdata:
                x2 = cell2[3]
                y2 = cell2[4]
                z2 = cell2[5]
                if i == j:
                    cell1_contact.append(cell1[2])
                    cell1_contact_bb_bd.append(0)
                    cell1_contact_aa.append(0)
                    cell1_contact_ab.append(0)
                    cell1_contact_ad.append(0)
                    cell1_contact_bb.append(0)
                    cell1_contact_bd.append(0)
                    cell1_contact_dd.append(0)
                    j = j + 1
                    continue
                d12 = np.sqrt( (x2 - x1)**2 + (y2 - y1)**2 + (z2 -z1)**2)
                # contacto de cualquier tipo
                if cell1[0] + cell2[0] + self.contacttol >= d12:
                    cell1_contact.append(1)
                    contacts_global +=1
                else:
                    cell1_contact.append(0)
                # betas-betas    
                if (cell1[2] == 12.0 and cell2[2] == 12.0):
                    cell1_contact_aa.append(0)
                    cell1_contact_ab.append(0)
                    cell1_contact_ad.append(0)
                    cell1_contact_bd.append(0)
                    cell1_contact_dd.append(0)
                    if cell1[0] + cell2[0] + self.contacttol >= d12:
                        cell1_contact_bb_bd.append(1)
                        cell1_contact_bb.append(1)
                        contacts_betas += 1
                    else:
                        cell1_contact_bb_bd.append(0)
                        cell1_contact_bb.append(0)
                # alfas-alfas
                elif (cell1[2] == 11.0 and cell2[2] == 11.0):
                    cell1_contact_bb_bd.append(0)
                    cell1_contact_ab.append(0)
                    cell1_contact_ad.append(0)
                    cell1_contact_bb.append(0)
                    cell1_contact_bd.append(0)
                    cell1_contact_dd.append(0)
                    if cell1[0] + cell2[0] + self.contacttol >= d12:
                        contacts_alfas += 1
                        cell1_contact_aa.append(1)
                    else:
                        cell1_contact_aa.append(0)
                # deltas-deltas
                elif (cell1[2] == 13.0 and cell2[2] == 13.0):
                    cell1_contact_bb_bd.append(0)
                    cell1_contact_aa.append(0)
                    cell1_contact_ab.append(0)
                    cell1_contact_ad.append(0)
                    cell1_contact_bd.append(0)
                    cell1_contact_bb.append(0)
                    if cell1[0] + cell2[0] + self.contacttol >= d12:
                        contacts_deltas += 1
                        cell1_contact_dd.append(1)
                    else:
                        cell1_contact_dd.append(0)
                # betas - deltas
                elif (cell1[2] == 12.0 and cell2[2] == 13.0) or (cell1[2] == 13.0 and cell2[2] == 12.0):
                    cell1_contact_aa.append(0)
                    cell1_contact_ab.append(0)
                    cell1_contact_ad.append(0)
                    cell1_contact_bb.append(0)
                    cell1_contact_dd.append(0)
                    if cell1[0] + cell2[0] + self.contacttol >= d12:
                        cell1_contact_bb_bd.append(1)
                        contacts_betas_deltas += 1
                        cell1_contact_bd.append(1)
                    else:
                        cell1_contact_bb_bd.append(0)
                        cell1_contact_bd.append(0)
                # alfas - betas
                elif (cell1[2] == 11.0 and cell2[2] == 12.0) or (cell1[2] == 12.0 and cell2[2] == 11.0):
                    cell1_contact_bb_bd.append(0)
                    cell1_contact_aa.append(0)
                    cell1_contact_ad.append(0)
                    cell1_contact_bb.append(0)
                    cell1_contact_dd.append(0)
                    cell1_contact_bd.append(0)
                    if cell1[0] + cell2[0] + self.contacttol >= d12:
                        contacts_alfas_betas += 1
                        cell1_contact_ab.append(1)
                    else:
                        cell1_contact_ab.append(0)
                elif (cell1[2] == 11.0 and cell2[2] == 13.0) or (cell1[2] == 13.0 and cell2[2] == 11.0):
                    cell1_contact_bb_bd.append(0)
                    cell1_contact_aa.append(0)
                    cell1_contact_ab.append(0)
                    cell1_contact_bd.append(0)
                    cell1_contact_bb.append(0)
                    cell1_contact_dd.append(0)
                    if cell1[0] + cell2[0] + self.contacttol >= d12:
                        contacts_alfas_deltas += 1 
                        cell1_contact_ad.append(1)
                    else:
                        cell1_contact_ad.append(0)
                else:
                    print('Caso raro')
                    #print(str(cell1[2]) + ' , ' + str(cell2[2]))
                    #cell1_contact.append(0)
                #print(np.sum(cell1_contact))
                j = j + 1
            #print(np.shape(cell1_contact))
            contact_matrix.append(np.asarray(cell1_contact))
            contact_matrix_bb_bd.append(np.asarray(cell1_contact_bb_bd))
            contact_matrix_aa.append(np.asarray(cell1_contact_aa))
            contact_matrix_ab.append(np.asarray(cell1_contact_ab))
            contact_matrix_ad.append(np.asarray(cell1_contact_ad))
            contact_matrix_bb.append(np.asarray(cell1_contact_bb))
            contact_matrix_bd.append(np.asarray(cell1_contact_bd))
            contact_matrix_dd.append(np.asarray(cell1_contact_dd))
            i = i + 1
        
        
        self.contacts_islet['all'] = np.stack(np.array(contact_matrix), axis = 0)
        np.savetxt(self.current_islet_file[:-4]+"_all_contacts.txt", self.contacts_islet['all'], fmt='%1.0f')
        self.contacts_islet['bbbd'] = np.stack(np.array(contact_matrix_bb_bd), axis=0)
        np.savetxt(self.current_islet_file[:-4]+"_bbbd_contacts.txt", self.contacts_islet['bbbd'], fmt='%1.0f')
        self.contacts_islet['aa'] = np.stack(np.array(contact_matrix_aa), axis=0)
        np.savetxt(self.current_islet_file[:-4]+"_aa_contacts.txt", self.contacts_islet['aa'], fmt='%1.0f')
        self.contacts_islet['ab'] = np.stack(np.array(contact_matrix_ab), axis=0)
        np.savetxt(self.current_islet_file[:-4]+"_ab_contacts.txt", self.contacts_islet['ab'], fmt='%1.0f')
        self.contacts_islet['ad'] = np.stack(np.array(contact_matrix_ad), axis=0)
        np.savetxt(self.current_islet_file[:-4]+"_ad_contacts.txt", self.contacts_islet['ad'], fmt='%1.0f')
        self.contacts_islet['bb'] = np.stack(np.array(contact_matrix_bb), axis=0)
        np.savetxt(self.current_islet_file[:-4]+"_bb_contacts.txt", self.contacts_islet['bb'], fmt='%1.0f')
        self.contacts_islet['bd'] = np.stack(np.array(contact_matrix_bd), axis=0)
        np.savetxt(self.current_islet_file[:-4]+"_bd_contacts.txt", self.contacts_islet['bd'], fmt='%1.0f')
        self.contacts_islet['dd'] = np.stack(np.array(contact_matrix_dd), axis=0)
        np.savetxt(self.current_islet_file[:-4]+"_dd_contacts.txt", self.contacts_islet['dd'], fmt='%1.0f')
        #contact_matrix.astype('int')
        contact_count_vec = [contacts_global/2, contacts_alfas/2, contacts_betas/2, contacts_deltas/2, contacts_alfas_betas/2, contacts_alfas_deltas/2, contacts_betas_deltas/2]
        #print(contact_count_vec)
        #return [contacts_islet, contact_count_vec]

        self.total_contacts_value.setText(str(contact_count_vec[0]))
        self.total_contacts_perc.setText("100 %")
        self.alphaalpha_contacts_value.setText(str(contact_count_vec[1]))
        self.alphaalpha_contacts_perc.setText(str(np.round(contact_count_vec[1]*100./contact_count_vec[0],2))+" %")
        self.betabeta_contacts_value.setText(str(contact_count_vec[2]))
        self.betabeta_contacts_perc.setText(str(np.round(contact_count_vec[2]*100./contact_count_vec[0],2))+" %")
        self.deltadelta_contacts_value.setText(str(contact_count_vec[3]))
        self.deltadelta_contacts_perc.setText(str(np.round(contact_count_vec[3]*100./contact_count_vec[0],2))+" %")
        self.alphabeta_contacts_value.setText(str(contact_count_vec[4]))
        self.alphabeta_contacts_perc.setText(str(np.round(contact_count_vec[4]*100./contact_count_vec[0],2))+" %")
        self.alphadelta_contacts_value.setText(str(contact_count_vec[5]))
        self.alphadelta_contacts_perc.setText(str(np.round(contact_count_vec[5]*100./contact_count_vec[0],2))+" %")
        self.betadelta_contacts_value.setText(str(contact_count_vec[6]))
        self.betadelta_contacts_perc.setText(str(np.round(contact_count_vec[6]*100./contact_count_vec[0],2))+" %")
        homotypic_contacts = np.sum(contact_count_vec[1:4])
        self.homotypic_contacts_value.setText(str(homotypic_contacts))
        self.homotypic_contacts_perc.setText(str(np.round(homotypic_contacts*100./contact_count_vec[0],2))+" %")
        heterotypic_contacts = np.sum(contact_count_vec[4:])
        self.heterotypic_contacts_value.setText(str(heterotypic_contacts))
        self.heterotypic_contacts_perc.setText(str(np.round(heterotypic_contacts*100./contact_count_vec[0],2))+" %")
        #return [contacts_islet, contact_count_vec]
        self.tabWidget_islet_stats.setTabEnabled(2, True)
        self.tabWidget_islet_stats.setCurrentIndex(2)
            
        self.tabWidget_Plots.setTabEnabled(2, True)
        self.tabWidget_Plots.setCurrentIndex(2)
        self.plot_contacts(isletdata)
        self.contacts_button.setEnabled(False)
        self.network_button.setEnabled(True)
        self.contacts_status_label.setText("Contacts identified")
        self.contacts_status_label.setStyleSheet("color: Green")
        self.tabWidget_settings.setTabEnabled(1, True)
        #self.contacts_plot_button.setEnabled(False)

        
    def plot_contacts(self, isletdata):
        layout = QtWidgets.QVBoxLayout()
        self.contacts_plot_tab.setLayout(layout)

        figure = plt.figure()
        figure.subplots_adjust(left=0.1, right=0.99, bottom=0.05, top=1.0, wspace=0.2, hspace=0.2)
        new_canvas = FigureCanvas(figure)
        new_canvas.setFocusPolicy(QtCore.Qt.StrongFocus)
        new_canvas.setFocus()
        
        ax = Axes3D(figure)
        ax.set_xlabel('X (' + r'$\mu$ m'+')')
        ax.set_ylabel('Y (' + r'$\mu$ m'+')')
        ax.set_zlabel('Z (' + r'$\mu$ m'+')')
        ax.view_init(elev = -80., azim = 90)
        # grafico los puntos (celulas)
        scattercolors = self.pointcolors(isletdata[:,2])
        ax.scatter(isletdata[:,3], isletdata[:,4],isletdata[:,5], c=scattercolors, s=3)
        ax.legend()

        #self.contacts_islet['bbbd'] = np.stack(np.array(contact_matrix_bb_bd), axis=0)
        #self.contacts_islet['aa'] = np.stack(np.array(contact_matrix_aa), axis=0)
        #self.contacts_islet['ab'] = np.stack(np.array(contact_matrix_ab), axis=0)
        #self.contacts_islet['ad'] = np.stack(np.array(contact_matrix_ad), axis=0)
        #self.contacts_islet['bb'] = np.stack(np.array(contact_matrix_bb), axis=0)
        #self.contacts_islet['bd'] = np.stack(np.array(contact_matrix_bd), axis=0)
        #self.contacts_islet['dd'] 

        for key, value in self.contacts_islet.items():
            if key == 'aa':
                linkcolor = 'red'
            elif key == 'ab':
                linkcolor = 'brown'
            elif key == 'ad':
                linkcolor = 'purple'
            elif key == 'bb':
                linkcolor = 'green'
            elif key == 'bd':
                linkcolor = 'cyan'
            elif key == 'dd':
                linkcolor = 'blue'

            for c1 in np.arange(len(value)):
                for c2 in np.arange(c1 + 1, len(value)):
                    if value[c1,c2] == 1:
                        ax.plot([isletdata[c1,3], isletdata[c2,3]], [isletdata[c1,4], isletdata[c2,4]], [isletdata[c1,5], isletdata[c2,5]], c='black')

       
        center_coords = self.islet_center(isletdata[:,3:])
        ax.scatter(center_coords[0], center_coords[1], center_coords[2], alpha=1, s=0.1, color="Red", label=r'$\alpha$'+"-cells")
        ax.scatter(center_coords[0], center_coords[1], center_coords[2], alpha=1, s=0.1, color="Green", label=r'$\beta$'+"-cells")
        ax.scatter(center_coords[0], center_coords[1], center_coords[2], alpha=1, s=0.1, color="Blue", label=r'$\delta$'+"-cells")
        ax.legend(frameon=False, loc='lower center', ncol=3, markerscale=20)

        ax.mouse_init()

        new_toolbar = NavigationToolbar(new_canvas, self.contacts_plot_tab)
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
        self.tab_handles.append(self.contacts_plot_tab)


    def pointcolors(self, celltypes):
        cols=[]
        for l in celltypes:
            if l==11.:
                cols.append('red')
            elif l==12.:
                cols.append('green')
            else:
                cols.append('blue')
        return cols


    def build_network(self):
        isletdata = np.loadtxt(self.current_islet_file[:-4]+"_postprocessed_islet.txt")
        # global connectivity
        #g_connectivity = np.loadtxt(self.current_islet_file[:-4]+"_all_contacts.txt")
        np.fill_diagonal(self.contacts_islet['all'], 0.)
        tipo_global = isletdata[:,2]
        G_global = nx.from_numpy_matrix(self.contacts_islet['all'])
        self.tabWidget_Plots.setTabEnabled(3, True)
        self.tabWidget_Plots.setCurrentIndex(3)
        self.tabWidget_islet_stats.setTabEnabled(3, True)
        self.tabWidget_islet_stats.setCurrentIndex(3)
        self.network_status_button.setText("Network generated")
        self.network_status_button.setStyleSheet("color: Green")
        self.plot_network(G_global, tipo_global)
        self.network_stats(G_global)
        self.network_button.setEnabled(False)
        #self.network_metrics_plots_butthon.setEnabled(True)

    def node_colors(self, tipocelulas):
        color_nodos = []
        for tipocel in tipocelulas:
            if tipocel == 12.:
                color_nodos.append('green')
            elif tipocel == 11.:
                color_nodos.append('red')
            else:
                color_nodos.append('blue')
        return color_nodos
    

    def plot_network(self, grafo, tipo_global):
        layout = QtWidgets.QVBoxLayout()
        self.networks_plot_tab.setLayout(layout)

        figure = plt.figure()
        #figure.subplots_adjust(left=0.1, right=0.99, bottom=0.05, top=1.0, wspace=0.2, hspace=0.2)
        new_canvas = FigureCanvas(figure)
        new_canvas.setFocusPolicy(QtCore.Qt.StrongFocus)
        new_canvas.setFocus()
        
        
        nx.draw(grafo, node_size=3,with_labels=False, node_color=self.node_colors(tipo_global),ax=figure.add_subplot(111))
        plt.scatter([],[], c="Red", label=r'$\alpha$-cells')
        plt.scatter([],[], c="Green", label=r'$\beta$-cells')
        plt.scatter([],[], c="Blue", label=r'$\delta$-cells')
        plt.legend(frameon=False, loc='lower center', ncol=3, markerscale=1, bbox_to_anchor=(0.5, -0.1))
        #ax.mouse_init()

        new_toolbar = NavigationToolbar(new_canvas, self.contacts_plot_tab)
        unwanted_buttons = ["Subplots"]
        for x in new_toolbar.actions():
            if x.text() in unwanted_buttons:
                new_toolbar.removeAction(x)

        layout.addWidget(new_canvas)
        layout.addWidget(new_toolbar)
        #self.tabWidget_stats.addTab(new_tab, "txt")
        self.toolbar_handles.append(new_toolbar)
        self.canvases.append(new_canvas)
        self.figure_handles.append(figure)
        self.tab_handles.append(self.contacts_plot_tab)    

    def network_stats(self, G_global):
        ave_clustering_global = nx.average_clustering(G_global)
        self.clustering_value.setText(str(np.round(ave_clustering_global,5)))
        degree_global = [v for k, v in G_global.degree()]
        ave_degree_global = np.mean(degree_global)
        self.degree_value.setText(str(np.round(ave_degree_global,5)))
        eficiencia_global_global = nx.global_efficiency(G_global)
        self.efficiency_value.setText(str(np.round(eficiencia_global_global,5)))
        dens_global = nx.density(G_global)
        self.density_value.setText(str(np.round(dens_global,5)))
        con_com_global = list(nx.connected_components(G_global))
        largest_component_global = max(con_com_global, key=len)
        subgraph_global = G_global.subgraph(largest_component_global)
        diameter_global = nx.diameter(subgraph_global)
        self.diameter_value.setText(str(np.round(diameter_global,5)))


    def plotOptConvergence(self):

        optdata = np.loadtxt(self.current_islet_file[:-4]+"_process_log.txt", skiprows=1, usecols=(0,1,2,3,4,5))
        layout = QtWidgets.QVBoxLayout()
        self.opt_conv_plot_tab = QtWidgets.QWidget()
        self.opt_conv_plot_tab.setObjectName("opt_conv_plot_tab")
        self.opt_conv_plot_tab.setLayout(layout)

        figure = plt.figure()
        #figure.subplots_adjust(left=0.1, right=0.99, bottom=0.05, top=1.0, wspace=0.2, hspace=0.2)
        new_canvas = FigureCanvas(figure)
        new_canvas.setFocusPolicy(QtCore.Qt.StrongFocus)
        new_canvas.setFocus()
        
        
        plt.plot(np.arange(len(optdata[:,2])), optdata[:,2])
        plt.xlabel("Temperature iteration")
        plt.ylabel("Number of overlapped cells")
        #plt.show()

        #ax.mouse_init()

        new_toolbar = NavigationToolbar(new_canvas, self.contacts_plot_tab)
        unwanted_buttons = ["Subplots"]
        for x in new_toolbar.actions():
            if x.text() in unwanted_buttons:
                new_toolbar.removeAction(x)

        layout.addWidget(new_canvas)
        layout.addWidget(new_toolbar)
        #self.tabWidget_stats.addTab(new_tab, "txt")
        self.tabWidget_Plots.addTab(self.opt_conv_plot_tab, "Convergence")
        self.toolbar_handles.append(new_toolbar)
        self.canvases.append(new_canvas)
        self.figure_handles.append(figure)
        #self.tab_handles.append(self.contacts_plot_tab)    
        self.tab_handles.append(self.opt_conv_plot_tab)
    

    def open_interaction_strength_dialog(self):
        Dialog = QtWidgets.QDialog()
        pars = [self.Kaa, self.Kba, self.Kda, self.Kab, self.Kbb, self.Kdb, self.Kad, self.Kbd, self.Kdd]
        ui = Ui_interaction_strength_Dialog()
        ui.setupUi(Dialog, pars)
        Dialog.exec_()

        if ui.Kaa_value.text() == "":
            ui.Kaa_value.setText(str(self.Kaa)) 
        else:
            self.Kaa = float(ui.Kaa_value.text())

        if ui.Kba_value.text() == "":
            ui.Kba_value.setText(str(self.Kba)) 
        else:
            self.Kba = float(ui.Kba_value.text())


        if ui.Kda_value.text() == "":
            ui.Kda_value.setText(str(self.Kda)) 
        else:
            self.Kda = float(ui.Kda_value.text())


        if ui.Kab_value.text() == "":
            ui.Kab_value.setText(str(self.Kab)) 
        else:
            self.Kab = float(ui.Kab_value.text())

        if ui.Kbb_value.text() == "":
            ui.Kbb_value.setText(str(self.Kbb)) 
        else:
            self.Kbb = float(ui.Kbb_value.text())

        if ui.Kdb_value.text() == "":
            ui.Kdb_value.setText(str(self.Kdb)) 
        else:
            self.Kdb = float(ui.Kdb_value.text())


        if ui.Kad_value.text() == "":
            ui.Kad_value.setText(str(self.Kad)) 
        else:
            self.Kad = float(ui.Kad_value.text())


        if ui.Kbd_value.text() == "":
            ui.Kbd_value.setText(str(self.Kbd)) 
        else:
            self.Kbd = float(ui.Kbd_value.text())


        if ui.Kdd_value.text() == "":
            ui.Kdd_value.setText(str(self.Kdd)) 
        else:
            self.Kdd = float(ui.Kdd_value.text())

    # def open_interaction_strength_file(self, s):
    #     #print("click", s)
    #     dlg = QtWidgets.QFileDialog()
    #     filename = dlg.getOpenFileName()
    #     #dlg.setWindowTitle("Hello")
    #     if filename[0]:
    #         try:
    #             self.int_strength_data = np.loadtxt(filename[0])
    #             self.interaction_strength_file = filename[0]
    #             # abrevio nombre para mostrar en GUI

    #             self.abbv_int_strength_filename = re.search("(/.*/)(.*)", self.interaction_strength_file)[2]
    #             #print(self.abbv_filename)
    #             #print(self.exp_islet_data[:,0])
    #             #print(self.current_islet_file)
    #             #self.load_islet_status_label.setText(self.abbv_filename + " loaded succesfully")
    #             #self.load_islet_status_label.setStyleSheet("color: Green")


    #             #self.load_islet_button.setEnabled(False)
    #             #self.reconstruction_status_label.setEnabled(True)
    #             #self.reconstruct_button.setEnabled(True)
    #             #self.tabWidget_islet_stats.setTabEnabled(0, True)
    #             #self.tabWidget_Plots.setTabEnabled(0, True)
    #         except: 
    #             print("Error abriendo interaction strength file")
    #             #self.load_islet_status_label.setText("Error loading islet file")
    #             #self.load_islet_status_label.setStyleSheet("color: Red")


    def selectInitialPhaseConfig(self):
        if self.initialphase_constant_radio.isChecked():
            self.initialphase_type = "Constant"
            self.open_const_phase_settings()
            #print(self.initialphase_type)
        if self.initialphase_random_radio.isChecked():
            self.initialphase_type = "Random"
            #self.open_rand_phase_settings()
            #print(self.initialphase_type)


    def selectIntrinsicFreqConfig(self):
        if self.intrinsicfreq_constant_radio.isChecked():
            self.intrinsicfreq_type = "Constant"
            self.open_const_freq_settings()
            #print(self.intrinsicfreq_type)
        if self.intrinsicfreq_random_radio.isChecked():
            self.intrinsicfreq_type = "Random"
            self.open_rand_freq_settings()
            #print(self.intrinsicfreq_type)

    def open_const_freq_settings(self):
        const_freq_dialog = QtWidgets.QDialog()
        ui = Ui_const_freq_dialog()
        ui.setupUi(const_freq_dialog, self.constfreq, "Constant frequency")
        const_freq_dialog.exec_()
        #ui.const_freq_value.setText(str(self.constfreq))
        
        # preventing empty form
        if ui.const_freq_value.text() == "":
            ui.const_freq_value.setText(str(np.round(self.constfreq,2)))
        else:
            self.constfreq = float(ui.const_freq_value.text())

    def open_const_phase_settings(self):
        initial_phase_dialog = QtWidgets.QDialog()
        ui = Ui_const_freq_dialog()
        ui.setupUi(initial_phase_dialog, self.constphase, "Constant phase")
        initial_phase_dialog.exec_()
        #ui.const_freq_value.setText(str(self.constphase))
        # preventing empty form
        if ui.const_freq_value.text() == "":
            ui.const_freq_value.setText(str(np.round(self.constphase,2))) 
        else:
            self.constphase = float(ui.const_freq_value.text())


    def open_rand_freq_settings(self):
        random_freq_dialog = QtWidgets.QDialog()
        ui = Ui_random_freq_dialog()
        ui.setupUi(random_freq_dialog, [self.meanfreq, self.sdfreq])
        random_freq_dialog.exec_()
        if ui.mean_value.text() == "":
            ui.mean_value.setText(str(np.round(self.meanfreq))) 
        else:
            self.meanfreq = float(ui.mean_value.text())

        if ui.sd_value.text() == "":
            ui.sd_value.setText(str(np.round(self.sdfreq))) 
        else:
            self.sdfreq = float(ui.sd_value.text())

    def open_rand_phase_settings(self):
        random_phase_dialog = QtWidgets.QDialog()
        ui = Ui_random_freq_dialog()
        ui.setupUi(random_phase_dialog, [self.meanphase, self.sdphase])
        random_phase_dialog.exec_()
        if ui.mean_value.text() == "":
            ui.mean_value.setText(str(self.meanphase)) 
        else:
            self.meanphase = float(ui.mean_value.text())

        if ui.sd_value.text() == "":
            ui.sd_value.setText(str(self.sdphase)) 
        else:
            self.sdphase = float(ui.sd_value.text())


    def generate_Kmatrix(self):
        try:
            '''
            Load cell-to-cell contact file from reconstructed islet
            '''
            global_contacts = np.loadtxt(self.current_islet_file[:-4]+"_all_contacts.txt")
            # numero de celulas en islote
            ncells = len(global_contacts)
        except: 
            self.sim_status_label.setText("Error loading cell-to-cell contacts")

        try:

            # genero matriz en blanco para guardar Kij
            Kmat = np.zeros([ncells, ncells])
            n_vecinos_vec = np.zeros(ncells)
            for i in np.arange(ncells):
                n_vecinos_cell_i = 0
                cell1 = global_contacts[i,i]
                for j in np.arange(ncells):
                    cell2 = global_contacts[j,j]
                    # Para considerar interacciones de la celula con ella misma:
                    #if global_contacts[i,j] != 0.0:

                   
                    # Para considerar solo interacciones con vecinas.
                    if global_contacts[i,j] == 1.0:
                        n_vecinos_cell_i = n_vecinos_cell_i + 1
                        #print(global_contacts[i,j])
                        if cell1 == 12. and cell2 == 12.:
                            Kmat[i,j] = self.Kbb
                        elif cell1 == 12. and cell2 == 11.:
                            Kmat[i,j] = self.Kba
                        elif cell1 == 11. and cell2 == 11.:
                            Kmat[i,j] = self.Kaa
                        elif cell1 == 11. and cell2 == 12.:
                            Kmat[i,j] = self.Kab
                        elif cell1 == 13. and cell2 == 13.:
                            Kmat[i,j] = self.Kdd
                        elif cell1 == 13. and cell2 == 12.:
                            Kmat[i,j] = self.Kdb
                        elif cell1 == 12. and cell2 == 13.:
                            Kmat[i,j] = self.Kbd
                        elif cell1 == 13. and cell2 == 11.:
                            Kmat[i,j] = self.Kda
                        elif cell1 == 11. and cell2 == 13.:
                            Kmat[i,j] = self.Kad
                    else:
                        continue
                    n_vecinos_vec[i] = n_vecinos_cell_i
        except:
            self.sim_status_label.setText("Error generating K matrix")
        np.savetxt(self.current_islet_file[:-4] + '_Kmat.txt', Kmat, delimiter = ' ', fmt='%1.3f')
        #return global_contacts, Kmat, n_vecinos_vec
        return ncells




    def generate_cuda_code(self, ncells):
        # extract simulation parameters
        if self.total_time_lineedit.text() == "":
            self.total_time_lineedit.setText(str(self.totaltimesim))
        else: 
            self.totaltimesim = float(self.total_time_lineedit.text())

        if self.timestep_lineedit.text()== "":
            self.timestep_lineedit.setText(str(self.dtsim))
        else:
            self.dtsim = float(self.timestep_lineedit.text())

        if self.save_mult_lineedit.text()=="":
            self.save_mult_lineedit.setText(str(self.saveMultiple))
        else:
            self.saveMultiple = int(self.save_mult_lineedit.text())

        if self.nblocks_lineedit.text()=="":
            self.nblocks_lineedit.setText(str(self.nblocks))
        else:
            self.nblocks = int(self.nblocks_lineedit.text())
        if self.ncudathreads_lineedit.text()=="":
            self.ncudathreads_lineedit.setText(str(self.ncudathreads))
        else:
            self.ncudathreads = int(self.ncudathreads_lineedit.text())

        try:
            # base cuda code
            fsource = open('kuramoto_islets.cu')
            # output cuda file
            fout = self.current_islet_file[:-4] + "_kuramoto_sim.cu"
            # open output file
            fsalida = open(fout, "w")
            # read source cuda file
            lines = fsource.readlines()
            lines[20] = "#define totalCelulas " + str(ncells) +"\n"
            #lines[25] = "#define saveMultiple " + str(self.saveMultiple) +"\n"
            lines[29] = "const int numBlocks = " + str(self.nblocks) + ";\n"
            lines[30] = "const int threadsPerBlock = " + str(self.ncudathreads) + ";\n"
            lines[139] = 'fp = fopen("' + self.current_islet_file[:-4] + '_all_contacts.txt" ,"r");\n' 

            if self.initialphase_constant_radio.isChecked():
                lines[231] = "theta ="  +str(self.constphase)+";\n"

            if self.initialphase_random_radio.isChecked():
                lines[231] = "theta = 2 * PI * get_random();\n"


            if self.intrinsicfreq_constant_radio.isChecked():
                lines[235] ="         frec = " +str(self.constfreq) + ";\n"
            
            if self.intrinsicfreq_random_radio.isChecked():
                lines[235] = "        frec = rand_normal("+str(self.meanfreq)+","+ str(self.sdfreq) +");\n"


            lines[247] = 'fp = fopen("' + self.current_islet_file[:-4] + '_Kmat.txt", "r");\n'
            lines[326] = 'double Tf = ' + str(self.totaltimesim) +";\n"
            lines[329] = 'double dt = ' + str(self.dtsim)+";\n"
            lines[333] = 'FILE *salidaAngulosIslote = fopen("'+self.current_islet_file[:-4] +'_kuramoto_angles.data", "w");\n'
            lines[362] = "if (indice % "+ str(self.saveMultiple)+ " == 0){\n"
            #escribo archivo de salida
            for line in lines:
                fsalida.write(line)
                
            fsalida.close()
            fsource.close()
        except:
            self.sim_status_label.setText("Error generating cuda code")

    def compile_cuda_code(self):
        try:
            subprocess.run(["nvcc", self.current_islet_file[:-4] + "_kuramoto_sim.cu" , "-o", self.current_islet_file[:-4] + "_kuramoto_sim"])
            #print("compilation success")
        except:
            #print("CUDA compilation failed")
            self.sim_status_label.setText("Error compiling cuda code")


    def launch_cudasim_window(self, fout):
        Dialog1 = QtWidgets.QDialog()
        ui1 = Ui_OptLog_Dialog()
        ui1.setupUi(Dialog1, fout, "Simulation log")
        Dialog1.exec_()
        Dialog1.reject()
        return ui1.optstatus, ui1.computing_time_processed

    def run_kuramoto_simulation(self):
        # Generate K matrix
        ncells = self.generate_Kmatrix()
        #print("K matrix generada")

        self.sim_status_label.setText("Generating CUDA code")
        self.sim_status_label.setStyleSheet("color: Green")
        self.generate_cuda_code(ncells)
        #print("Cuda code generado")

        self.sim_status_label.setText("Compiling CUDA code")
        self.sim_status_label.setStyleSheet("color: Green")
        self.compile_cuda_code()
        #print("Cuda code compilado")

        #print(self.current_islet_file[:-4]+"_kuramoto_sim")
        try:
            self.sim_status_label.setText("Simulating...")
            self.sim_status_label.setStyleSheet("color: Green")
            self.launch_cudasim_window(self.current_islet_file[:-4] + "_kuramoto_sim..")
            self.sim_status_label.setText("Simulation completed")
        except:
            self.sim_status_label.setText("Error executing cuda simulation")
            self.sim_status_label.setStyleSheet("color:Red")
    
        
        self.plot_kuramoto_results()
        
        

    def phase_coherence(self, angles_vec):
        '''
        Compute global order parameter R_t - mean length of resultant vector
        '''
        suma = sum([(np.e ** (1j * 2*i)) for i in angles_vec])
        return abs(suma / len(angles_vec))

    # def ave_phase_coherence(self, data, muestras):
    #     rt = np.zeros(muestras)
    #     i = 0
    #     for j in np.arange(len(data)-muestras,len(data)):
    #         rt[i] = phase_coherence(data[j,1:])
    #         i = i + 1
    #     return np.mean(rt)


    def plot_kuramoto_results(self):
        data = np.loadtxt(self.current_islet_file[:-4] +"_kuramoto_angles.data")
        #print(np.shape(data))
        layout = QtWidgets.QVBoxLayout()
        self.kuramoto_results_tab = QtWidgets.QWidget()
        self.kuramoto_results_tab.setObjectName("kuramoto_results_tab")
        self.kuramoto_results_tab.setLayout(layout)

        figure, (ax1, ax2) = plt.subplots(2)
        #figure = plt.figure()
        #figure.subplots_adjust(left=0.1, right=0.99, bottom=0.05, top=1.0, wspace=0.2, hspace=0.2)
        new_canvas = FigureCanvas(figure)
        new_canvas.setFocusPolicy(QtCore.Qt.StrongFocus)
        new_canvas.setFocus()
        
        #np.linspace(0, model.T, int(model.T/model.dt)),
        ax2.plot(data[:,0],[self.phase_coherence(vec)
            for vec in data[:,self.ind_alfas]], 'o')
        ax2.get_yaxis().get_major_formatter().set_useOffset(False)
        ax2.get_yaxis().set_major_formatter(FormatStrFormatter('%.2f'))
        ax2.set_xlabel("Time (s)")
        ax2.set_ylabel("Sync index")

        #phase_coherence_alphas = self.phase_coherence(data[:, self.ind_alfas+1].T)
        #phase_coherence_betas = self.phase_coherence(data[:, self.ind_betas+1].T)
        #phase_coherence_deltas = self.phase_coherence(data[:, self.ind_deltas+1].T)
        #phase_coherence_islet = self.phase_coherence(data[:, 1:].T)
        #plt.plot(theta_data[:,0],[phase_coherence(vec) for vec in theta_data[:,1:]],'o')


        sum_osc_alphas = np.sum(np.sin(data[:, self.ind_alfas+1]), 1)
        sum_osc_betas = np.sum(np.sin(data[:, self.ind_betas+1]), 1)
        sum_osc_deltas = np.sum(np.sin(data[:,self.ind_deltas+1]), 1)
        sum_osc_islote = np.sum(np.sin(data[:, 1:]), 1)

        
        #fig.suptitle('Vertically stacked subplots')
        ax1.plot(data[:,0],sum_osc_islote, color="Black", label = "Islet")
        ax1.plot(data[:,0],sum_osc_alphas, color="Red", label = r'$\alpha$'+'-cells')
        ax1.plot(data[:,0],sum_osc_betas, color="Green", label = r'$\beta$'+'-cells')
        ax1.plot(data[:,0],sum_osc_deltas, color="Blue", label = r'$\delta$'+'-cells')
        ax1.set_xlabel("Time (s)")
        ax1.set_ylabel("Sin("+r'$\theta$'+")")
        ax1.legend(frameon=False, loc='lower center', ncol=4, bbox_to_anchor=(0.5, 1.01))
        #ax2.plot(phase_coherence_islet, color="Black")
        #ax2.plot(phase_coherence_alphas, color="Red")
        #ax2.plot(phase_coherence_betas, color="Green")
        #ax2.plot(phase_coherence_deltas, color="Blue")
        #ax.mouse_init()

        new_toolbar = NavigationToolbar(new_canvas, self.kuramoto_results_tab)
        unwanted_buttons = ["Subplots"]
        for x in new_toolbar.actions():
            if x.text() in unwanted_buttons:
                new_toolbar.removeAction(x)

        layout.addWidget(new_canvas)
        layout.addWidget(new_toolbar)
        #self.tabWidget_stats.addTab(new_tab, "txt")
        self.tabWidget_Plots.addTab(self.kuramoto_results_tab, "Simulation")
        self.toolbar_handles.append(new_toolbar)
        self.canvases.append(new_canvas)
        self.figure_handles.append(figure)
        #self.tab_handles.append(self.contacts_plot_tab)    
        self.tab_handles.append(self.kuramoto_results_tab)
        self.tabWidget_Plots.setCurrentIndex(5)



class Ui_OptLog_Dialog(object):
    def setupUi(self, Dialog, fout, windowtitle):
        Dialog.setObjectName("Dialog")
        Dialog.resize(650, 400)
        Dialog.setMinimumSize(QtCore.QSize(650, 400))
        Dialog.setMaximumSize(QtCore.QSize(650, 400))
        Dialog.setWindowTitle(windowtitle)
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(10, 10, 630, 350))
        self.textEdit.setObjectName("textEdit")
        self.runopt_pushButton = QtWidgets.QPushButton(Dialog)
        self.runopt_pushButton.setGeometry(QtCore.QRect(180, 365, 131, 23))
        self.runopt_pushButton.setObjectName("runopt_pushButton")
        self.runopt_pushButton.clicked.connect(lambda: self.callProcess(fout))
        self.abortopt_pushbutton = QtWidgets.QPushButton(Dialog)
        self.abortopt_pushbutton.setGeometry(QtCore.QRect(340, 365, 131, 23))
        self.abortopt_pushbutton.setObjectName("abortopt_pushbutton")
        self.abortopt_pushbutton.clicked.connect(self.abort_opt)
        self.abortopt_pushbutton.clicked.connect(Dialog.reject)


        self.process = QtCore.QProcess(Dialog)
        self.process.readyRead.connect(self.dataReady)

        self.optstatus = 0
        self.status_item = ''

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        #Dialog.setWindowTitle(_translate("Dialog", "Optimization log"))
        self.runopt_pushButton.setText(_translate("Dialog", "Run"))
        self.abortopt_pushbutton.setText(_translate("Dialog", "Abort"))


    def abort_opt(self, Dialog):
        self.process.kill()
        self.optstatus = 0
        self.computing_time_processed = [0,0,0]
        #self.runopt_pushButton.setEnabled(True)
        #self.abortopt_pushbutton.setEnabled(False)
        #status = {self.process.NotRunning: "Not Running", self.process.Starting: "Starting", self.process.Running: "Running"}
        #self.status_item = str(status[self.process.stateChanged])
        #print(self.status_item)


    def callProcess(self, fout):
        self.opt_start_time = datetime.now()
        #print(self.opt_start_time)
        self.runopt_pushButton.setEnabled(False)
        self.process.start(fout[:-2])
        #print("Proceso iniciado")
        self.optstatus = 1
        self.abortopt_pushbutton.setEnabled(True)
        self.process.finished.connect(self.process_finished)


    def process_finished(self):
        if self.optstatus == 0:
            print("Proceso abortado")
            
        else: 
            self.opt_end_time = datetime.now()
            self.computing_time = self.opt_end_time - self.opt_start_time
                
            self.hours, self.remainder = divmod(self.computing_time.seconds, 3600)
            self.minutes, self.seconds = divmod(self.remainder, 60)
            self.computing_time_processed = [self.hours, self.minutes, self.seconds]
            #self.comp_time_value.setText(str(hours)+" h "+str(minutes)+" min "+str(seconds)+ " s")
            self.optstatus = 2
            #print("Proceso terminado")
            self.abortopt_pushbutton.setEnabled(False)
            self.runopt_pushButton.setEnabled(False)
            self.process = None
        


    def dataReady(self):
        cursor = self.textEdit.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(bytearray(self.process.readAllStandardOutput()).decode("ascii"))
        #cursor.insertText(str(self.process.readAllStandardOutput()))
        self.textEdit.ensureCursorVisible()


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


class Ui_const_freq_dialog(object):
    def setupUi(self, const_freq_dialog, constvalue, title):
        self.constfreq = constvalue

        # para validacion de entradas solo numeros
        reg_ex_numeros = QtCore.QRegExp("[+]?[0-9]*\.?[0-9]+")
        const_freq_dialog.setObjectName("const_freq_dialog")
        const_freq_dialog.resize(294, 94)
        const_freq_dialog.setMinimumSize(QtCore.QSize(294, 94))
        const_freq_dialog.setMaximumSize(QtCore.QSize(294, 94))
        self.const_freq_buttonBox = QtWidgets.QDialogButtonBox(const_freq_dialog)
        self.const_freq_buttonBox.setGeometry(QtCore.QRect(-150, 50, 341, 32))
        self.const_freq_buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.const_freq_buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        #self.const_freq_buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
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
        self.const_freq_value.setMaxLength(6)
        self.const_freq_value.setText(str(self.constfreq))
        freq_validator = QtGui.QRegExpValidator(reg_ex_numeros, self.const_freq_value)
        self.const_freq_value.setValidator(freq_validator)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.const_freq_value)
        #self.const_freq_value.setText(str(constvalue))
        self.retranslateUi(const_freq_dialog, title)
        self.const_freq_buttonBox.accepted.connect(const_freq_dialog.accept)
        self.const_freq_buttonBox.rejected.connect(const_freq_dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(const_freq_dialog)

    def retranslateUi(self, const_freq_dialog, title):
        _translate = QtCore.QCoreApplication.translate
        const_freq_dialog.setWindowTitle(_translate("const_freq_dialog", "Configure"))
        self.const_freq_label.setText(_translate("const_freq_dialog", title))


class Ui_random_freq_dialog(object):
    def setupUi(self, random_freq_dialog, randompars):

        self.mean = randompars[0]
        self.sd = randompars[1]

        # para validacion de entradas solo numeros
        reg_ex_numeros = QtCore.QRegExp("[+]?[0-9]*\.?[0-9]+")

        random_freq_dialog.setObjectName("random_freq_dialog")
        random_freq_dialog.resize(192, 120)
        self.buttonBox = QtWidgets.QDialogButtonBox(random_freq_dialog)
        self.buttonBox.setGeometry(QtCore.QRect(-190, 80, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        #self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
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
        self.mean_value.setText(str(self.mean))
        self.mean_value.setMaxLength(6)
        mean_validator = QtGui.QRegExpValidator(reg_ex_numeros, self.mean_value)
        self.mean_value.setValidator(mean_validator)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.mean_value)
        self.sd_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.sd_label.setObjectName("sd_label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.sd_label)
        self.sd_value = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.sd_value.setObjectName("sd_value")
        self.sd_value.setText(str(self.sd))
        self.sd_value.setMaxLength(6)
        sd_validator = QtGui.QRegExpValidator(reg_ex_numeros, self.sd_value)
        self.sd_value.setValidator(sd_validator)
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

class Ui_interaction_strength_Dialog(object):
    def setupUi(self, Dialog, int_strength_pars):
        self.Kaa = int_strength_pars[0]
        self.Kba = int_strength_pars[1]
        self.Kda = int_strength_pars[2]
        self.Kab = int_strength_pars[3]
        self.Kbb = int_strength_pars[4]
        self.Kdb = int_strength_pars[5]
        self.Kad = int_strength_pars[6]
        self.Kbd = int_strength_pars[7]
        self.Kdd = int_strength_pars[8]

        # para validacion de entradas solo numeros
        reg_ex_numeros = QtCore.QRegExp("[+]?[0-9]*\.?[0-9]+")

        Dialog.setObjectName("Dialog")
        Dialog.resize(232, 340)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(21, 300, 150, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        #self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox_int_strength_dialog")
        self.formLayoutWidget = QtWidgets.QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(30, 10, 161, 291))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout_int_strength")
        self.Kaa_value = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.Kaa_value.setAlignment(QtCore.Qt.AlignCenter)
        self.Kaa_value.setObjectName("Kaa_value")
        self.Kaa_value.setText(str(self.Kaa))
        Kaa_validator = QtGui.QRegExpValidator(reg_ex_numeros, self.Kaa_value)
        self.Kaa_value.setValidator(Kaa_validator)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.Kaa_value)
        self.Kba_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.Kba_label.setObjectName("Kba_label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.Kba_label)
        self.Kba_value = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.Kba_value.setAlignment(QtCore.Qt.AlignCenter)
        self.Kba_value.setObjectName("Kba_value")
        self.Kba_value.setText(str(self.Kba))
        Kba_validator = QtGui.QRegExpValidator(reg_ex_numeros, self.Kba_value)
        self.Kba_value.setValidator(Kba_validator)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.Kba_value)
        self.Kaa_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.Kaa_label.setObjectName("Kaa_label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.Kaa_label)
        self.Kda_value = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.Kda_value.setAlignment(QtCore.Qt.AlignCenter)
        self.Kda_value.setObjectName("Kda_value")
        self.Kda_value.setText(str(self.Kda))
        Kda_validator = QtGui.QRegExpValidator(reg_ex_numeros, self.Kda_value)
        self.Kda_value.setValidator(Kda_validator)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.Kda_value)
        self.Kda_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.Kda_label.setObjectName("Kda_label")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.Kda_label)
        self.Kab_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.Kab_label.setObjectName("Kab_label")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.Kab_label)
        self.Kbb_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.Kbb_label.setObjectName("Kbb_label")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.Kbb_label)
        self.Kdb_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.Kdb_label.setObjectName("Kdb_label")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.Kdb_label)
        self.Kad_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.Kad_label.setObjectName("Kad_label")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.Kad_label)
        self.Kbd_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.Kbd_label.setObjectName("Kbd_label")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.Kbd_label)
        self.Kdd_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.Kdd_label.setObjectName("Kdd_label")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.Kdd_label)
        self.Kab_value = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.Kab_value.setAlignment(QtCore.Qt.AlignCenter)
        self.Kab_value.setObjectName("Kab_value")
        self.Kab_value.setText(str(self.Kab))
        Kab_validator = QtGui.QRegExpValidator(reg_ex_numeros, self.Kab_value)
        self.Kab_value.setValidator(Kab_validator)
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.Kab_value)
        self.Kbb_value = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.Kbb_value.setAlignment(QtCore.Qt.AlignCenter)
        self.Kbb_value.setObjectName("Kbb_value")
        self.Kbb_value.setText(str(self.Kbb))
        Kbb_validator = QtGui.QRegExpValidator(reg_ex_numeros, self.Kbb_value)
        self.Kbb_value.setValidator(Kbb_validator)
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.Kbb_value)
        self.Kdb_value = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.Kdb_value.setAlignment(QtCore.Qt.AlignCenter)
        self.Kdb_value.setObjectName("Kdb_value")
        self.Kdb_value.setText(str(self.Kdb))
        Kdb_validator = QtGui.QRegExpValidator(reg_ex_numeros, self.Kdb_value)
        self.Kdb_value.setValidator(Kdb_validator)
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.Kdb_value)
        self.Kad_value = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.Kad_value.setAlignment(QtCore.Qt.AlignCenter)
        self.Kad_value.setObjectName("Kad_value")
        self.Kad_value.setText(str(self.Kad))
        Kad_validator = QtGui.QRegExpValidator(reg_ex_numeros, self.Kad_value)
        self.Kad_value.setValidator(Kad_validator)
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.Kad_value)
        self.Kbd_value = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.Kbd_value.setAlignment(QtCore.Qt.AlignCenter)
        self.Kbd_value.setObjectName("Kbd_value")
        self.Kbd_value.setText(str(self.Kbd))
        Kbd_validator = QtGui.QRegExpValidator(reg_ex_numeros, self.Kbd_value)
        self.Kbd_value.setValidator(Kbd_validator)
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.Kbd_value)
        self.Kdd_value = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.Kdd_value.setAlignment(QtCore.Qt.AlignCenter)
        self.Kdd_value.setObjectName("Kdd_value")
        self.Kdd_value.setText(str(self.Kdd))
        Kdd_validator = QtGui.QRegExpValidator(reg_ex_numeros, self.Kdd_value)
        self.Kdd_value.setValidator(Kdd_validator)
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.FieldRole, self.Kdd_value)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Interaction strength"))
        #self.Kaa_value.setText(_translate("Dialog", str(self.Kaa)))
        self.Kba_label.setText(_translate("Dialog", "Kba"))
        #self.Kba_value.setText(_translate("Dialog", str(self.Kba)))
        self.Kaa_label.setText(_translate("Dialog", "Kaa"))
        #self.Kda_value.setText(_translate("Dialog", str(self.Kda)))
        self.Kda_label.setText(_translate("Dialog", "Kda"))
        self.Kab_label.setText(_translate("Dialog", "Kab"))
        self.Kbb_label.setText(_translate("Dialog", "Kbb"))
        self.Kdb_label.setText(_translate("Dialog", "Kdb"))
        self.Kad_label.setText(_translate("Dialog", "Kad"))
        self.Kbd_label.setText(_translate("Dialog", "Kbd"))
        self.Kdd_label.setText(_translate("Dialog", "Kdd"))
        #self.Kab_value.setText(_translate("Dialog", str(self.Kab)))
        #self.Kbb_value.setText(_translate("Dialog", str(self.Kbb)))
        #self.Kdb_value.setText(_translate("Dialog", str(self.Kdb)))
        #self.Kad_value.setText(_translate("Dialog", str(self.Kad)))
        #self.Kbd_value.setText(_translate("Dialog", str(self.Kbd)))
        #self.Kdd_value.setText(_translate("Dialog", str(self.Kdd)))

    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

