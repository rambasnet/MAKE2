#-----------------------------------------------------------------------------
# Name:        PlatformMethods.py
# Purpose:     
#
# Author:      Ram Basnet
#
# Created:     2007/11/10
# RCS-ID:      $Id: PlatformMethods.py,v 1.4 2007/11/15 07:56:38 rbasnet Exp $
# Copyright:   (c) 2006
# Licence:     <your licence>
# New field:   Whatever
#-----------------------------------------------------------------------------
# helper function to make sure we don't convert unicode objects to strings
# or vice versa when converting lists and None values to text.
import wx
import os
import os.path
import sys

"""
Convert = str
if 'unicode' in wx.PlatformInfo:
    Convert = unicode
"""
def Decode(strValue):
    """
    if strValue == None:
        return str(strValue)
    try:
        return unicode(strValue)
    except:
    """
    try:
        return unicode(strValue, 'utf-8', 'replace')
    except:
        try:
            return unicode(strValue)
        except:
            return strValue
    
def Encode(strValue):
    try:
        return strValue.encode('utf-8', 'replace')
    except:
        return strValue
    

def GetDirSeparator():
    return os.path.sep
    """
    dirSep = "\\"
    if not sys.platform == "win32":
        dirSep = "/"
    return dirSep
    """

def ConvertFilePath(path):
    """Convert paths to the platform-specific separator"""
    str = apply(os.path.join, tuple(path.split('/')))
    # HACK: on Linux, a leading / gets lost...
    if path.startswith('/'):
        str = '/' + str
    return str

def GetWildcard():
    if sys.platform == 'win32':
        wildcard = "All files (*.*)|*.*|"\
                   "Text files (*.txt)|*.txt"
    else:
        wildcard = "All files|*|"\
                   "Text files (*.txt)|*.txt"
    return wildcard