# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'isletlabgui_v0.0.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTabWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel
from shape import Shape
from sphere import Sphere
from mpl_toolkits.mplot3d import Axes3D

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1019, 768)
        MainWindow.setFixedSize(1019,768)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(0, 0, 1021, 721))
        self.widget.setObjectName("widget")

        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        
        # Tabs de graficas de islotes, redes, etc.
        self.tabWidget_islets = QtWidgets.QTabWidget(self.widget)
        self.tabWidget_islets.setObjectName("tabWidget_islets")
        self.tabWidget_islets.setTabsClosable(True)
        self.tab_islote3d = QtWidgets.QWidget()
        self.tab_islote3d.setObjectName("Islet_Plot")
        self.tabWidget_islets.addTab(self.tab_islote3d, "Islet Plot")
        #self.tab_4 = QtWidgets.QWidget()
        #self.tab_4.setObjectName("tab_4")
        #self.tabWidget_islets.addTab(self.tab_4, "")
        self.gridLayout.addWidget(self.tabWidget_islets, 0, 1, 1, 1)
        

        self.tabWidget_stats = QtWidgets.QTabWidget(self.widget)
        self.tabWidget_stats.setObjectName("tabWidget_stats")
        # self.tab_5 = QtWidgets.QWidget()
        # self.tab_5.setObjectName("tab_5")
        # self.tabWidget_stats.addTab(self.tab_5, "")
        # self.tab_6 = QtWidgets.QWidget()
        # self.tab_6.setObjectName("tab_6")
        # self.tabWidget_stats.addTab(self.tab_6, "")
        self.gridLayout.addWidget(self.tabWidget_stats, 1, 1, 1, 1)
        
        self.tabWidget_settings = QtWidgets.QTabWidget(self.widget)
        self.tabWidget_settings.setObjectName("tabWidget_settings")
        #self.tab = QtWidgets.QWidget()
        #self.tab.setObjectName("tab")
        #self.tabWidget_settings.addTab(self.tab, "")
        #self.tab_2 = QtWidgets.QWidget()
        #self.tab_2.setObjectName("tab_2")
        #self.tabWidget_settings.addTab(self.tab_2, "")
        self.gridLayout.addWidget(self.tabWidget_settings, 0, 0, 1, 1)
        

        self.tabWidget_analysis = QtWidgets.QTabWidget(self.widget)
        self.tabWidget_analysis.setObjectName("tabWidget_analysis")
        self.tab_7 = QtWidgets.QWidget()
        self.tab_7.setObjectName("tab_7")
        self.tabWidget_analysis.addTab(self.tab_7, "")
        self.tab_8 = QtWidgets.QWidget()
        self.tab_8.setObjectName("tab_8")
        self.tabWidget_analysis.addTab(self.tab_8, "")
        self.gridLayout.addWidget(self.tabWidget_analysis, 1, 0, 1, 1)
        

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1019, 20))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuProcess = QtWidgets.QMenu(self.menubar)
        self.menuProcess.setObjectName("menuProcess")
        self.menuPreferences = QtWidgets.QMenu(self.menubar)
        self.menuPreferences.setObjectName("menuPreferences")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuProcess.menuAction())
        self.menubar.addAction(self.menuPreferences.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget_islets.setCurrentIndex(0)
        self.tabWidget_stats.setCurrentIndex(0)
        self.tabWidget_settings.setCurrentIndex(0)
        self.tabWidget_analysis.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Para agregar figuras en pestañas
        self.canvases = []
        self.figure_handles = []
        self.toolbar_handles = []
        self.tab_handles = []
        self.current_window = -1

        # arreglo numpy para guardar datos de islote
        self.exp_islet_data = np.array([])

        # string para guardar archivo actual de islote
        self.current_islet_file = ""
        self.islet_file_status = False

        






    def addPlot(self, title, figure):

        new_tab = QWidget()
        layout = QVBoxLayout()
        new_tab.setLayout(layout)

        figure.subplots_adjust(left=0.1, right=0.99, bottom=0.05, top=1.0, wspace=0.2, hspace=0.2)
        new_canvas = FigureCanvas(figure)
        new_toolbar = NavigationToolbar(new_canvas, new_tab)

        layout.addWidget(new_canvas)
        layout.addWidget(new_toolbar)
        
        self.tabWidget_islets.addTab(new_tab, title)
        self.toolbar_handles.append(new_toolbar)
        self.canvases.append(new_canvas)
        self.figure_handles.append(figure)
        self.tab_handles.append(new_tab)

    def plot_islet_button_clicked(self):
        #new_tab = QWidget()
        layout = QVBoxLayout()
        self.tab_islote3d.setLayout(layout)

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
            x_coord = cell[3]
            y_coord = cell[4]
            z_coord = cell[5]
            r_cell = cell[0]
            cell_type = cell[2]
            if cell_type == 12.:
                cell_color = "g"
            elif cell_type == 11.:
                cell_color = "r"
            elif cell_type == 13:
                cell_color = "b"
            else:
                cell_color = "k"
            s = Sphere(ax, x = x_coord, y = y_coord, z = z_coord, radius = r_cell, detail_level = 8, rstride = 5, cstride = 1, color = cell_color)
            #s.modify_x(2)
        ax.mouse_init()


        new_toolbar = NavigationToolbar(new_canvas, self.tab_islote3d)
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
        self.tab_handles.append(self.tab_islote3d)

    def reconstruction_tab(self, title):
        new_tab = QWidget()
        layout = QVBoxLayout()
        new_tab.setLayout(layout)

        # boton para abrir archivo de islote
        rec_exp_file_button = QtWidgets.QPushButton("Open islet data")
        rec_exp_file_button.clicked.connect(self.open_islet_file_button_clicked)
        layout.addWidget(rec_exp_file_button)
        
        # etiqueta que muestra estatus de archivo
        if self.exp_islet_data.size == 0:
            exp_file_status_label_text = "Islet file not loaded"
        else:
            exp_file_status_label_text = "Islet file loaded"
        exp_file_status_label = QtWidgets.QLabel()
        exp_file_status_label.setText(exp_file_status_label_text)
        layout.addWidget(exp_file_status_label)

        # Etiqueta para mostrar archivo cargado
        # boton para graficar islote
        plot_islet_button = QtWidgets.QPushButton("Plot islet")
        plot_islet_button.clicked.connect(self.plot_islet_button_clicked)
        layout.addWidget(plot_islet_button)

        self.tabWidget_settings.addTab(new_tab, title)




    def open_islet_file_button_clicked(self, s):
        #print("click", s)
        dlg = QFileDialog()
        filename = dlg.getOpenFileName()
        #dlg.setWindowTitle("Hello")
        if filename[0]:
            self.exp_islet_data = np.loadtxt(filename[0])
            self.current_islet_file = filename[0]
            print(self.exp_islet_data[:,0])
            print(self.current_islet_file)







    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        #self.tabWidget_islets.setTabText(self.tabWidget_islets.indexOf(self.tab_3), _translate("MainWindow", "Tab 1"))
        #self.tabWidget_islets.setTabText(self.tabWidget_islets.indexOf(self.tab_4), _translate("MainWindow", "Tab 2"))
        # self.tabWidget_stats.setTabText(self.tabWidget_stats.indexOf(self.tab_5), _translate("MainWindow", "Tab 1"))
        # self.tabWidget_stats.setTabText(self.tabWidget_stats.indexOf(self.tab_6), _translate("MainWindow", "Tab 2"))
        #self.tabWidget_settings.setTabText(self.tabWidget_settings.indexOf(self.tab), _translate("MainWindow", "Reconstruction"))
        #self.tabWidget_settings.setTabText(self.tabWidget_settings.indexOf(self.tab_2), _translate("MainWindow", "Contacts"))
        self.tabWidget_analysis.setTabText(self.tabWidget_analysis.indexOf(self.tab_7), _translate("MainWindow", "Tab 7"))
        self.tabWidget_analysis.setTabText(self.tabWidget_analysis.indexOf(self.tab_8), _translate("MainWindow", "Tab 8"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuProcess.setTitle(_translate("MainWindow", "Process"))
        self.menuPreferences.setTitle(_translate("MainWindow", "Preferences"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    
    x = np.arange(0, 10, 0.001)
    f = plt.figure()
    ysin = np.sin(x)
    plt.plot(x, ysin, '--')
    ui.addPlot("sin 1", f)

    f = plt.figure()
    ycos = np.cos(x)
    plt.plot(x, ycos, '--')
    ui.addPlot("cos 1", f)


    # x = np.arange(0, 10, 0.001)
    # f = plt.figure()
    # ysin = np.sin(x)
    # plt.plot(x, ysin, '--')
    # ui.addPlot2("sin 2", f)

    # f = plt.figure()
    # ycos = np.cos(x)
    # plt.plot(x, ycos, '--')
    # ui.addPlot2("cos 2", f)

    #ui.addPlot3DIslet("Sphere")
    ui.reconstruction_tab("Reconstruction")


    MainWindow.show()



    sys.exit(app.exec_())

