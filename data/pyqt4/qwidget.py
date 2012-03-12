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


from PyQt4.QtCore import *
from PyQt4.QtGui import *

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import %(PACKAGE_NAME)s
from %(PACKAGE_NAME)s import config
from %(PACKAGE_NAME)s.gui.%(MODULE_NAME)s import Ui_Form

class AboutDialog(QWidget, Ui_Form):
    
    def __init__(self, parent=None):
        
        QWidget.__init__(self, parent)
        self.setupUi(self)
 
