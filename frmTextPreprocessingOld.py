#Boa:Frame:frmTextPreprocessing

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


def create(parent):
    return frmTextPreprocessing(parent)

[wxID_FRMTEXTPREPROCESSING, wxID_FRMTEXTPREPROCESSINGBTNCLOSE, 
 wxID_FRMTEXTPREPROCESSINGBTNPREPROCESS, wxID_FRMTEXTPREPROCESSINGBTNSAVE, 
 wxID_FRMTEXTPREPROCESSINGBTNSELECTFOLDER, 
 wxID_FRMTEXTPREPROCESSINGBTNSTOPWORDS, 
 wxID_FRMTEXTPREPROCESSINGCHOICESTEMMERS, 
 wxID_FRMTEXTPREPROCESSINGPANCATEGORYVIEW, 
 wxID_FRMTEXTPREPROCESSINGPANDIRVIEW, 
 wxID_FRMTEXTPREPROCESSINGPANTEXTPREPROCESSING, 
 wxID_FRMTEXTPREPROCESSINGSPLITTERWINDOW1, 
 wxID_FRMTEXTPREPROCESSINGSTATICTEXT1, wxID_FRMTEXTPREPROCESSINGSTATICTEXT3, 
 wxID_FRMTEXTPREPROCESSINGSTATICTEXT4, wxID_FRMTEXTPREPROCESSINGSTATICTEXT5, 
 wxID_FRMTEXTPREPROCESSINGSTATICTEXT6, wxID_FRMTEXTPREPROCESSINGSTATICTEXT7, 
 wxID_FRMTEXTPREPROCESSINGSTATICTEXT8, wxID_FRMTEXTPREPROCESSINGSTATICTEXT9, 
] = [wx.NewId() for _init_ctrls in range(19)]

class frmTextPreprocessing(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRMTEXTPREPROCESSING,
              name=u'frmTextPreprocessing', parent=prnt, pos=wx.Point(622, 176),
              size=wx.Size(795, 731), style=wx.DEFAULT_FRAME_STYLE,
              title=u'Text Preprocessing')
        self.SetClientSize(wx.Size(787, 700))
        self.SetWindowVariant(wx.WINDOW_VARIANT_MINI)
        self.SetCursor(wx.STANDARD_CURSOR)
        self.Center(wx.BOTH)
        self.SetIcon(wx.Icon('./Images/FNSFIcon.ico',wx.BITMAP_TYPE_ICO))
        self.SetBackgroundColour(wx.Colour(125, 152, 221))
        self.SetAutoLayout(True)

        self.panTextPreProcessing = wx.Panel(id=wxID_FRMTEXTPREPROCESSINGPANTEXTPREPROCESSING,
              name=u'panTextPreProcessing', parent=self, pos=wx.Point(16, 16),
              size=wx.Size(756, 628), style=wx.TAB_TRAVERSAL)
        self.panTextPreProcessing.SetBackgroundColour(wx.Colour(225, 236, 255))
        self.panTextPreProcessing.SetAutoLayout(False)
        self.panTextPreProcessing.SetConstraints(LayoutAnchors(self.panTextPreProcessing,
              True, True, True, True))
        self.panTextPreProcessing.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL,
              wx.NORMAL, False, u'Tahoma'))

        self.btnClose = wx.Button(id=wxID_FRMTEXTPREPROCESSINGBTNCLOSE,
              label='&Cancel', name='btnClose', parent=self, pos=wx.Point(545,
              660), size=wx.Size(96, 23), style=0)
        self.btnClose.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL, False,
              'Arial'))
        self.btnClose.SetConstraints(LayoutAnchors(self.btnClose, False, False,
              True, True))
        self.btnClose.Bind(wx.EVT_BUTTON, self.OnBtnCloseButton,
              id=wxID_FRMTEXTPREPROCESSINGBTNCLOSE)

        self.btnSave = wx.Button(id=wxID_FRMTEXTPREPROCESSINGBTNSAVE,
              label='&Save And Close', name='btnSave', parent=self,
              pos=wx.Point(653, 662), size=wx.Size(120, 23), style=0)
        self.btnSave.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL, False,
              'Arial'))
        self.btnSave.SetConstraints(LayoutAnchors(self.btnSave, False, False,
              True, True))
        self.btnSave.Bind(wx.EVT_BUTTON, self.OnBtnSaveButton,
              id=wxID_FRMTEXTPREPROCESSINGBTNSAVE)

        self.btnStopwords = wx.Button(id=wxID_FRMTEXTPREPROCESSINGBTNSTOPWORDS,
              label=u'Stopwords List...', name=u'btnStopwords',
              parent=self.panTextPreProcessing, pos=wx.Point(168, 48),
              size=wx.Size(120, 23), style=0)
        self.btnStopwords.Bind(wx.EVT_BUTTON, self.OnBtnStopwordsButton,
              id=wxID_FRMTEXTPREPROCESSINGBTNSTOPWORDS)

        self.choiceStemmers = wx.Choice(choices=[u'Porter Stemmer'],
              id=wxID_FRMTEXTPREPROCESSINGCHOICESTEMMERS,
              name=u'choiceStemmers', parent=self.panTextPreProcessing,
              pos=wx.Point(168, 80), size=wx.Size(120, 21), style=0)
        self.choiceStemmers.SetStringSelection(u'None')
        self.choiceStemmers.SetHelpText(u'')
        self.choiceStemmers.SetSelection(0)

        self.btnPreprocess = wx.Button(id=wxID_FRMTEXTPREPROCESSINGBTNPREPROCESS,
              label=u'Start Indexing', name=u'btnPreprocess',
              parent=self.panTextPreProcessing, pos=wx.Point(48, 591),
              size=wx.Size(128, 23), style=0)
        self.btnPreprocess.SetConstraints(LayoutAnchors(self.btnPreprocess,
              True, False, False, True))
        self.btnPreprocess.Bind(wx.EVT_BUTTON, self.OnBtnPreprocessButton,
              id=wxID_FRMTEXTPREPROCESSINGBTNPREPROCESS)

        self.staticText3 = wx.StaticText(id=wxID_FRMTEXTPREPROCESSINGSTATICTEXT3,
              label=u'3.', name='staticText3', parent=self.panTextPreProcessing,
              pos=wx.Point(16, 116), size=wx.Size(15, 19), style=0)
        self.staticText3.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'Tahoma'))

        self.staticText1 = wx.StaticText(id=wxID_FRMTEXTPREPROCESSINGSTATICTEXT1,
              label=u'Get Stopwords List:', name='staticText1',
              parent=self.panTextPreProcessing, pos=wx.Point(48, 56),
              size=wx.Size(94, 13), style=0)

        self.staticText4 = wx.StaticText(id=wxID_FRMTEXTPREPROCESSINGSTATICTEXT4,
              label=u'Text Preprocessing Steps:', name='staticText4',
              parent=self.panTextPreProcessing, pos=wx.Point(16, 16),
              size=wx.Size(213, 19), style=0)
        self.staticText4.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'Tahoma'))

        self.staticText5 = wx.StaticText(id=wxID_FRMTEXTPREPROCESSINGSTATICTEXT5,
              label=u'Select a Stemmer:', name='staticText5',
              parent=self.panTextPreProcessing, pos=wx.Point(48, 88),
              size=wx.Size(87, 13), style=0)

        self.staticText6 = wx.StaticText(id=wxID_FRMTEXTPREPROCESSINGSTATICTEXT6,
              label=u'1.', name='staticText6', parent=self.panTextPreProcessing,
              pos=wx.Point(16, 52), size=wx.Size(15, 19), style=0)
        self.staticText6.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'Tahoma'))

        self.staticText7 = wx.StaticText(id=wxID_FRMTEXTPREPROCESSINGSTATICTEXT7,
              label=u'Select Folders and  File Types to Index:',
              name='staticText7', parent=self.panTextPreProcessing,
              pos=wx.Point(48, 120), size=wx.Size(190, 13), style=0)

        self.staticText8 = wx.StaticText(id=wxID_FRMTEXTPREPROCESSINGSTATICTEXT8,
              label=u'4.', name='staticText8', parent=self.panTextPreProcessing,
              pos=wx.Point(16, 596), size=wx.Size(15, 19), style=0)
        self.staticText8.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'Tahoma'))
        self.staticText8.SetConstraints(LayoutAnchors(self.staticText8, True,
              False, False, True))

        self.staticText9 = wx.StaticText(id=wxID_FRMTEXTPREPROCESSINGSTATICTEXT9,
              label=u'2.', name='staticText9', parent=self.panTextPreProcessing,
              pos=wx.Point(16, 84), size=wx.Size(15, 19), style=0)
        self.staticText9.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'Tahoma'))

        self.splitterWindow1 = wx.SplitterWindow(id=wxID_FRMTEXTPREPROCESSINGSPLITTERWINDOW1,
              name='splitterWindow1', parent=self.panTextPreProcessing,
              pos=wx.Point(16, 144), size=wx.Size(720, 432), style=wx.SP_3D)
        self.splitterWindow1.SetMinimumPaneSize(20)
        self.splitterWindow1.SetConstraints(LayoutAnchors(self.splitterWindow1,
              True, True, True, True))
        self.splitterWindow1.SetBorderSize(2)

        self.panCategoryView = wx.Panel(id=wxID_FRMTEXTPREPROCESSINGPANCATEGORYVIEW,
              name=u'panCategoryView', parent=self.splitterWindow1,
              pos=wx.Point(368, 0), size=wx.Size(352, 432),
              style=wx.TAB_TRAVERSAL)
        self.panCategoryView.SetAutoLayout(True)

        self.panDirView = wx.Panel(id=wxID_FRMTEXTPREPROCESSINGPANDIRVIEW,
              name=u'panDirView', parent=self.splitterWindow1, pos=wx.Point(0,
              0), size=wx.Size(364, 432), style=wx.TAB_TRAVERSAL)
        self.panDirView.SetAutoLayout(True)
        self.splitterWindow1.SplitVertically(self.panDirView,
              self.panCategoryView, 364)

        self.btnSelectFolder = wx.Button(id=wxID_FRMTEXTPREPROCESSINGBTNSELECTFOLDER,
              label=u'Select A Folder', name=u'btnSelectFolder',
              parent=self.panTextPreProcessing, pos=wx.Point(256, 112),
              size=wx.Size(112, 23), style=0)
        self.btnSelectFolder.Bind(wx.EVT_BUTTON, self.OnBtnSelectFolderButton,
              id=wxID_FRMTEXTPREPROCESSINGBTNSELECTFOLDER)

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.DirList = ""
        self.CategoryList = ""
        self.LoadSettingsTable()
        self.InitDirCheckView()
        self.OneFolderList = []
        self.OneFolderSelected = False
        self.OneFolderPath = ""
        if len(Globals.Stopwords) == 0:
            self.ReadStopwordsFromDB()
        
    def InitDirCheckView(self):

        self.treeDirCheckView = DirectoryCheckView(self.panDirView, id=wx.NewId(), pos=wx.Point(0, 0),
              size=wx.Size(352, 432), CheckedList=Globals.TextCatDirList) 
        self.treeDirCheckView.SetConstraints(LayoutAnchors(self.treeDirCheckView,
              True, True, True, True))
              
        self.treeCategoryCheckView = FileCategoryCheckView(self.panCategoryView, id=wx.NewId(), pos=wx.Point(8, 0),
              size=wx.Size(344, 432), CheckedList=Globals.TextCatCategoryList) 
        self.treeCategoryCheckView.SetConstraints(LayoutAnchors(self.treeCategoryCheckView,
              True, True, True, True))
                  
        """
        self.treeCtrl1 = wx.TreeCtrl(id=wxID_FRMTEXTPREPROCESSINGTREECTRL1,
              name='treeCtrl1', parent=self.panDirView, pos=wx.Point(0, 0),
              size=wx.Size(352, 432), style=wx.TR_HAS_BUTTONS)

        self.treeCtrl2 = wx.TreeCtrl(id=wxID_FRMTEXTPREPROCESSINGTREECTRL2,
              name='treeCtrl2', parent=self.panCategoryView, pos=wx.Point(8, 0),
              size=wx.Size(344, 432), style=wx.TR_HAS_BUTTONS)
        """

        #self.keywordsRoot = self.treeDirCheckView.AddDirectoryTreeNodes()
        
    def OnBtnCloseButton(self, event):
        self.Destroy()

    def OnBtnSaveButton(self, event):
        self.UpdateSettings()
        if not self.CheckSettingsError():
            return
        
        self.Close()
    
    def ReadStopwordsFromDB(self):
        db = SqliteDatabase(Globals.TextCatFileName)
        if not db.OpenConnection():
            return
        
        query = "SELECT Stopword FROM " + Constants.StopwordsTable
        rows = db.FetchAllRows(query)
        #print len(rows)
        self.StopwordsValue = ""
        i = 0
        for row in rows:
            #print row[0]
            Globals.Stopwords.add(row[0])
            if i == 0:
                self.StopwordsValue += row[0]
            else:
                self.StopwordsValue += "; " + row[0]
            i += 1
            
        #print Globals.KeyWords
        db.CloseConnection()
        
    
    def CheckSettingsError(self):
        #Globals.TextCatDirList = []
        #self.treeDirCheckView.UpdateCheckedList(Globals.TextCatDirList)
        #Globals.TextCatCategoryList = []
        #self.treeCategoryCheckView.UpdateCheckedList(Globals.TextCatCategoryList)
        errMsg = ""
        """
        if len(Globals.Keywords) == 0:
            errMsg = "Please import keywords from a text file before start searching.\n File must have one keyword per line."
        """
        if len(Globals.TextCatDirList) == 0:
            errMsg = "Please select directories to get text for categorization."
        elif len(Globals.TextCatCategoryList) == 0:
            errMsg = "Please select file types / categories to read for text categorization."
        
        if not errMsg == "" :
            dlg = wx.MessageDialog(self, errMsg,
              'Error', wx.OK | wx.ICON_ERROR)
            try:
                dlg.ShowModal()
            finally:
                dlg.Destroy()
                return False
        else:
            return True
    
    def LoadSettingsTable(self):
        if len(Globals.TextCatDirList) == 0:
            db = SqliteDatabase(Globals.TextCatFileName)
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
            

    def UpdateSettings(self):
        Globals.TextCatCategoryList = []
        Globals.TextCatDirList = []
        self.DirList = ""
        self.CategoryList = ""
        self.treeCategoryCheckView.UpdateCheckedList(Globals.TextCatCategoryList)
        self.treeDirCheckView.UpdateCheckedList(Globals.TextCatDirList)
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
        
        db = SqliteDatabase(Globals.TextCatFileName)
        if not db.OpenConnection():
            return
        
        query = "delete from " + Constants.TextCatSettingsTable + ";"
        db.ExecuteNonQuery(query)
        
        query = "insert into " + Constants.TextCatSettingsTable + " (Stemmer, DirList, CategoryList) values ( + " 
        query += db.SqlSQuote(Globals.Stemmer) + "," + db.SqlSQuote(self.DirList) + ","
        query += db.SqlSQuote(self.CategoryList) + ")"
        db.ExecuteNonQuery(query)
        db.CloseConnection()
        
    def OnBtnStopwordsButton(self, event):
        import frmStopwords
        formStopwords = frmStopwords.create(self)
        formStopwords.Show()
        event.Skip()


    def OnBtnPreprocessButton(self, event):
        self.UpdateSettings()
        if not self.CheckSettingsError():
            return
        
        import dlgTextPreprocessingProgress
        textCat = dlgTextPreprocessingProgress.create(self)
        #scanMAC.StartScan(dir)
        textCat.ShowModal()
        self.Close()
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







