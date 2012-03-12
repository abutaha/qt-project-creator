#!/usr/bin/python
# -*- coding: utf-8 -*-


import os
import sys
import shutil
import platform
from distutils.spawn import find_executable, spawn
from distutils.sysconfig import get_python_lib


class Installer:
    def __init__(self):
        self.os = platform.system()
        self.check_permission()
        self.cwd = os.getcwd()
        if self.os == 'Windows': self.cwd = os.getcwd().replace('\\', '/')
        self.needed_execs = ('pyuic4', 'pylupdate4', 'lrelease-qt4')
        self.vars = {
            'Linux': {
                'data': '/usr/share/qt-project-creator',
                'bin': '/usr/bin',
                'docs': '/usr/share/doc/qt-project-creator',
                'package': os.path.join(get_python_lib(), 'qtprojectcreator'),
                'lib': get_python_lib(),
                'exec': '/usr/bin/qt-project-creator.py'
            },
            'Windows': {
                'data': 'C:/Program Files/qt-project-creator/data',
                'docs': 'C:/Program Files/qt-project-creator/docs',
                'bin': 'C:/Program Files/qt-project-creator/bin',
                'exec': 'C:/Program Files/qt-project-creator/bin/qt-project-creator.py',
                'package': os.path.join(get_python_lib(), 'qtprojectcreator').replace('\\', '/'),
                'lib': get_python_lib().replace('\\', '/'),
            }
        }
        self.all_paths = (self.vars[self.os]['data'], self.vars[self.os]['docs'], \
                    self.vars[self.os]['package'], self.vars[self.os]['exec']
        )


    def check_permission(self):
        if self.os == 'Linux':
            if not os.getenv('USER') == 'root':
                print "ERROR: You should be root to run this tool"
                sys.exit(0)
        return True


    def check_depends(self):
        if self.os == 'Linux':
            for exe in self.needed_execs:
                if not find_executable(exe):
                    print "ERROR: %s not found, are you sure it's installed?" % exe
                    print "If you're running Kubuntu/Ubuntu try: apt-get install pyqt4-dev-tools"
                    print "Exit...."
                    sys.exit(1)
        
        elif self.os == 'Windows':
            """ For some reason, find_executable() isn't working in Windows XP.
            This is a work-around until I find a solution or discover what is
            happening"""

            py_paths = (os.path.join(get_python_lib(), 'PyQt4', 'bin').replace('\\', '/'),
                        os.path.join(get_python_lib(), 'PyQt4', 'uic').replace('\\', '/')
            )
            
            if not os.path.exists(os.path.join(py_paths[0], 'pylupdate4.exe')):
                print "ERROR: <pylupdate4.exe> not found, are you sure you've installed PyQt4?"
                print "You can download it from: http://www.riverbankcomputing.co.uk/software/pyqt/download"
                print "Exit...."
                sys.exit(1)
            
            if not os.path.exists(os.path.join(py_paths[0], 'lrelease.exe')):
                print "ERROR: <lrelease.exe> not found, are you sure you've installed PyQt4?"
                print "You can download it from: http://www.riverbankcomputing.co.uk/software/pyqt/download"
                print "Exit...."
                sys.exit(1)
            
            if not os.path.exists(os.path.join(py_paths[1], 'pyuic.py')):
                print "ERROR: <pyuic.py> not found, are you sure you've installed PyQt4?"
                print "You can download it from: http://www.riverbankcomputing.co.uk/software/pyqt/download"
                print "Exit...."
                sys.exit(1)
            
            self.windows_execs = (os.path.join(py_paths[0], 'pylupdate4.exe'),
                                  os.path.join(py_paths[0], 'lrelease.exe'),
                                  os.path.join(py_paths[1], 'pyuic.py')
            )


    def do_uninstall(self):
        if self.os == 'Windows':
            project_dir = os.path.dirname(self.vars['Windows']['data']).replace('/', '\\')
            package_dir = self.vars['Windows']['package'].replace('/', '\\')
            for p in (project_dir, package_dir):
                cmd = 'rmdir /s /q "%s"' % p
                os.system(cmd)

        elif self.os == 'Linux':
            for p in self.all_paths:
                if os.path.isdir(p):
                    shutil.rmtree(p)
                elif os.path.isfile(p):
                    os.unlink(p)
            
        print "Uninstallation finished"


    def check_paths(self):
        for p in self.all_paths:
            if os.path.exists(p):
                print "ERROR: Directory <%s> already exist.." % p
                print "ERROR: Installation failed!"
                print "Try to run: <python setup.py unistall> first"
                sys.exit(1)


    def do_install(self):
        
        data = os.path.join(self.cwd, 'data').replace('\\', '/')
        print "Copying %s ---> %s" % (data, self.vars[self.os]['data'])
        shutil.copytree(data, self.vars[self.os]['data'])
        
        docs = os.path.join(self.cwd, 'docs').replace('\\', '/')
        print "Copying %s ---> %s" % (docs, self.vars[self.os]['docs'])
        shutil.copytree(docs, self.vars[self.os]['docs'])
        
        package = os.path.join(self.cwd, 'qtprojectcreator').replace('\\', '/')
        print "Copying %s ---> %s" % (package, self.vars[self.os]['package'])
        shutil.copytree(package, self.vars[self.os]['package'])
        
        binary = os.path.join(self.cwd, 'bin', 'qt-project-creator.py').replace('\\', '/')
        if self.os == 'Windows':
            os.mkdir(self.vars[self.os]['bin'])
            print "Copying %s ---> %s" % (binary, self.vars[self.os]['exec'])
            shutil.copy(binary, self.vars[self.os]['exec'])
        else:
            print "Copying %s ---> %s" % (binary, self.vars[self.os]['bin'])
            shutil.copy(binary, self.vars[self.os]['bin'])
        
        print "Installation finished successfully!"


    def build_config(self):
        if self.os == 'Linux':
            cfg = os.path.join(self.vars['Linux']['package'], '_config.py')
            fhandler = open(cfg, 'w')
            fhandler.write("""#-*- coding: utf-8 -*- \n\n
import os

DATA_DIR = "%s"
BIN_DIR = "%s"

ICONS_DIR = os.path.join(DATA_DIR, 'icons')
UI_DIR = os.path.join(DATA_DIR, 'ui')
PYQT4_DIR = os.path.join(DATA_DIR, 'pyqt4')
PYUIC4 = "%s"
PYLUPDATE4 = "%s"
LRELEASE = "%s"

""" %(self.vars['Linux']['data'], self.vars['Linux']['bin'], \
      find_executable('pyuic4'), find_executable('pylupdate4'), \
      find_executable('lrelease-qt4')))
        
        elif self.os == 'Windows':
            cfg = os.path.join(self.vars['Windows']['package'], '_config.py')
            fhandler = open(cfg, 'w')
            fhandler.write("""#-*- coding: utf-8 -*- \n\n
import os

DATA_DIR = "%s"
BIN_DIR = "%s"

ICONS_DIR = os.path.join(DATA_DIR, 'icons')
UI_DIR = os.path.join(DATA_DIR, 'ui')
PYQT4_DIR = os.path.join(DATA_DIR, 'pyqt4')
PYLUPDATE4 = "%s"
LRELEASE = "%s"
PYUIC4 = "%s"

""" %(self.vars['Windows']['data'], self.vars['Windows']['bin'], \
      self.windows_execs[0].replace('\\', '/'), self.windows_execs[1].replace('\\', '/'), \
      self.windows_execs[2].replace('\\', '/')))



if __name__ == '__main__':
    c = Installer()
    arg = sys.argv[1]
    if arg == 'install':
        c.check_depends()
        c.check_paths()
        c.do_install()
        c.build_config()
    elif arg == 'uninstall':
        c.do_uninstall()

