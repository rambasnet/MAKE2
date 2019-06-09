#Boa:Frame:frmEmailCentralID

#-----------------------------------------------------------------------------
# Name:        frmEmailCentralID.py
# Purpose:     
#
# Author:      Ram Basnet
#
# Created:     2007/11/01
# RCS-ID:      $Id: frmEmailCentralID.py,v 1.2 2007/11/04 03:17:30 rbasnet Exp $
# Copyright:   (c) 2007
# Licence:     All Rights Reserved.
# New field:   Whatever
#-----------------------------------------------------------------------------


import wx, re

from SqliteDatabase import *
import Globals
import Constants
import CommonFunctions
import DBFunctions
import EmailUtilities
import EmailMapWindow

def create(parent):
    return frmEmailCentralID(parent)

[wxID_FRMEMAILCENTRALID, wxID_FRMEMAILCENTRALIDBTNCANCEL, 
 wxID_FRMEMAILCENTRALIDBTNIMPORT, wxID_FRMEMAILCENTRALIDBTNOK, 
 wxID_FRMEMAILCENTRALIDPANSETTINGS, wxID_FRMEMAILCENTRALIDSTATICBOX1, 
 wxID_FRMEMAILCENTRALIDSTATICTEXT1, wxID_FRMEMAILCENTRALIDSTATICTEXT2, 
 wxID_FRMEMAILCENTRALIDTXTCENTRALID, wxID_FRMEMAILCENTRALIDTXTEMAILS, 
] = [wx.NewId() for _init_ctrls in range(10)]

class frmEmailCentralID(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRMEMAILCENTRALID,
              name='frmEmailCentralID', parent=prnt, pos=wx.Point(828, 380),
              size=wx.Size(416, 384), style=wx.DEFAULT_DIALOG_STYLE,
              title='Email Central ID')
        self.SetClientSize(wx.Size(408, 353))
        self.SetAutoLayout(True)
        self.SetIcon(wx.Icon('./Images/FNSFIcon.ico',wx.BITMAP_TYPE_ICO))
        self.SetBackgroundColour(wx.Colour(125, 152, 221))
        self.SetCursor(wx.STANDARD_CURSOR)
        self.SetMinSize(wx.Size(-1, -1))
        self.Center(wx.BOTH)

        self.btnOK = wx.Button(id=wxID_FRMEMAILCENTRALIDBTNOK, label=u'&OK',
              name=u'btnOK', parent=self, pos=wx.Point(144, 312),
              size=wx.Size(75, 23), style=0)
        self.btnOK.Bind(wx.EVT_BUTTON, self.OnBtnOKButton,
              id=wxID_FRMEMAILCENTRALIDBTNOK)

        self.btnCancel = wx.Button(id=wxID_FRMEMAILCENTRALIDBTNCANCEL,
              label=u'&Cancel', name=u'btnCancel', parent=self,
              pos=wx.Point(232, 312), size=wx.Size(75, 23), style=0)
        self.btnCancel.Bind(wx.EVT_BUTTON, self.OnBtnCancelButton,
              id=wxID_FRMEMAILCENTRALIDBTNCANCEL)

        self.panSettings = wx.Panel(id=wxID_FRMEMAILCENTRALIDPANSETTINGS,
              name='panSettings', parent=self, pos=wx.Point(16, 16),
              size=wx.Size(376, 280), style=wx.TAB_TRAVERSAL)
        self.panSettings.SetBackgroundColour(wx.Colour(225, 236, 255))
        self.panSettings.SetAutoLayout(True)

        self.txtCentralID = wx.TextCtrl(id=wxID_FRMEMAILCENTRALIDTXTCENTRALID,
              name='txtCentralID', parent=self.panSettings, pos=wx.Point(16,
              40), size=wx.Size(344, 21), style=0, value='')
        self.txtCentralID.Enable(True)

        self.staticText1 = wx.StaticText(id=wxID_FRMEMAILCENTRALIDSTATICTEXT1,
              label='* Please enter account Email ID or Full Name:',
              name='staticText1', parent=self.panSettings, pos=wx.Point(16, 16),
              size=wx.Size(217, 13), style=0)

        self.staticBox1 = wx.StaticBox(id=wxID_FRMEMAILCENTRALIDSTATICBOX1,
              label='Communication Maps With (optional):', name='staticBox1',
              parent=self.panSettings, pos=wx.Point(8, 72), size=wx.Size(360,
              200), style=0)

        self.txtEmails = wx.TextCtrl(id=wxID_FRMEMAILCENTRALIDTXTEMAILS,
              name='txtEmails', parent=self.panSettings, pos=wx.Point(16, 120),
              size=wx.Size(344, 144),
              style=wx.SUNKEN_BORDER | wx.TE_MULTILINE | wx.VSCROLL, value='')

        self.staticText2 = wx.StaticText(id=wxID_FRMEMAILCENTRALIDSTATICTEXT2,
              label='Enter comma separated email id or full name:',
              name='staticText2', parent=self.panSettings, pos=wx.Point(16, 96),
              size=wx.Size(215, 13), style=0)

        self.btnImport = wx.Button(id=wxID_FRMEMAILCENTRALIDBTNIMPORT,
              label='Import Emails List', name='btnImport',
              parent=self.panSettings, pos=wx.Point(240, 88), size=wx.Size(115,
              23), style=0)
        self.btnImport.Bind(wx.EVT_BUTTON, self.OnBtnImportButton,
              id=wxID_FRMEMAILCENTRALIDBTNIMPORT)

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.parent = parent
        self.EmailRE = re.compile('([\W]*)([A-Z0-9._%-]+@[A-Z0-9._%-]+\.[A-Z]+)([\W]*)', re.I)            
        self.Emails = ""
        self.EmailsList = []
        
    def CheckSettingsInput(self):
        message = ""
        if len(self.txtCentralID.GetValue().strip()) == 0:
            message = "Please enter account Email ID or Full Name."
         
        return message
    
    
    def OnBtnOKButton(self, event):
        msg = self.CheckSettingsInput()
        
        if msg:
            dlg = wx.MessageDialog(self, msg,
              'Error', wx.OK | wx.ICON_ERROR)
            try:
                dlg.ShowModal()
            finally:
                dlg.Destroy()
                return
    
        
        busy = wx.BusyInfo("Please wait! Processing emails data...")
        wx.Yield()
        self.CentralID = self.txtCentralID.GetValue().strip().lower()
        
        if not Globals.EmailsDict.has_key(self.CentralID):
            if not self.EmailRE.search(self.CentralID):
                self.CentralID = EmailUtilities.LookupEmailID(self.CentralID).lower()
            
            if not Globals.EmailsDict.has_key(self.CentralID):
                CommonFunctions.ShowErrorMessage(self, "Central ID: %s is not found in database!"%self.CentralID)
                return
            
        
        emails = self.txtEmails.GetValue()
        self.GroupEmailsDict = {}
        if len(emails) > 0:
            mailsList = emails.split(",")
            for emailID in mailsList:
                if not self.EmailRE.search(emailID):
                    email = EmailUtilities.LookupEmailID(emailID.strip()).lower()
                    self.GroupEmailsDict[email] = {}
                else:
                    self.GroupEmailsDict[emailID.strip().lower()] = {}
                    
            
        if Globals.CentralID != self.CentralID or self.GroupEmailsDict != Globals.GroupEmailsDict:
            Globals.GroupEmailsDict = self.GroupEmailsDict
            Globals.CentralID = self.CentralID
            Globals.OrderedEmailDict = {}
            EmailUtilities.OrderEmailsToCentralEmail(self.CentralID, Globals.EmailsDict, Globals.OrderedEmailDict, Globals.GroupEmailsDict)
        map = EmailMapWindow.WindowHolder(Globals.frmGlobalMainForm, Globals.OrderedEmailDict, self.CentralID)
        map.Show(True)
        self.Close()
        
        
    def OnBtnCancelButton(self, event):
        self.Close()

    def OnBtnImportButton(self, event):
        dlg = wx.FileDialog(self, "Open Comma Separated Emails File", ".", "", "*.*", wx.OPEN)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                FileName = dlg.GetPath()
                self.ReadKeywordsFromFile(FileName)
                self.txtKeywords.SetValue(self.Emails)
            else:
                return None
        finally:
            dlg.Destroy()
        event.Skip()

    def ReadKeywordsFromFile(self, fileName):
        fin = open(fileName, "r")
        while True:
            lines = fin.readlines()
            if not lines:
                break
            for word in lines:
                #self.Keywords.add(word.strip())
                if self.Emails == "":
                    self.Emails += word.strip()
                else:
                    self.Emails += ", " + word.strip()
     
        fin.close()


    
