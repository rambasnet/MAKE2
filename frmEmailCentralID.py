#Boa:Frame:frmEmailCentralID

import wx, re
import wx.lib.buttons

from SqliteDatabase import *
import Globals
import Constants
import CommonFunctions
import DBFunctions
import EmailUtilities
import EmailMapWindow
import images

def create(parent):
    return frmEmailCentralID(parent)

[wxID_FRMEMAILCENTRALID, wxID_FRMEMAILCENTRALIDBTNCANCEL, 
 wxID_FRMEMAILCENTRALIDBTNIMPORT, wxID_FRMEMAILCENTRALIDBTNOK, 
 wxID_FRMEMAILCENTRALIDBTNSHOWALL, wxID_FRMEMAILCENTRALIDBTNSHOWRECEIVERS, 
 wxID_FRMEMAILCENTRALIDBTNSHOWSENDERS, wxID_FRMEMAILCENTRALIDPANSETTINGS, 
 wxID_FRMEMAILCENTRALIDSTATICBOX1, wxID_FRMEMAILCENTRALIDSTATICTEXT1, 
 wxID_FRMEMAILCENTRALIDSTATICTEXT2, wxID_FRMEMAILCENTRALIDTXTEMAILS, 
] = [wx.NewId() for _init_ctrls in range(12)]

class frmEmailCentralID(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRMEMAILCENTRALID,
              name='frmEmailCentralID', parent=prnt, pos=wx.Point(596, 148),
              size=wx.Size(417, 418), style=wx.DEFAULT_DIALOG_STYLE,
              title=u'Centralized Graph')
        self.SetClientSize(wx.Size(409, 384))
        self.SetAutoLayout(True)
        self.SetBackgroundColour(wx.Colour(125, 152, 221))
        self.SetCursor(wx.STANDARD_CURSOR)
        self.SetMinSize(wx.Size(-1, -1))
        self.Center(wx.BOTH)

        self.btnOK = wx.Button(id=wxID_FRMEMAILCENTRALIDBTNOK, label=u'&OK',
              name=u'btnOK', parent=self, pos=wx.Point(144, 344),
              size=wx.Size(75, 23), style=0)
        self.btnOK.Bind(wx.EVT_BUTTON, self.OnBtnOKButton,
              id=wxID_FRMEMAILCENTRALIDBTNOK)

        self.btnCancel = wx.Button(id=wxID_FRMEMAILCENTRALIDBTNCANCEL,
              label=u'&Cancel', name=u'btnCancel', parent=self,
              pos=wx.Point(232, 344), size=wx.Size(75, 23), style=0)
        self.btnCancel.Bind(wx.EVT_BUTTON, self.OnBtnCancelButton,
              id=wxID_FRMEMAILCENTRALIDBTNCANCEL)

        self.panSettings = wx.Panel(id=wxID_FRMEMAILCENTRALIDPANSETTINGS,
              name='panSettings', parent=self, pos=wx.Point(16, 16),
              size=wx.Size(376, 320), style=wx.TAB_TRAVERSAL)
        self.panSettings.SetBackgroundColour(wx.Colour(225, 236, 255))
        self.panSettings.SetAutoLayout(True)

        self.staticText1 = wx.StaticText(id=wxID_FRMEMAILCENTRALIDSTATICTEXT1,
              label=u'* Please Select Central Graph Node:', name='staticText1',
              parent=self.panSettings, pos=wx.Point(16, 16), size=wx.Size(174,
              13), style=0)

        self.staticBox1 = wx.StaticBox(id=wxID_FRMEMAILCENTRALIDSTATICBOX1,
              label=u'Limit Graph Amongst (optional):', name='staticBox1',
              parent=self.panSettings, pos=wx.Point(8, 112), size=wx.Size(360,
              200), style=0)

        self.txtEmails = wx.TextCtrl(id=wxID_FRMEMAILCENTRALIDTXTEMAILS,
              name='txtEmails', parent=self.panSettings, pos=wx.Point(16, 160),
              size=wx.Size(344, 144),
              style=wx.SUNKEN_BORDER | wx.TE_MULTILINE | wx.VSCROLL, value='')

        self.staticText2 = wx.StaticText(id=wxID_FRMEMAILCENTRALIDSTATICTEXT2,
              label='Enter comma separated email id or full name:',
              name='staticText2', parent=self.panSettings, pos=wx.Point(16,
              136), size=wx.Size(215, 13), style=0)

        self.btnImport = wx.Button(id=wxID_FRMEMAILCENTRALIDBTNIMPORT,
              label='Import Emails List', name='btnImport',
              parent=self.panSettings, pos=wx.Point(240, 128), size=wx.Size(115,
              23), style=0)
        self.btnImport.Bind(wx.EVT_BUTTON, self.OnBtnImportButton,
              id=wxID_FRMEMAILCENTRALIDBTNIMPORT)

        self.btnShowSenders = wx.lib.buttons.GenToggleButton(id=wxID_FRMEMAILCENTRALIDBTNSHOWSENDERS,
              label=u'Show Senders', name=u'btnShowSenders',
              parent=self.panSettings, pos=wx.Point(16, 40), size=wx.Size(101,
              25), style=0)
        self.btnShowSenders.SetToggle(True)
        self.btnShowSenders.Bind(wx.EVT_BUTTON, self.OnBtnShowSendersButton,
              id=wxID_FRMEMAILCENTRALIDBTNSHOWSENDERS)

        self.btnShowReceivers = wx.lib.buttons.GenToggleButton(id=wxID_FRMEMAILCENTRALIDBTNSHOWRECEIVERS,
              label=u'Show Receivers', name=u'btnShowReceivers',
              parent=self.panSettings, pos=wx.Point(136, 40), size=wx.Size(101,
              25), style=0)
        self.btnShowReceivers.SetToggle(False)
        self.btnShowReceivers.Bind(wx.EVT_BUTTON, self.OnBtnShowReceiversButton,
              id=wxID_FRMEMAILCENTRALIDBTNSHOWRECEIVERS)

        self.btnShowAll = wx.lib.buttons.GenToggleButton(id=wxID_FRMEMAILCENTRALIDBTNSHOWALL,
              label=u'Show All Accounts', name=u'btnShowAll',
              parent=self.panSettings, pos=wx.Point(256, 40), size=wx.Size(101,
              25), style=0)
        self.btnShowAll.SetToggle(False)
        self.btnShowAll.Bind(wx.EVT_BUTTON, self.OnBtnShowAllButton,
              id=wxID_FRMEMAILCENTRALIDBTNSHOWALL)

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.SetIcon(images.getMAKE2Icon())
        self.parent = parent
        self.EmailRE = re.compile('([\W]*)([A-Z0-9._%-]+@[A-Z0-9._%-]+\.[A-Z]+)([\W]*)', re.I)            
        self.Emails = ""
        self.EmailsList = []
        try:
            self.AddSenderEmailsToChoiceBox()
        except:
            pass
        
    def AddSenderEmailsToChoiceBox(self):
        """
                self.choice1 = wx.Choice(choices=[], id=wxID_FRMEMAILCENTRALIDCHOICE1,
              name='choice1', parent=self.panSettings, pos=wx.Point(16, 80),
              size=wx.Size(344, 21), style=0)
        """
        db = SqliteDatabase(Globals.EmailsFileName)
        if not db.OpenConnection():
            return
        
        self.choiceEmails = wx.Choice(choices=[],
          id=wx.NewId(), name='choiceEmails',
          parent=self.panSettings, pos=wx.Point(16, 80), size=wx.Size(344,
          21), style=0)
        rows = db.FetchAllRows('select fromid, count(fromid) as total from %s group by fromid order by total desc;'%(Constants.EmailsTable))
        for row in rows:
            self.choiceEmails.Append("%s (%d)"%(row[0], row[1]))
        
        self.btnShowSenders.Enable(False)
        db.CloseConnection()
    
    def CheckSettingsInput(self):
        message = ""
        if len(self.choiceEmails.GetStringSelection().strip()) == 0:
            message = "Please select an email account name from dropdown."
         
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
        #self.CentralID = self.txtCentralID.GetValue().strip().lower()
        self.CentralID = self.choiceEmails.GetStringSelection().split('(')[0].strip()
        
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
                    
            
        
        #if Globals.CentralID != self.CentralID or self.GroupEmailsDict != Globals.GroupEmailsDict:
        #Globals.GroupEmailsDict = self.GroupEmailsDict
        #Globals.CentralID = self.CentralID
        OrderedEmailDict = {}
        EmailsInfo = EmailUtilities.OrderEmailsToCentralEmail(self.CentralID, Globals.EmailsDict, OrderedEmailDict, self.GroupEmailsDict)
            
        map = EmailMapWindow.WindowHolder(Globals.frmGlobalMainForm, OrderedEmailDict, EmailsInfo, self.CentralID)
        map.Show(True)
        #self.Close()
        
        
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

    def OnBtnShowSendersButton(self, event):
        #print self.btnShowSenders.GetValue()
        #print self.btnShowSenders.GetToggle()
        busy = wx.BusyInfo("Pleae hold! Reloading dropdown list with all Senders...")
        wx.Yield()
        db = SqliteDatabase(Globals.EmailsFileName)
        if not db.OpenConnection():
            return

        rows = db.FetchAllRows('select fromid, count(fromid) as total from %s group by fromid order by total desc;'%(Constants.EmailsTable))
        self.choiceEmails.Clear()
        for row in rows:
            self.choiceEmails.Append("%s (%d)"%(row[0], row[1]))
        
        self.btnShowSenders.Enable(False)
        db.CloseConnection()
        
        self.btnShowReceivers.SetToggle(False)
        self.btnShowReceivers.Enable(True)
        self.btnShowAll.SetToggle(False)
        self.btnShowAll.Enable(True)
        self.btnShowSenders.Enable(False)
        
        event.Skip()

    def OnBtnShowReceiversButton(self, event):
        busy = wx.BusyInfo("Pleae hold! Reloading dropdown list with all Receivers...")
        wx.Yield()
        
        db = SqliteDatabase(Globals.EmailsFileName)
        if not db.OpenConnection():
            return

        rows = db.FetchAllRows('select toid, count(toid) as total from %s group by toid order by total desc;'%(Constants.EmailsTable))
        self.choiceEmails.Clear()
        for row in rows:
            self.choiceEmails.Append("%s (%d)"%(row[0], row[1]))
        
        self.btnShowReceivers.Enable(False)
        db.CloseConnection()
        
        self.btnShowSenders.SetToggle(False)
        self.btnShowSenders.Enable(True)
        self.btnShowAll.SetToggle(False)
        self.btnShowAll.Enable(True)
        event.Skip()

    def OnBtnShowAllButton(self, event):
        busy = wx.BusyInfo("Pleae hold! Reloading dropdown list with all Emails...")
        wx.Yield()
        #rows = db.FetchAllRows('select toid, count(toid) as total from %s group by toid order by total desc;'%(Constants.EmailsTable))
        self.choiceEmails.Clear()
        for key in Globals.EmailsDict:
            self.choiceEmails.Append(key)
        
        self.btnShowAll.Enable(False)
                
        self.btnShowSenders.SetToggle(False)
        self.btnShowSenders.Enable(True)
        self.btnShowReceivers.SetToggle(False)
        self.btnShowReceivers.Enable(True)
        event.Skip()


    
