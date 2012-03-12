#!/usr/bin/env python
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

 
import sys
import locale

from PyQt4 import QtCore
from PyQt4 import QtGui

import %(PACKAGE_NAME)s
from %(PACKAGE_NAME)s.controller import MainWindow


def main():
    
    # Qt main application instance
    application = QtGui.QApplication(sys.argv)

    # Set everything to UTF-8
    QtCore.QTextCodec.setCodecForCStrings(
                         QtCore.QTextCodec.codecForName("UTF-8"))
    
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(application.exec_())
    

if __name__ == "__main__":
    main()
 
