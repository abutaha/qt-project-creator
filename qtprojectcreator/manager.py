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
#
# $Id: manager.py 32 2010-10-07 06:50:40Z muslim $
# $Rev: 32 $
# $LastChangedDate: 2010-10-07 09:50:40 +0300 (Thu, 07 Oct 2010) $
# $LastChangedBy: muslim $


import os
import sys
from ConfigParser import RawConfigParser as ConfigParser

from qtprojectcreator import _config

class Controller:

    def __init__(self):
        
        os.environ['PYTHONPATH'] = "."
        self.config_file = "qt_project_config.ini"

        if not os.path.exists(self.config_file):
            print "ERROR: You're not in the top-level directory of the project."
            sys.exit(1)

        self.config = ConfigParser()
        self.config.read(self.config_file)

        self.project_dir = self.config.get('project', 'proj_dir')
        self.binaries_dir = self.config.get('project', 'bin_dir')
        self.binaries_name = self.config.get('project', 'bin_name')
        self.modules_dir = self.config.get('project', 'modules_dir')
        self.gui_dir = self.config.get('project', 'gui_dir')
        self.ui_dir = self.config.get('project', 'ui_dir')

        self.package_name = self.config.get('information', 'package_name')

        self.data_to_change = {
            "FULLNAME": self.config.get('information', 'full_name'),
            "EMAIL": self.config.get('information', 'email'),
            "WEBSITE": self.config.get('information', 'website'),
            "PROJECT_NAME": self.config.get('information', 'project_name'),
            "LICENSE": self.config.get('information', 'license'),
            "SHORT_DESC": self.config.get('information', 'short_description'),
            "LONG_DESC": self.config.get('information', 'long_description'),
            "PACKAGE_NAME": self.config.get('information', 'package_name'),
            "MODULES_DIR": self.config.get('project', 'modules_dir'),
            "PROJ_DIR": self.config.get('project', 'proj_dir'),
            "DATA_DIR": self.config.get('project', 'data_dir'),
            "GUI_DIR": self.config.get('project', 'gui_dir'),
            "READY_DIR": self.config.get('project', 'ready_dir'),
            "ICONS_DIR": self.config.get('project', 'icons_dir'),
            "BIN_DIR": self.config.get('project', 'bin_dir'),
            "UI_DIR": self.config.get('project', 'ui_dir'),
            "DOCS_DIR": self.config.get('project', 'docs_dir'),
            "OS": self.config.get('project', 'os'),
        }


    def do_cleanup(self):

        for root, dirs, files in os.walk(self.project_dir):
            for f in files:
                fname = os.path.join(root, f)
                if fname.endswith('.pyc'):
                    print '-*- ', fname
                    os.unlink(fname)

        gui_files = os.listdir(self.gui_dir)

        for gui in gui_files:
            gname = os.path.join(self.gui_dir, gui)
            print '-*- ', gname
            os.unlink(gname)

    def do_compile(self):

        ui_files = os.listdir(self.ui_dir)

        for ui in ui_files:
            ui_file = os.path.join(self.ui_dir, ui)
            py_file = os.path.join(self.gui_dir, ui.split('.')[0] + '.py')
            
            cmd = "%s %s -o %s" %(_config.PYUIC4, ui_file, py_file)
            print "-*- %s --> %s" %(ui_file, py_file)
            os.system(cmd)

    def create_gui_init(self):
        
        gui_files = os.listdir(self.gui_dir)
        files = []
        
        for f in gui_files:
            files.append(f.split('.')[0])
            files.sort()
            
        fhandler = open(os.path.join(self.gui_dir, '__init__.py'), 'w')
        
        for f in files:
            fhandler.write('import %s\n' % f)
        
        fhandler.write('\n')
        
        # Write __all__
        fhandler.write('__all__ = [ ')
        
        total = len(files)
        for x in range(0, total):
            if not x == (total - 1):
                fhandler.write("'%s', " % files[x])
            else:
                fhandler.write("'%s' " % files[x])
        
        fhandler.write(']')
        fhandler.write('\n')
        fhandler.close()

    def add_module(self, name=None, args=None):
        
        if not args:
            print "Please choose the type of the new module:"
            print "\t[1] QDialog"
            print "\t[2] QWidget"
            print "\t[3] Cancel"
            ret = raw_input("Select an option [1, 2, 3]: ")

        if ret == "1":
            if not name:
                name = raw_input("Enter a name for this module: ")
            tmpl_ui_file = os.path.join(_config.UI_DIR, 'Dialog.ui')
            new_ui_file = os.path.join(self.ui_dir, name + '.ui')
            fhandler = open(new_ui_file, 'w')
            fhandler.write(file(tmpl_ui_file).read())
            fhandler.close()
            
            tmpl_py_file = file(os.path.join(_config.PYQT4_DIR, \
                                             'qdialog.py')).read()
            
            new_py_file = os.path.join(self.modules_dir, name + '.py')
            handler = open(new_py_file, 'w')
            
            self.data_to_change['MODULE_NAME'] = name
            handler.write(tmpl_py_file % self.data_to_change)
            
        elif ret == "2":
            if not name:
                name = raw_input("Enter a name for this module: ")
            tmpl_ui_file = os.path.join(_config.UI_DIR, 'Widget.ui')
            new_ui_file = os.path.join(self.ui_dir, name + '.ui')
            fhandler = open(new_ui_file, 'w')
            fhandler.write(file(tmpl_ui_file).read())
            fhandler.close()
            
            tmpl_py_file = file(os.path.join(_config.PYQT4_DIR, \
                                             'qwidget.py')).read()
            
            new_py_file = os.path.join(self.modules_dir, name + '.py')
            handler = open(new_py_file, 'w')
            
            self.data_to_change['MODULE_NAME'] = name
            handler.write(tmpl_py_file % self.data_to_change)

        elif ret == "3":
            sys.exit(0)
        else:
            sys.exit(1)


    def run(self):
        
        print "Step 1: Removing *.pyc and .~ files..."
        self.do_cleanup()
        
        print
        print "Step 2: Compiling designer UI files, please wait...."
        self.do_compile()
        
        print
        print "Step 3: Creating '__init__.py' files again..."
        self.create_gui_init()
        print '-*- Done.'
        
        print
        print "Step 4: Running..."
        cmd = os.path.join(self.binaries_dir, self.binaries_name)
        os.system('python %s' % cmd)
 
