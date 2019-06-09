#-----------------------------------------------------------------------------
# Name:        setup.py
# Purpose:     
#
# Author:      Ram Basnet
#
# Created:     2008/04/28
# RCS-ID:      $Id: setup.py $
# Copyright:   (c) 2008
# Licence:     All Rights Reserved.
#-----------------------------------------------------------------------------


from distutils.core import setup
import py2exe

myrevisionstring = "Internal Rev 2.0"
setup(windows=[{'script': 'MAKE2.py',
            'other_resources': [(u"VERSIONTAB", 2, myrevisionstring)],
            'icon_resources': [(1, r'Images\MAKE2.ico')]
            }],
            name = 'MAKE2::Digital Forensics Toolkit',
            version = "2.0",
            description = 'Media Analysis and Knowledge Extraction and Exploration::Digital Forensics Toolkit',
            author = 'Ram Basnet',
            author_email = 'rambasnet@gmail.com',
            data_files = [('Data', [r'Images\MAKE2.ico', r'Data\NSRL.db', r'Data\stoplist.txt', r'Images\Spinning_wheel_throbber.gif'])]
            )