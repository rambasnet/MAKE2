#Boa:MDIChild:dlgKnownFilesReport

#-----------------------------------------------------------------------------
# Name:        dlgEmailKeyExtract.py
# Purpose:     
#
# Author:      Ram B. Basnet
#
# Created:     2008/04/17
# RCS-ID:      $Id: dlgEmailKeyExtract.py $
# Copyright:   (c) 2008
# Licence:     All Rights Reserved.

#-----------------------------------------------------------------------------

import wx
import time
import re, string
import os, os.path, sys
import binascii
import shutil


from SqliteDatabase import *
import Globals
import Constants
import CommonFunctions
import images

from wx.lib.anchors import LayoutAnchors


def create(parent):
    return dlgKnownFilesReport(parent)

[wxID_DLGKNOWNFILESREPORT, wxID_DLGKNOWNFILESREPORTBTNCANCEL, 
 wxID_DLGKNOWNFILESREPORTBTNSAVEREPORT, 
 wxID_DLGKNOWNFILESREPORTCHKLISTBOXDATAFIELDS, 
 wxID_DLGKNOWNFILESREPORTPANSETTINGS, wxID_DLGKNOWNFILESREPORTRADCOMMA, 
 wxID_DLGKNOWNFILESREPORTRADSEMICOLON, wxID_DLGKNOWNFILESREPORTSTATICBOX1, 
 wxID_DLGKNOWNFILESREPORTSTATICTEXT1, 
] = [wx.NewId() for _init_ctrls in range(9)]

class dlgKnownFilesReport(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DLGKNOWNFILESREPORT,
              name=u'dlgKnownFilesReport', parent=prnt, pos=wx.Point(528, 310),
              size=wx.Size(497, 282), style=wx.DEFAULT_DIALOG_STYLE,
              title=u'Known Files Report')
        self.SetClientSize(wx.Size(489, 248))
        self.SetAutoLayout(True)
        self.SetBackgroundColour(wx.Colour(125, 152, 221))
        self.SetCursor(wx.STANDARD_CURSOR)
        self.SetMinSize(wx.Size(-1, -1))
        self.Center(wx.BOTH)

        self.btnSaveReport = wx.Button(id=wxID_DLGKNOWNFILESREPORTBTNSAVEREPORT,
              label=u'&Save Report', name=u'btnSaveReport', parent=self,
              pos=wx.Point(280, 208), size=wx.Size(107, 23), style=0)
        self.btnSaveReport.Bind(wx.EVT_BUTTON, self.OnBtnSaveReportButton,
              id=wxID_DLGKNOWNFILESREPORTBTNSAVEREPORT)

        self.btnCancel = wx.Button(id=wxID_DLGKNOWNFILESREPORTBTNCANCEL,
              label=u'&Cancel', name=u'btnCancel', parent=self,
              pos=wx.Point(400, 208), size=wx.Size(75, 23), style=0)
        self.btnCancel.Bind(wx.EVT_BUTTON, self.OnBtnCancelButton,
              id=wxID_DLGKNOWNFILESREPORTBTNCANCEL)

        self.panSettings = wx.Panel(id=wxID_DLGKNOWNFILESREPORTPANSETTINGS,
              name='panSettings', parent=self, pos=wx.Point(16, 16),
              size=wx.Size(456, 176), style=wx.TAB_TRAVERSAL)
        self.panSettings.SetBackgroundColour(wx.Colour(225, 236, 255))
        self.panSettings.SetAutoLayout(True)

        self.chkListBoxDataFields = wx.CheckListBox(choices=['File Path',
              'MD5'], id=wxID_DLGKNOWNFILESREPORTCHKLISTBOXDATAFIELDS,
              name=u'chkListBoxDataFields', parent=self.panSettings,
              pos=wx.Point(8, 24), size=wx.Size(440, 71), style=wx.VSCROLL)
        self.chkListBoxDataFields.SetChecked(())
        self.chkListBoxDataFields.SetCheckedStrings(('File Path', 'MD5'))

        self.staticText1 = wx.StaticText(id=wxID_DLGKNOWNFILESREPORTSTATICTEXT1,
              label=u'Select Data Field(s):', name='staticText1',
              parent=self.panSettings, pos=wx.Point(8, 8), size=wx.Size(97, 13),
              style=0)

        self.staticBox1 = wx.StaticBox(id=wxID_DLGKNOWNFILESREPORTSTATICBOX1,
              label=u'Select Delimeter', name='staticBox1',
              parent=self.panSettings, pos=wx.Point(8, 112), size=wx.Size(440,
              48), style=0)

        self.radSemiColon = wx.RadioButton(id=wxID_DLGKNOWNFILESREPORTRADSEMICOLON,
              label=u'Semi Colon', name=u'radSemiColon',
              parent=self.panSettings, pos=wx.Point(16, 136), size=wx.Size(72,
              13), style=0)
        self.radSemiColon.SetValue(True)

        self.radComma = wx.RadioButton(id=wxID_DLGKNOWNFILESREPORTRADCOMMA,
              label=u'Comma', name=u'radComma', parent=self.panSettings,
              pos=wx.Point(96, 136), size=wx.Size(81, 13), style=0)
        self.radComma.SetValue(False)

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.SetIcon(images.getMAKE2Icon())
        
        
    def OnBtnCancelButton(self, event):
        self.Close()


    def OnBtnSaveReportButton(self, event):
        self.startTime = time.time()
        dlg = wx.FileDialog(self, "Save Known Files Report", ".", "", "*.csv", wx.SAVE)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                db = SqliteDatabase(Globals.FileSystemName)
                if not db.OpenConnection():
                    return
        
                busy = wx.BusyInfo("It might take a while...")
                wx.Yield()
                
                query = "select DirPath||'%s'||Name, MD5 from %s where KnownFile = 1;"%(os.path.sep, Globals.CurrentEvidenceID)
                fileName = dlg.GetPath()
                
                fout = open(fileName, 'wb')
                fout.write('Report Generated on: %s\n'%(time.ctime()))
                rows = db.FetchAllRows(query)
                
                fout.write('There are %d total known files.\n\n'%(len(rows)))
                delimeter = ";"
                if self.radComma.GetValue():
                    delimeter = ","
                    
                for row in rows:
                    fout.write("%s%s%s\n"%(unicode(row[0]), delimeter, unicode(row[1])))
                
                db.CloseConnection()
                fout.close()
                self.elapsedTime = CommonFunctions.ConvertSecondsToYearDayHourMinSec(time.time() - self.startTime)
                msg = "Done generating report! (%s)"%(self.elapsedTime)
                CommonFunctions.ShowErrorMessage(self, msg, error=False)
        
        except Exception, value:
            CommonFunctions.ShowErrorMessage(self, "Failed to Save Known Files Report! Error: %s"%value)
        finally:
            dlg.Destroy()
                    
        self.Close()

