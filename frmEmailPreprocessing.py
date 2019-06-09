#-----------------------------------------------------------------------------
# Name:        frmEmailPreprocessing.py
# Purpose:     
#
# Author:      Ram B. Basnet
#
# Created:     2009/02/10
# RCS-ID:      $Id: frmEmailPreprocessing.py $
# Copyright:   (c) 2009
# Licence:     All Rights Reserved.
# New field:   Whatever
#-----------------------------------------------------------------------------
#Boa:Frame:frmEmailPreprocessing

import wx
import os
import wx.lib.buttons
from wx.lib.anchors import LayoutAnchors
#from MySqlDatabase import *
from SqliteDatabase import *
import Globals
import Constants

from DirectoryCheckView import *
from FileCategoryCheckView import *
import PlatformMethods
import CommonFunctions
import images

def create(parent):
    return frmEmailPreprocessing(parent)

[wxID_FRMEMAILPREPROCESSING, wxID_FRMEMAILPREPROCESSINGBTNBROWSEADDRESSBOOK, 
 wxID_FRMEMAILPREPROCESSINGBTNBROWSEATTACHMENTSPATH, 
 wxID_FRMEMAILPREPROCESSINGBTNBROWSEEMAILPATH, 
 wxID_FRMEMAILPREPROCESSINGBTNCLOSE, wxID_FRMEMAILPREPROCESSINGBTNSAVE, 
 wxID_FRMEMAILPREPROCESSINGBTNSTARTSCAN, 
 wxID_FRMEMAILPREPROCESSINGBTNSTOPWORDS, 
 wxID_FRMEMAILPREPROCESSINGCHKINDEXATTACHMENTS, 
 wxID_FRMEMAILPREPROCESSINGCHKINDEXMESSAGES, 
 wxID_FRMEMAILPREPROCESSINGCHOICESTEMMERS, 
 wxID_FRMEMAILPREPROCESSINGPANEMAILPREPROCESSING, 
 wxID_FRMEMAILPREPROCESSINGSTATICTEXT1, 
 wxID_FRMEMAILPREPROCESSINGSTATICTEXT10, 
 wxID_FRMEMAILPREPROCESSINGSTATICTEXT11, 
 wxID_FRMEMAILPREPROCESSINGSTATICTEXT12, 
 wxID_FRMEMAILPREPROCESSINGSTATICTEXT13, 
 wxID_FRMEMAILPREPROCESSINGSTATICTEXT14, 
 wxID_FRMEMAILPREPROCESSINGSTATICTEXT15, 
 wxID_FRMEMAILPREPROCESSINGSTATICTEXT2, wxID_FRMEMAILPREPROCESSINGSTATICTEXT3, 
 wxID_FRMEMAILPREPROCESSINGSTATICTEXT4, wxID_FRMEMAILPREPROCESSINGSTATICTEXT5, 
 wxID_FRMEMAILPREPROCESSINGSTATICTEXT6, wxID_FRMEMAILPREPROCESSINGSTATICTEXT7, 
 wxID_FRMEMAILPREPROCESSINGSTATICTEXT8, wxID_FRMEMAILPREPROCESSINGSTATICTEXT9, 
 wxID_FRMEMAILPREPROCESSINGTXTADDRESSBOOKPATH, 
 wxID_FRMEMAILPREPROCESSINGTXTATTACHMENTSPATH, 
 wxID_FRMEMAILPREPROCESSINGTXTEMAILSPATH, 
] = [wx.NewId() for _init_ctrls in range(30)]

class frmEmailPreprocessing(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRMEMAILPREPROCESSING,
              name='frmEmailPreprocessing', parent=prnt, pos=wx.Point(352, -17),
              size=wx.Size(699, 804), style=wx.DEFAULT_FRAME_STYLE,
              title='Email Preprocessing')
        self.SetClientSize(wx.Size(691, 770))
        self.SetWindowVariant(wx.WINDOW_VARIANT_MINI)
        self.SetCursor(wx.STANDARD_CURSOR)
        self.Center(wx.BOTH)
        self.SetBackgroundColour(wx.Colour(125, 152, 221))
        self.SetAutoLayout(True)

        self.panEmailPreProcessing = wx.Panel(id=wxID_FRMEMAILPREPROCESSINGPANEMAILPREPROCESSING,
              name='panEmailPreProcessing', parent=self, pos=wx.Point(16, 16),
              size=wx.Size(656, 700), style=wx.TAB_TRAVERSAL)
        self.panEmailPreProcessing.SetBackgroundColour(wx.Colour(225, 236, 255))
        self.panEmailPreProcessing.SetAutoLayout(False)
        self.panEmailPreProcessing.SetConstraints(LayoutAnchors(self.panEmailPreProcessing,
              True, True, True, True))
        self.panEmailPreProcessing.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL,
              wx.NORMAL, False, u'Tahoma'))

        self.btnClose = wx.Button(id=wxID_FRMEMAILPREPROCESSINGBTNCLOSE,
              label='&Cancel', name='btnClose', parent=self, pos=wx.Point(449,
              730), size=wx.Size(96, 23), style=0)
        self.btnClose.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL, False,
              'Arial'))
        self.btnClose.SetConstraints(LayoutAnchors(self.btnClose, False, False,
              True, True))
        self.btnClose.Bind(wx.EVT_BUTTON, self.OnBtnCloseButton,
              id=wxID_FRMEMAILPREPROCESSINGBTNCLOSE)

        self.btnSave = wx.Button(id=wxID_FRMEMAILPREPROCESSINGBTNSAVE,
              label='&Save And Close', name='btnSave', parent=self,
              pos=wx.Point(557, 732), size=wx.Size(120, 23), style=0)
        self.btnSave.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL, False,
              'Arial'))
        self.btnSave.SetConstraints(LayoutAnchors(self.btnSave, False, False,
              True, True))
        self.btnSave.Bind(wx.EVT_BUTTON, self.OnBtnSaveButton,
              id=wxID_FRMEMAILPREPROCESSINGBTNSAVE)

        self.staticText1 = wx.StaticText(id=wxID_FRMEMAILPREPROCESSINGSTATICTEXT1,
              label='Address Book Path:', name='staticText1',
              parent=self.panEmailPreProcessing, pos=wx.Point(48, 56),
              size=wx.Size(94, 13), style=0)

        self.staticText4 = wx.StaticText(id=wxID_FRMEMAILPREPROCESSINGSTATICTEXT4,
              label='Preprocess Emails and Attachments:', name='staticText4',
              parent=self.panEmailPreProcessing, pos=wx.Point(16, 16),
              size=wx.Size(297, 19), style=0)
        self.staticText4.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'Tahoma'))

        self.staticText5 = wx.StaticText(id=wxID_FRMEMAILPREPROCESSINGSTATICTEXT5,
              label=u'Select File Types To Index:', name='staticText5',
              parent=self.panEmailPreProcessing, pos=wx.Point(48, 200),
              size=wx.Size(80, 48), style=0)

        self.staticText6 = wx.StaticText(id=wxID_FRMEMAILPREPROCESSINGSTATICTEXT6,
              label=u'1.', name='staticText6',
              parent=self.panEmailPreProcessing, pos=wx.Point(16, 52),
              size=wx.Size(15, 19), style=0)
        self.staticText6.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'Tahoma'))

        self.staticText9 = wx.StaticText(id=wxID_FRMEMAILPREPROCESSINGSTATICTEXT9,
              label='5.', name='staticText9', parent=self.panEmailPreProcessing,
              pos=wx.Point(16, 588), size=wx.Size(15, 19), style=0)
        self.staticText9.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'Tahoma'))

        self.btnBrowseAddressBook = wx.Button(id=wxID_FRMEMAILPREPROCESSINGBTNBROWSEADDRESSBOOK,
              label='...', name='btnBrowseAddressBook',
              parent=self.panEmailPreProcessing, pos=wx.Point(600, 48),
              size=wx.Size(43, 23), style=0)
        self.btnBrowseAddressBook.Bind(wx.EVT_BUTTON,
              self.OnBtnBrowseAddressBookButton,
              id=wxID_FRMEMAILPREPROCESSINGBTNBROWSEADDRESSBOOK)

        self.staticText2 = wx.StaticText(id=wxID_FRMEMAILPREPROCESSINGSTATICTEXT2,
              label='4.', name='staticText2', parent=self.panEmailPreProcessing,
              pos=wx.Point(16, 196), size=wx.Size(15, 19), style=0)
        self.staticText2.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'Tahoma'))

        self.btnBrowseEmailPath = wx.Button(id=wxID_FRMEMAILPREPROCESSINGBTNBROWSEEMAILPATH,
              label='...', name='btnBrowseEmailPath',
              parent=self.panEmailPreProcessing, pos=wx.Point(600, 80),
              size=wx.Size(43, 23), style=0)
        self.btnBrowseEmailPath.Bind(wx.EVT_BUTTON,
              self.OnBtnBrowseEmailPathButton,
              id=wxID_FRMEMAILPREPROCESSINGBTNBROWSEEMAILPATH)

        self.staticText7 = wx.StaticText(id=wxID_FRMEMAILPREPROCESSINGSTATICTEXT7,
              label='6.', name='staticText7', parent=self.panEmailPreProcessing,
              pos=wx.Point(16, 620), size=wx.Size(15, 19), style=0)
        self.staticText7.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'Tahoma'))

        self.staticText3 = wx.StaticText(id=wxID_FRMEMAILPREPROCESSINGSTATICTEXT3,
              label='Messages Path:', name='staticText3',
              parent=self.panEmailPreProcessing, pos=wx.Point(48, 88),
              size=wx.Size(76, 13), style=0)

        self.btnBrowseAttachmentsPath = wx.Button(id=wxID_FRMEMAILPREPROCESSINGBTNBROWSEATTACHMENTSPATH,
              label='...', name='btnBrowseAttachmentsPath',
              parent=self.panEmailPreProcessing, pos=wx.Point(600, 136),
              size=wx.Size(43, 23), style=0)
        self.btnBrowseAttachmentsPath.Bind(wx.EVT_BUTTON,
              self.OnBtnBrowseAttachmentsPathButton,
              id=wxID_FRMEMAILPREPROCESSINGBTNBROWSEATTACHMENTSPATH)

        self.staticText8 = wx.StaticText(id=wxID_FRMEMAILPREPROCESSINGSTATICTEXT8,
              label='7.', name='staticText8', parent=self.panEmailPreProcessing,
              pos=wx.Point(16, 660), size=wx.Size(15, 19), style=0)
        self.staticText8.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'Tahoma'))

        self.staticText11 = wx.StaticText(id=wxID_FRMEMAILPREPROCESSINGSTATICTEXT11,
              label='3.', name='staticText11',
              parent=self.panEmailPreProcessing, pos=wx.Point(16, 140),
              size=wx.Size(15, 19), style=0)
        self.staticText11.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'Tahoma'))

        self.staticText10 = wx.StaticText(id=wxID_FRMEMAILPREPROCESSINGSTATICTEXT10,
              label='Attachments Path:', name='staticText10',
              parent=self.panEmailPreProcessing, pos=wx.Point(48, 144),
              size=wx.Size(90, 13), style=0)

        self.staticText12 = wx.StaticText(id=wxID_FRMEMAILPREPROCESSINGSTATICTEXT12,
              label='Get Stopwords List:', name='staticText12',
              parent=self.panEmailPreProcessing, pos=wx.Point(40, 592),
              size=wx.Size(94, 13), style=0)

        self.staticText13 = wx.StaticText(id=wxID_FRMEMAILPREPROCESSINGSTATICTEXT13,
              label=u'2.', name='staticText13',
              parent=self.panEmailPreProcessing, pos=wx.Point(16, 84),
              size=wx.Size(15, 19), style=0)
        self.staticText13.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'Tahoma'))

        self.txtAddressBookPath = wx.TextCtrl(id=wxID_FRMEMAILPREPROCESSINGTXTADDRESSBOOKPATH,
              name='txtAddressBookPath', parent=self.panEmailPreProcessing,
              pos=wx.Point(152, 48), size=wx.Size(432, 21), style=0, value='')

        self.txtEmailsPath = wx.TextCtrl(id=wxID_FRMEMAILPREPROCESSINGTXTEMAILSPATH,
              name='txtEmailsPath', parent=self.panEmailPreProcessing,
              pos=wx.Point(152, 80), size=wx.Size(432, 21), style=0, value='')

        self.txtAttachmentsPath = wx.TextCtrl(id=wxID_FRMEMAILPREPROCESSINGTXTATTACHMENTSPATH,
              name='txtAttachmentsPath', parent=self.panEmailPreProcessing,
              pos=wx.Point(152, 136), size=wx.Size(432, 21), style=0, value='')

        self.btnStopwords = wx.Button(id=wxID_FRMEMAILPREPROCESSINGBTNSTOPWORDS,
              label='Stopwords List...', name='btnStopwords',
              parent=self.panEmailPreProcessing, pos=wx.Point(152, 584),
              size=wx.Size(208, 23), style=0)
        self.btnStopwords.Bind(wx.EVT_BUTTON, self.OnBtnStopwordsButton,
              id=wxID_FRMEMAILPREPROCESSINGBTNSTOPWORDS)

        self.choiceStemmers = wx.Choice(choices=[u'None - Do not Stem Words',
              u'Porter Stemmer'], id=wxID_FRMEMAILPREPROCESSINGCHOICESTEMMERS,
              name=u'choiceStemmers', parent=self.panEmailPreProcessing,
              pos=wx.Point(152, 616), size=wx.Size(208, 21), style=0)
        self.choiceStemmers.SetStringSelection(u'None')
        self.choiceStemmers.SetHelpText(u'')
        self.choiceStemmers.SetSelection(0)
        self.choiceStemmers.SetLabel('')

        self.btnStartScan = wx.Button(id=wxID_FRMEMAILPREPROCESSINGBTNSTARTSCAN,
              label='Start Preprocessing', name='btnStartScan',
              parent=self.panEmailPreProcessing, pos=wx.Point(152, 656),
              size=wx.Size(208, 23), style=0)
        self.btnStartScan.Bind(wx.EVT_BUTTON, self.OnBtnStartScanButton,
              id=wxID_FRMEMAILPREPROCESSINGBTNSTARTSCAN)

        self.staticText14 = wx.StaticText(id=wxID_FRMEMAILPREPROCESSINGSTATICTEXT14,
              label=u'Finally:', name='staticText14',
              parent=self.panEmailPreProcessing, pos=wx.Point(40, 664),
              size=wx.Size(34, 13), style=0)

        self.staticText15 = wx.StaticText(id=wxID_FRMEMAILPREPROCESSINGSTATICTEXT15,
              label=u'Select a Stemmer:', name='staticText15',
              parent=self.panEmailPreProcessing, pos=wx.Point(40, 624),
              size=wx.Size(87, 13), style=0)

        self.chkIndexMessages = wx.CheckBox(id=wxID_FRMEMAILPREPROCESSINGCHKINDEXMESSAGES,
              label=u'Index Messages for quick searching',
              name=u'chkIndexMessages', parent=self.panEmailPreProcessing,
              pos=wx.Point(152, 112), size=wx.Size(216, 13), style=0)
        self.chkIndexMessages.SetValue(True)
        self.chkIndexMessages.Bind(wx.EVT_CHECKBOX,
              self.OnChkIndexMessagesCheckbox,
              id=wxID_FRMEMAILPREPROCESSINGCHKINDEXMESSAGES)

        self.chkIndexAttachments = wx.CheckBox(id=wxID_FRMEMAILPREPROCESSINGCHKINDEXATTACHMENTS,
              label=u'Index Attachments for quick searching',
              name=u'chkIndexAttachments', parent=self.panEmailPreProcessing,
              pos=wx.Point(152, 168), size=wx.Size(216, 13), style=0)
        self.chkIndexAttachments.SetValue(True)
        self.chkIndexAttachments.Bind(wx.EVT_CHECKBOX,
              self.OnChkIndexAttachmentsCheckbox,
              id=wxID_FRMEMAILPREPROCESSINGCHKINDEXATTACHMENTS)

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.SetIcon(images.getMAKE2Icon())
        self.InitCategoryCheckView()
        if len(Globals.EmailsStopwords) == 0:
            try:
                self.ReadStopwordsFromDB()
            except:
                pass
        
    def OnBtnCloseButton(self, event):
        self.Destroy()

    def OnBtnSaveButton(self, event):
        event.Skip()
        
        self.UpdateSettings()
        if not self.CheckSettingsError():
            return
        
        self.Close()
    
       
    def ReadStopwordsFromDB(self):
        db = SqliteDatabase(Globals.EmailsFileName)
        if not db.OpenConnection():
            return
        
        query = "SELECT Stopword FROM %s"%Constants.StopwordsTable
        rows = db.FetchAllRows(query)
        #print len(rows)
        for row in rows:
            #print row[0]
            Globals.EmailsStopwords.add(row[0])
            
        #print Globals.KeyWords
        db.CloseConnection()
        
    def InitCategoryCheckView(self):
        #if not Globals.MimeTypesSet:
            # Populate the Known MIME types list with what is in the database
        try:
            mtypes = wx.TheMimeTypesManager.EnumAllFileTypes()
        except wx.PyAssertionError:
            mtypes = []
        
        # TODO: On wxMac, EnumAllFileTypes produces tons of dupes, which
        # causes quirky behavior because the list control doesn't expect
        # dupes, and simply wastes space. So remove the dupes for now,
        # then remove this hack when we fix EnumAllFileTypes on Mac.
        
        #mimes = set(mtypes)
        mimes = set()
        for mime in mtypes:
            if not mime.startswith('image') and not mime.startswith('audio') and not mime.startswith('video'):
                mimes.add(mime)
        
        """
        mimes = {}
        for mt in mtypes:
            category = mt.lower().split("/")
            #print category
            if mimes.has_key(category[0]):
                if len(category) >= 2:
                    if category[1] not in mimes[category[0]]:
                        mimes[category[0]].append(category[1])
            else:
                if len(category) >= 2:
                    mimes[category[0]] = [category[1]]
                else:
                    mimes[category[0]] = []
        """           
                  
        """
        self.listCtrl1 = wx.ListCtrl(id=wxID_FRMEMAILPREPROCESSINGLISTCTRL1,
              name='listCtrl1', parent=self.panEmailPreProcessing,
              pos=wx.Point(152, 200), size=wx.Size(432, 368), style=wx.LC_ICON)
              
        """  
        self.treeCategoryCheckView = FileCategoryCheckView(self.panEmailPreProcessing, MimeTypeSet=mimes, id=wx.NewId(), pos=wx.Point(152, 200), size=wx.Size(432, 368),
            CheckedList=Globals.AttachmentsCheckedMimes)
            
        self.treeCategoryCheckView.SetConstraints(LayoutAnchors(self.treeCategoryCheckView,
              True, True, True, True))
    
    def CheckSettingsError(self):
        #Globals.TextCatDirList = []
        #self.treeDirCheckView.UpdateCheckedList(Globals.TextCatDirList)
        #Globals.TextCatCategoryList = []
        self.treeCategoryCheckView.UpdateCheckedList(Globals.AttachmentsCheckedMimes)
        errMsg = ""
        """
        if len(Globals.Keywords) == 0:
            errMsg = "Please import keywords from a text file before start searching.\n File must have one keyword per line."
        """
        #if len(self.txtAddressBookPath.GetValue()) == 0:
        #    errMsg = "Please enter or browse to the directory path where address book is present."
        if len(self.txtEmailsPath.GetValue()) == 0:
            errMsg = "Please enter or browse to the directory path where email files are present."
            CommonFunctions.ShowErrorMessage(self, errMsg, True)
            return False
        else:
            return True
        
    
    """
    def LoadSettingsTable(self):
        if len(Globals.TextCatDirList) == 0:
            db = SqliteDatabase(Globals.EmailsFileName)
            if not db.OpenConnection():
                return
            query = "select Stemmer, DirList, CategoryList from " + Constants.TextCatSettingsTable
            rows = db.FetchAllRows(query)
            for row in rows:
                Globals.Stemmer = row[0]
                self.DirList = CommonFunctions.RemoveDoubleSlashes(row[1])
                self.CategoryList = row[2]
            
            Globals.TextCatCategoryList = self.CategoryList.split(';')
            Globals.TextCatDirList = self.DirList.split(';')
            
        self.choiceStemmers.SetStringSelection(Globals.Stemmer)
        #print Globals.TextCatCategoryList
        #print Globals.TextCatDirList
        """   

    def UpdateSettings(self):
        Globals.TextCatCategoryList = []
        Globals.TextCatDirList = []
        self.DirList = ""
        self.CategoryList = ""
        self.treeCategoryCheckView.UpdateCheckedList(Globals.TextCatCategoryList)
        #self.treeDirCheckView.UpdateCheckedList(Globals.TextCatDirList)
        #UpdateTextCatDirList
        #if self.OneFolderSelected:
        if self.OneFolderSelected:
            for adir in self.OneFolderList:
                self.DirList += adir
                Globals.TextCatDirList.append(adir)
                
        """
        if self.OneFolderPath:
            Globals.TextCatDirList.append(self.OneFolderPath)
        """
        
        
        Globals.Stemmer = self.choiceStemmers.GetStringSelection()
                    
        for adir in Globals.TextCatDirList:
            if not self.DirList == "":
                self.DirList += ";"
            self.DirList += adir
            
        for cat in  Globals.TextCatCategoryList:
            if not self.CategoryList == "":
                self.CategoryList += ";"
            self.CategoryList += cat
        
        db = SqliteDatabase(Globals.EmailsFileName)
        if not db.OpenConnection():
            return
        
        query = "delete from %s;"%Constants.TextCatSettingsTable
        db.ExecuteNonQuery(query)
        
        query = "insert into " + Constants.TextCatSettingsTable + " (Stemmer, DirList, CategoryList) values (?,?,?)" 
        #query += db.SqlSQuote(Globals.Stemmer) + "," + db.SqlSQuote(self.DirList) + ","
        #query += db.SqlSQuote(self.CategoryList) + ")"
        db.ExecuteNonQuery(query, [(Globals.Stemmer, PlatformMethods.Encode(self.DirList), self.CategoryList)])
        db.CloseConnection()
        
    def OnBtnStopwordsButton(self, event):
        import frmStopwords
        formStopwords = frmStopwords.create(self, IsEmail=True, Stopwords=Globals.EmailsStopwords)
        #formStopwords = frmStopwords.create(self, IsEmail=True)
        formStopwords.Show()
        event.Skip()


    def OnBtnSelectFolderButton(self, event):
        self.OneFolderList = []
        dlg = wx.DirDialog(self)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                dirPath = dlg.GetPath()
                self.OneFolderSelected = True
                #self.OneFolderPath = dir
                for root, dirs, files in os.walk(dirPath):
                    for adir in dirs:
                        self.OneFolderList.append(os.path.join(root, adir))
                """
                for dir in self.OneFolderList:
                    print dir
                """
        finally:
            dlg.Destroy()
        
        event.Skip()

    def OnBtnBrowseAddressBookButton(self, event):
        dlg = wx.DirDialog(self)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                dirPath = dlg.GetPath()
                #self.OneFolderPath = dir
                self.txtAddressBookPath.SetValue(dirPath)
                
        finally:
            dlg.Destroy()
        event.Skip()

    def OnBtnStartScanButton(self, event):
        if not self.CheckSettingsError():
            return
        
        import dlgEmailPreprocessingProgress
        
        emailProcess = dlgEmailPreprocessingProgress.create(self, self.txtAddressBookPath.GetValue(), self.txtEmailsPath.GetValue(), self.txtAttachmentsPath.GetValue(), Globals.AttachmentsCheckedMimes, self.chkIndexMessages.GetValue(), self.chkIndexAttachments.GetValue())
        #scanMAC.StartScan(dir)
        emailProcess.ShowModal()
        #emailProcess.scanThread.Start()
        self.Close()
        event.Skip()

    def OnBtnBrowseEmailPathButton(self, event):
        dlg = wx.DirDialog(self)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                dirPath = dlg.GetPath()
                #self.OneFolderPath = dir
                self.txtEmailsPath.SetValue(dirPath)
                
        finally:
            dlg.Destroy()
        event.Skip()

    def OnBtnBrowseAttachmentsPathButton(self, event):
        dlg = wx.DirDialog(self)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                dirPath = dlg.GetPath()
                #self.OneFolderPath = dir
                self.txtAttachmentsPath.SetValue(dirPath)
                
        finally:
            dlg.Destroy()
        event.Skip()

    def OnChkIndexMessagesCheckbox(self, event):
        event.Skip()

    def OnChkIndexAttachmentsCheckbox(self, event):
        self.treeCategoryCheckView.Enable(self.chkIndexAttachments.GetValue())
        event.Skip()







