#-----------------------------------------------------------------------------
# Name:        frmCustomizeSearch.py
# Purpose:     
#
# Author:      Ram Basnet
#
# Created:     2008/06/30
# Last Modified: 06/30/2009
# RCS-ID:      $Id: frmCustomizeSearch.py $
# Copyright:   (c) 2006
# Licence:     All Rights Reserved.
# New field:   Whatever
#-----------------------------------------------------------------------------
#Boa:Frame:frmCustomizeKeywordSearch

import wx, re
from wx.lib.anchors import LayoutAnchors
#from MySqlDatabase import *
from SqliteDatabase import *
import Globals
import Constants
from DirectoryCheckView import *
from FileCategoryCheckView import *
import CommonFunctions
import DBFunctions
import images



def create(parent):
    return frmCustomizeKeywordSearch(parent)

[wxID_FRMCUSTOMIZEKEYWORDSEARCH, wxID_FRMCUSTOMIZEKEYWORDSEARCHBTNBROWSE, 
 wxID_FRMCUSTOMIZEKEYWORDSEARCHBTNCLOSE, 
 wxID_FRMCUSTOMIZEKEYWORDSEARCHBTNSAVE, 
 wxID_FRMCUSTOMIZEKEYWORDSEARCHBTNSELECTFOLDER, 
 wxID_FRMCUSTOMIZEKEYWORDSEARCHBTNSTARTSEARCH, 
 wxID_FRMCUSTOMIZEKEYWORDSEARCHCHKCASEINSENSITIVE, 
 wxID_FRMCUSTOMIZEKEYWORDSEARCHCHKCASESENSITIVE, 
 wxID_FRMCUSTOMIZEKEYWORDSEARCHLBLKEYWORDS, 
 wxID_FRMCUSTOMIZEKEYWORDSEARCHNOTEBOOKCUSTOMIZE, 
 wxID_FRMCUSTOMIZEKEYWORDSEARCHPANCATEGORYVIEW, 
 wxID_FRMCUSTOMIZEKEYWORDSEARCHPANCUSTOMIZE, 
 wxID_FRMCUSTOMIZEKEYWORDSEARCHPANDIRVIEW, 
 wxID_FRMCUSTOMIZEKEYWORDSEARCHPANKEYWORDS, 
 wxID_FRMCUSTOMIZEKEYWORDSEARCHPANSTRINGMATCHING, 
 wxID_FRMCUSTOMIZEKEYWORDSEARCHSTATICTEXT1, 
 wxID_FRMCUSTOMIZEKEYWORDSEARCHSTATICTEXT2, 
 wxID_FRMCUSTOMIZEKEYWORDSEARCHSTATICTEXT3, 
 wxID_FRMCUSTOMIZEKEYWORDSEARCHSTATICTEXT4, 
 wxID_FRMCUSTOMIZEKEYWORDSEARCHSTATICTEXT5, 
 wxID_FRMCUSTOMIZEKEYWORDSEARCHTXTFILENAME, 
 wxID_FRMCUSTOMIZEKEYWORDSEARCHTXTKEYWORDS, 
 wxID_FRMCUSTOMIZEKEYWORDSEARCHTXTPATH, 
] = [wx.NewId() for _init_ctrls in range(23)]

class frmCustomizeKeywordSearch(wx.Frame):
    def _init_coll_notebookCustomize_Pages(self, parent):
        # generated method, don't edit

        parent.AddPage(imageId=-1, page=self.panStringMatching, select=False,
              text=u'String Matching')
        parent.AddPage(imageId=-1, page=self.panKeywords, select=False,
              text=u'Keywords')
        parent.AddPage(imageId=-1, page=self.panDirView, select=True,
              text=u'Select Directory')
        parent.AddPage(imageId=-1, page=self.panCategoryView, select=False,
              text=u'Select File Types')

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRMCUSTOMIZEKEYWORDSEARCH,
              name=u'frmCustomizeKeywordSearch', parent=prnt, pos=wx.Point(428,
              61), size=wx.Size(720, 665), style=wx.DEFAULT_FRAME_STYLE,
              title=u'Customized Keyword Search')
        self.SetClientSize(wx.Size(712, 631))
        self.SetWindowVariant(wx.WINDOW_VARIANT_MINI)
        self.SetCursor(wx.STANDARD_CURSOR)
        self.Center(wx.BOTH)
        self.SetBackgroundColour(wx.Colour(125, 152, 221))
        self.SetAutoLayout(True)
        self.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL, False,
              u'MS Shell Dlg 2'))

        self.panCustomize = wx.Panel(id=wxID_FRMCUSTOMIZEKEYWORDSEARCHPANCUSTOMIZE,
              name=u'panCustomize', parent=self, pos=wx.Point(16, 16),
              size=wx.Size(678, 559), style=wx.TAB_TRAVERSAL)
        self.panCustomize.SetBackgroundColour(wx.Colour(225, 236, 255))
        self.panCustomize.SetAutoLayout(False)
        self.panCustomize.SetConstraints(LayoutAnchors(self.panCustomize, True,
              True, True, True))
        self.panCustomize.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, u'Tahoma'))

        self.staticText1 = wx.StaticText(id=wxID_FRMCUSTOMIZEKEYWORDSEARCHSTATICTEXT1,
              label=u'Customized Keyword Search', name='staticText1',
              parent=self.panCustomize, pos=wx.Point(16, 16), size=wx.Size(231,
              19), style=wx.ALIGN_CENTRE)
        self.staticText1.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, 'Tahoma'))
        self.staticText1.SetForegroundColour(wx.Colour(0, 0, 255))

        self.btnClose = wx.Button(id=wxID_FRMCUSTOMIZEKEYWORDSEARCHBTNCLOSE,
              label='&Cancel', name='btnClose', parent=self, pos=wx.Point(454,
              591), size=wx.Size(96, 23), style=0)
        self.btnClose.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL, False,
              'Arial'))
        self.btnClose.SetConstraints(LayoutAnchors(self.btnClose, False, False,
              True, True))
        self.btnClose.Bind(wx.EVT_BUTTON, self.OnBtnCloseButton,
              id=wxID_FRMCUSTOMIZEKEYWORDSEARCHBTNCLOSE)

        self.btnSave = wx.Button(id=wxID_FRMCUSTOMIZEKEYWORDSEARCHBTNSAVE,
              label='&Save And Close', name='btnSave', parent=self,
              pos=wx.Point(570, 593), size=wx.Size(120, 23), style=0)
        self.btnSave.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL, False,
              'Arial'))
        self.btnSave.SetConstraints(LayoutAnchors(self.btnSave, False, False,
              True, True))
        self.btnSave.Bind(wx.EVT_BUTTON, self.OnBtnSaveButton,
              id=wxID_FRMCUSTOMIZEKEYWORDSEARCHBTNSAVE)

        self.btnStartSearch = wx.Button(id=wxID_FRMCUSTOMIZEKEYWORDSEARCHBTNSTARTSEARCH,
              label=u'Start Search...', name=u'btnStartSearch',
              parent=self.panCustomize, pos=wx.Point(16, 518), size=wx.Size(192,
              24), style=0)
        self.btnStartSearch.SetConstraints(LayoutAnchors(self.btnStartSearch,
              True, False, False, True))
        self.btnStartSearch.Bind(wx.EVT_BUTTON, self.OnBtnStartSearchButton,
              id=wxID_FRMCUSTOMIZEKEYWORDSEARCHBTNSTARTSEARCH)

        self.notebookCustomize = wx.Notebook(id=wxID_FRMCUSTOMIZEKEYWORDSEARCHNOTEBOOKCUSTOMIZE,
              name=u'notebookCustomize', parent=self.panCustomize,
              pos=wx.Point(16, 48), size=wx.Size(646, 456), style=0)
        self.notebookCustomize.SetConstraints(LayoutAnchors(self.notebookCustomize,
              True, True, True, True))

        self.panStringMatching = wx.Panel(id=wxID_FRMCUSTOMIZEKEYWORDSEARCHPANSTRINGMATCHING,
              name=u'panStringMatching', parent=self.notebookCustomize,
              pos=wx.Point(0, 0), size=wx.Size(638, 430),
              style=wx.TAB_TRAVERSAL)
        self.panStringMatching.SetAutoLayout(True)

        self.chkCaseInsensitive = wx.CheckBox(id=wxID_FRMCUSTOMIZEKEYWORDSEARCHCHKCASEINSENSITIVE,
              label=u'Case Insensitive', name=u'chkCaseInsensitive',
              parent=self.panStringMatching, pos=wx.Point(16, 24),
              size=wx.Size(128, 13), style=0)
        self.chkCaseInsensitive.SetValue(True)
        self.chkCaseInsensitive.Enable(False)

        self.chkCaseSensitive = wx.CheckBox(id=wxID_FRMCUSTOMIZEKEYWORDSEARCHCHKCASESENSITIVE,
              label=u'Case Sensitive', name=u'chkCaseSensitive',
              parent=self.panStringMatching, pos=wx.Point(16, 56),
              size=wx.Size(120, 13), style=0)
        self.chkCaseSensitive.SetValue(False)
        self.chkCaseSensitive.Enable(False)
        self.chkCaseSensitive.SetToolTipString(u'chkCaseSensitive')

        self.panKeywords = wx.Panel(id=wxID_FRMCUSTOMIZEKEYWORDSEARCHPANKEYWORDS,
              name=u'panKeywords', parent=self.notebookCustomize,
              pos=wx.Point(0, 0), size=wx.Size(638, 430),
              style=wx.TAB_TRAVERSAL)
        self.panKeywords.SetAutoLayout(True)

        self.panDirView = wx.Panel(id=wxID_FRMCUSTOMIZEKEYWORDSEARCHPANDIRVIEW,
              name=u'panDirView', parent=self.notebookCustomize, pos=wx.Point(0,
              0), size=wx.Size(638, 430), style=wx.TAB_TRAVERSAL)
        self.panDirView.SetAutoLayout(True)

        self.panCategoryView = wx.Panel(id=wxID_FRMCUSTOMIZEKEYWORDSEARCHPANCATEGORYVIEW,
              name=u'panCategoryView', parent=self.notebookCustomize,
              pos=wx.Point(0, 0), size=wx.Size(638, 430),
              style=wx.TAB_TRAVERSAL)
        self.panCategoryView.SetAutoLayout(True)

        self.staticText2 = wx.StaticText(id=wxID_FRMCUSTOMIZEKEYWORDSEARCHSTATICTEXT2,
              label=u'Select the File Types/Categories in which you want to search for Keywords:',
              name='staticText2', parent=self.panCategoryView, pos=wx.Point(8,
              8), size=wx.Size(363, 13), style=0)

        self.staticText3 = wx.StaticText(id=wxID_FRMCUSTOMIZEKEYWORDSEARCHSTATICTEXT3,
              label=u'Select a Path to search recursivley:', name='staticText3',
              parent=self.panDirView, pos=wx.Point(8, 8), size=wx.Size(170, 13),
              style=0)

        self.txtKeywords = wx.TextCtrl(id=wxID_FRMCUSTOMIZEKEYWORDSEARCHTXTKEYWORDS,
              name=u'txtKeywords', parent=self.panKeywords, pos=wx.Point(8, 96),
              size=wx.Size(624, 328),
              style=wx.TE_LINEWRAP | wx.TE_MULTILINE | wx.TE_READONLY | wx.VSCROLL,
              value=u'')
        self.txtKeywords.SetConstraints(LayoutAnchors(self.txtKeywords, True,
              True, True, True))

        self.lblKeywords = wx.StaticText(id=wxID_FRMCUSTOMIZEKEYWORDSEARCHLBLKEYWORDS,
              label='Keywords found in database:', name=u'lblKeywords',
              parent=self.panKeywords, pos=wx.Point(16, 72), size=wx.Size(190,
              16), style=0)
        self.lblKeywords.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'Tahoma'))
        self.lblKeywords.SetForegroundColour(wx.Colour(0, 0, 255))

        self.txtFileName = wx.TextCtrl(id=wxID_FRMCUSTOMIZEKEYWORDSEARCHTXTFILENAME,
              name=u'txtFileName', parent=self.panKeywords, pos=wx.Point(112,
              32), size=wx.Size(440, 21), style=wx.TE_READONLY, value=u'')
        self.txtFileName.SetConstraints(LayoutAnchors(self.txtFileName, True,
              True, True, False))

        self.staticText4 = wx.StaticText(id=wxID_FRMCUSTOMIZEKEYWORDSEARCHSTATICTEXT4,
              label='Keywords Text File:', name='staticText4',
              parent=self.panKeywords, pos=wx.Point(8, 32), size=wx.Size(95,
              13), style=0)
        self.staticText4.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, u'Tahoma'))

        self.btnBrowse = wx.Button(id=wxID_FRMCUSTOMIZEKEYWORDSEARCHBTNBROWSE,
              label=u'Browse...', name=u'btnBrowse', parent=self.panKeywords,
              pos=wx.Point(568, 32), size=wx.Size(59, 23), style=0)
        self.btnBrowse.SetConstraints(LayoutAnchors(self.btnBrowse, False, True,
              True, False))
        self.btnBrowse.Bind(wx.EVT_BUTTON, self.OnBtnBrowseButton,
              id=wxID_FRMCUSTOMIZEKEYWORDSEARCHBTNBROWSE)

        self.staticText5 = wx.StaticText(id=wxID_FRMCUSTOMIZEKEYWORDSEARCHSTATICTEXT5,
              label=u'Keywords List:', name='staticText5',
              parent=self.panKeywords, pos=wx.Point(8, 8), size=wx.Size(70, 13),
              style=0)

        self.btnSelectFolder = wx.Button(id=wxID_FRMCUSTOMIZEKEYWORDSEARCHBTNSELECTFOLDER,
              label='...', name=u'btnSelectFolder', parent=self.panDirView,
              pos=wx.Point(392, 32), size=wx.Size(32, 23), style=0)
        self.btnSelectFolder.Enable(False)
        self.btnSelectFolder.Bind(wx.EVT_BUTTON, self.OnBtnSelectFolderButton,
              id=wxID_FRMCUSTOMIZEKEYWORDSEARCHBTNSELECTFOLDER)

        self.txtPath = wx.TextCtrl(id=wxID_FRMCUSTOMIZEKEYWORDSEARCHTXTPATH,
              name='txtPath', parent=self.panDirView, pos=wx.Point(8, 32),
              size=wx.Size(368, 21), style=0, value='')
        self.txtPath.Enable(False)

        self._init_coll_notebookCustomize_Pages(self.notebookCustomize)

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.SetIcon(images.getMAKE2Icon())
        self.FileName = ""
        self.Keywords = set([])
        self.KeywordsValue = ""
        self.DirPath = ""
        self.CategoryList = ""
        #self.KeywordsFromDB = True
        self.LoadSettingsTable()
        #DBFunctions.CreateKeywordsFrequencyTable(Globals.KeywordsFileName, False)
        """
        if len(Globals.Keywords) == 0:
            self.ReadKeyWordsFromDatabase()
        else:
            self.MakeKeywordsList()
            
        if self.KeywordsFromDB:
            self.lblKeywords.SetLabel("Keywords found in Project database:")
        else:
            self.lblKeywords.SetLabel("No keyword is found:")
        
        
        self.txtKeywords.SetValue(self.KeywordsValue)
        """
        
        
        self.InitCategoryCheckView()
        
    def InitCategoryCheckView(self):
        
        #if not Globals.MimeTypeSet:
        # Populate the Known MIME types list with what is in the database
        try:
            mtypes = wx.TheMimeTypesManager.EnumAllFileTypes()
        except wx.PyAssertionError:
            mtypes = []
        
        # TODO: On wxMac, EnumAllFileTypes produces tons of dupes, which
        # causes quirky behavior because the list control doesn't expect
        # dupes, and simply wastes space. So remove the dupes for now,
        # then remove this hack when we fix EnumAllFileTypes on Mac.
        
        mimes = set()
        for mime in mtypes:
            if not mime.startswith('image') and not mime.startswith('audio') and not mime.startswith('video'):
                mimes.add(mime)
                        
        #else:
        #    mimes = Globals.MimeTypeSet
        """         
        self.treeCategoryCheckView = FileCategoryCheckView(self.panTextPreProcessing, MimeTypeSet=mimes, id=wx.NewId(),pos=wx.Point(16, 200), size=wx.Size(440, 384),
            CheckedList=Globals.TextCatCategoryList) 
        self.treeCategoryCheckView.SetConstraints(LayoutAnchors(self.treeCategoryCheckView,
              True, True, True, True))
        """
        
        self.treeCategoryCheckView = FileCategoryCheckView(self.panCategoryView, MimeTypeSet=mimes, id=wx.NewId(), pos=wx.Point(8, 32),
              size=wx.Size(624, 392), CheckedList = Globals.KeywordsSearchCategoryList) 
        self.treeCategoryCheckView.SetConstraints(LayoutAnchors(self.treeCategoryCheckView,
              True, True, True, True))

        """
        self.treeDirCheckView = DirectoryCheckView(self.panDirView, id=wx.NewId(), pos=wx.Point(8, 32),
              size=wx.Size(624, 392), CheckedList=Globals.KeywordsSearchDirList) 
        self.treeDirCheckView.SetConstraints(LayoutAnchors(self.treeDirCheckView,
              True, True, True, True))  
        
        """
                   
        """
        self.treeCtrl1 = wx.TreeCtrl(id=wxID_FRMCUSTOMIZESEARCHTREECTRL1,
              name='treeCtrl1', parent=self.panCategoryView, pos=wx.Point(8,
              32), size=wx.Size(624, 392), style=wx.TR_HAS_BUTTONS)
        self.treeCtrl1 = wx.TreeCtrl(id=wxID_FRMCUSTOMIZESEARCHTREECTRL1,
              name='treeCtrl1', parent=self.panDirView, pos=wx.Point(8, 8),
              size=wx.Size(344, 432), style=wx.TR_HAS_BUTTONS)

        self.treeCtrl2 = wx.TreeCtrl(id=wxID_FRMCUSTOMIZESEARCHTREECTRL2,
              name='treeCtrl2', parent=self.panCategoryView, pos=wx.Point(8, 8),
              size=wx.Size(344, 432), style=wx.TR_HAS_BUTTONS)
        self.treeDirCheckView.SetConstraints(LayoutAnchors(self.treeDirCheckView,
              True, True, True, True))
        """
        #self.treeDirCheckView.Show(True)

        #self.keywordsRoot = self.treeDirCheckView.AddDirectoryTreeNodes()
        #self.catRoot = self.treeCategoryCheckView.AddCategoryTreeNodes()
        
        
    def OnBtnCloseButton(self, event):
        self.Close()

    def OnBtnSaveButton(self, event):
        if not self.CheckSettingsError():
            return
        self.UpdateSettingss()
        
        self.Close()
        
        
    
    def UpdateSearchDirectoriesAndCategories(self):
        Globals.KeywordsSearchCategoryList = []
        self.treeCategoryCheckView.UpdateCheckedList(Globals.KeywordsSearchCategoryList)
        #UpdateKeywordsSearchDirList
        #Globals.KeywordsSearchDirList = []
        #self.treeDirCheckView.UpdateKeywordsSearchDirList(Globals.KeywordsSearchDirList)
        #print Globals.KeywordsSearchDirList
        
    
    def CheckSettingsError(self):
        #Globals.KeywordsSearchDirList = []
        #self.treeDirCheckView.UpdateCheckedList(Globals.KeywordsSearchDirList)
        Globals.KeywordsSearchCategoryList = []
        self.treeCategoryCheckView.UpdateCheckedList(Globals.KeywordsSearchCategoryList)
        errMsg = ""
        #Globals.Keywords = self.KeywordsValue.split(";")
        if len(Globals.KeywordsDict) == 0:
            errMsg = "Please import keywords from a text file before start searching.\n File must have one keyword per line."
        #elif len(Globals.KeywordsSearchDirList) == 0:
        #    errMsg = "Please select directories where to search for Keywords."
        elif len(Globals.KeywordsSearchCategoryList) == 0:
            errMsg = "Please select file types / categories to search for Keywords."
        
        if not errMsg == "" :
            dlg = wx.MessageDialog(self, errMsg,
              'Error', wx.OK | wx.ICON_ERROR)
            try:
                dlg.ShowModal()
            finally:
                dlg.Destroy()
                return False
        else:
            self.UpdateSettings()
            return True
        
        
    def UpdateSettings(self):
        
        #UpdateKeywordsSearchDirList
        #Globals.Stemmer = self.choiceStemmers.GetStringSelection()
        #if self.chkCaseSensitive.GetValue():
        #    Globals.KeywordsSearchCaseSensitive = 1
        #else:
        #    Globals.KeywordsSearchCaseSensitive = 0
    
        self.DirPath = ""
        #self.CategoryList = ""
        """
        for dir in Globals.KeywordsSearchDirList:
            if not self.DirPath == "":
                self.DirPath += ";"
            self.DirPath += dir
        """ 
        #for cat in  Globals.KeywordsSearchCategoryList:
        self.CategoryList = ";".join(Globals.KeywordsSearchCategoryList)
        """
            if not self.CategoryList == "":
                self.CategoryList += ";"
            self.CategoryList += cat
        """
        
        db = SqliteDatabase(Globals.KeywordsFileName)
        if not db.OpenConnection():
            return
        
        query = "delete from " + Constants.KeywordsSettingsTable + ";"
        db.ExecuteNonQuery(query)
        
        query = "insert into %s (CategoryList) values (?)"%Constants.KeywordsSettingsTable 
        values = [(self.CategoryList),]
        db.ExecuteNonQuery(query, values)
        db.CloseConnection()
       
    
    def OnChkCaseInsensitiveCheckbox(self, event):
        event.Skip()

    def OnChkPrefixCheckbox(self, event):
        event.Skip()

    def OnChkSuffixCheckbox(self, event):
        event.Skip()

    def OnChkMiddleCheckbox(self, event):
        event.Skip()
    
    """
    def OnBtnKeywordsButton(self, event):
        import frmKeywords
        frmKey = frmKeywords.create(self)
        frmKey.ShowModal()
        event.Skip()
    """

    def OnBtnStartSearchButton(self, event):
        if not self.CheckSettingsError():
            return
        
        import dlgKeywordsSearchProgress
        search = dlgKeywordsSearchProgress.create(self)
        #scanMAC.StartScan(dir)
        search.ShowModal()
        event.Skip()

    def OnBtnBrowseButton(self, event):
        dlg = wx.FileDialog(self, "Open Line Separated Keyword Text File", ".", "", "*.*", wx.OPEN)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                self.FileName = dlg.GetPath()
                self.txtFileName.SetValue(self.FileName)
                self.ReadKeywordsFromFile(self.FileName)
                self.txtKeywords.SetValue(self.KeywordsValue.replace(';', '; '))
                self.lblKeywords.SetLabel("Keywords read from File:")
            else:
                return None
        finally:
            dlg.Destroy()


    def ReadKeywordsFromFile(self, fileName):
        fin = open(fileName, "rb")
        self.KeywordsValue = ""
        while True:
            lines = fin.readlines()
            if not lines:
                break
            for word in lines:
                self.Keywords.add(word.strip().lower())
                if self.KeywordsValue == "":
                    self.KeywordsValue += word.strip()
                else:
                    self.KeywordsValue += ";" + word.strip()
                    
        fin.close()
        #delete existing keywords from database
        print self.KeywordsValue
        db = SqliteDatabase(Globals.KeywordsFileName)
        if not db.OpenConnection():
            return
        db.ExecuteNonQuery('delete from %s'%Constants.KeywordsTable)
        query = "insert into %s (Keyword) values (?)"%Constants.KeywordsTable
        for word in self.Keywords:
            print word
            db.ExecuteMany(query, [(word,)])
        #load keywords with their ids
        self.LoadKeywordsFromDB()

    def MakeKeywordsList(self):
        i = 0
        for word in Globals.Keywords:
            if i == 0:
                self.KeywordsValue += word
            else:
                self.KeywordsValue += ";" + word
            i += 1

    def LoadSettingsTable(self):
        #if len(Globals.KeywordsSearchDirList) == 0:
        db = SqliteDatabase(Globals.KeywordsFileName)
        if not db.OpenConnection():
            return
        query = "select CategoryList from " + Constants.KeywordsSettingsTable
        rows = db.FetchAllRows(query)
        for row in rows:
            #Globals.KeywordsSearchCaseInsensitive = int(row[0])
            #Globals.KeywordsSearchCaseSensitive = int(row[1])
            #self.KeywordsValue = row[2]
            #self.DirPath = CommonFunctions.RemoveDoubleSlashes(row[3])
            #self.DirPath = row[0]
            self.CategoryList = row[0]
            
        db.CloseConnection()
        db = None
        #Globals.Keywords = set(self.KeywordsValue.split(';'))
        Globals.KeywordsSearchCategoryList = self.CategoryList.split(';')
        self.txtPath.SetValue(self.DirPath)
        #Globals.KeywordsSearchDirList = self.DirPath.split(';')

        self.LoadKeywordsFromDB()
        #self.MakeKeywordsList()
        
        self.txtKeywords.SetValue(self.KeywordsValue)
        #if Globals.CurrentProject.CaseSensitive:
        self.chkCaseInsensitive.SetValue(Globals.KeywordsSearchCaseSensitive)
        #self.chkCaseSensitive.SetValue(Globals.KeywordsSearchCaseSensitive)


    def LoadKeywordsFromDB(self):
        db = SqliteDatabase(Globals.KeywordsFileName)
        if not db.OpenConnection():
            return
        
        #load keywords with their ids
        rows = db.FetchAllRows('select rowid, Keyword from %s'%Constants.KeywordsTable)
        Globals.KeywordsDict = {}
        self.KeywordsValue = ""
        for row in rows:
            self.KeywordsValue += row[1] + "; "
            Globals.KeywordsDict[row[0]] = {'word':row[1], 're': re.compile("\\b" + row[1] + "\\b", re.I|re.S)} 
            
        db.CloseConnection()
        
        
    def OnBtnSelectFolderButton(self, event):
        #self.OneFolderList = []
        dlg = wx.DirDialog(self)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                self.txtPath.SetValue(dlg.GetPath())
        finally:
            dlg.Destroy()
        
        event.Skip()
        
        
        


