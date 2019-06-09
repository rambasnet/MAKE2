#-----------------------------------------------------------------------------
# Name:        dlgDataSource.py
# Purpose:     
#
# Author:      Ram Basnet
#
# Created:     2008/11/14
# RCS-ID:      $Id: dlgDataSource.py,v 1.8 2008/03/17 04:18:38 rbasnet Exp $
# Copyright:   (c) 2008
# Licence:     <your licence>
# New field:   Whatever
#-----------------------------------------------------------------------------
#Boa:MDIChild:dlgDataSource

import wx

from SqliteDatabase import *
import Globals
import Constants
import images


def create(parent, evidenceID):
    return dlgDataSource(parent, evidenceID)

[wxID_DLGDATASOURCE, wxID_DLGDATASOURCEBTNBROWSE, wxID_DLGDATASOURCEBTNOK, 
 wxID_DLGDATASOURCELBLEVIDENCEID, wxID_DLGDATASOURCELBLEVIDENCENAME, 
 wxID_DLGDATASOURCEPANSCANSTATUS, wxID_DLGDATASOURCESTATICTEXT1, 
 wxID_DLGDATASOURCESTATICTEXT2, wxID_DLGDATASOURCESTATICTEXT4, 
 wxID_DLGDATASOURCETXTROOTPATH, 
] = [wx.NewId() for _init_ctrls in range(10)]

#----------------------------------------------------------------------

class dlgDataSource(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DLGDATASOURCE, name='dlgDataSource',
              parent=prnt, pos=wx.Point(517, 215), size=wx.Size(601, 219),
              style=0, title='Select Source Data Root Path')
        self.SetClientSize(wx.Size(593, 185))
        self.SetAutoLayout(True)
        self.SetBackgroundColour(wx.Colour(125, 152, 221))
        self.SetCursor(wx.STANDARD_CURSOR)
        self.SetMinSize(wx.Size(-1, -1))
        self.Center(wx.BOTH)
        self.Bind(wx.EVT_CLOSE, self.OnDlgDataSourceClose)

        self.panScanStatus = wx.Panel(id=wxID_DLGDATASOURCEPANSCANSTATUS,
              name=u'panScanStatus', parent=self, pos=wx.Point(16, 16),
              size=wx.Size(560, 112), style=wx.TAB_TRAVERSAL)
        self.panScanStatus.SetBackgroundColour(wx.Colour(225, 236, 255))

        self.lblEvidenceID = wx.StaticText(id=wxID_DLGDATASOURCELBLEVIDENCEID,
              label='Evidence1', name='lblEvidenceID',
              parent=self.panScanStatus, pos=wx.Point(88, 24), size=wx.Size(49,
              13), style=0)

        self.staticText2 = wx.StaticText(id=wxID_DLGDATASOURCESTATICTEXT2,
              label='Evidence ID:', name='staticText2',
              parent=self.panScanStatus, pos=wx.Point(16, 24), size=wx.Size(61,
              13), style=wx.ALIGN_RIGHT)

        self.lblEvidenceName = wx.StaticText(id=wxID_DLGDATASOURCELBLEVIDENCENAME,
              label='Evidence Name', name='lblEvidenceName',
              parent=self.panScanStatus, pos=wx.Point(88, 48), size=wx.Size(73,
              13), style=0)

        self.staticText4 = wx.StaticText(id=wxID_DLGDATASOURCESTATICTEXT4,
              label='Display Name:', name='staticText4',
              parent=self.panScanStatus, pos=wx.Point(8, 48), size=wx.Size(68,
              13), style=wx.ALIGN_RIGHT)

        self.btnOK = wx.Button(id=wxID_DLGDATASOURCEBTNOK, label=u'&OK',
              name=u'btnOK', parent=self, pos=wx.Point(264, 144),
              size=wx.Size(88, 24), style=0)
        self.btnOK.Show(True)
        self.btnOK.Bind(wx.EVT_BUTTON, self.OnBtnOKButton,
              id=wxID_DLGDATASOURCEBTNOK)

        self.staticText1 = wx.StaticText(id=wxID_DLGDATASOURCESTATICTEXT1,
              label='Root Path:', name='staticText1', parent=self.panScanStatus,
              pos=wx.Point(24, 80), size=wx.Size(52, 13), style=0)

        self.txtRootPath = wx.TextCtrl(id=wxID_DLGDATASOURCETXTROOTPATH,
              name='txtRootPath', parent=self.panScanStatus, pos=wx.Point(88,
              72), size=wx.Size(408, 21), style=0, value='Root Path')

        self.btnBrowse = wx.Button(id=wxID_DLGDATASOURCEBTNBROWSE, label='...',
              name='btnBrowse', parent=self.panScanStatus, pos=wx.Point(504,
              72), size=wx.Size(40, 23), style=0)
        self.btnBrowse.Bind(wx.EVT_BUTTON, self.OnBtnBrowseButton,
              id=wxID_DLGDATASOURCEBTNBROWSE)

    def __init__(self, parent, evidenceID):
        
        self._init_ctrls(parent)
        self.SetIcon(images.getMAKE2Icon())
        self.evidenceID = evidenceID
        self.lblEvidenceID.SetLabel(str(evidenceID))
        self.lblEvidenceName.SetLabel(Globals.EvidencesDict[evidenceID]['DisplayName'])
        self.txtRootPath.SetValue(Globals.EvidencesDict[evidenceID]['Location'])
        #Globals.EvidencesDict[row[0]] = {'DisplayName': row[1], 'Location':row[2]}
        
       
    def OnBtnOKButton(self, event):
        self.Close()


    def OnBtnBrowseButton(self, event):
        dlg = wx.DirDialog(self)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                self.txtRootPath.SetValue(dlg.GetPath())
            else:
                return None
        finally:
            dlg.Destroy()
        event.Skip()

    def OnDlgDataSourceClose(self, event):
        if Globals.EvidencesDict[self.evidenceID]['Location'] != self.txtRootPath.GetValue():
            #self.UpdateEvidence(self.txtRootPath.GetValue())
            Globals.EvidencesDict[self.evidenceID]['NewLocation'] = self.txtRootPath.GetValue()
        else:
            Globals.EvidencesDict[self.evidenceID]['NewLocation'] = ""
            
        event.Skip()
            
 
    def UpdateEvidence(self, location):
        pass
        """
        db = SqliteDatabase(Globals.CurrentCaseFile)
        if not db.OpenConnection():
            return

        #query = "UPDATE %s set Location = %s where ID = '%s', DisplayName"%(Constants.EvidencesTable, db.SqlSQuote(location), self.evidenceID)
        Globals.EvidencesDict[self.evidenceID]['NewLocation'] = location
        
        db.ExecuteNonQuery(query)
        db.CloseConnection()
        """

        
