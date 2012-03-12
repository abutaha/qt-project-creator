#-*- coding: utf-8 -*-
#
# Copyright (C) 2010, %(FULLNAME)s <%(EMAIL)s>
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 3 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.


import os
import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import %(PACKAGE_NAME)s
from %(PACKAGE_NAME)s import config
from %(PACKAGE_NAME)s.modules import about
from %(PACKAGE_NAME)s.gui.MainWindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):

        QMainWindow.__init__(self, parent)
        self.setupUi(self)

        # Set Window Title
        self.setWindowTitle(self.tr("%(PROJECT_NAME)s"))

        # Set main central widget
        #self.setCentralWidget(<module_name>(self))
        
        # Setup Variables
        self.register_vars()
        
        # Create menus
        self.create_actions()
        self.create_menus()
        
        # Create Tool Bar
        self.create_toolbar()

        # Create Status bar
        self.create_statusbar()

        # Connect signals/slots
        self.connect_signals()

    def closeEvent(self, event):
        ''' This method is called when user tries to close the software '''

        msg_title = "Are you sure you want to exit?"
        body_msg = "You have unsaved data, are you sure you want to exit?"

        reply = QMessageBox.question(self, self.tr(msg_title), \
                   self.tr(body_msg), \
                   QMessageBox.Yes, \
                   QMessageBox.No, \
                   QMessageBox.Cancel)

        if reply == QMessageBox.Yes:
            event.accept()
            qApp.quit()

        elif reply == QMessageBox.No:
            event.ignore()
            return

        else:
            event.ignore()
            return

    def register_vars(self):
        ''' Declare all constants/variables needed by your methods '''

        self.icons = config.ICONS_DIR

    def create_actions(self):
        ''' Create actions which will be attached to the menu and toolbar '''

        # 'File' Menu, Save Action
        save_icon = os.path.join(self.icons, 'save.png')
        self.saveAction = QAction(QIcon(save_icon), self.tr("&Save"), self)
        self.saveAction.setShortcut(self.tr("Ctrl+S"))
        self.saveAction.setStatusTip(self.tr("Save current settings"))
        self.connect(self.saveAction, SIGNAL("triggered()"), self.do_save)
        
        # 'File' Menu, Exit action
        exit_icon = os.path.join(self.icons, 'exit.png')
        self.exitAction = QAction(QIcon(exit_icon), self.tr("E&xit"), self)
        self.exitAction.setShortcut(self.tr("Ctrl+Q"))
        self.exitAction.setStatusTip(self.tr("Exit"))
        self.connect(self.exitAction, SIGNAL("triggered()"), self, SLOT("close()"))
        
        # 'Help' Menu, About action
        about_icon = os.path.join(self.icons, 'about.png')
        self.aboutAction = QAction(QIcon(about_icon), self.tr("&About"), self)
        self.aboutAction.setShortcut(self.tr("Ctrl+A"))
        self.aboutAction.setStatusTip(self.tr("About"))
        self.connect(self.aboutAction, SIGNAL("triggered()"), self.show_about)

    def create_menus(self):
        ''' Show menu in the top of the window '''
        
        # Create a menu called 'File'
        self.fileMenu = self.menuBar().addMenu(self.tr("&File"))
        
        # Add save button to it
        self.fileMenu.addAction(self.saveAction)
        
        # Add a separator
        self.fileMenu.addSeparator()
        
        # Add exit button to it
        self.fileMenu.addAction(self.exitAction)
        
        # Create a menu called 'Help'
        self.helpMenu = self.menuBar().addMenu(self.tr("&Help"))
        
        # Add about button to it
        self.helpMenu.addAction(self.aboutAction)


    def create_toolbar(self):
        ''' Create a tool bar and attach actions to it '''
        
        self.toolBar.addAction(self.saveAction)
        self.toolBar.addAction(self.exitAction)
        self.toolBar.addSeparator()

    def create_statusbar(self):
        ''' Create a status bar in the buttom of the window '''
        
        self.statusBar().showMessage(self.tr('Ready'), 5000)

    def connect_signals(self):
        ''' Connect signals with slots (methods) '''
        pass

    def do_save(self):
        ''' Save changes '''
       
        self.statusBar().showMessage(self.tr('Saved!'), 5000)
    
    def show_about(self):
        about_window = about.AboutDialog(self)
        about_window.show()
