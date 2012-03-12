#!/usr/bin/env python
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
# $Id: qt-project-creator.py 38 2010-10-08 19:20:30Z muslim $
# $Rev: 38 $
# $LastChangedDate: 2010-10-08 22:20:30 +0300 (Fri, 08 Oct 2010) $
# $LastChangedBy: muslim $


import sys
import os
import platform
from ConfigParser import RawConfigParser as ConfigParser

from qtprojectcreator import generator
#from pyqtprojectcreator import _config

# Check PyQt4 modules
try:
    import PyQt4
    PYQT4 = True
except ImportError:
    PYQT4 = False

if not PYQT4:
    print "It seems you don't have PyQT4 installed."
    print "If you're running Debian/Ubuntu, you can install by running:"
    print
    print "apt-get install python-qt4 python-qt4-dev pyqt4-dev-tools"
    sys.exit(1)


OS = platform.system()
USER_HOME = os.path.expanduser('~')
USER_PROFILE = os.path.join(USER_HOME, '.pyqt-project-creator', 'user-profile.ini')


class StartProject:
    def __init__(self):
        '''Class Initialization'''
        self.check_pim()
        self.select_os()
        self.project_info()
        self.create_new_project()


    def header(self):
        '''Show a simple header in top of the window'''
        if OS == 'Windows':
            os.system('cls')
        else:
            os.system('clear')
        print 'PyQT Project Creator: Start New Project'
        print '============================================'
        print

    
    def check_pim(self):
        '''Check personal information'''
        if os.path.exists(USER_PROFILE):
            if not self.is_user_profile_ok():
                self.create_new_user_profile()
        else:
            self.create_new_user_profile()
    
    
    def create_new_user_profile(self):
        '''TODO:
        ^^^^^^^^^
        1. Ensure that @full_name is string
        2. Ensure that @email is a correct email address
        3. Ensure that @website is a correct URL'''
        
        # Show header
        self.header()
        
        # Define vars...
        full_name = None
        email = None
        website = None
        
        # Get input from user
        while not full_name:
            full_name = raw_input("1. Enter your full name: ")
        
        while not email:
            email = raw_input("2. Enter your email address: ")
        
        while not website:
            website = raw_input("3. Enter project website/blog: ")
        
        if not os.path.exists(os.path.join(USER_HOME, '.pyqt-project-creator')):
            os.mkdir(os.path.join(USER_HOME, '.pyqt-project-creator'))
        
        # Write new PIM file
        fhandler = ConfigParser()
        fhandler.add_section('PIM')
        fhandler.set('PIM', 'website', website)
        fhandler.set('PIM', 'email', email)
        fhandler.set('PIM', 'full_name', full_name)

        with open(USER_PROFILE, 'wb') as pim_file:
            fhandler.write(pim_file)
  

    def is_user_profile_ok(self):
        
        fhandler = ConfigParser()
        fhandler.read(USER_PROFILE)
        
        try:
            fhandler.get('PIM', 'full_name')
            fhandler.get('PIM', 'email')
            fhandler.get('PIM', 'website')
        except:
            return False
        
        return True


    def get_user_profile(self):
        
        fhandler = ConfigParser()
        fhandler.read(USER_PROFILE)
        
        data = {
            'full_name': fhandler.get('PIM', 'full_name'),
            'email': fhandler.get('PIM', 'email'),
            'website': fhandler.get('PIM', 'website'),
        }
        
        return data


    def select_os(self):
        self.header()
        
        allowed_entries = [ '1', '2', '3' ]
        oses = {'1': 'Linux', '2': 'Windows', '3': 'All'}
        os = None
        
        print 'Where you want to run your project?'
        print
        print '1. Linux'
        print '2. Windows'
        print '3. All'
        print
        while not os in allowed_entries:
            os = raw_input('Please select [1, 2, 3]: ')
        
        self.OS = oses[os]


    def project_info(self):
        self.header()
        self.pname = None
        self.version = None
        self.license = None
        self.short_desc = None
        self.long_desc = None
        
        while not self.pname:
            self.pname = raw_input('1. Enter project name [e.g. mynewproject]: ')
        
        while not self.version:
            self.version = raw_input('2. Enter project version [e.g. 0.1]: ')
        
        while not self.license:
            self.license = raw_input('3. Enter project license [e.g. GPLv3]: ')
            
        while not self.short_desc:
            self.short_desc = raw_input('4. Enter a short description: ')
        
        while not self.long_desc:
            self.long_desc = raw_input('5. Enter a long description: ')


    def create_new_project(self):
        pim = self.get_user_profile()
        proj = {
            'project_name': self.pname,
            'license': self.license,
            'short_desc': self.short_desc,
            'long_desc': self.long_desc,
            'OS': self.OS,
        }
        
        # data = proj
        # data.update(pim)
        data = dict(proj, **pim)
        
        g = generator.CreateProject(data)
        g.generate_pyqt_data_from_template()


if __name__ == '__main__':
    msg = 'Usage: %s startproject' % os.path.basename(sys.argv[0])
    try:
        arg = sys.argv[1]
        if arg == 'startproject':
            s = StartProject()
        else:
            print msg
    except:
        print msg
    #StartProject()