#Boa:MDIChild:dlgCaseProperties

import wx
import wx.lib.buttons
import time
import os.path, sys

from wx.lib.anchors import LayoutAnchors

from SqliteDatabase import *
import Globals
import Constants
import CommonFunctions
import DBFunctions
import Classes
import Win32RawIO
import images

def create(parent, Case = None):
    return dlgCaseProperties(parent, Case)

[wxID_DLGCASEPROPERTIES, wxID_DLGCASEPROPERTIESBTNCANCEL, 
 wxID_DLGCASEPROPERTIESBTNOK, wxID_DLGCASEPROPERTIESLBLCASENAME, 
 wxID_DLGCASEPROPERTIESNOTEBOOKASSESSMENT, wxID_DLGCASEPROPERTIESPANSETTINGS, 
 wxID_DLGCASEPROPERTIESSTATICTEXT1, wxID_DLGCASEPROPERTIESSTATICTEXT12, 
 wxID_DLGCASEPROPERTIESSTATICTEXT13, wxID_DLGCASEPROPERTIESSTATICTEXT2, 
 wxID_DLGCASEPROPERTIESTXTCASEID, wxID_DLGCASEPROPERTIESTXTCREATEDBY, 
 wxID_DLGCASEPROPERTIESTXTDESCRIPTION, wxID_DLGCASEPROPERTIESTXTDISPLAYNAME, 
] = [wx.NewId() for _init_ctrls in range(14)]

class dlgCaseProperties(wx.Dialog):
    def _init_coll_NoteBookAssessment_Pages(self, parent):
        # generated method, don't edit

        parent.AddPage(imageId=-1, page=self.panSettings, select=True,
              text='Settings')

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DLGCASEPROPERTIES,
              name=u'dlgCaseProperties', parent=prnt, pos=wx.Point(851, 209),
              size=wx.Size(440, 526), style=wx.DEFAULT_DIALOG_STYLE,
              title=u'Case Properties')
        self.SetClientSize(wx.Size(432, 495))
        self.SetAutoLayout(True)
        self.SetBackgroundColour(wx.Colour(125, 152, 221))
        self.SetCursor(wx.STANDARD_CURSOR)
        self.SetMinSize(wx.Size(-1, -1))
        self.Center(wx.BOTH)

        self.NoteBookAssessment = wx.Notebook(id=wxID_DLGCASEPROPERTIESNOTEBOOKASSESSMENT,
              name='NoteBookAssessment', parent=self, pos=wx.Point(16, 48),
              size=wx.Size(400, 400), style=0)
        self.NoteBookAssessment.SetBackgroundColour(wx.Colour(125, 152, 221))
        self.NoteBookAssessment.SetAutoLayout(True)

        self.panSettings = wx.Panel(id=wxID_DLGCASEPROPERTIESPANSETTINGS,
              name='panSettings', parent=self.NoteBookAssessment,
              pos=wx.Point(0, 0), size=wx.Size(392, 374),
              style=wx.TAB_TRAVERSAL)
        self.panSettings.SetBackgroundColour(wx.Colour(225, 236, 255))
        self.panSettings.SetAutoLayout(True)

        self.staticText12 = wx.StaticText(id=wxID_DLGCASEPROPERTIESSTATICTEXT12,
              label=u'Description (optional):', name='staticText12',
              parent=self.panSettings, pos=wx.Point(16, 168), size=wx.Size(106,
              13), style=0)

        self.staticText13 = wx.StaticText(id=wxID_DLGCASEPROPERTIESSTATICTEXT13,
              label='Created By:', name='staticText13', parent=self.panSettings,
              pos=wx.Point(16, 112), size=wx.Size(58, 13), style=0)

        self.lblCaseName = wx.StaticText(id=wxID_DLGCASEPROPERTIESLBLCASENAME,
              label=u'Case Properties    ', name='lblCaseName', parent=self,
              pos=wx.Point(0, 0), size=wx.Size(432, 32),
              style=wx.ALIGN_RIGHT | wx.RAISED_BORDER | wx.ST_NO_AUTORESIZE)
        self.lblCaseName.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, 'Tahoma'))
        self.lblCaseName.SetForegroundColour(wx.Colour(0, 78, 155))
        self.lblCaseName.SetBackgroundColour(wx.Colour(215, 235, 255))

        self.staticText1 = wx.StaticText(id=wxID_DLGCASEPROPERTIESSTATICTEXT1,
              label='Display Name:', name='staticText1',
              parent=self.panSettings, pos=wx.Point(16, 64), size=wx.Size(68,
              13), style=0)

        self.staticText2 = wx.StaticText(id=wxID_DLGCASEPROPERTIESSTATICTEXT2,
              label='Case ID:', name='staticText2', parent=self.panSettings,
              pos=wx.Point(16, 16), size=wx.Size(42, 13), style=0)

        self.txtCaseID = wx.TextCtrl(id=wxID_DLGCASEPROPERTIESTXTCASEID,
              name='txtCaseID', parent=self.panSettings, pos=wx.Point(16, 32),
              size=wx.Size(176, 21), style=0, value='')

        self.txtDisplayName = wx.TextCtrl(id=wxID_DLGCASEPROPERTIESTXTDISPLAYNAME,
              name='txtDisplayName', parent=self.panSettings, pos=wx.Point(16,
              80), size=wx.Size(352, 21), style=0, value='')
        self.txtDisplayName.Enable(True)

        self.txtCreatedBy = wx.TextCtrl(id=wxID_DLGCASEPROPERTIESTXTCREATEDBY,
              name=u'txtCreatedBy', parent=self.panSettings, pos=wx.Point(16,
              128), size=wx.Size(352, 21), style=0, value='')

        self.txtDescription = wx.TextCtrl(id=wxID_DLGCASEPROPERTIESTXTDESCRIPTION,
              name=u'txtDescription', parent=self.panSettings, pos=wx.Point(16,
              184), size=wx.Size(352, 80), style=wx.TE_MULTILINE | wx.VSCROLL,
              value='')

        self.btnOK = wx.Button(id=wxID_DLGCASEPROPERTIESBTNOK, label=u'&OK',
              name=u'btnOK', parent=self, pos=wx.Point(256, 456),
              size=wx.Size(75, 23), style=0)
        self.btnOK.Bind(wx.EVT_BUTTON, self.OnBtnOKButton,
              id=wxID_DLGCASEPROPERTIESBTNOK)

        self.btnCancel = wx.Button(id=wxID_DLGCASEPROPERTIESBTNCANCEL,
              label=u'&Cancel', name=u'btnCancel', parent=self,
              pos=wx.Point(336, 456), size=wx.Size(75, 23), style=0)
        self.btnCancel.Bind(wx.EVT_BUTTON, self.OnBtnCancelButton,
              id=wxID_DLGCASEPROPERTIESBTNCANCEL)

        self._init_coll_NoteBookAssessment_Pages(self.NoteBookAssessment)

    def __init__(self, parent, Case):
        
        self._init_ctrls(parent)
        self.SetIcon(images.getMAKE2Icon())
        self.Case = Case
        self.addingNewCase = True
        if self.Case:
            self.addingNewCase = False
            self.LoadCurrentCase()
            self.lblCaseName.SetLabel("Edit Case - " + self.Case.DisplayName + "    ")
            
        else:
            self.Case = Globals.CurrentCase = Classes.CFICase()
            self.lblCaseName.SetLabel("New Case    ")

        
    def CheckSettingsInput(self):
        message = "success"
        if len(self.txtCaseID.GetValue().strip()) == 0:
            message = "Please enter Case ID."
        elif len(self.txtDisplayName.GetValue().strip()) == 0:
            message = "Please enter Display Name."
        elif len(self.txtCreatedBy.GetValue()) == 0:
            message = "Please enter investigator's name."
        elif self.addingNewCase:
            if self.CaseNameExists(self.txtDisplayName.GetValue().strip()):
                message = "Case name already exists. Please choose a different case name!"
            elif self.CaseNameExists(self.txtCaseID.GetValue().strip()):
                message = "Case ID already exists. Please choose a different case name!"
            #elif self.DatabaseNameExists(self.txtDisplayName.GetValue().strip()):
            #    message = "Database name already exists. Please choose a different database name!"
            
                
        return message

    
                
    def CaseNameExists(self, name):
        if CommonFunctions.FileExists(name):
            return True
        elif CommonFunctions.FileExists(name+Constants.CaseNameExtension):
            return True
        elif CommonFunctions.FileExists(name+Constants.MACExtension):
            return True
        elif CommonFunctions.FileExists(name+Constants.KeywordsExtension):
            return True
        elif CommonFunctions.FileExists(name+Constants.TextCatExtension):
            return True
        else:
            return False

        
    def SaveCaseInfo(self):
        #dbName = CaseMods.GetIndvidualCaseDB(self.Case)
        #dbPath = CaseMods.GetDBPath()
        #dbName = dbPath + self.Case.DBName
        #msg = CaseMods.SetupIndCaseDB(dbName)
        self.ApplyToCurrentCase()
        DBFunctions.CreateCaseSettingsTable(Globals.CurrentCaseFile)
        '''
        if msg <> "success":
            dlg = wx.MessageDialog(self, msg,
              'Error', wx.OK | wx.ICON_ERROR)
            try:
                dlg.ShowModal()
            finally:
                dlg.Destroy()
                return
        '''
        db = SqliteDatabase(Globals.CurrentCaseFile)
        if not db.OpenConnection():
            return
 
        #Save self.Case info
        query = ""
        #self.Case = self.Case
        self.Case.DateTimestamp = time.time()
        if self.addingNewCase:
            query = "insert into " + Constants.CaseSettingsTable + " (ID, DisplayName, DateTimestamp, CreatedBy, Description) values (?,?,?,?,?)"
            tuple = (self.Case.ID, self.Case.DisplayName, self.Case.DateTimestamp, self.Case.CreatedBy, self.Case.Description)
            
            """
            query += db.SqlSQuote() + ","
            query += db.SqlSQuote(self.Case.CaseDate) + ","
            query += db.SqlSQuote() + ","
            query += db.SqlSQuote(str() + ","
            query += db.SqlSQuote(str(self.Case.TotalDirectories)) + ","
            query += db.SqlSQuote(str(self.Case.TotalFiles)) + ","
            query += db.SqlSQuote(self.Case.GetKeywordFrequencyCount) + ","
            query += db.SqlSQuote(self.Case.GetFileProperties) + ","
            query += db.SqlSQuote(self.Case.CaseSensitive) + ","
            query += db.SqlSQuote(self.Case.SearchInPrefix) + ","
            query += db.SqlSQuote(self.Case.SearchInSuffix) + ","
            query += db.SqlSQuote(self.Case.SearchInMiddle) + ","
            query += db.SqlSQuote(self.Case.GetFileExtension) + ","
            query += db.SqlSQuote(self.Case.GetFileSize) + ","
            query += db.SqlSQuote(self.Case.GetCreatedTime) + ","
            query += db.SqlSQuote(self.Case.GetModifiedTime) + ","
            query += db.SqlSQuote(self.Case.GetAccessedTime) + ","
            query += db.SqlSQuote(self.Case.GetFileOwner) + ");"
            """
            
            db.ExecuteMany(query, [tuple])
                
        else:
            query = "UPDATE " + Constants.CaseSettingsTable + " set "
            #query += "CaseDate = " + db.SqlSQuote(self.Case.CaseDate) + ","
            query += "Description = " + db.SqlSQuote(self.Case.Description) + ","
            query += "CreatedBy = " + db.SqlSQuote(self.Case.CreatedBy) + ";"
            #print query
            db.ExecuteNonQuery(query)
            
        db.CloseConnection()

    
    def LoadCurrentCase(self):
        #Settings tab
        self.txtDisplayName.SetValue(self.Case.DisplayName)
        self.txtDisplayName.Enable(False)
        self.txtCaseID.SetValue(self.Case.ID)
        self.txtCaseID.Enable(False)
        #self.txtDate.SetValue(self.Case.CaseDate)
        #prjDateTime = self.Case.CaseDate.split("/")
        #CaseDateTime = wx.DateTimeFromDMY(25, 3, 2007)
        #print CaseDateTime
        #print int(prjDateTime[0])
        #print int(prjDateTime[1])
        #print int(prjDateTime[2])
        #CaseDateTime.SetYear(int(prjDateTime[2]))
        #CaseDateTime.SetDay(int(prjDateTime[1]))
       
        #CaseDateTime.SetMonth(int(prjDateTime[0])- 1)
        #self.datePickerCaseDate.SetValue(CaseDateTime)
        self.txtDescription.SetValue(self.Case.Description)
        self.txtCreatedBy.SetValue(self.Case.CreatedBy)
        

    def ApplyToCurrentCase(self):
        self.Case.ID = self.txtCaseID.GetValue().strip()
        self.Case.DisplayName = self.txtDisplayName.GetValue().strip()
        #self.Case.CaseDate = self.txtDate.GetValue().strip()
        #self.Case.CaseDate = self.datePickerCaseDate.GetLabel()
        self.Case.CreatedBy = self.txtCreatedBy.GetValue().strip()
        self.Case.Description = self.txtDescription.GetValue().strip()
        

    def OnBtnOKButton(self, event):
        import Init
        msg = self.CheckSettingsInput()
        
        if msg <> "success" :
            dlg = wx.MessageDialog(self, msg,
              'Error', wx.OK | wx.ICON_ERROR)
            try:
                dlg.ShowModal()
                return
            finally:
                dlg.Destroy()
        
        if self.addingNewCase:
            dlg = wx.FileDialog(self, "Save Case", ".", "", "*.cfi", wx.SAVE)
            try:
                if dlg.ShowModal() == wx.ID_OK:
                    Globals.CurrentCaseFile = dlg.GetPath()
                    self.SaveCaseInfo()
                    Init.InitAllDBFileNames()
                                        
                    #Globals.MACFileName = os.path.join(Globals.CasePath, self.Case.DisplayName + Constants.MACExtension)
                    #setup all the required database
                    #DBFunctions.SetupFileInfoDB(Globals.MACFileName)
                    #Globals.KeywordsFileName = os.path.join(Globals.CasePath, self.Case.DisplayName + Constants.KeywordsExtension)
                    #DBFunctions.SetupKeywordsTable(Globals.KeywordsFileName, True)
                    #Globals.TextCatFileName = os.path.join(Globals.CasePath, self.Case.DisplayName + Constants.TextCatExtension)
                    #DBFunctions.SetupStopwordsTable(Globals.TextCatFileName, True)
                    Init.InitDatabases()
                    
                    Globals.frmGlobalMainForm.ShowCaseProperties(True)
                    Globals.CaseOpen = True
                    self.Close()
            finally:
                dlg.Destroy()
        else:   
            Init.InitAllDBFileNames()
            self.SaveCaseInfo()
            self.Close()

    def OnBtnCancelButton(self, event):
        self.Close()

    def OnChoiceSourceTypeChoice(self, event):
        if self.choiceSourceType.GetStringSelection() == "Logical Drive":
            if not hasattr(self, "IDLogicalDriveSource"):
                #logicalSources = []
                self.IDLogicalDriveSource = wx.NewId()
                self.choiceSource = wx.Choice(choices=Win32RawIO.GetWin32LogicalDrivesForDisplay(),
                  id=self.IDLogicalDriveSource, name='choiceSource',
                  parent=self.panEvidence, pos=wx.Point(24, 112), size=wx.Size(192,
                  21), style=0)
                self.choiceSource.SetSelection(0)
                
        event.Skip()

    def OnBtnAddDestinationButton(self, event):
        dlg = wx.FileDialog(self, "Save Image File As", ".", "", "All files (*.*)|*.*", wx.SAVE)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                self.imageFileName = dlg.GetPath()
                listItem = [self.imageFileName]
                self.lstDestinations.Append(listItem)
            else:
                return False
        
        finally:
            dlg.Destroy()
        event.Skip()

    def OnBtnEditDestinationButton(self, event):
        event.Skip()


    
