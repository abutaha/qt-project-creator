#-*- coding: utf-8 -*-
#
# Copyright (C) 2010, Muslim Adel Abu Taha <qtprojectcreator@qtprojectcreator>
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 3 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

# $Id: manage.py 32 2010-10-07 06:50:40Z muslim $
# $Rev: 32 $
# $LastChangedDate: 2010-10-07 09:50:40 +0300 (Thu, 07 Oct 2010) $
# $LastChangedBy: muslim $


import os
import sys
from qtprojectcreator import manager


if __name__ == '__main__':
    msg = "Usage: %s [run, clean]" % os.path.basename(sys.argv[0])
    allowed_options = ('run', 'clean', 'addmodule')
    m = manager.Controller()
    try:
        arg = sys.argv[1]
        if arg == 'run':
            m.run()
        elif arg == 'clean':
            m.clean()
        elif arg == 'addmodule':
            m.add_module()
        else:
            print 'Option not support.'
            print msg
    except:
        print msg
    
 
