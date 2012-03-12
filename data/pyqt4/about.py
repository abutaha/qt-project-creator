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

import %(PACKAGE_NAME)s
from %(PACKAGE_NAME)s import config
from %(PACKAGE_NAME)s.gui.about import Ui_Dialog

class AboutDialog(QDialog, Ui_Dialog):
    
    def __init__(self, parent=None):
        
        QDialog.__init__(self, parent)
        self.setupUi(self)

        # Setup window title
        self.setWindowTitle(self.tr("About %(PROJECT_NAME)s"))

        # Connect 'close' button to built-in close() method
        self.connect(self.cancel, SIGNAL("clicked()"), self.close)

        # Setup labels
        self.text_label.setText("<b>%(PROJECT_NAME)s</b><br />%(SHORT_DESC)s<br />")
 
